from typing import List
from src.core.event_bus import EventBus
from src.core.data_structures import (
    Recipe,
    IngredientInstance,
    CrafterStats,
    CraftInput,
    CraftResult,
    Quality,
)
from src.crafting.system import CraftingSystem


class CraftingTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.crafting = CraftingSystem(self.event_bus)

        self.stats = CrafterStats(knowledge=50, precision=40, intuition=30)
        self.tool_bonus = 0.1
        self.mastery = {}
        self.event_log = []

        self.event_bus.subscribe_all(self._on_event)

        self.recipes = self._create_sample_recipes()

    def run(self):
        print("=" * 60)
        print("CRAFTING TESTBED (God Mode)")
        print("=" * 60)

        while True:
            self._display_status()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "stats" and len(cmd) >= 4:
                self._set_stats(cmd[1:])
            elif cmd[0] == "tool" and len(cmd) >= 2:
                self._set_tool(float(cmd[1]))
            elif cmd[0] == "mastery" and len(cmd) >= 3:
                self._set_mastery(cmd[1], int(cmd[2]))
            elif cmd[0] == "craft" and len(cmd) >= 2:
                self._craft(cmd[1])
            elif cmd[0] == "batch" and len(cmd) >= 3:
                self._batch_craft(cmd[1], int(cmd[2]))
            elif cmd[0] == "recipes":
                self._list_recipes()
            elif cmd[0] == "events":
                self._show_events()
            elif cmd[0] == "test":
                self._run_tests()
            elif cmd[0] == "help":
                self._show_help()
            elif cmd[0] == "quit":
                break
            else:
                print("Unknown command. Type 'help' for commands.")

    def _display_status(self):
        print(f"\nCurrent Stats: K:{self.stats.knowledge} P:{self.stats.precision} I:{self.stats.intuition}")
        print(f"Tool Bonus: {self.tool_bonus:.1%}")
        if self.mastery:
            print(f"Recipe Mastery: {', '.join(f'{k}:{v}' for k, v in self.mastery.items())}")

    def _set_stats(self, args):
        self.stats.knowledge = int(args[0])
        self.stats.precision = int(args[1])
        self.stats.intuition = int(args[2])
        print(f"Stats set to K:{args[0]} P:{args[1]} I:{args[2]}")

    def _set_tool(self, bonus: float):
        self.tool_bonus = max(0.0, min(0.3, bonus))
        print(f"Tool bonus set to {self.tool_bonus:.1%}")

    def _set_mastery(self, recipe_id: str, mastery: int):
        self.mastery[recipe_id] = max(0, min(100, mastery))
        print(f"Mastery for {recipe_id} set to {self.mastery[recipe_id]}")

    def _craft(self, recipe_id: str):
        recipe = self._get_recipe(recipe_id)
        if not recipe:
            print(f"Recipe '{recipe_id}' not found. Use 'recipes' to list available recipes.")
            return

        input = CraftInput(
            recipe=recipe,
            ingredients=self._create_test_ingredients(recipe),
            crafter_stats=self.stats,
            tool_bonus=self.tool_bonus
        )

        current_mastery = self.mastery.get(recipe_id, 0)
        result = self.crafting.craft(input, crafter_id="testbed", current_mastery=current_mastery)

        self.mastery[recipe_id] = current_mastery + result.mastery_gain

        self._display_craft_result(result)

    def _batch_craft(self, recipe_id: str, count: int):
        recipe = self._get_recipe(recipe_id)
        if not recipe:
            print(f"Recipe '{recipe_id}' not found. Use 'recipes' to list available recipes.")
            return

        print(f"\nBatch crafting {recipe_id} x{count}...")

        results = []
        for i in range(count):
            input = CraftInput(
                recipe=recipe,
                ingredients=self._create_test_ingredients(recipe),
                crafter_stats=self.stats,
                tool_bonus=self.tool_bonus
            )

            current_mastery = self.mastery.get(recipe_id, 0)
            result = self.crafting.craft(input, crafter_id="testbed", current_mastery=current_mastery)
            results.append(result)

            self.mastery[recipe_id] = current_mastery + result.mastery_gain

            if (i + 1) % 10 == 0:
                print(f"  {i + 1}/{count}...")

        self._display_batch_results(results)

    def _display_craft_result(self, result: CraftResult):
        print("\n" + "=" * 60)
        print("CRAFT RESULT")
        print("=" * 60)

        breakdown = result.formula_breakdown
        print(f"\nSuccess Calculation:")
        print(f"  Base:            {breakdown.base_chance:>6.1%}")
        print(f"  + Knowledge/2:   {breakdown.knowledge_bonus:>+6.1%}")
        print(f"  + Tool Bonus:    {breakdown.tool_bonus:>+6.1%}")
        print(f"  + Mastery:       {breakdown.mastery_bonus:>+6.1%}")
        print(f"  - Difficulty:    {-breakdown.difficulty_penalty:>+6.1%}")
        print(f"  + d20 ({breakdown.dice_roll:>2}):    {(breakdown.dice_roll-10)/20:>+6.1%}")
        print(f"  {'-' * 30}")
        print(f"  TOTAL:           {breakdown.final_chance:>6.1%}")

        print(f"\n  Threshold: {breakdown.success_threshold:.1%}")
        print(f"  Result: {'✓ SUCCESS' if result.success else '✗ FAILURE'}")

        if result.success and result.quality and result.potion:
            margin = breakdown.final_chance - breakdown.success_threshold
            print(f"  Margin: {margin:+.1%}")
            print(f"\n  Quality: {result.quality.name}")
            print(f"  Potency: {result.potion.potency:.1%}")
            print(f"  Potion ID: {result.potion.id}")

        print(f"\nXP Rewards:")
        for stat, xp in result.xp_rewards.items():
            if xp > 0:
                print(f"  {stat.capitalize():>12}: +{xp}")

        print(f"\nMastery Gain: +{result.mastery_gain}")

    def _display_batch_results(self, results: List[CraftResult]):
        total = len(results)
        successes = sum(1 for r in results if r.success)
        failures = total - successes

        print(f"\n{'=' * 60}")
        print(f"BATCH RESULTS (n={total})")
        print(f"{'=' * 60}")

        print(f"\nSuccess Rate: {successes}/{total} ({successes/total:.1%})")
        print(f"Failure Rate: {failures}/{total} ({failures/total:.1%})")

        if successes > 0:
            qualities = [r.quality for r in results if r.success and r.quality]
            print(f"\nQuality Distribution:")
            for q in Quality:
                count = sum(1 for qual in qualities if qual == q)
                if count > 0:
                    print(f"  {q.name:>12}: {count:>3} ({count/successes:.1%})")

        avg_xp = {
            "knowledge": sum(r.xp_rewards["knowledge"] for r in results) / total,
            "precision": sum(r.xp_rewards["precision"] for r in results) / total,
            "intuition": sum(r.xp_rewards["intuition"] for r in results) / total
        }

        print(f"\nAverage XP per Craft:")
        for stat, xp in avg_xp.items():
            if xp > 0:
                print(f"  {stat.capitalize():>12}: {xp:.1f}")

        total_mastery = sum(r.mastery_gain for r in results)
        print(f"\nTotal Mastery Gained: {total_mastery}")

    def _list_recipes(self):
        print("\nAvailable Recipes:")
        print("=" * 60)
        for recipe in self.recipes:
            mastery = self.mastery.get(recipe.id, 0)
            print(f"  {recipe.id:20} | Diff: {recipe.difficulty:>3} | Mastery: {mastery:>3}")

    def _show_events(self):
        print("\nRecent Events (last 10):")
        print("=" * 60)
        for event in self.event_log[-10:]:
            print(f"  {type(event).__name__}: {event}")

    def _run_tests(self):
        print("\nRunning validation tests...")
        from src.crafting.tests import test_formulas
        from src.crafting.tests import test_system
        from src.core.tests import test_event_bus

        test_event_bus.test_subscribe_and_emit()
        test_event_bus.test_multiple_subscribers()
        test_event_bus.test_different_event_types()
        test_event_bus.test_subscribe_all()
        test_event_bus.test_clear()

        test_formulas.test_success_formula_high_stats_easy_recipe()
        test_formulas.test_success_formula_low_stats_hard_recipe()
        test_formulas.test_success_formula_clamping()
        test_formulas.test_quality_scales_with_margin()
        test_formulas.test_potency_multipliers()
        test_formulas.test_xp_reward_scales_with_difficulty()
        test_formulas.test_mastery_progression_failure()
        test_formulas.test_mastery_bonus_tiers()

        test_system.test_craft_success_emits_events()
        test_system.test_xp_gained_event_emission()

        print("✓ All validation tests passed!")

    def _show_help(self):
        print("\nCommands:")
        print("  stats <K> <P> <I>    - Set crafter stats (god mode)")
        print("  tool <bonus>         - Set tool bonus (0.0-0.3)")
        print("  mastery <recipe> <n> - Set recipe mastery (god mode)")
        print("  craft <recipe>       - Craft once with breakdown")
        print("  batch <recipe> <n>   - Craft N times, show stats")
        print("  recipes              - List available recipes")
        print("  test                 - Run validation tests")
        print("  events               - Show recent events")
        print("  help                 - Show this help")
        print("  quit                 - Exit")

    def _on_event(self, event):
        self.event_log.append(event)

    def _get_recipe(self, recipe_id: str) -> Recipe:
        for recipe in self.recipes:
            if recipe.id == recipe_id:
                return recipe
        return None

    def _create_test_ingredients(self, recipe: Recipe) -> List[IngredientInstance]:
        return [
            IngredientInstance(
                id=f"{ing}_test",
                type=ing,
                quality=Quality.STANDARD,
                freshness=1.0
            )
            for ing in recipe.ingredients
        ]

    def _create_sample_recipes(self) -> List[Recipe]:
        return [
            Recipe(
                id="healing_basic",
                name="Basic Healing Potion",
                difficulty=20,
                esens="H[+5]",
                base_potency=1.0,
                ingredients=["herb"]
            ),
            Recipe(
                id="healing_advanced",
                name="Advanced Healing Potion",
                difficulty=50,
                esens="H[+15]",
                base_potency=1.5,
                ingredients=["herb", "mineral"]
            ),
            Recipe(
                id="healing_master",
                name="Master Healing Potion",
                difficulty=80,
                esens="H[+30]",
                base_potency=2.0,
                ingredients=["herb", "mineral", "crystal"]
            ),
            Recipe(
                id="stamina_basic",
                name="Basic Stamina Potion",
                difficulty=15,
                esens="S[+10]",
                base_potency=1.0,
                ingredients=["herb"]
            ),
            Recipe(
                id="mana_restore",
                name="Mana Restore Potion",
                difficulty=40,
                esens="M[+20]",
                base_potency=1.2,
                ingredients=["herb", "sap"]
            ),
        ]


def main():
    testbed = CraftingTestbed()
    testbed.run()


if __name__ == "__main__":
    main()
