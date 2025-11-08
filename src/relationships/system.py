from src.core.event_bus import EventBus
from src.core.data_structures import NPC, Action, Memory, AffinityChange
from src.core.events import (
    AffinityChanged,
    ThresholdCrossed,
    MemoryCreated,
    RelationshipDecayed,
)
from src.relationships.formulas import (
    calculate_reaction,
    calculate_decay_with_memories,
    should_create_memory,
    check_threshold_crossed,
)


class RelationshipSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def apply_action(
        self,
        npc: NPC,
        action: Action,
        current_day: int
    ) -> AffinityChange:
        delta = calculate_reaction(npc.personality, action)

        old_affinity = npc.affinity
        new_affinity = max(-5.0, min(5.0, old_affinity + delta))

        threshold_crossed, new_level = check_threshold_crossed(old_affinity, new_affinity)

        memory = None
        if should_create_memory(delta, action.creates_memory_threshold):
            memory = Memory(
                event=action.id,
                affinity_change=delta,
                day_created=current_day,
                decay_resistance=min(1.0, abs(delta) / 2.0)
            )
            npc.memories.append(memory)
            self.event_bus.emit(MemoryCreated(npc.id, memory))

        npc.affinity = new_affinity
        npc.last_interaction = current_day

        self.event_bus.emit(AffinityChanged(
            npc_id=npc.id,
            delta=delta,
            new_affinity=new_affinity,
            reason=action.id,
            timestamp=current_day
        ))

        if threshold_crossed:
            direction = "positive" if new_level > int(old_affinity) else "negative"
            self.event_bus.emit(ThresholdCrossed(
                npc_id=npc.id,
                old_level=int(old_affinity),
                new_level=new_level,
                direction=direction
            ))

        return AffinityChange(
            npc_id=npc.id,
            delta=delta,
            new_affinity=new_affinity,
            old_affinity=old_affinity,
            threshold_crossed=threshold_crossed,
            new_threshold_level=new_level,
            memory_created=memory,
            reason=action.id
        )

    def apply_time_decay(
        self,
        npc: NPC,
        current_day: int,
        decay_rate: float = 0.5
    ) -> AffinityChange:
        days_passed = current_day - npc.last_interaction

        if days_passed == 0:
            return None

        old_affinity = npc.affinity
        new_affinity = calculate_decay_with_memories(
            old_affinity,
            days_passed,
            npc.memories,
            decay_rate
        )

        npc.affinity = new_affinity

        delta = new_affinity - old_affinity

        self.event_bus.emit(RelationshipDecayed(
            npc_id=npc.id,
            old_affinity=old_affinity,
            new_affinity=new_affinity,
            days_passed=days_passed
        ))

        return AffinityChange(
            npc_id=npc.id,
            delta=delta,
            new_affinity=new_affinity,
            old_affinity=old_affinity,
            threshold_crossed=False,
            new_threshold_level=int(new_affinity),
            memory_created=None,
            reason="decay"
        )
