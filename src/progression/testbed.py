from src.core.event_bus import EventBus
from src.core.data_structures import Quality
from src.progression.system import ProgressionSystem
from src.progression.formulas import (
    xp_to_stat, stat_to_xp, xp_for_next_milestone,
    calculate_reputation_level, get_reputation_modifiers,
    get_mastery_bonuses, SPECIALIZATIONS
)


class ProgressionTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.system = ProgressionSystem(self.event_bus)

        self.player_xp = {
            "knowledge": 0,
            "precision": 0,
            "intuition": 0,
            "business_acumen": 0,
            "combat_instinct": 0
        }

        self.player_stats = {
            "knowledge": 0,
            "precision": 0,
            "intuition": 0,
            "business_acumen": 0,
            "combat_instinct": 0
        }

        self.reputation = {
            "village": 50,
            "city": 50,
            "capital": 50
        }

        self.recipe_mastery = {}
        self.specializations = []
        self.events = []

        self.event_bus.subscribe(self._on_event)

    def _on_event(self, event):
        self.events.append(event)

    def run(self):
        print("PROGRESSION TESTBED")
        print("=" * 60)

        while True:
            self._display_status()
            print()
            cmd_input = input("> ").strip()

            if not cmd_input:
                continue

            cmd = cmd_input.split()

            if cmd[0] == "add":
                if len(cmd) < 3:
                    print("Usage: add <stat> <xp>")
                else:
                    self._add_xp(cmd[1], int(cmd[2]))

            elif cmd[0] == "set":
                if len(cmd) < 3:
                    print("Usage: set <stat> <xp>")
                else:
                    self._set_xp(cmd[1], int(cmd[2]))

            elif cmd[0] == "spec":
                if len(cmd) < 2:
                    print("Usage: spec <specialization_id>")
                else:
                    self._choose_spec(cmd[1])

            elif cmd[0] == "specs":
                self._list_specializations()

            elif cmd[0] == "rep":
                if len(cmd) < 3:
                    print("Usage: rep <region> <delta>")
                else:
                    self._update_reputation(cmd[1], int(cmd[2]))

            elif cmd[0] == "mastery":
                if len(cmd) < 2:
                    print("Usage: mastery <recipe_id> [quality]")
                else:
                    quality_str = cmd[2] if len(cmd) > 2 else "STANDARD"
                    self._update_mastery(cmd[1], quality_str)

            elif cmd[0] == "sim":
                self._simulate_progression()

            elif cmd[0] == "events":
                limit = int(cmd[1]) if len(cmd) > 1 else 10
                self._show_events(limit)

            elif cmd[0] == "test":
                self._run_tests()

            elif cmd[0] == "help":
                self._show_help()

            elif cmd[0] == "quit":
                break

            else:
                print(f"Unknown command: {cmd[0]}")
                print("Type 'help' for commands")

    def _display_status(self):
        print()
        print("PLAYER STATS")
        print("-" * 60)

        for stat, xp in self.player_xp.items():
            stat_value = self.player_stats[stat]
            next_xp = xp_for_next_milestone(xp)
            milestone_indicator = " ✓" if stat_value % 20 == 0 and stat_value > 0 else ""

            print(f"{stat:20s} {stat_value:3d}/100  ({xp:6d} XP, {next_xp:6d} to next){milestone_indicator}")

        print()
        print("REPUTATION")
        print("-" * 60)

        for region, rep in self.reputation.items():
            level = calculate_reputation_level(rep)
            modifiers = get_reputation_modifiers(rep)
            print(f"{region:15s} {rep:3d}/100  [{level:10s}]  Price: {modifiers['price_modifier']:.2f}x")

        if self.specializations:
            print()
            print("SPECIALIZATIONS")
            print("-" * 60)
            for spec in self.specializations:
                print(f"  {spec.name} ({spec.category})")

        if self.recipe_mastery:
            print()
            print("RECIPE MASTERY")
            print("-" * 60)
            for recipe_id, mastery in sorted(self.recipe_mastery.items()):
                bonuses = get_mastery_bonuses(mastery)
                level = mastery // 20
                level_names = ["Novice", "Competent", "Proficient", "Expert", "Master"]
                level_name = level_names[min(level, 4)]
                print(f"  {recipe_id:20s} {mastery:3d}/100  [{level_name:10s}]  Success: +{bonuses['success_bonus']:.0%}")

    def _add_xp(self, stat: str, amount: int):
        if stat not in self.player_xp:
            print(f"Unknown stat: {stat}")
            return

        result = self.system.add_xp("player", stat, amount, self.player_xp[stat])

        self.player_xp[stat] = result.new_xp
        self.player_stats[stat] = result.new_stat

        print(f"\n+{amount} XP to {stat}")
        print(f"  {result.old_stat} → {result.new_stat}")
        print(f"  ({result.new_xp} XP, {xp_for_next_milestone(result.new_xp)} to next)")

        if result.milestone_reached:
            print(f"  🎉 MILESTONE REACHED: {result.new_stat}!")

    def _set_xp(self, stat: str, xp: int):
        if stat not in self.player_xp:
            print(f"Unknown stat: {stat}")
            return

        self.player_xp[stat] = xp
        self.player_stats[stat] = xp_to_stat(xp)

        print(f"\n{stat} set to {xp} XP (stat: {self.player_stats[stat]})")

    def _choose_spec(self, spec_id: str):
        success = self.system.choose_specialization("player", spec_id, self.player_stats)

        if success:
            spec = next(s for s in SPECIALIZATIONS if s.id == spec_id)
            self.specializations.append(spec)
            print(f"\n✓ Chosen specialization: {spec.name}")
            print(f"  Category: {spec.category}")
            print(f"  Bonuses: {spec.bonuses}")
        else:
            print(f"\n✗ Cannot choose {spec_id}")
            spec = next((s for s in SPECIALIZATIONS if s.id == spec_id), None)
            if spec:
                print(f"  Prerequisites: {spec.prerequisites}")

    def _list_specializations(self):
        print("\nAVAILABLE SPECIALIZATIONS")
        print("=" * 60)

        by_category = {}
        for spec in SPECIALIZATIONS:
            if spec.category not in by_category:
                by_category[spec.category] = []
            by_category[spec.category].append(spec)

        for category, specs in sorted(by_category.items()):
            print(f"\n{category.upper()}")
            print("-" * 60)
            for spec in specs:
                available = all(
                    self.player_stats.get(stat, 0) >= val
                    for stat, val in spec.prerequisites.items()
                )
                marker = "✓" if available else "✗"
                print(f"  {marker} {spec.id:20s} {spec.name}")
                print(f"     Prerequisites: {spec.prerequisites}")
                print(f"     Bonuses: {spec.bonuses}")

    def _update_reputation(self, region: str, delta: int):
        if region not in self.reputation:
            self.reputation[region] = 50

        old_value = self.reputation[region]
        new_value = self.system.update_reputation(
            "player", region, delta, old_value, "manual_update"
        )

        self.reputation[region] = new_value

        old_level = calculate_reputation_level(old_value)
        new_level = calculate_reputation_level(new_value)

        print(f"\n{region} reputation: {old_value} → {new_value}")
        if old_level != new_level:
            print(f"  Level changed: {old_level} → {new_level}")

    def _update_mastery(self, recipe_id: str, quality_str: str):
        quality_map = {
            "POOR": Quality.POOR,
            "STANDARD": Quality.STANDARD,
            "FINE": Quality.FINE,
            "EXCEPTIONAL": Quality.EXCEPTIONAL,
            "MASTERWORK": Quality.MASTERWORK
        }

        quality = quality_map.get(quality_str.upper(), Quality.STANDARD)

        if recipe_id not in self.recipe_mastery:
            self.recipe_mastery[recipe_id] = 0

        old_mastery = self.recipe_mastery[recipe_id]
        new_mastery = self.system.update_recipe_mastery(
            "player", recipe_id, old_mastery, True, quality
        )

        self.recipe_mastery[recipe_id] = new_mastery

        print(f"\n{recipe_id} mastery: {old_mastery} → {new_mastery}")

        old_bonuses = get_mastery_bonuses(old_mastery)
        new_bonuses = get_mastery_bonuses(new_mastery)

        if old_bonuses != new_bonuses:
            print(f"  Bonuses updated!")
            print(f"    Success: {old_bonuses['success_bonus']:.0%} → {new_bonuses['success_bonus']:.0%}")

    def _simulate_progression(self):
        print("\n═══ SIMULATING PROGRESSION ═══")
        print("Crafting 100 potions of increasing difficulty...\n")

        for i in range(100):
            difficulty = min(100, 20 + i)
            xp = difficulty

            result = self.system.add_xp(
                "player", "knowledge", xp, self.player_xp["knowledge"]
            )

            self.player_xp["knowledge"] = result.new_xp
            self.player_stats["knowledge"] = result.new_stat

            if result.milestone_reached:
                print(f"Craft #{i+1}: MILESTONE {result.new_stat}!")

        print(f"\nFinal Knowledge: {self.player_stats['knowledge']}")
        print(f"Total XP: {self.player_xp['knowledge']}")

    def _show_events(self, limit: int):
        print(f"\nRECENT EVENTS (last {limit})")
        print("=" * 60)

        for event in self.events[-limit:]:
            print(f"  {event.__class__.__name__}: {event}")

    def _run_tests(self):
        print("\nRUNNING VALIDATION TESTS")
        print("=" * 60)

        tests_passed = 0
        tests_total = 0

        tests_total += 1
        if xp_to_stat(0) == 0 and xp_to_stat(100000) == 100:
            print("✓ XP to stat conversion boundaries")
            tests_passed += 1
        else:
            print("✗ XP to stat conversion boundaries")

        tests_total += 1
        if stat_to_xp(20) < stat_to_xp(40) < stat_to_xp(60):
            print("✓ XP curve is logarithmic")
            tests_passed += 1
        else:
            print("✗ XP curve is logarithmic")

        tests_total += 1
        if calculate_reputation_level(0) == "Unknown" and calculate_reputation_level(90) == "Legendary":
            print("✓ Reputation levels")
            tests_passed += 1
        else:
            print("✗ Reputation levels")

        tests_total += 1
        bonuses = get_mastery_bonuses(50)
        if bonuses["success_bonus"] == 0.20:
            print("✓ Mastery bonuses")
            tests_passed += 1
        else:
            print("✗ Mastery bonuses")

        tests_total += 1
        if len(SPECIALIZATIONS) == 7:
            print("✓ All specializations defined")
            tests_passed += 1
        else:
            print("✗ All specializations defined")

        print()
        print(f"Tests passed: {tests_passed}/{tests_total}")

        if tests_passed == tests_total:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed")

    def _show_help(self):
        print("\nCOMMANDS")
        print("=" * 60)
        print("add <stat> <xp>          - Add XP to stat")
        print("set <stat> <xp>          - Set XP value (god mode)")
        print("spec <id>                - Choose specialization")
        print("specs                    - List all specializations")
        print("rep <region> <delta>     - Update reputation")
        print("mastery <recipe> [qual]  - Update recipe mastery")
        print("sim                      - Simulate progression curve")
        print("events [n]               - Show recent events")
        print("test                     - Run validation tests")
        print("help                     - Show this help")
        print("quit                     - Exit testbed")
        print()
        print("Stats: knowledge, precision, intuition, business_acumen, combat_instinct")
        print("Qualities: POOR, STANDARD, FINE, EXCEPTIONAL, MASTERWORK")


if __name__ == "__main__":
    testbed = ProgressionTestbed()
    testbed.run()
