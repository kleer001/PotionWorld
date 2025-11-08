import math
from typing import Dict, List
from src.core.data_structures import Quality
from src.progression.data_structures import Specialization


def xp_to_stat(xp: int) -> int:
    if xp <= 0:
        return 0
    if xp >= 100000:
        return 100

    stat = 40 * math.log10(xp) - 100
    return int(min(100, max(0, stat)))


def stat_to_xp(stat: int) -> int:
    if stat <= 0:
        return 0
    if stat >= 100:
        return 100000

    xp = math.pow(10, (stat + 100) / 40)
    return int(xp)


def xp_for_next_milestone(current_xp: int) -> int:
    current_stat = xp_to_stat(current_xp)
    next_milestone = ((current_stat // 20) + 1) * 20

    if next_milestone > 100:
        return 0

    return stat_to_xp(next_milestone) - current_xp


def update_mastery(current_mastery: int, success: bool, quality: Quality) -> int:
    if not success:
        gain = 1
    else:
        gain_map = {
            Quality.POOR: 3,
            Quality.STANDARD: 5,
            Quality.FINE: 8,
            Quality.EXCEPTIONAL: 12,
            Quality.MASTERWORK: 15
        }
        gain = gain_map[quality]

    if current_mastery >= 80:
        gain //= 2
    elif current_mastery >= 60:
        gain = int(gain * 0.75)

    return min(100, current_mastery + gain)


def get_mastery_bonuses(mastery: int) -> Dict[str, float]:
    level = mastery // 20

    bonuses_map = {
        0: {
            "success_bonus": 0.0,
            "quality_bonus": 0.0,
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        1: {
            "success_bonus": 0.10,
            "quality_bonus": 0.0,
            "waste_reduction": 0.10,
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        2: {
            "success_bonus": 0.20,
            "quality_bonus": 0.10,
            "waste_reduction": 0.10,
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        3: {
            "success_bonus": 0.30,
            "quality_bonus": 0.20,
            "waste_reduction": 0.10,
            "can_teach": True,
            "can_innovate": False,
            "batch_craft": True
        },
        4: {
            "success_bonus": 0.40,
            "quality_bonus": 0.30,
            "waste_reduction": 0.10,
            "can_teach": True,
            "can_innovate": True,
            "batch_craft": True
        }
    }

    return bonuses_map.get(min(4, level), bonuses_map[0])


def calculate_reputation_level(reputation: int) -> str:
    if reputation >= 81:
        return "Legendary"
    elif reputation >= 61:
        return "Renowned"
    elif reputation >= 41:
        return "Respected"
    elif reputation >= 21:
        return "Known"
    else:
        return "Unknown"


def get_reputation_modifiers(reputation: int) -> Dict[str, float]:
    level = calculate_reputation_level(reputation)

    modifiers_map = {
        "Unknown": {
            "price_modifier": 0.90,
            "quest_access": 1,
            "npc_initial_affinity": -0.5
        },
        "Known": {
            "price_modifier": 1.0,
            "quest_access": 2,
            "npc_initial_affinity": 0.0
        },
        "Respected": {
            "price_modifier": 1.05,
            "quest_access": 3,
            "npc_initial_affinity": 0.5
        },
        "Renowned": {
            "price_modifier": 1.10,
            "quest_access": 4,
            "npc_initial_affinity": 1.0
        },
        "Legendary": {
            "price_modifier": 1.20,
            "quest_access": 5,
            "npc_initial_affinity": 1.5
        }
    }

    return modifiers_map[level]


SPECIALIZATIONS = [
    Specialization(
        id="perfectionist",
        name="Perfectionist",
        category="crafting",
        bonuses={"precision": 20, "quality_bonus": 0.10},
        prerequisites={"precision": 60}
    ),
    Specialization(
        id="innovator",
        name="Innovator",
        category="crafting",
        bonuses={"intuition": 15, "can_substitute": True},
        prerequisites={"intuition": 60}
    ),
    Specialization(
        id="speed_brewer",
        name="Speed Brewer",
        category="crafting",
        bonuses={"craft_time": -0.25, "precision": -5},
        prerequisites={"knowledge": 50}
    ),
    Specialization(
        id="diplomat",
        name="Diplomat",
        category="social",
        bonuses={"affinity_gain": 15},
        prerequisites={"reputation": 40}
    ),
    Specialization(
        id="merchant",
        name="Merchant",
        category="social",
        bonuses={"profit_margin": 0.20},
        prerequisites={"business_acumen": 50}
    ),
    Specialization(
        id="analyst",
        name="Analyst",
        category="research",
        bonuses={"reverse_engineer_speed": 0.50},
        prerequisites={"knowledge": 70}
    ),
    Specialization(
        id="ethicist",
        name="Ethicist",
        category="research",
        bonuses={"moral_rep_bonus": 2},
        prerequisites={"reputation": 60}
    )
]


def can_choose_specialization(spec: Specialization, player_stats: Dict[str, int]) -> bool:
    for stat, required_value in spec.prerequisites.items():
        if player_stats.get(stat, 0) < required_value:
            return False
    return True


def apply_specialization_bonuses(
    player_stats: Dict[str, float],
    specs: List[Specialization]
) -> Dict[str, float]:
    modified = player_stats.copy()

    for spec in specs:
        for stat, bonus in spec.bonuses.items():
            if stat in modified:
                modified[stat] += bonus

    return modified


def get_specialization_by_id(spec_id: str) -> Specialization:
    for spec in SPECIALIZATIONS:
        if spec.id == spec_id:
            return spec
    return None
