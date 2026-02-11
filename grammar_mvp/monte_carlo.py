"""Monte Carlo battle simulator — balance tool for PotionWorld.

Simulate team battles: an arbitrary number of heroes vs an arbitrary
number of enemies.  Each round every living combatant acts once,
targeting the frontline enemy.  Standard RPG party combat.

The headline stat is LD50: the turn at which 50% of hero teams are wiped.

Usage examples:

  # Simple — current game defaults (1v1)
  python -m grammar_mvp.monte_carlo

  # 1 hero vs 4 skeletons (gauntlet)
  python -m grammar_mvp.monte_carlo \\
      --hero "Sir Aldric:30/6/3" \\
      --enemy "Skeleton:30/5/2" --enemy "Skeleton:30/5/2" \\
      --enemy "Skeleton:30/5/2" --enemy "Skeleton:30/5/2"

  # 3 heroes vs 1 boss
  python -m grammar_mvp.monte_carlo \\
      --hero "Paladin:40/7/5" --hero "Rogue:25/9/2" --hero "Cleric:30/5/4" \\
      --enemy "Ogre:50/10/4"

  # With timing info (turn delay in seconds)
  python -m grammar_mvp.monte_carlo --turn-delay 5.0

  # Test first-strike advantage
  python -m grammar_mvp.monte_carlo --first both

  # CSV output for spreadsheets
  python -m grammar_mvp.monte_carlo --csv
"""

import argparse
import copy
import csv
import io
import statistics

from grammar_mvp.battle import resolve_turn, tick_effects
from grammar_mvp.game_state import Character


# ── Character parsing ────────────────────────────────────────────────

def parse_character(spec: str, default_name: str = "Fighter") -> Character:
    """Parse 'Name:HP/STR/DEF' or 'HP/STR/DEF' into a Character."""
    if ":" in spec:
        name, stats = spec.split(":", 1)
    else:
        name, stats = default_name, spec
    parts = stats.split("/")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(
            f"Expected HP/STR/DEF (e.g. '30/6/3'), got '{stats}'"
        )
    hp, strength, defense = int(parts[0]), int(parts[1]), int(parts[2])
    return Character(name, hp, hp, strength, defense)


def _char_label(chars: list[Character]) -> str:
    """Short label for a team: 'Goblin' or 'Goblin, Skeleton x2'."""
    counts: dict[str, int] = {}
    for c in chars:
        key = f"{c.name}({c.max_hp}/{c.strength}/{c.defense})"
        counts[key] = counts.get(key, 0) + 1
    parts = []
    for name, n in counts.items():
        parts.append(f"{name} x{n}" if n > 1 else name)
    return ", ".join(parts)


def _team_total_hp(chars: list[Character]) -> int:
    return sum(c.max_hp for c in chars)


# ── Simulation ───────────────────────────────────────────────────────

def run_battle(
    heroes: list[Character],
    enemies: list[Character],
    hero_first: bool = True,
) -> dict:
    """Simulate one full battle between hero team and enemy team.

    Each round every living combatant acts once.  The side indicated by
    *hero_first* swings first, then the other side.  Each attacker
    targets the first living fighter on the opposing side (frontline).
    One round = one turn for timing purposes.
    """
    h_team = [copy.deepcopy(c) for c in heroes]
    e_team = [copy.deepcopy(c) for c in enemies]
    turn = 0

    def living(team):
        return [c for c in team if c.hp > 0]

    while living(h_team) and living(e_team):
        if hero_first:
            sides = [(living(h_team), e_team), (living(e_team), h_team)]
        else:
            sides = [(living(e_team), h_team), (living(h_team), e_team)]

        for attackers, target_team in sides:
            for attacker in attackers:
                targets = living(target_team)
                if targets:
                    resolve_turn(attacker, targets[0])

        for c in h_team + e_team:
            if c.hp > 0:
                tick_effects(c)

        turn += 1

    heroes_fallen = sum(1 for h in h_team if h.hp <= 0)
    enemies_fallen = sum(1 for e in e_team if e.hp <= 0)
    hero_side_won = bool(living(h_team))
    surviving_heroes = living(h_team)
    surviving_enemies = living(e_team)

    return {
        "result": "win" if hero_side_won else "lose",
        "turns": turn,
        "last_hero_hp": surviving_heroes[-1].hp if surviving_heroes else 0,
        "last_enemy_hp": surviving_enemies[-1].hp if surviving_enemies else 0,
        "heroes_fallen": heroes_fallen,
        "enemies_fallen": enemies_fallen,
    }


def monte_carlo(
    heroes: list[Character],
    enemies: list[Character],
    runs: int,
    hero_first: bool = True,
) -> dict:
    """Run *runs* battles and return aggregate stats."""
    wins = 0
    losses = 0
    turn_counts = []
    win_hp = []
    lose_hp = []
    death_turns = []
    heroes_fallen_counts = []
    enemies_fallen_counts = []

    for _ in range(runs):
        outcome = run_battle(heroes, enemies, hero_first)
        turn_counts.append(outcome["turns"])
        heroes_fallen_counts.append(outcome["heroes_fallen"])
        enemies_fallen_counts.append(outcome["enemies_fallen"])
        if outcome["result"] == "win":
            wins += 1
            win_hp.append(outcome["last_hero_hp"])
        else:
            losses += 1
            lose_hp.append(outcome["last_enemy_hp"])
            death_turns.append(outcome["turns"])

    sorted_turns = sorted(turn_counts)
    n = len(sorted_turns)

    def percentile(p):
        idx = int(n * p / 100)
        return sorted_turns[min(idx, n - 1)]

    ld50 = statistics.median(death_turns) if death_turns else None

    return {
        "runs": runs,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / runs,
        "ld50": ld50,
        "avg_turns": statistics.mean(turn_counts),
        "min_turns": min(turn_counts),
        "max_turns": max(turn_counts),
        "p10_turns": percentile(10),
        "p25_turns": percentile(25),
        "p50_turns": percentile(50),
        "p75_turns": percentile(75),
        "p90_turns": percentile(90),
        "avg_hero_hp_on_win": statistics.mean(win_hp) if win_hp else 0,
        "avg_enemy_hp_on_loss": statistics.mean(lose_hp) if lose_hp else 0,
        "avg_heroes_fallen": statistics.mean(heroes_fallen_counts),
        "avg_enemies_fallen": statistics.mean(enemies_fallen_counts),
    }


# ── Output ───────────────────────────────────────────────────────────

def format_table(result: dict, turn_delay: float | None) -> str:
    """Pretty-print results as a table."""
    lines = []
    hdr = f"{result['hero_label']}  vs  {result['enemy_label']}"
    if result.get("first_strike"):
        hdr += f"  (first: {result['first_strike']})"
    lines.append(hdr)
    lines.append("=" * len(hdr))

    lines.append(f"  Heroes: {result['hero_count']}  (total HP {result['hero_total_hp']})")
    lines.append(f"  Enemies: {result['enemy_count']}  (total HP {result['enemy_total_hp']})")

    s = result["stats"]
    lines.append(f"  Runs:  {s['runs']}")
    lines.append("")

    # LD50 — headline stat
    ld50 = s["ld50"]
    if ld50 is not None:
        ld50_line = f"  LD50 (hero team): turn {ld50:.0f}"
        if turn_delay:
            ld50_line += f"  ({ld50 * turn_delay:.0f}s / {ld50 * turn_delay / 60:.1f}min)"
        lines.append(ld50_line)
    else:
        lines.append("  LD50 (hero team): N/A (heroes always win)")

    lines.append("")
    lines.append(
        f"  Win rate:  {s['win_rate']:.1%}  "
        f"({s['wins']}W / {s['losses']}L)"
    )
    lines.append(
        f"  Turns:     avg {s['avg_turns']:.1f}  "
        f"(range {s['min_turns']}–{s['max_turns']})"
    )
    lines.append(
        f"  Quartiles: p10={s['p10_turns']}  p25={s['p25_turns']}  "
        f"p50={s['p50_turns']}  p75={s['p75_turns']}  p90={s['p90_turns']}"
    )

    if turn_delay:
        avg_secs = s["avg_turns"] * turn_delay
        fast_secs = s["p10_turns"] * turn_delay
        slow_secs = s["p90_turns"] * turn_delay
        lines.append(
            f"  Duration:  avg {avg_secs:.0f}s ({avg_secs/60:.1f}min)  "
            f"fast {fast_secs:.0f}s  slow {slow_secs:.0f}s"
        )

    lines.append(
        f"  Avg last hero HP on win:   {s['avg_hero_hp_on_win']:.1f}"
    )
    lines.append(
        f"  Avg last enemy HP on loss: {s['avg_enemy_hp_on_loss']:.1f}"
    )
    lines.append(
        f"  Avg heroes fallen:  {s['avg_heroes_fallen']:.1f} / {result['hero_count']}"
    )
    lines.append(
        f"  Avg enemies fallen: {s['avg_enemies_fallen']:.1f} / {result['enemy_count']}"
    )

    lines.append("")
    return "\n".join(lines)


def format_csv(results: list[dict], turn_delay: float | None) -> str:
    """Format results as CSV."""
    buf = io.StringIO()
    fieldnames = [
        "heroes", "enemies", "first_strike",
        "hero_count", "hero_total_hp",
        "enemy_count", "enemy_total_hp",
        "runs", "wins", "losses", "win_rate", "ld50",
        "avg_turns", "min_turns", "max_turns",
        "p10", "p25", "p50", "p75", "p90",
        "avg_hero_hp_on_win", "avg_enemy_hp_on_loss",
        "avg_heroes_fallen", "avg_enemies_fallen",
    ]
    if turn_delay:
        fieldnames.extend(["avg_duration_s", "ld50_s"])
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()

    for r in results:
        s = r["stats"]
        row = {
            "heroes": r["hero_label"],
            "enemies": r["enemy_label"],
            "first_strike": r.get("first_strike", "hero"),
            "hero_count": r["hero_count"],
            "hero_total_hp": r["hero_total_hp"],
            "enemy_count": r["enemy_count"],
            "enemy_total_hp": r["enemy_total_hp"],
            "runs": s["runs"],
            "wins": s["wins"],
            "losses": s["losses"],
            "win_rate": f"{s['win_rate']:.4f}",
            "ld50": f"{s['ld50']:.0f}" if s["ld50"] is not None else "",
            "avg_turns": f"{s['avg_turns']:.1f}",
            "min_turns": s["min_turns"],
            "max_turns": s["max_turns"],
            "p10": s["p10_turns"],
            "p25": s["p25_turns"],
            "p50": s["p50_turns"],
            "p75": s["p75_turns"],
            "p90": s["p90_turns"],
            "avg_hero_hp_on_win": f"{s['avg_hero_hp_on_win']:.1f}",
            "avg_enemy_hp_on_loss": f"{s['avg_enemy_hp_on_loss']:.1f}",
            "avg_heroes_fallen": f"{s['avg_heroes_fallen']:.1f}",
            "avg_enemies_fallen": f"{s['avg_enemies_fallen']:.1f}",
        }
        if turn_delay:
            row["avg_duration_s"] = f"{s['avg_turns'] * turn_delay:.0f}"
            row["ld50_s"] = f"{s['ld50'] * turn_delay:.0f}" if s["ld50"] is not None else ""
        writer.writerow(row)

    return buf.getvalue()


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo battle simulator for PotionWorld",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Character format:  Name:HP/STR/DEF  or  HP/STR/DEF\n"
            "\n"
            "All --hero flags form one team; all --enemy flags form the\n"
            "other.  Each round every living combatant acts once, targeting\n"
            "the frontline enemy.  Standard RPG party combat.\n"
            "\n"
            "Examples:\n"
            "  %(prog)s --hero 'Paladin:40/7/5' --enemy 'Goblin:25/7/3'\n"
            "  %(prog)s --hero 30/6/3 --enemy 25/7/3 --turn-delay 5\n"
            "  %(prog)s --hero 30/6/3 --enemy 25/7/3 --first both\n"
            "  %(prog)s --hero 30/6/3 --enemy 20/5/2 --enemy 20/5/2 --enemy 20/5/2\n"
            "  %(prog)s --csv > balance.csv\n"
        ),
    )
    parser.add_argument(
        "--hero", action="append", dest="heroes", metavar="SPEC",
        help="Hero spec: 'Name:HP/STR/DEF' or 'HP/STR/DEF' (repeatable — forms a team)",
    )
    parser.add_argument(
        "--enemy", action="append", dest="enemies", metavar="SPEC",
        help="Enemy spec: 'Name:HP/STR/DEF' or 'HP/STR/DEF' (repeatable — forms a team)",
    )
    parser.add_argument(
        "--runs", type=int, default=1000,
        help="Simulations per matchup (default: 1000)",
    )
    parser.add_argument(
        "--turn-delay", type=float, default=None, metavar="SECS",
        help="Seconds per turn — enables duration estimates (LD50 in seconds, etc.)",
    )
    parser.add_argument(
        "--first", choices=["hero", "enemy", "both"], default="hero",
        help="Who strikes first: hero, enemy, or both (tests each)",
    )
    parser.add_argument(
        "--csv", action="store_true",
        help="Output as CSV instead of table",
    )
    args = parser.parse_args()

    # Defaults
    heroes = []
    if args.heroes:
        for i, spec in enumerate(args.heroes):
            heroes.append(parse_character(spec, f"Hero{i+1}"))
    else:
        heroes.append(Character("Sir Aldric", 30, 30, 6, 3))

    enemies = []
    if args.enemies:
        for i, spec in enumerate(args.enemies):
            enemies.append(parse_character(spec, f"Enemy{i+1}"))
    else:
        enemies.append(Character("Goblin", 25, 25, 7, 3))

    # Determine first-strike variants to test
    first_options = (
        [("hero", True), ("enemy", False)]
        if args.first == "both"
        else [("hero", True)] if args.first == "hero"
        else [("enemy", False)]
    )

    hero_label = _char_label(heroes)
    enemy_label = _char_label(enemies)

    all_results = []
    for label, hero_first in first_options:
        stats = monte_carlo(heroes, enemies, args.runs, hero_first)
        all_results.append({
            "hero_label": hero_label,
            "enemy_label": enemy_label,
            "hero_count": len(heroes),
            "enemy_count": len(enemies),
            "hero_total_hp": _team_total_hp(heroes),
            "enemy_total_hp": _team_total_hp(enemies),
            "first_strike": label if args.first == "both" else None,
            "stats": stats,
        })

    # Output
    if args.csv:
        print(format_csv(all_results, args.turn_delay), end="")
    else:
        for r in all_results:
            print(format_table(r, args.turn_delay))


if __name__ == "__main__":
    main()
