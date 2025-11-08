from src.core.event_bus import EventBus
from src.core.data_structures import Personality, Quality
from src.crafting.data_structures import Potion
from src.combat.data_structures import (
    Combatant, CombatStats, CombatAction, StatusEffect, Trigger
)
from src.combat.system import CombatSystem
import sys


class CombatTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.combat = CombatSystem(self.event_bus)
        self.events = []

        self.event_bus.subscribe_all(self._capture_event)

        self.player = self._create_player()
        self.opponent = self._create_opponent()
        self.turn = 1
        self.combat_id = "testbed_combat"

    def _capture_event(self, event):
        self.events.append(event)

    def _create_player(self):
        stats = CombatStats(
            health=100,
            max_health=100,
            strength=50,
            defense=30,
            initiative=10,
            resistance=5
        )

        potions = [
            Potion(
                "fire_blast",
                "fire",
                "E#Damage30",
                Quality.STANDARD,
                1.0,
                "player",
                0
            ),
            Potion(
                "healing",
                "heal",
                "P+H25",
                Quality.STANDARD,
                1.0,
                "player",
                0
            ),
            Potion(
                "strength_boost",
                "buff",
                "P+S30%3T",
                Quality.FINE,
                1.1,
                "player",
                0
            ),
            Potion(
                "weaken",
                "debuff",
                "E-D25%2T",
                Quality.STANDARD,
                1.0,
                "player",
                0
            ),
        ]

        return Combatant(
            id="player",
            name="Player",
            stats=stats,
            active_effects=[],
            combat_belt=potions,
            personality=None
        )

    def _create_opponent(self):
        stats = CombatStats(
            health=100,
            max_health=100,
            strength=40,
            defense=25,
            initiative=8,
            resistance=5
        )

        potions = [
            Potion(
                "shadow_strike",
                "dark",
                "E#Damage25",
                Quality.STANDARD,
                1.0,
                "opponent",
                0
            ),
            Potion(
                "dark_heal",
                "heal",
                "P+H20",
                Quality.STANDARD,
                1.0,
                "opponent",
                0
            ),
        ]

        personality = Personality(
            openness=1,
            conscientiousness=0,
            extraversion=1,
            agreeableness=-1,
            neuroticism=0
        )

        return Combatant(
            id="opponent",
            name="Dark Alchemist",
            stats=stats,
            active_effects=[],
            combat_belt=potions,
            personality=personality
        )

    def run(self):
        print("\n" + "=" * 60)
        print("COMBAT TESTBED")
        print("=" * 60)
        print("\nCommands:")
        print("  1-4       - Use potion from belt")
        print("  guard     - Boost defense this turn")
        print("  observe   - Skip turn and observe")
        print("  status    - Show combat status")
        print("  events    - Show recent events")
        print("  test      - Run validation tests")
        print("  reset     - Reset combat")
        print("  help      - Show this help")
        print("  quit      - Exit")
        print()

        while True:
            if self.player.stats.health <= 0:
                print("\n" + "=" * 60)
                print("DEFEAT!")
                print("=" * 60)
                break

            if self.opponent.stats.health <= 0:
                print("\n" + "=" * 60)
                print("VICTORY!")
                print("=" * 60)
                break

            self._display_status()

            cmd = input(f"\n[Turn {self.turn}] > ").strip().lower()

            if cmd == "quit":
                break
            elif cmd == "help":
                self._show_help()
            elif cmd == "status":
                self._display_detailed_status()
            elif cmd == "events":
                self._show_events()
            elif cmd == "test":
                self._run_tests()
            elif cmd == "reset":
                self.__init__()
                print("\nCombat reset!")
            elif cmd == "guard":
                self._execute_player_turn(CombatAction(action_type="GUARD"))
                self._execute_opponent_turn()
            elif cmd == "observe":
                self._execute_player_turn(CombatAction(action_type="OBSERVE"))
                self._execute_opponent_turn()
            elif cmd.isdigit():
                idx = int(cmd) - 1
                if 0 <= idx < len(self.player.combat_belt):
                    potion = self.player.combat_belt[idx]
                    action = CombatAction(action_type="USE_POTION", potion=potion)
                    self._execute_player_turn(action)
                    self._execute_opponent_turn()
                else:
                    print("Invalid potion number!")
            else:
                print("Unknown command. Type 'help' for commands.")

    def _display_status(self):
        print("\n" + "-" * 60)
        print(f"Turn {self.turn}")
        print("-" * 60)

        print(f"\n{self.player.name}")
        self._show_health_bar(
            self.player.stats.health,
            self.player.stats.max_health
        )
        if self.player.active_effects:
            effects_str = ", ".join(
                f"{e.name}({e.duration}T)" for e in self.player.active_effects
            )
            print(f"  Effects: {effects_str}")

        print(f"\n{self.opponent.name}")
        self._show_health_bar(
            self.opponent.stats.health,
            self.opponent.stats.max_health
        )
        if self.opponent.active_effects:
            effects_str = ", ".join(
                f"{e.name}({e.duration}T)" for e in self.opponent.active_effects
            )
            print(f"  Effects: {effects_str}")

        print("\nYour Potions:")
        for i, potion in enumerate(self.player.combat_belt, 1):
            print(f"  {i}. {potion.recipe_id:15} - {potion.esens_notation}")

    def _show_health_bar(self, current, maximum):
        pct = current / maximum if maximum > 0 else 0
        bar_length = 30
        filled = int(bar_length * pct)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"  HP: [{bar}] {current}/{maximum}")

    def _display_detailed_status(self):
        print("\n" + "=" * 60)
        print("DETAILED STATUS")
        print("=" * 60)

        print(f"\n{self.player.name}")
        print(f"  HP: {self.player.stats.health}/{self.player.stats.max_health}")
        print(f"  Strength: {self.player.stats.strength}")
        print(f"  Defense: {self.player.stats.defense}")
        print(f"  Initiative: {self.player.stats.initiative}")
        print(f"  Resistance: {self.player.stats.resistance}")

        if self.player.active_effects:
            print("  Active Effects:")
            for effect in self.player.active_effects:
                print(f"    - {effect.name}: {effect.stat_affected} "
                      f"x{effect.modifier:.1f} for {effect.duration} turns")

        print(f"\n{self.opponent.name}")
        print(f"  HP: {self.opponent.stats.health}/{self.opponent.stats.max_health}")
        print(f"  Strength: {self.opponent.stats.strength}")
        print(f"  Defense: {self.opponent.stats.defense}")
        print(f"  Initiative: {self.opponent.stats.initiative}")
        print(f"  Resistance: {self.opponent.stats.resistance}")

        if self.opponent.active_effects:
            print("  Active Effects:")
            for effect in self.opponent.active_effects:
                print(f"    - {effect.name}: {effect.stat_affected} "
                      f"x{effect.modifier:.1f} for {effect.duration} turns")

    def _execute_player_turn(self, action):
        print(f"\n>>> {self.player.name}'s turn")

        result = self.combat.execute_turn(
            self.combat_id,
            self.turn,
            self.player,
            action,
            self.opponent
        )

        for change in result.changes:
            print(f"    {change}")

        self.turn += 1

    def _execute_opponent_turn(self):
        if self.opponent.stats.health <= 0:
            return

        print(f"\n>>> {self.opponent.name}'s turn")

        action = self.combat.create_ai_action(self.opponent, self.player)

        if action.action_type == "USE_POTION":
            print(f"    Uses {action.potion.recipe_id}")

        result = self.combat.execute_turn(
            self.combat_id,
            self.turn,
            self.opponent,
            action,
            self.player
        )

        for change in result.changes:
            print(f"    {change}")

        self.turn += 1

    def _show_events(self):
        print("\n" + "=" * 60)
        print("RECENT EVENTS (last 10)")
        print("=" * 60)

        for event in self.events[-10:]:
            print(f"  {event.__class__.__name__}: {event}")

    def _run_tests(self):
        print("\n" + "=" * 60)
        print("RUNNING VALIDATION TESTS")
        print("=" * 60)

        import unittest
        from src.combat.tests import test_formulas, test_system

        loader = unittest.TestLoader()
        suite = unittest.TestSuite()

        suite.addTests(loader.loadTestsFromModule(test_formulas))
        suite.addTests(loader.loadTestsFromModule(test_system))

        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        print("\n" + "=" * 60)
        if result.wasSuccessful():
            print("ALL TESTS PASSED")
        else:
            print("SOME TESTS FAILED")
        print("=" * 60)

    def _show_help(self):
        print("\n" + "=" * 60)
        print("COMBAT TESTBED HELP")
        print("=" * 60)
        print("\nCommands:")
        print("  1-4       - Use potion from your belt")
        print("  guard     - Increase defense by 50% for this turn")
        print("  observe   - Skip your turn")
        print("  status    - Show detailed combat statistics")
        print("  events    - Show last 10 events emitted")
        print("  test      - Run all unit and integration tests")
        print("  reset     - Reset combat to initial state")
        print("  help      - Show this help message")
        print("  quit      - Exit testbed")
        print("\nCombat Mechanics:")
        print("  - Damage is calculated using strength vs defense")
        print("  - Status effects modify stats temporarily")
        print("  - Effects decrease in duration each turn")
        print("  - AI opponent uses personality-based decisions")
        print("=" * 60)


def main():
    testbed = CombatTestbed()
    testbed.run()


if __name__ == "__main__":
    main()
