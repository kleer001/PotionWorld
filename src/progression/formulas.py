import math
from typing import Dict, List
from src.core.data_structures import Quality
from src.progression.data_structures import Specialization
from src.progression.config import (
    get_xp_curve_params, get_mastery_gains, get_mastery_diminishing,
    get_mastery_bonus_config, get_reputation_thresholds, get_reputation_modifier_config,
    get_milestone_interval, load_specialization_from_config
)


def xp_to_stat(xp: int) -> int:
    params = get_xp_curve_params()

    if xp <= 0:
        return 0
    if xp >= params["max_xp"]:
        return params["max_stat"]

    stat = params["scale"] * math.log10(xp) - params["offset"]
    return int(min(params["max_stat"], max(0, stat)))


def stat_to_xp(stat: int) -> int:
    params = get_xp_curve_params()

    if stat <= 0:
        return 0
    if stat >= params["max_stat"]:
        return params["max_xp"]

    xp = math.pow(10, (stat + params["offset"]) / params["scale"])
    return int(xp)


def xp_for_next_milestone(current_xp: int) -> int:
    current_stat = xp_to_stat(current_xp)
    interval = get_milestone_interval()
    next_milestone = ((current_stat // interval) + 1) * interval

    params = get_xp_curve_params()
    if next_milestone > params["max_stat"]:
        return 0

    return stat_to_xp(next_milestone) - current_xp


def update_mastery(current_mastery: int, success: bool, quality: Quality) -> int:
    gains = get_mastery_gains()
    diminishing = get_mastery_diminishing()

    if not success:
        gain = gains["failure"]
    else:
        gain_map = {
            Quality.POOR: gains["poor"],
            Quality.STANDARD: gains["standard"],
            Quality.FINE: gains["fine"],
            Quality.EXCEPTIONAL: gains["exceptional"],
            Quality.MASTERWORK: gains["masterwork"]
        }
        gain = gain_map[quality]

    if current_mastery >= diminishing["threshold_high"]:
        gain = int(gain * diminishing["multiplier_high"])
    elif current_mastery >= diminishing["threshold_mid"]:
        gain = int(gain * diminishing["multiplier_mid"])

    return min(100, current_mastery + gain)


def get_mastery_bonuses(mastery: int) -> Dict[str, float]:
    interval = get_milestone_interval()
    level = mastery // interval

    bonuses = get_mastery_bonus_config()
    return bonuses.get(min(4, level), bonuses[0])


def calculate_reputation_level(reputation: int) -> str:
    thresholds = get_reputation_thresholds()

    if reputation >= thresholds["legendary"]:
        return "Legendary"
    elif reputation >= thresholds["renowned"]:
        return "Renowned"
    elif reputation >= thresholds["respected"]:
        return "Respected"
    elif reputation >= thresholds["known"]:
        return "Known"
    else:
        return "Unknown"


def get_reputation_modifiers(reputation: int) -> Dict[str, float]:
    level = calculate_reputation_level(reputation)
    modifiers = get_reputation_modifier_config()
    return modifiers[level]


SPECIALIZATIONS = [
    Specialization(**load_specialization_from_config("perfectionist", "Perfectionist")),
    Specialization(**load_specialization_from_config("innovator", "Innovator")),
    Specialization(**load_specialization_from_config("speed_brewer", "Speed Brewer")),
    Specialization(**load_specialization_from_config("diplomat", "Diplomat")),
    Specialization(**load_specialization_from_config("merchant", "Merchant")),
    Specialization(**load_specialization_from_config("analyst", "Analyst")),
    Specialization(**load_specialization_from_config("ethicist", "Ethicist"))
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
