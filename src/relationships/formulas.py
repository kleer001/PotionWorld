from typing import List, Tuple
from src.core.data_structures import Personality, Action, Memory


def calculate_reaction(personality: Personality, action: Action) -> float:
    delta = 0.0

    trait_map = {
        'O': personality.openness,
        'C': personality.conscientiousness,
        'E': personality.extraversion,
        'A': personality.agreeableness,
        'N': personality.neuroticism,
        'openness': personality.openness,
        'conscientiousness': personality.conscientiousness,
        'extraversion': personality.extraversion,
        'agreeableness': personality.agreeableness,
        'neuroticism': personality.neuroticism,
    }

    for trait_name, impact in action.personality_impacts.items():
        if trait_name in trait_map:
            delta += trait_map[trait_name] * impact

    return max(-2.0, min(2.0, delta))


def calculate_decay(
    current_affinity: float,
    days_passed: int,
    decay_rate: float = 0.5
) -> float:
    if current_affinity == 0 or days_passed == 0:
        return current_affinity

    weeks_passed = days_passed / 7.0
    decay_amount = weeks_passed * decay_rate

    if current_affinity > 0:
        return max(0, current_affinity - decay_amount)
    else:
        return min(0, current_affinity + decay_amount)


def calculate_decay_with_memories(
    current_affinity: float,
    days_passed: int,
    memories: List[Memory],
    decay_rate: float = 0.5
) -> float:
    base_decay = calculate_decay(current_affinity, days_passed, decay_rate)

    if not memories:
        return base_decay

    memory_resistance = sum(m.decay_resistance for m in memories) / len(memories)
    actual_decay = current_affinity + (base_decay - current_affinity) * (1 - memory_resistance)

    return actual_decay


def should_create_memory(affinity_delta: float, threshold: float = 1.0) -> bool:
    return abs(affinity_delta) >= threshold


def check_threshold_crossed(old_affinity: float, new_affinity: float) -> Tuple[bool, int]:
    old_level = int(old_affinity)
    new_level = int(new_affinity)

    if old_level != new_level:
        return (True, new_level)

    return (False, old_level)
