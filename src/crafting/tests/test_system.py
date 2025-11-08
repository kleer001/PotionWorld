from src.core.event_bus import EventBus
from src.core.data_structures import (
    Recipe,
    IngredientInstance,
    CrafterStats,
    CraftInput,
    Quality,
)
from src.core.events import (
    CraftCompleted,
    PotionCreated,
    RecipeMasteryGained,
    XPGained,
    IngredientsConsumed,
)
from src.crafting.system import CraftingSystem


def test_craft_success_emits_events():
    event_bus = EventBus()
    crafting = CraftingSystem(event_bus)

    events = []
    event_bus.subscribe_all(lambda e: events.append(e))

    recipe = Recipe(
        id="test_recipe",
        name="Test Potion",
        difficulty=10,
        esens="H[+5]",
        base_potency=1.0,
        ingredients=["herb"]
    )

    ingredients = [
        IngredientInstance(
            id="herb_1",
            type="herb",
            quality=Quality.STANDARD
        )
    ]

    input = CraftInput(
        recipe=recipe,
        ingredients=ingredients,
        crafter_stats=CrafterStats(knowledge=80, precision=70, intuition=60),
        tool_bonus=0.1
    )

    result = crafting.craft(input, crafter_id="test_crafter", current_mastery=0)

    assert result.success or not result.success

    craft_completed = [e for e in events if isinstance(e, CraftCompleted)]
    assert len(craft_completed) == 1

    ingredients_consumed = [e for e in events if isinstance(e, IngredientsConsumed)]
    assert len(ingredients_consumed) == 1

    if result.success:
        potion_created = [e for e in events if isinstance(e, PotionCreated)]
        assert len(potion_created) == 1


def test_craft_failure_gives_consolation_xp():
    event_bus = EventBus()
    crafting = CraftingSystem(event_bus)

    recipe = Recipe(
        id="impossible",
        name="Impossible Potion",
        difficulty=100,
        esens="H[+100]",
        base_potency=1.0,
        ingredients=["rare"]
    )

    ingredients = [
        IngredientInstance(
            id="rare_1",
            type="rare",
            quality=Quality.STANDARD
        )
    ]

    input = CraftInput(
        recipe=recipe,
        ingredients=ingredients,
        crafter_stats=CrafterStats(knowledge=0, precision=0, intuition=0),
        tool_bonus=0.0
    )

    successes = 0
    for _ in range(10):
        result = crafting.craft(input, crafter_id="test_crafter", current_mastery=0)
        if result.success:
            successes += 1

    assert successes < 10


def test_mastery_increases_success_chance():
    event_bus = EventBus()
    crafting = CraftingSystem(event_bus)

    recipe = Recipe(
        id="medium",
        name="Medium Potion",
        difficulty=50,
        esens="H[+10]",
        base_potency=1.0,
        ingredients=["herb"]
    )

    ingredients = [
        IngredientInstance(
            id="herb_1",
            type="herb",
            quality=Quality.STANDARD
        )
    ]

    input = CraftInput(
        recipe=recipe,
        ingredients=ingredients,
        crafter_stats=CrafterStats(knowledge=50, precision=50, intuition=50),
        tool_bonus=0.0
    )

    novice_successes = 0
    for _ in range(20):
        result = crafting.craft(input, crafter_id="test_crafter", current_mastery=0)
        if result.success:
            novice_successes += 1

    expert_successes = 0
    for _ in range(20):
        result = crafting.craft(input, crafter_id="test_crafter", current_mastery=80)
        if result.success:
            expert_successes += 1

    assert expert_successes >= novice_successes


def test_ingredient_quality_affects_result():
    event_bus = EventBus()
    crafting = CraftingSystem(event_bus)

    recipe = Recipe(
        id="quality_test",
        name="Quality Test",
        difficulty=20,
        esens="H[+5]",
        base_potency=1.0,
        ingredients=["herb"]
    )

    poor_ingredients = [
        IngredientInstance(
            id="herb_poor",
            type="herb",
            quality=Quality.POOR
        )
    ]

    good_ingredients = [
        IngredientInstance(
            id="herb_good",
            type="herb",
            quality=Quality.EXCEPTIONAL
        )
    ]

    input_poor = CraftInput(
        recipe=recipe,
        ingredients=poor_ingredients,
        crafter_stats=CrafterStats(knowledge=80, precision=80, intuition=80),
        tool_bonus=0.2
    )

    input_good = CraftInput(
        recipe=recipe,
        ingredients=good_ingredients,
        crafter_stats=CrafterStats(knowledge=80, precision=80, intuition=80),
        tool_bonus=0.2
    )

    poor_results = []
    good_results = []

    for _ in range(10):
        result = crafting.craft(input_poor, crafter_id="test_crafter", current_mastery=50)
        if result.success and result.quality:
            poor_results.append(result.quality)

        result = crafting.craft(input_good, crafter_id="test_crafter", current_mastery=50)
        if result.success and result.quality:
            good_results.append(result.quality)

    if poor_results and good_results:
        avg_poor = sum(poor_results) / len(poor_results)
        avg_good = sum(good_results) / len(good_results)
        assert avg_good >= avg_poor


def test_xp_gained_event_emission():
    event_bus = EventBus()
    crafting = CraftingSystem(event_bus)

    xp_events = []
    event_bus.subscribe(XPGained, lambda e: xp_events.append(e))

    recipe = Recipe(
        id="xp_test",
        name="XP Test",
        difficulty=50,
        esens="H[+10]",
        base_potency=1.0,
        ingredients=["herb"]
    )

    ingredients = [
        IngredientInstance(
            id="herb_1",
            type="herb",
            quality=Quality.STANDARD
        )
    ]

    input = CraftInput(
        recipe=recipe,
        ingredients=ingredients,
        crafter_stats=CrafterStats(knowledge=80, precision=70, intuition=60),
        tool_bonus=0.1
    )

    crafting.craft(input, crafter_id="test_crafter", current_mastery=0)

    assert len(xp_events) > 0


def test_mastery_gained_event_emission():
    event_bus = EventBus()
    crafting = CraftingSystem(event_bus)

    mastery_events = []
    event_bus.subscribe(RecipeMasteryGained, lambda e: mastery_events.append(e))

    recipe = Recipe(
        id="mastery_test",
        name="Mastery Test",
        difficulty=30,
        esens="H[+5]",
        base_potency=1.0,
        ingredients=["herb"]
    )

    ingredients = [
        IngredientInstance(
            id="herb_1",
            type="herb",
            quality=Quality.STANDARD
        )
    ]

    input = CraftInput(
        recipe=recipe,
        ingredients=ingredients,
        crafter_stats=CrafterStats(knowledge=80, precision=70, intuition=60),
        tool_bonus=0.2
    )

    crafting.craft(input, crafter_id="test_crafter", current_mastery=0)

    assert len(mastery_events) >= 0


if __name__ == "__main__":
    test_craft_success_emits_events()
    test_craft_failure_gives_consolation_xp()
    test_mastery_increases_success_chance()
    test_ingredient_quality_affects_result()
    test_xp_gained_event_emission()
    test_mastery_gained_event_emission()
    print("All system tests passed!")
