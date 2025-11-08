import random
from src.crafting.formulas import (
    calculate_success_chance,
    roll_craft_attempt,
    determine_quality,
    calculate_potency,
    calculate_xp_reward,
    update_recipe_mastery,
    get_mastery_bonus,
)
from src.core.data_structures import Quality


def test_success_formula_high_stats_easy_recipe():
    chance = calculate_success_chance(
        knowledge=80,
        precision=70,
        intuition=60,
        recipe_difficulty=20,
        tool_bonus=0.1
    )
    assert chance >= 0.8


def test_success_formula_low_stats_hard_recipe():
    chance = calculate_success_chance(
        knowledge=20,
        precision=20,
        intuition=20,
        recipe_difficulty=80,
        tool_bonus=0.0
    )
    assert chance <= 0.3


def test_success_formula_clamping():
    very_high = calculate_success_chance(
        knowledge=200,
        precision=200,
        intuition=200,
        recipe_difficulty=0,
        tool_bonus=0.3
    )
    assert very_high <= 1.0

    very_low = calculate_success_chance(
        knowledge=0,
        precision=0,
        intuition=0,
        recipe_difficulty=100,
        tool_bonus=0.0
    )
    assert very_low >= 0.0


def test_critical_rolls():
    random.seed(42)
    results = []
    for _ in range(100):
        success, roll = roll_craft_attempt(1.0)
        if roll == 1:
            assert not success
        if roll == 20:
            assert success
        results.append((success, roll))

    assert len(results) == 100


def test_quality_scales_with_margin():
    q1 = determine_quality(0.05, Quality.STANDARD, precision=50)
    q2 = determine_quality(0.30, Quality.STANDARD, precision=50)
    q3 = determine_quality(0.60, Quality.STANDARD, precision=50)

    assert q1 <= q2 <= q3


def test_quality_poor_ingredients_downgrade():
    random.seed(42)
    quality = determine_quality(0.6, Quality.POOR, precision=50)
    assert quality < Quality.EXCEPTIONAL


def test_quality_high_precision_upgrade():
    random.seed(42)
    results = []
    for _ in range(100):
        q = determine_quality(0.6, Quality.STANDARD, precision=90)
        results.append(q)

    has_upgrade = any(q >= Quality.EXCEPTIONAL for q in results)
    assert has_upgrade


def test_potency_multipliers():
    assert calculate_potency(Quality.POOR) == 0.75
    assert calculate_potency(Quality.STANDARD) == 1.0
    assert calculate_potency(Quality.FINE) == 1.1
    assert calculate_potency(Quality.EXCEPTIONAL) == 1.25
    assert calculate_potency(Quality.MASTERWORK) == 1.5


def test_potency_with_base():
    assert calculate_potency(Quality.STANDARD, 2.0) == 2.0
    assert calculate_potency(Quality.FINE, 2.0) == 2.2


def test_xp_reward_scales_with_difficulty():
    easy_xp = calculate_xp_reward(20, True, Quality.STANDARD)
    hard_xp = calculate_xp_reward(80, True, Quality.STANDARD)

    assert hard_xp["knowledge"] > easy_xp["knowledge"]


def test_xp_reward_scales_with_quality():
    standard_xp = calculate_xp_reward(50, True, Quality.STANDARD)
    exceptional_xp = calculate_xp_reward(50, True, Quality.EXCEPTIONAL)

    assert exceptional_xp["knowledge"] > standard_xp["knowledge"]


def test_xp_reward_failure_consolation():
    fail_xp = calculate_xp_reward(50, False, Quality.POOR)

    assert fail_xp["knowledge"] > 0
    assert fail_xp["precision"] == 0
    assert fail_xp["intuition"] > 0


def test_mastery_progression_failure():
    mastery = update_recipe_mastery(0, False, Quality.POOR)
    assert mastery == 1


def test_mastery_progression_success():
    mastery = update_recipe_mastery(0, True, Quality.FINE)
    assert mastery == 8


def test_mastery_progression_masterwork():
    mastery = update_recipe_mastery(10, True, Quality.MASTERWORK)
    assert mastery == 25


def test_mastery_progression_cap():
    mastery = update_recipe_mastery(95, True, Quality.MASTERWORK)
    assert mastery == 100


def test_mastery_bonus_tiers():
    assert get_mastery_bonus(0) == 0.0
    assert get_mastery_bonus(24) == 0.0
    assert get_mastery_bonus(25) == 0.10
    assert get_mastery_bonus(50) == 0.15
    assert get_mastery_bonus(75) == 0.20


if __name__ == "__main__":
    test_success_formula_high_stats_easy_recipe()
    test_success_formula_low_stats_hard_recipe()
    test_success_formula_clamping()
    test_critical_rolls()
    test_quality_scales_with_margin()
    test_quality_poor_ingredients_downgrade()
    test_quality_high_precision_upgrade()
    test_potency_multipliers()
    test_potency_with_base()
    test_xp_reward_scales_with_difficulty()
    test_xp_reward_scales_with_quality()
    test_xp_reward_failure_consolation()
    test_mastery_progression_failure()
    test_mastery_progression_success()
    test_mastery_progression_masterwork()
    test_mastery_progression_cap()
    test_mastery_bonus_tiers()
    print("All formula tests passed!")
