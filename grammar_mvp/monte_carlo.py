"""Monte Carlo battle simulator — balance tool for PotionWorld.

Test arbitrary hero/enemy matchups over thousands of runs.
The headline stat is LD50: the turn at which 50% of heroes are dead.

Usage examples:

  # Simple — current game defaults
  python -m grammar_mvp.monte_carlo

  # Custom matchup
  python -m grammar_mvp.monte_carlo --hero "Sir Aldric:30/6/3" --enemy "Goblin:25/7/3"

  # Multiple matchups — tests every combination
  python -m grammar_mvp.monte_carlo \\
      --hero "Paladin:40/7/5" --hero "Rogue:25/9/2" \\
      --enemy "Goblin:25/7/3" --enemy "Skeleton:30/5/2" --enemy "Ogre:50/10/4"

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

from grammar_mvp.battle import check_battle_end, resolve_turn, tick_effects
from grammar_mvp.game_state import Character, GameState


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


# ── Simulation ───────────────────────────────────────────────────────

def run_battle(hero: Character, enemy: Character, hero_first: bool = True) -> dict:
    """Simulate one full battle (no potions). Returns result dict."""
    h = copy.deepcopy(hero)
    e = copy.deepcopy(enemy)
    state = GameState(
        hero=h, enemy=e,
        mana=0, max_mana=0,
        deck=[], hand=[], lock=[],
        slot_count=0, hand_size=0,
        phase="resolve",
    )
    hero_attacks = hero_first
    turn = 0
    while True:
        if hero_attacks:
            resolve_turn(h, e)
        else:
            resolve_turn(e, h)
        hero_attacks = not hero_attacks
        turn += 1
        tick_effects(h)
        tick_effects(e)
        result = check_battle_end(state)
        if result:
            return {
                "result": result,
                "turns": turn,
                "hero_hp": h.hp,
                "enemy_hp": e.hp,
            }


def monte_carlo(
    hero: Character,
    enemy: Character,
    runs: int,
    hero_first: bool = True,
) -> dict:
    """Run *runs* battles and return aggregate stats."""
    wins = 0
    losses = 0
    turn_counts = []
    win_hp = []
    lose_hp = []
    death_turns = []  # turn numbers where the hero died

    for _ in range(runs):
        outcome = run_battle(hero, enemy, hero_first)
        turn_counts.append(outcome["turns"])
        if outcome["result"] == "win":
            wins += 1
            win_hp.append(outcome["hero_hp"])
        else:
            losses += 1
            lose_hp.append(outcome["enemy_hp"])
            death_turns.append(outcome["turns"])

    sorted_turns = sorted(turn_counts)
    n = len(sorted_turns)

    def percentile(p):
        idx = int(n * p / 100)
        return sorted_turns[min(idx, n - 1)]

    # LD50: the median turn at which the hero dies.
    # If the hero wins >50% of the time, LD50 is None (they usually survive).
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
    }


# ── Output ───────────────────────────────────────────────────────────

def format_table(all_results: list[dict], turn_delay: float | None) -> str:
    """Pretty-print results as a table."""
    lines = []
    for r in all_results:
        hdr = f"{r['hero_name']} vs {r['enemy_name']}"
        if r.get("first_strike"):
            hdr += f"  (first: {r['first_strike']})"
        lines.append(hdr)
        lines.append("=" * len(hdr))

        stats = r["stats"]
        lines.append(
            f"  Hero:  HP={r['hero_hp']}  STR={r['hero_str']}  DEF={r['hero_def']}"
        )
        lines.append(
            f"  Enemy: HP={r['enemy_hp']}  STR={r['enemy_str']}  DEF={r['enemy_def']}"
        )
        lines.append(f"  Runs:  {stats['runs']}")
        lines.append("")

        # LD50 — headline stat
        ld50 = stats["ld50"]
        if ld50 is not None:
            ld50_line = f"  LD50 (hero):   turn {ld50:.0f}"
            if turn_delay:
                ld50_line += f"  ({ld50 * turn_delay:.0f}s / {ld50 * turn_delay / 60:.1f}min)"
            lines.append(ld50_line)
        else:
            lines.append("  LD50 (hero):   N/A (hero never dies)")

        lines.append("")
        lines.append(
            f"  Win rate:  {stats['win_rate']:.1%}  "
            f"({stats['wins']}W / {stats['losses']}L)"
        )
        lines.append(
            f"  Turns:     avg {stats['avg_turns']:.1f}  "
            f"(range {stats['min_turns']}–{stats['max_turns']})"
        )
        lines.append(
            f"  Quartiles: p10={stats['p10_turns']}  p25={stats['p25_turns']}  "
            f"p50={stats['p50_turns']}  p75={stats['p75_turns']}  p90={stats['p90_turns']}"
        )

        if turn_delay:
            avg_secs = stats["avg_turns"] * turn_delay
            fast_secs = stats["p10_turns"] * turn_delay
            slow_secs = stats["p90_turns"] * turn_delay
            lines.append(
                f"  Duration:  avg {avg_secs:.0f}s ({avg_secs/60:.1f}min)  "
                f"fast {fast_secs:.0f}s  slow {slow_secs:.0f}s"
            )

        lines.append(
            f"  Avg hero HP on win:    {stats['avg_hero_hp_on_win']:.1f}"
        )
        lines.append(
            f"  Avg enemy HP on loss:  {stats['avg_enemy_hp_on_loss']:.1f}"
        )

        lines.append("")

    return "\n".join(lines)


def format_csv(all_results: list[dict], turn_delay: float | None) -> str:
    """Format results as CSV."""
    buf = io.StringIO()
    fieldnames = [
        "hero", "enemy", "first_strike",
        "hero_hp", "hero_str", "hero_def",
        "enemy_hp", "enemy_str", "enemy_def",
        "runs", "wins", "losses", "win_rate", "ld50",
        "avg_turns", "min_turns", "max_turns",
        "p10", "p25", "p50", "p75", "p90",
        "avg_hero_hp_on_win", "avg_enemy_hp_on_loss",
    ]
    if turn_delay:
        fieldnames.extend(["avg_duration_s", "ld50_s"])
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()

    for r in all_results:
        s = r["stats"]
        row = {
            "hero": r["hero_name"],
            "enemy": r["enemy_name"],
            "first_strike": r.get("first_strike", "hero"),
            "hero_hp": r["hero_hp"],
            "hero_str": r["hero_str"],
            "hero_def": r["hero_def"],
            "enemy_hp": r["enemy_hp"],
            "enemy_str": r["enemy_str"],
            "enemy_def": r["enemy_def"],
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
            "Examples:\n"
            "  %(prog)s --hero 'Paladin:40/7/5' --enemy 'Goblin:25/7/3'\n"
            "  %(prog)s --hero 30/6/3 --enemy 25/7/3 --turn-delay 5\n"
            "  %(prog)s --hero 30/6/3 --enemy 25/7/3 --first both\n"
            "  %(prog)s --csv > balance.csv\n"
        ),
    )
    parser.add_argument(
        "--hero", action="append", dest="heroes", metavar="SPEC",
        help="Hero spec: 'Name:HP/STR/DEF' or 'HP/STR/DEF' (repeatable)",
    )
    parser.add_argument(
        "--enemy", action="append", dest="enemies", metavar="SPEC",
        help="Enemy spec: 'Name:HP/STR/DEF' or 'HP/STR/DEF' (repeatable)",
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

    # Run all matchups
    all_results = []
    for hero in heroes:
        for enemy in enemies:
            for label, hero_first in first_options:
                stats = monte_carlo(hero, enemy, args.runs, hero_first)
                all_results.append({
                    "hero_name": hero.name,
                    "enemy_name": enemy.name,
                    "hero_hp": hero.max_hp,
                    "hero_str": hero.strength,
                    "hero_def": hero.defense,
                    "enemy_hp": enemy.max_hp,
                    "enemy_str": enemy.strength,
                    "enemy_def": enemy.defense,
                    "first_strike": label if args.first == "both" else None,
                    "stats": stats,
                })

    # Output
    if args.csv:
        print(format_csv(all_results, args.turn_delay), end="")
    else:
        print(format_table(all_results, args.turn_delay))


if __name__ == "__main__":
    main()
