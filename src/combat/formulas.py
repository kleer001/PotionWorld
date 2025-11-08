from typing import List, Optional, Tuple
from src.core.data_structures import Personality
from src.crafting.data_structures import Potion
from src.combat.data_structures import Combatant, StatusEffect, Trigger
import random


def calculate_damage(
    attacker_strength: int,
    defender_defense: int,
    base_damage: int,
    element: Optional[str] = None
) -> int:
    modified_damage = base_damage * (1 + attacker_strength / 100)
    damage_reduction = defender_defense / 100
    final_damage = modified_damage * (1 - damage_reduction)
    return max(1, int(final_damage))


def calculate_modified_stat(
    base_stat: int,
    effects: List[StatusEffect],
    stat_name: str
) -> int:
    modified = float(base_stat)

    for effect in effects:
        if effect.stat_affected == stat_name:
            if effect.modifier < 1.0:
                modified *= effect.modifier
            else:
                modified *= effect.modifier

    return int(modified)


def apply_status_effect(
    combatant: Combatant,
    effect: StatusEffect
) -> None:
    if effect.stackable:
        combatant.active_effects.append(effect)
    else:
        combatant.active_effects = [
            e for e in combatant.active_effects
            if e.name != effect.name
        ]
        combatant.active_effects.append(effect)


def remove_status_effect(
    combatant: Combatant,
    effect_name: str
) -> bool:
    initial_count = len(combatant.active_effects)
    combatant.active_effects = [
        e for e in combatant.active_effects
        if e.name != effect_name
    ]
    return len(combatant.active_effects) < initial_count


def trigger_matches_phase(trigger_type: str, phase: str) -> bool:
    mapping = {
        "^S": "start_turn",
        "vE": "end_turn",
        ">A": "on_attack",
        "<D": "on_defend",
        ">Sprd": "on_spread"
    }
    return mapping.get(trigger_type) == phase


def evaluate_triggers(
    phase: str,
    combatant: Combatant,
    context: dict
) -> List[Tuple[str, str]]:
    triggered_effects = []

    for effect in combatant.active_effects:
        for trigger in effect.triggers:
            if trigger_matches_phase(trigger.trigger_type, phase):
                triggered_effects.append((effect.name, trigger.effect_esens))

    return triggered_effects


def update_durations(combatant: Combatant) -> List[str]:
    removed_effects = []
    updated_effects = []

    for effect in combatant.active_effects:
        if effect.duration > 0:
            effect.duration -= 1
            if effect.duration == 0:
                removed_effects.append(effect.name)
            else:
                updated_effects.append(effect)
        elif effect.duration == -1:
            updated_effects.append(effect)

    combatant.active_effects = updated_effects
    return removed_effects


def evaluate_potion_value(
    potion: Potion,
    actor: Combatant,
    target: Combatant,
    personality: Personality
) -> float:
    score = 0.0

    esens = potion.esens_notation

    if "E" in esens and ("#" in esens or "-" in esens):
        score += 50
        if personality.extraversion > 0:
            score *= 1.5

    if "P" in esens and "+" in esens:
        score += 30
        if personality.agreeableness > 0:
            score *= 1.3

    if "+H" in esens or "P+H" in esens:
        health_deficit = actor.stats.max_health - actor.stats.health
        health_pct = health_deficit / actor.stats.max_health
        score += health_pct * 100

        if actor.stats.health < actor.stats.max_health * 0.3:
            if personality.neuroticism > 0:
                score *= 2.0

    if "#" in esens:
        if personality.openness > 0:
            score += 20

    return score


def choose_best_potion(
    available_potions: List[Potion],
    actor: Combatant,
    target: Combatant,
    personality: Personality
) -> Potion:
    if not available_potions:
        return None

    scores = [
        (potion, evaluate_potion_value(potion, actor, target, personality))
        for potion in available_potions
    ]

    if personality.conscientiousness > 0:
        return max(scores, key=lambda x: x[1])[0]
    else:
        total_score = sum(s for _, s in scores)
        if total_score == 0:
            return random.choice(available_potions)

        weights = [max(1, s) for _, s in scores]
        return random.choices(
            [p for p, _ in scores],
            weights=weights
        )[0]


def parse_simple_esens_damage(esens: str) -> int:
    if "#Damage" in esens:
        parts = esens.split("#Damage")
        if len(parts) > 1:
            num_str = ""
            for char in parts[1]:
                if char.isdigit():
                    num_str += char
                else:
                    break
            if num_str:
                return int(num_str)

    if "-H" in esens:
        parts = esens.split("-H")
        if len(parts) > 1:
            num_str = ""
            for char in parts[1]:
                if char.isdigit():
                    num_str += char
                else:
                    break
            if num_str:
                return int(num_str)

    return 0


def parse_simple_esens_healing(esens: str) -> int:
    if "+H" in esens:
        parts = esens.split("+H")
        if len(parts) > 1:
            num_str = ""
            for char in parts[1]:
                if char.isdigit():
                    num_str += char
                else:
                    break
            if num_str:
                return int(num_str)

    return 0


def parse_simple_esens_buff(esens: str) -> Optional[Tuple[str, float, int]]:
    if "+S" in esens:
        stat = "strength"
        parts = esens.split("+S")
        if len(parts) > 1:
            num_str = ""
            has_percent = False
            for char in parts[1]:
                if char.isdigit():
                    num_str += char
                elif char == '%':
                    has_percent = True
                    break
                else:
                    break

            if has_percent and num_str:
                value = int(num_str)
                modifier = 1 + (value / 100)
            else:
                modifier = 1.3

            duration = 3
            if "T" in esens:
                t_idx = esens.index("T")
                dur_str = ""
                for i in range(t_idx - 1, -1, -1):
                    if esens[i].isdigit():
                        dur_str = esens[i] + dur_str
                    else:
                        break
                if dur_str:
                    duration = int(dur_str)

            return (stat, modifier, duration)

    if "+D" in esens:
        stat = "defense"
        parts = esens.split("+D")
        if len(parts) > 1:
            num_str = ""
            has_percent = False
            for char in parts[1]:
                if char.isdigit():
                    num_str += char
                elif char == '%':
                    has_percent = True
                    break
                else:
                    break

            if has_percent and num_str:
                value = int(num_str)
                modifier = 1 + (value / 100)
            else:
                modifier = 1.3

            duration = 3
            if "T" in esens:
                t_idx = esens.index("T")
                dur_str = ""
                for i in range(t_idx - 1, -1, -1):
                    if esens[i].isdigit():
                        dur_str = esens[i] + dur_str
                    else:
                        break
                if dur_str:
                    duration = int(dur_str)

            return (stat, modifier, duration)

    return None


def parse_simple_esens_debuff(esens: str) -> Optional[Tuple[str, float, int]]:
    if "-S" in esens:
        stat = "strength"
        parts = esens.split("-S")
        if len(parts) > 1:
            num_str = ""
            has_percent = False
            for char in parts[1]:
                if char.isdigit():
                    num_str += char
                elif char == '%':
                    has_percent = True
                    break
                else:
                    break

            if has_percent and num_str:
                value = int(num_str)
                modifier = 1 - (value / 100)
            else:
                modifier = 0.7

            duration = 3
            if "T" in esens:
                t_idx = esens.index("T")
                dur_str = ""
                for i in range(t_idx - 1, -1, -1):
                    if esens[i].isdigit():
                        dur_str = esens[i] + dur_str
                    else:
                        break
                if dur_str:
                    duration = int(dur_str)

            return (stat, modifier, duration)

    if "-D" in esens:
        stat = "defense"
        parts = esens.split("-D")
        if len(parts) > 1:
            num_str = ""
            has_percent = False
            for char in parts[1]:
                if char.isdigit():
                    num_str += char
                elif char == '%':
                    has_percent = True
                    break
                else:
                    break

            if has_percent and num_str:
                value = int(num_str)
                modifier = 1 - (value / 100)
            else:
                modifier = 0.7

            duration = 3
            if "T" in esens:
                t_idx = esens.index("T")
                dur_str = ""
                for i in range(t_idx - 1, -1, -1):
                    if esens[i].isdigit():
                        dur_str = esens[i] + dur_str
                    else:
                        break
                if dur_str:
                    duration = int(dur_str)

            return (stat, modifier, duration)

    return None
