# Monte Carlo Balance Findings

Preliminary combat balance analysis using the Monte Carlo simulator.
All runs: 5 000 iterations, 5s turn delay. Party RPG model (every living
combatant acts each round, targeting the frontline enemy).

## Combat Formula

```
hit    = randint(1, attacker.STR)
block  = randint(0, defender.DEF)
damage = max(1, hit - block)
```

Minimum 1 damage per hit guarantees fights always end.

## Key Stat: LD50

**LD50** = the median turn at which the hero team is wiped (across losing
runs only). Analogous to the pharmacological "lethal dose 50%". Lower LD50
means the hero team dies faster. If heroes always win, LD50 is N/A.

---

## Scenario Results

### 1. Default 1v1 &mdash; Sir Aldric (30/6/3) vs Goblin (25/7/3)

| Metric | Hero first | Enemy first |
|---|---|---|
| Win rate | 44.9% | 46.6% |
| Avg turns | 9.8 | 9.8 |
| LD50 | turn 10 (50s) | turn 10 (50s) |
| Last hero HP on win | 6.1 | 6.2 |
| Last enemy HP on loss | 3.7 | 3.8 |

**Takeaway:** The Goblin has a slight edge despite lower HP, because its
STR 7 vs DEF 3 generates more expected damage than Sir Aldric's STR 6 vs
DEF 3. First-strike advantage is negligible when both sides swing each
round. Fights are close and swingy &mdash; good for drama.

---

### 2. Tank vs Mob Pack &mdash; Knight (40/8/5) vs 3x Goblin (25/7/3)

| Metric | Value |
|---|---|
| Win rate | 0.0% |
| Avg turns | 6.3 |
| LD50 | turn 6 (30s) |
| Enemies fallen | 0.3 / 3 |

**Takeaway:** Action economy dominates. Even a tanky knight with 40 HP,
STR 8, DEF 5 cannot survive 3 goblins attacking every round. The knight
deals ~1 kill over 6 rounds but takes 3x incoming damage per round. Potions
or abilities that remove enemies or reduce incoming attacks would be
essential for solo-vs-pack encounters.

---

### 3. Solo vs Swarm &mdash; Sir Aldric (30/6/3) vs 5x Skeleton (20/4/2)

| Metric | Value |
|---|---|
| Win rate | 0.0% |
| Avg turns | 4.2 |
| LD50 | turn 4 (20s) |
| Enemies fallen | 0.0 / 5 |

**Takeaway:** Completely hopeless. 5 attackers per round overwhelms any
single fighter instantly. The hero cannot even kill one skeleton before
dying. This confirms that "mob swarm" encounters **require** party support
or AoE potions to be viable.

---

### 4. Party vs Boss &mdash; Paladin/Rogue/Cleric vs Dragon (80/12/6)

Heroes: Paladin (40/7/5), Rogue (25/9/2), Cleric (30/5/4) &mdash; 95 total HP

| Metric | Value |
|---|---|
| Win rate | 79.2% |
| Avg turns | 14.7 |
| LD50 | turn 18 (90s) |
| Heroes fallen on avg | 1.6 / 3 |
| Last hero HP on win | 26.8 |
| Last enemy HP on loss | 7.9 |

**Takeaway:** A 3-person party beats a single boss ~80% of the time, but
it's not free &mdash; they lose 1-2 party members on average. The Rogue
(low DEF 2) tends to fall fast to the Dragon's STR 12. The Dragon's high
DEF 6 makes the Cleric (STR 5) nearly useless offensively. Good boss
tension: winnable but costly.

---

### 5. 2v2 Balanced &mdash; Paladin + Rogue vs 2x Orc (35/8/4)

Heroes: Paladin (40/7/5), Rogue (25/9/2) &mdash; 65 total HP
Enemies: 2x Orc (35/8/4) &mdash; 70 total HP

| Metric | Value |
|---|---|
| Win rate | 57.1% |
| Avg turns | 12.9 |
| LD50 | turn 14 (70s) |
| Heroes fallen | 1.3 / 2 |
| Enemies fallen | 1.6 / 2 |

**Takeaway:** Slight hero edge from the Rogue's STR 9 focus-firing the
first Orc down, then the Paladin tanks the remaining one. The Rogue often
dies but its burst damage pulls its weight. Comparable to a "hard random
encounter" difficulty.

---

### 6. 3v3 Party vs Pack &mdash; Mixed party vs 3x Goblin (25/7/3)

Heroes: Paladin (40/7/5), Rogue (25/9/2), Cleric (30/5/4) &mdash; 95 total HP
Enemies: 3x Goblin (25/7/3) &mdash; 75 total HP

| Metric | Value |
|---|---|
| Win rate | 96.2% |
| Avg turns | 10.9 |
| Heroes fallen | 0.9 / 3 |

**Takeaway:** A diverse party shreds a goblin pack. The Rogue's high STR
burns down goblins fast, the Paladin tanks, and the damage spreads well.
Losing ~1 hero on average makes it feel like a real fight without real risk.
Good for "normal encounter" difficulty.

---

### 7. Mirror Match &mdash; 2x Sir Aldric (30/6/3) vs 2x Goblin (25/7/3)

| Metric | Value |
|---|---|
| Win rate | 50.2% |
| Avg turns | 13.4 |
| LD50 | turn 14 (70s) |
| Heroes fallen | 1.5 / 2 |

**Takeaway:** Near-perfect coin flip, as expected for similar stat totals.
The heroes' slight HP advantage (60 vs 50) barely offsets the goblins'
higher STR. Validates that the combat math is fair.

---

## Balance Observations

1. **Action economy is king.** Outnumbering the opponent is the single
   largest advantage. A solo hero cannot survive 3+ enemies regardless of
   stats. This is correct RPG behavior and makes party composition matter.

2. **STR matters more than DEF.** In the formula `max(1, randint(1,STR) -
   randint(0,DEF))`, the minimum 1 damage means DEF can never fully block.
   High STR generates disproportionately more expected damage than high DEF
   prevents. Offense wins races.

3. **First-strike is negligible.** Because both sides act every round,
   going first is worth ~1-2% win rate. This means the `--first` flag
   matters less for balance than stat choices.

4. **Fights are appropriately swingy.** The p10-p90 turn range is roughly
   2x (e.g. 8-12 turns for 1v1). Enough variance for drama, not so much
   that outcomes feel random.

5. **Duration sweet spots** (at 5s/turn):
   - Quick encounter: ~30-50s (1v1 or small fights)
   - Boss fight: ~60-90s (party vs boss)
   - Swarm wipe: ~20s (solo vs mob &mdash; intentionally brutal)

6. **Glass cannon archetype works.** The Rogue (25/9/2) consistently
   punches above its weight by focus-firing targets down, but dies to any
   sustained incoming damage. This creates interesting party dynamics.

## Implications for Potion Design

- **Healing potions** should restore ~5-10 HP to meaningfully extend
  survival (one extra round against typical incoming damage).
- **AoE damage potions** are essential to make solo-vs-swarm encounters
  viable. Even 3-5 damage to all enemies would dramatically shift the
  action economy.
- **DEF buffs** have diminishing returns due to `max(1, ...)`. A +2 DEF
  buff is noticeable but not fight-changing. STR buffs would be stronger.
- **Crowd control** (skip enemy turn) would be the most powerful potion
  type, effectively removing one attacker from the action economy per round.

## Adaptive Difficulty — Auto-Scaling Results

The simulator now includes `suggest_scaling()` which binary-searches an
enemy stat multiplier to hit a target hero win rate. This can be called at
runtime by the game backend to adjust the next encounter up or down.

### How it works

1. Binary-search over 12 iterations (always runs all of them &mdash; no
   early exit on noisy MC data).
2. Each iteration runs N battles at the current scale factor.
3. After converging, a confirmation pass at 2x samples locks in the final
   win rate.
4. Returns the scale factor and pre-built scaled enemy team.

### Auto-scale test: 1v1 default to 65% hero win rate

The default matchup (Sir Aldric 30/6/3 vs Goblin 25/7/3) has a ~45% hero
win rate.  Auto-scaling goblin HP down to hit 65%:

| Run | Scale | Goblin HP | Achieved |
|---|---|---|---|
| 1 | 0.860x | 22 | 62.4% |
| 2 | 0.850x | 21 | 69.6% |
| 3 | 0.867x | 22 | 64.3% |
| 4 | 0.861x | 22 | 62.0% |
| 5 | 0.862x | 22 | 61.6% |

Converges to Goblin HP 22 (down from 25) in 4/5 runs.  The outlier (HP 21)
is at the rounding boundary.  Stable enough for runtime use.

### Auto-scale test: party vs boss to 65%

Paladin/Rogue/Cleric vs Dragon (80/12/6) &mdash; baseline ~79% win rate.

| Stat scaled | Scale | Dragon stats | Achieved |
|---|---|---|---|
| HP only | 1.087x | 87/12/6 | 63.5% |
| All stats | 1.041x | 83/12/6 | 71.9% |

HP-only is the cleanest single knob.  Scaling all stats can overshoot
because STR and DEF compound non-linearly.

### Practical guidance for game integration

- **`difficulty_check()`** is cheap (~500 battles, <100ms). Call it
  before each encounter to decide if adjustment is needed.
- **`suggest_scaling()`** is heavier (~12x500 + 1000 confirmation =
  ~7000 battles). Call it once when building a level/wave, cache the
  result.
- **HP is the best single knob.** It scales fight duration linearly
  without changing the feel of individual hits.  STR scaling changes
  damage spikiness.  DEF scaling has diminishing returns.
- **Target 65% for normal encounters.** The player should usually win
  but occasionally lose.  Boss fights can target 55-70%.
