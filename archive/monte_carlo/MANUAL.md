# Monte Carlo Battle Simulator &mdash; Manual

A command-line tool for testing PotionWorld combat balance. Runs thousands
of simulated battles and reports win rates, turn distributions, timing
estimates, and the LD50 (median hero death turn).

## Quick Start

```bash
# Default 1v1 (Sir Aldric vs Goblin)
python -m grammar_mvp.monte_carlo

# Custom matchup
python -m grammar_mvp.monte_carlo \
    --hero "Paladin:40/7/5" \
    --enemy "Goblin:25/7/3"
```

## Character Format

```
Name:HP/STR/DEF
```

| Field | Meaning |
|---|---|
| Name | Display name (optional &mdash; defaults to Hero1, Enemy1, etc.) |
| HP | Hit points |
| STR | Strength &mdash; attack rolls `randint(1, STR)` |
| DEF | Defense &mdash; block rolls `randint(0, DEF)` |

If you omit the name, just use `HP/STR/DEF`:

```bash
--hero 30/6/3          # named "Hero1"
--hero "Knight:40/8/5" # named "Knight"
```

## CLI Flags

### `--hero SPEC` (repeatable)

Add a hero to the hero team. Use multiple `--hero` flags for a party:

```bash
--hero "Paladin:40/7/5" --hero "Rogue:25/9/2" --hero "Cleric:30/5/4"
```

**Default** (if no `--hero` given): `Sir Aldric:30/6/3`

### `--enemy SPEC` (repeatable)

Add an enemy to the enemy team. Same format as `--hero`:

```bash
--enemy "Goblin:25/7/3" --enemy "Goblin:25/7/3" --enemy "Goblin:25/7/3"
```

**Default** (if no `--enemy` given): `Goblin:25/7/3`

### `--runs N`

Number of simulated battles. Default: `1000`. Use higher values (5000+)
for more stable statistics on close matchups.

```bash
--runs 5000
```

### `--turn-delay SECS`

Seconds per round in the actual game. Enables duration estimates in the
output (total fight time, LD50 in seconds/minutes).

```bash
--turn-delay 5.0
```

### `--first hero|enemy|both`

Which side acts first each round:

| Value | Behavior |
|---|---|
| `hero` (default) | Heroes swing first every round |
| `enemy` | Enemies swing first every round |
| `both` | Runs the simulation twice and prints both results side-by-side |

```bash
--first both
```

### `--csv`

Output results as CSV instead of the human-readable table. Pipe to a file
for spreadsheet analysis:

```bash
python -m grammar_mvp.monte_carlo --csv > balance.csv
```

### `--check TARGET`

Quick difficulty assessment. Runs the simulation and compares the hero win
rate against TARGET (0.0-1.0). Prints a verdict: EASY, FAIR, or HARD.

```bash
# Is this encounter roughly 65% winnable?
python -m grammar_mvp.monte_carlo \
    --hero "Paladin:40/7/5" --enemy "Orc:35/8/4" --check 0.65
```

Output:

```
Paladin(40/7/5)  vs  Orc(35/8/4)
  Target win rate: 65%
  Actual win rate: 71.2%
  Delta:           +6.2%
  Verdict:         FAIR
```

Verdict uses a +/-10% tolerance band around the target. Useful for the
game backend to quickly test "should I adjust this encounter?" before
committing to a full auto-scale.

### `--auto-scale TARGET`

Binary-searches an enemy stat multiplier that produces a hero win rate
close to TARGET. Always runs all 12 iterations (no early exit) so the
result is stable across runs, then does a confirmation pass at 2x samples.

```bash
# Scale goblin HP until heroes win ~65% of the time
python -m grammar_mvp.monte_carlo \
    --hero "Sir Aldric:30/6/3" --enemy "Goblin:25/7/3" \
    --auto-scale 0.65

# Scale all enemy stats together
python -m grammar_mvp.monte_carlo \
    --hero "Sir Aldric:30/6/3" --enemy "Goblin:25/7/3" \
    --auto-scale 0.65 --scale-stat all
```

Output:

```
Sir Aldric(30/6/3)  vs  Goblin(25/7/3)
  Target:    65% hero win rate
  Achieved:  64.3% (12 iterations)
  Scale:     0.867x (hp)
  Scaled enemies: Goblin(22/7/3)
    Goblin: 22/7/3
```

### `--scale-stat hp|str|def|all`

Which enemy stat to adjust with `--auto-scale`. Default: `hp`.

| Value | Effect |
|---|---|
| `hp` (default) | Scale enemy HP only &mdash; safest single knob |
| `str` | Scale enemy STR &mdash; changes damage output |
| `def` | Scale enemy DEF &mdash; changes damage taken |
| `all` | Scale all three together |

## Adaptive Difficulty (Runtime API)

Three functions are importable for use by the game backend:

```python
from grammar_mvp.monte_carlo import (
    difficulty_check,
    suggest_scaling,
    scale_team,
)
```

### `scale_team(team, hp_scale, str_scale, def_scale)`

Returns a deep copy of a team with stats multiplied. All values clamp
to a minimum of 1.

```python
tougher_goblins = scale_team(goblins, hp_scale=1.3)
```

### `difficulty_check(heroes, enemies, target_win_rate, ...)`

Runs a quick MC simulation and returns a verdict dict:

```python
result = difficulty_check(hero_party, next_enemies, target_win_rate=0.65)
if result["verdict"] == "hard":
    # nerf the encounter or offer a potion
```

Returns: `win_rate`, `target`, `delta`, `verdict` ("easy"/"fair"/"hard"),
`stats` (full monte_carlo result).

### `suggest_scaling(heroes, enemies, target_win_rate, ...)`

Binary-searches an enemy multiplier to hit the target win rate. Runs all
iterations for stability, then a 2x confirmation pass.

```python
result = suggest_scaling(hero_party, base_enemies, target_win_rate=0.65)
adjusted_enemies = result["scaled_enemies"]
# result["scale"] is the multiplier (e.g. 1.35)
```

### Example: adaptive encounter setup

```python
from grammar_mvp.monte_carlo import difficulty_check, suggest_scaling

def setup_encounter(hero_party, base_enemies, target=0.65):
    """Adjust enemies so the encounter hits the target win rate."""
    check = difficulty_check(hero_party, base_enemies, target)
    if check["verdict"] == "fair":
        return base_enemies  # already balanced

    result = suggest_scaling(hero_party, base_enemies, target)
    return result["scaled_enemies"]
```

## Combat Model

Each round:

1. **All living fighters on the first-strike side** attack, in order.
   Each attacker targets the **first living enemy** on the opposing side
   (frontline targeting).
2. **All living fighters on the other side** attack the same way.
3. **Effects tick** &mdash; active duration-based effects decrement on all
   living combatants.
4. Dead fighters are removed. If a side has no living fighters, battle ends.

One round = one turn in the output. The damage formula:

```
hit    = randint(1, attacker.STR)
block  = randint(0, defender.DEF)
damage = max(1, hit - block)
```

Minimum 1 damage per hit. Fights always terminate.

## Understanding the Output

```
Paladin(40/7/5), Rogue(25/9/2)  vs  Orc(35/8/4) x2
==================================================
  Heroes: 2  (total HP 65)
  Enemies: 2  (total HP 70)
  Runs:  5000

  LD50 (hero team): turn 14  (70s / 1.2min)

  Win rate:  57.1%  (2855W / 2145L)
  Turns:     avg 12.9  (range 7-23)
  Quartiles: p10=10  p25=11  p50=13  p75=14  p90=16
  Duration:  avg 65s (1.1min)  fast 50s  slow 80s
  Avg last hero HP on win:   17.0
  Avg last enemy HP on loss: 12.9
  Avg heroes fallen:  1.3 / 2
  Avg enemies fallen: 1.6 / 2
```

| Line | Meaning |
|---|---|
| **Header** | Team compositions with stat summary. Duplicate fighters show `x2`, `x3`, etc. |
| **Heroes/Enemies** | Team size and combined HP pool |
| **LD50** | Median turn at which hero teams die (losing runs only). "N/A" if heroes always win. Lower = heroes die faster. |
| **Win rate** | Percentage of runs where all enemies die before all heroes. |
| **Turns** | Average rounds to battle resolution, with min-max range. |
| **Quartiles** | Turn count at p10, p25, p50, p75, p90. Shows the spread. |
| **Duration** | Wall-clock estimates (only with `--turn-delay`). "fast" = p10, "slow" = p90. |
| **Last hero HP on win** | Average remaining HP of the last surviving hero when heroes win. Low = close fights. |
| **Last enemy HP on loss** | Average remaining HP of the last surviving enemy when heroes lose. |
| **Heroes/Enemies fallen** | Average casualties per battle out of total team size. |

## Example Workflows

### Tuning a 1v1 matchup

```bash
# Is this fight fair?
python -m grammar_mvp.monte_carlo \
    --hero "Knight:35/7/4" --enemy "Bandit:30/8/3" --runs 5000

# Too easy? Buff the enemy
python -m grammar_mvp.monte_carlo \
    --hero "Knight:35/7/4" --enemy "Bandit:35/9/3" --runs 5000
```

Aim for 40-60% hero win rate for "fair" encounters.

### Checking boss difficulty

```bash
python -m grammar_mvp.monte_carlo \
    --hero "Paladin:40/7/5" --hero "Rogue:25/9/2" --hero "Cleric:30/5/4" \
    --enemy "Dragon:80/12/6" --runs 5000 --turn-delay 5
```

Boss fights should be winnable (60-85%) but costly (1-2 heroes fallen).
Duration 60-90s at 5s/turn feels right for a climactic fight.

### Verifying swarm balance

```bash
python -m grammar_mvp.monte_carlo \
    --hero "Knight:40/8/5" \
    --enemy "Goblin:25/7/3" --enemy "Goblin:25/7/3" --enemy "Goblin:25/7/3" \
    --runs 5000
```

Solo-vs-pack should be near-impossible without potions. This validates that
potion/ability design is necessary for those encounters.

### Batch CSV export

```bash
# Run all your test scenarios and export to one CSV
python -m grammar_mvp.monte_carlo --hero 30/6/3 --enemy 25/7/3 --csv > out.csv
python -m grammar_mvp.monte_carlo --hero 40/8/5 --enemy 25/7/3 --enemy 25/7/3 --csv >> out.csv
```

### First-strike analysis

```bash
python -m grammar_mvp.monte_carlo --first both --runs 5000
```

Compares hero-first and enemy-first in one run. Useful for verifying that
first-strike advantage is small (it should be ~1-2%).

## Balance Guidelines

| Encounter type | Target win rate | Target duration (5s/turn) |
|---|---|---|
| Easy random encounter | 85-95% | 30-40s |
| Normal encounter | 60-75% | 40-60s |
| Hard encounter | 40-55% | 50-70s |
| Boss fight | 60-85% | 60-90s |
| Swarm (no potions) | 0-10% | 20-30s |
| Swarm (with AoE) | 50-70% | 40-60s |
