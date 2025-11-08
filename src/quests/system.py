import time
from typing import Dict, List, Optional, Any
from src.core.event_bus import EventBus
from src.core.events import (
    QuestUnlocked, QuestStarted, ObjectiveUpdated, QuestCompleted,
    QuestFailed, MoralChoiceMade, WorldStateChanged,
    PotionCreated, ItemAdded, AffinityChanged, CombatEnded,
    TransactionCompleted, StatIncreased
)
from src.quests.data_structures import (
    Quest, QuestState, Objective, ObjectiveType, MoralChoice,
    QuestProgress, QuestRewards
)
from src.quests.formulas import (
    can_start_quest, calculate_next_state, check_objective_complete,
    calculate_quest_progress, are_all_objectives_complete,
    calculate_choice_consequences, apply_consequences_to_state
)


class QuestSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.active_quests: Dict[str, Dict[str, Quest]] = {}
        self.completed_quests: Dict[str, List[str]] = {}

        event_bus.subscribe(PotionCreated, self.on_potion_created)
        event_bus.subscribe(ItemAdded, self.on_item_added)
        event_bus.subscribe(AffinityChanged, self.on_affinity_changed)
        event_bus.subscribe(CombatEnded, self.on_combat_ended)
        event_bus.subscribe(TransactionCompleted, self.on_transaction_completed)
        event_bus.subscribe(StatIncreased, self.on_stat_increased)

    def unlock_quest(
        self,
        quest: Quest,
        player_id: str
    ) -> bool:
        if quest.state != QuestState.LOCKED:
            return False

        quest.state = calculate_next_state(quest.state, "unlock", False)

        self.event_bus.emit(QuestUnlocked(
            quest_id=quest.id,
            quest_name=quest.name,
            player_id=player_id
        ))

        return True

    def start_quest(
        self,
        quest: Quest,
        player_id: str,
        player_state: Dict[str, Any]
    ) -> tuple[bool, str]:
        can_start, reason = can_start_quest(
            quest.id,
            player_state,
            {quest.id: quest.prerequisites}
        )

        if not can_start:
            return (False, reason)

        if quest.state != QuestState.AVAILABLE:
            return (False, f"Quest is {quest.state.value}")

        quest.state = calculate_next_state(quest.state, "start", False)

        if player_id not in self.active_quests:
            self.active_quests[player_id] = {}

        self.active_quests[player_id][quest.id] = quest

        self.event_bus.emit(QuestStarted(
            quest_id=quest.id,
            quest_name=quest.name,
            player_id=player_id,
            timestamp=int(time.time())
        ))

        return (True, "Quest started")

    def update_objective(
        self,
        quest: Quest,
        objective_id: str,
        increment: int,
        player_id: str,
        player_state: Dict[str, Any]
    ):
        if quest.state != QuestState.ACTIVE:
            return

        old_progress = quest.progress.get(objective_id, 0)
        new_progress = old_progress + increment
        quest.progress[objective_id] = new_progress

        obj_index = int(objective_id.split("_")[1])
        objective = quest.objectives[obj_index]

        complete = check_objective_complete(
            {
                "type": objective.type.value,
                "target": objective.target,
                "quantity": objective.quantity,
                "value": objective.value
            },
            new_progress,
            player_state
        )

        self.event_bus.emit(ObjectiveUpdated(
            quest_id=quest.id,
            objective_id=objective_id,
            old_progress=old_progress,
            new_progress=new_progress,
            complete=complete,
            player_id=player_id
        ))

    def complete_quest(
        self,
        quest: Quest,
        player_id: str,
        player_state: Dict[str, Any]
    ) -> tuple[bool, str]:
        all_complete = are_all_objectives_complete(
            [
                {
                    "type": obj.type.value,
                    "target": obj.target,
                    "quantity": obj.quantity,
                    "value": obj.value
                }
                for obj in quest.objectives
            ],
            quest.progress,
            player_state
        )

        if not all_complete:
            return (False, "Not all objectives complete")

        if quest.state != QuestState.ACTIVE:
            return (False, f"Quest is {quest.state.value}")

        quest.state = calculate_next_state(quest.state, "complete", True)

        if player_id in self.active_quests:
            if quest.id in self.active_quests[player_id]:
                del self.active_quests[player_id][quest.id]

        if player_id not in self.completed_quests:
            self.completed_quests[player_id] = []

        self.completed_quests[player_id].append(quest.id)

        self.event_bus.emit(QuestCompleted(
            quest_id=quest.id,
            quest_name=quest.name,
            player_id=player_id,
            timestamp=int(time.time()),
            choices_made=quest.moral_choices
        ))

        return (True, "Quest completed")

    def fail_quest(
        self,
        quest: Quest,
        player_id: str,
        reason: str
    ) -> bool:
        if quest.state != QuestState.ACTIVE:
            return False

        quest.state = calculate_next_state(quest.state, "fail", False)

        if player_id in self.active_quests:
            if quest.id in self.active_quests[player_id]:
                del self.active_quests[player_id][quest.id]

        self.event_bus.emit(QuestFailed(
            quest_id=quest.id,
            quest_name=quest.name,
            reason=reason,
            player_id=player_id
        ))

        return True

    def abandon_quest(
        self,
        quest: Quest,
        player_id: str
    ) -> bool:
        return self.fail_quest(quest, player_id, "abandoned")

    def make_choice(
        self,
        choice: MoralChoice,
        selected_option: str,
        player_id: str,
        player_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        consequences = calculate_choice_consequences(
            choice.id,
            choice.options,
            selected_option
        )

        self.event_bus.emit(MoralChoiceMade(
            quest_id=choice.quest_id,
            choice_id=choice.id,
            selected_option=selected_option,
            consequences=consequences,
            player_id=player_id
        ))

        for flag, value in consequences.get("world_flags", {}).items():
            self.event_bus.emit(WorldStateChanged(
                flag=flag,
                old_value=player_state.get(f"flag_{flag}"),
                new_value=value,
                source_quest=choice.quest_id
            ))

        return consequences

    def get_quest_progress(
        self,
        quest: Quest,
        player_state: Dict[str, Any]
    ) -> QuestProgress:
        completed, total = calculate_quest_progress(
            [
                {
                    "type": obj.type.value,
                    "target": obj.target,
                    "quantity": obj.quantity,
                    "value": obj.value
                }
                for obj in quest.objectives
            ],
            quest.progress,
            player_state
        )

        can_complete = are_all_objectives_complete(
            [
                {
                    "type": obj.type.value,
                    "target": obj.target,
                    "quantity": obj.quantity,
                    "value": obj.value
                }
                for obj in quest.objectives
            ],
            quest.progress,
            player_state
        )

        return QuestProgress(
            quest_id=quest.id,
            objectives_complete=completed,
            objectives_total=total,
            can_complete=can_complete
        )

    def get_active_quests(self, player_id: str) -> List[Quest]:
        return list(self.active_quests.get(player_id, {}).values())

    def on_potion_created(self, event: PotionCreated):
        for quest in self.get_active_quests(event.crafter_id):
            for i, obj in enumerate(quest.objectives):
                if obj.type == ObjectiveType.CRAFT_POTION:
                    if obj.target == "any" or obj.target in event.potion.recipe_id:
                        self.update_objective(
                            quest,
                            f"obj_{i}",
                            1,
                            event.crafter_id,
                            {}
                        )

    def on_item_added(self, event: ItemAdded):
        for quest in self.get_active_quests(event.owner_id):
            for i, obj in enumerate(quest.objectives):
                if obj.type == ObjectiveType.GATHER_ITEM:
                    if obj.target == event.item_id:
                        self.update_objective(
                            quest,
                            f"obj_{i}",
                            event.quantity,
                            event.owner_id,
                            {}
                        )

    def on_affinity_changed(self, event: AffinityChanged):
        pass

    def on_combat_ended(self, event: CombatEnded):
        for quest in self.get_active_quests(event.winner_id):
            for i, obj in enumerate(quest.objectives):
                if obj.type == ObjectiveType.WIN_DUEL:
                    self.update_objective(
                        quest,
                        f"obj_{i}",
                        1,
                        event.winner_id,
                        {}
                    )

    def on_transaction_completed(self, event: TransactionCompleted):
        for quest in self.get_active_quests(event.seller_id):
            for i, obj in enumerate(quest.objectives):
                if obj.type == ObjectiveType.EARN_GOLD:
                    self.update_objective(
                        quest,
                        f"obj_{i}",
                        event.total_price,
                        event.seller_id,
                        {}
                    )

    def on_stat_increased(self, event: StatIncreased):
        pass
