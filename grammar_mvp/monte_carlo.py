"""Monte Carlo battle simulator — pit a hero against a monster many times.

Usage:
    python -m grammar_mvp.monte_carlo [--runs N] [--hero HP STR DEF] [--enemy HP STR DEF]

Defaults match the current BattleView values.
"""

import argparse
import copy
import statistics

from grammar_mvp.battle import check_battle_end, resolve_turn, tick_effects
from grammar_mvp.game_state import Character, GameState


def run_battle(hero: Character, enemy: Character) -> dict:
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
    hero_attacks_next = True
    turn = 0
    while True:
        if hero_attacks_next:
            resolve_turn(h, e)
        else:
            resolve_turn(e, h)
        hero_attacks_next = not hero_attacks_next
        turn += 1
        tick_effects(h)
        tick_effects(e)
        result = check_battle_end(state)
        if result:
            return {"result": result, "turns": turn, "hero_hp": h.hp, "enemy_hp": e.hp}


def monte_carlo(hero: Character, enemy: Character, runs: int) -> dict:
    """Run *runs* battles and return aggregate stats."""
    wins = 0
    losses = 0
    turn_counts = []
    win_hp_remaining = []
    lose_hp_remaining = []

    for _ in range(runs):
        outcome = run_battle(hero, enemy)
        turn_counts.append(outcome["turns"])
        if outcome["result"] == "win":
            wins += 1
            win_hp_remaining.append(outcome["hero_hp"])
        else:
            losses += 1
            lose_hp_remaining.append(outcome["enemy_hp"])

    return {
        "runs": runs,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / runs,
        "avg_turns": statistics.mean(turn_counts),
        "min_turns": min(turn_counts),
        "max_turns": max(turn_counts),
        "avg_hero_hp_on_win": statistics.mean(win_hp_remaining) if win_hp_remaining else 0,
        "avg_enemy_hp_on_loss": statistics.mean(lose_hp_remaining) if lose_hp_remaining else 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Monte Carlo battle simulator")
    parser.add_argument("--runs", type=int, default=1000, help="Number of simulations")
    parser.add_argument("--hero", nargs=3, type=int, metavar=("HP", "STR", "DEF"),
                        default=[30, 6, 3], help="Hero stats: HP STR DEF")
    parser.add_argument("--enemy", nargs=3, type=int, metavar=("HP", "STR", "DEF"),
                        default=[25, 7, 3], help="Enemy stats: HP STR DEF")
    args = parser.parse_args()

    hero = Character("Hero", args.hero[0], args.hero[0], args.hero[1], args.hero[2])
    enemy = Character("Enemy", args.enemy[0], args.enemy[0], args.enemy[1], args.enemy[2])

    print(f"Hero:  HP={hero.max_hp}  STR={hero.strength}  DEF={hero.defense}")
    print(f"Enemy: HP={enemy.max_hp}  STR={enemy.strength}  DEF={enemy.defense}")
    print(f"Runs:  {args.runs}")
    print("-" * 40)

    results = monte_carlo(hero, enemy, args.runs)

    print(f"Hero wins:   {results['wins']}/{results['runs']}  ({results['win_rate']:.1%})")
    print(f"Hero losses: {results['losses']}/{results['runs']}  ({1 - results['win_rate']:.1%})")
    print(f"Avg turns:   {results['avg_turns']:.1f}  (range {results['min_turns']}–{results['max_turns']})")
    print(f"Avg hero HP remaining on win:  {results['avg_hero_hp_on_win']:.1f}")
    print(f"Avg enemy HP remaining on loss: {results['avg_enemy_hp_on_loss']:.1f}")


if __name__ == "__main__":
    main()
