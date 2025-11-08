import random
from src.core.data_structures import Quality


def calculate_success_chance(
    knowledge: int,
    precision: int,
    intuition: int,
    recipe_difficulty: int,
    tool_bonus: float,
    prep_bonus: float = 0.0
) -> float:
    return max(0.0, min(1.0,
        0.5 +
        (knowledge / 200.0) +
        tool_bonus +
        prep_bonus -
        (recipe_difficulty / 100.0)
    ))


def roll_craft_attempt(success_chance: float) -> tuple[bool, int]:
    roll = random.randint(1, 20)

    if roll == 1:
        return (False, roll)

    if roll == 20:
        return (True, roll)

    adjusted_chance = success_chance + ((roll - 10) / 20.0)

    return (adjusted_chance >= 0.5, roll)


def determine_quality(
    success_margin: float,
    ingredient_quality: Quality,
    precision: int
) -> Quality:
    if success_margin >= 0.5:
        base = Quality.EXCEPTIONAL
    elif success_margin >= 0.3:
        base = Quality.FINE
    elif success_margin >= 0.1:
        base = Quality.STANDARD
    else:
        base = Quality.POOR

    if precision >= 80 and random.random() < 0.2:
        base = min(Quality.MASTERWORK, base + 1)

    if ingredient_quality == Quality.POOR:
        base = max(Quality.POOR, base - 1)

    return base


def calculate_potency(quality: Quality, recipe_base: float = 1.0) -> float:
    multipliers = {
        Quality.POOR: 0.75,
        Quality.STANDARD: 1.0,
        Quality.FINE: 1.1,
        Quality.EXCEPTIONAL: 1.25,
        Quality.MASTERWORK: 1.5
    }
    return recipe_base * multipliers[quality]


def calculate_xp_reward(
    recipe_difficulty: int,
    success: bool,
    quality: Quality
) -> dict[str, int]:
    base_xp = recipe_difficulty

    if not success:
        return {
            "knowledge": base_xp // 10,
            "precision": 0,
            "intuition": base_xp // 20
        }

    quality_bonus = {
        Quality.POOR: 0.8,
        Quality.STANDARD: 1.0,
        Quality.FINE: 1.2,
        Quality.EXCEPTIONAL: 1.5,
        Quality.MASTERWORK: 2.0
    }[quality]

    return {
        "knowledge": int(base_xp * quality_bonus),
        "precision": int((base_xp / 2) * quality_bonus),
        "intuition": 0
    }


def update_recipe_mastery(
    current_mastery: int,
    success: bool,
    quality: Quality
) -> int:
    if not success:
        gain = 1
    else:
        gain = {
            Quality.POOR: 3,
            Quality.STANDARD: 5,
            Quality.FINE: 8,
            Quality.EXCEPTIONAL: 12,
            Quality.MASTERWORK: 15
        }[quality]

    return min(100, current_mastery + gain)


def get_mastery_bonus(mastery: int) -> float:
    if mastery >= 75:
        return 0.20
    elif mastery >= 50:
        return 0.15
    elif mastery >= 25:
        return 0.10
    else:
        return 0.0
