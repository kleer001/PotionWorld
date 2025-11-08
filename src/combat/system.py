from typing import Optional
from src.core.event_bus import EventBus
from src.core.data_structures import (
    Combatant, CombatAction, TurnResult, StatusEffect, Trigger, Potion
)
from src.core.events import (
    TurnExecuted, DamageDealt, StatusApplied,
    TriggerActivated, CombatEnded
)
from src.combat.formulas import (
    calculate_damage,
    calculate_modified_stat,
    apply_status_effect,
    update_durations,
    evaluate_triggers,
    choose_best_potion,
    parse_simple_esens_damage,
    parse_simple_esens_healing,
    parse_simple_esens_buff,
    parse_simple_esens_debuff
)


class CombatSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def execute_turn(
        self,
        combat_id: str,
        turn_number: int,
        actor: Combatant,
        action: CombatAction,
        target: Combatant
    ) -> TurnResult:
        changes = []
        status_applied = []
        status_removed = []

        removed_actor = update_durations(actor)
        status_removed.extend(removed_actor)
        for effect_name in removed_actor:
            changes.append(f"{actor.name}: {effect_name} wore off")

        removed_target = update_durations(target)
        status_removed.extend(removed_target)
        for effect_name in removed_target:
            changes.append(f"{target.name}: {effect_name} wore off")

        start_triggers = evaluate_triggers("start_turn", actor, {})
        for effect_name, trigger_esens in start_triggers:
            changes.append(f"{actor.name}: {effect_name} triggered at start of turn")
            self.event_bus.emit(TriggerActivated(
                combatant_id=actor.id,
                trigger_type="^S",
                effect_name=effect_name
            ))

        if action.action_type == "USE_POTION":
            result = self._apply_potion(action.potion, actor, target)
            changes.extend(result["changes"])
            status_applied.extend(result["status_applied"])

            for status in result["status_applied"]:
                self.event_bus.emit(StatusApplied(
                    target_id=result["target_id"],
                    effect_name=status.name,
                    source_id=actor.id,
                    duration=status.duration
                ))

            if result.get("damage", 0) > 0:
                self.event_bus.emit(DamageDealt(
                    source_id=actor.id,
                    target_id=target.id,
                    amount=result["damage"],
                    element=None
                ))

        elif action.action_type == "GUARD":
            guard_effect = StatusEffect(
                name="Guard",
                source=actor.id,
                stat_affected="defense",
                modifier=1.5,
                duration=1,
                triggers=[],
                removable=False,
                stackable=False
            )
            apply_status_effect(actor, guard_effect)
            status_applied.append(guard_effect)
            changes.append(f"{actor.name} guards (+50% defense this turn)")

        elif action.action_type == "OBSERVE":
            changes.append(f"{actor.name} observes the battlefield")

        end_triggers = evaluate_triggers("end_turn", actor, {})
        for effect_name, trigger_esens in end_triggers:
            changes.append(f"{actor.name}: {effect_name} triggered at end of turn")
            self.event_bus.emit(TriggerActivated(
                combatant_id=actor.id,
                trigger_type="vE",
                effect_name=effect_name
            ))

        victor = None
        if target.stats.health <= 0:
            victor = actor.id
            changes.append(f"{target.name} has been defeated!")
        elif actor.stats.health <= 0:
            victor = target.id
            changes.append(f"{actor.name} has been defeated!")

        result = TurnResult(
            changes=changes,
            actor_health=actor.stats.health,
            target_health=target.stats.health,
            status_applied=status_applied,
            status_removed=status_removed,
            victor=victor
        )

        self.event_bus.emit(TurnExecuted(
            combat_id=combat_id,
            turn_number=turn_number,
            actor_id=actor.id,
            action_type=action.action_type,
            result_changes=changes
        ))

        if victor:
            self.event_bus.emit(CombatEnded(
                combat_id=combat_id,
                winner_id=victor,
                turn_count=turn_number
            ))

        return result

    def create_ai_action(
        self,
        actor: Combatant,
        target: Combatant
    ) -> CombatAction:
        if not actor.combat_belt:
            return CombatAction(action_type="GUARD")

        if not actor.personality:
            potion = actor.combat_belt[0] if actor.combat_belt else None
            return CombatAction(
                action_type="USE_POTION" if potion else "GUARD",
                potion=potion
            )

        potion = choose_best_potion(
            actor.combat_belt,
            actor,
            target,
            actor.personality
        )

        return CombatAction(
            action_type="USE_POTION" if potion else "GUARD",
            potion=potion
        )

    def _apply_potion(
        self,
        potion: Potion,
        actor: Combatant,
        target: Combatant
    ) -> dict:
        changes = []
        status_applied = []
        damage = 0
        target_id = target.id

        esens = potion.esens_notation

        if esens.startswith("E"):
            damage_amount = parse_simple_esens_damage(esens)
            if damage_amount > 0:
                actual_damage = calculate_damage(
                    actor.stats.strength,
                    target.stats.defense,
                    damage_amount
                )
                target.stats.health = max(0, target.stats.health - actual_damage)
                damage = actual_damage
                changes.append(
                    f"{actor.name} dealt {actual_damage} damage to {target.name}"
                )

            debuff = parse_simple_esens_debuff(esens)
            if debuff:
                stat_name, modifier, duration = debuff
                effect = StatusEffect(
                    name=f"Weakened {stat_name.capitalize()}",
                    source=potion.id,
                    stat_affected=stat_name,
                    modifier=modifier,
                    duration=duration,
                    triggers=[],
                    removable=True,
                    stackable=False
                )
                apply_status_effect(target, effect)
                status_applied.append(effect)
                changes.append(
                    f"{target.name} suffers {effect.name} for {duration} turns"
                )

        elif esens.startswith("P"):
            healing = parse_simple_esens_healing(esens)
            if healing > 0:
                old_health = actor.stats.health
                actor.stats.health = min(
                    actor.stats.max_health,
                    actor.stats.health + healing
                )
                actual_healing = actor.stats.health - old_health
                changes.append(f"{actor.name} restored {actual_healing} health")
                target_id = actor.id

            buff = parse_simple_esens_buff(esens)
            if buff:
                stat_name, modifier, duration = buff
                effect = StatusEffect(
                    name=f"Enhanced {stat_name.capitalize()}",
                    source=potion.id,
                    stat_affected=stat_name,
                    modifier=modifier,
                    duration=duration,
                    triggers=[],
                    removable=True,
                    stackable=False
                )
                apply_status_effect(actor, effect)
                status_applied.append(effect)
                changes.append(
                    f"{actor.name} gains {effect.name} for {duration} turns"
                )
                target_id = actor.id

        return {
            "changes": changes,
            "status_applied": status_applied,
            "damage": damage,
            "target_id": target_id
        }
