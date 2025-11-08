from typing import Dict, List, Any, Optional
from src.quests.data_structures import (
    Quest, QuestState, Objective, ObjectiveType, MoralChoice
)


class QuestBuilder:
    def __init__(self, quest_id: str):
        self._id = quest_id
        self._name: Optional[str] = None
        self._description: Optional[str] = None
        self._objectives: List[Objective] = []
        self._state = QuestState.AVAILABLE
        self._prerequisites: Dict[str, Any] = {}
        self._moral_choices: List[str] = []

    def name(self, name: str) -> 'QuestBuilder':
        self._name = name
        return self

    def description(self, description: str) -> 'QuestBuilder':
        self._description = description
        return self

    def state(self, state: QuestState) -> 'QuestBuilder':
        self._state = state
        return self

    def craft_objective(
        self,
        target: str,
        quantity: int,
        description: Optional[str] = None
    ) -> 'QuestBuilder':
        obj_id = f"obj_{len(self._objectives)}"
        desc = description or f"Craft {quantity}x {target}"

        self._objectives.append(Objective(
            id=obj_id,
            type=ObjectiveType.CRAFT_POTION,
            target=target,
            quantity=quantity,
            description=desc
        ))
        return self

    def gather_objective(
        self,
        target: str,
        quantity: int,
        description: Optional[str] = None
    ) -> 'QuestBuilder':
        obj_id = f"obj_{len(self._objectives)}"
        desc = description or f"Gather {quantity}x {target}"

        self._objectives.append(Objective(
            id=obj_id,
            type=ObjectiveType.GATHER_ITEM,
            target=target,
            quantity=quantity,
            description=desc
        ))
        return self

    def talk_objective(
        self,
        target: str,
        description: Optional[str] = None
    ) -> 'QuestBuilder':
        obj_id = f"obj_{len(self._objectives)}"
        desc = description or f"Talk to {target}"

        self._objectives.append(Objective(
            id=obj_id,
            type=ObjectiveType.TALK_TO_NPC,
            target=target,
            description=desc
        ))
        return self

    def affinity_objective(
        self,
        target: str,
        value: float,
        description: Optional[str] = None
    ) -> 'QuestBuilder':
        obj_id = f"obj_{len(self._objectives)}"
        desc = description or f"Reach {value} affinity with {target}"

        self._objectives.append(Objective(
            id=obj_id,
            type=ObjectiveType.REACH_AFFINITY,
            target=target,
            value=value,
            description=desc
        ))
        return self

    def stat_objective(
        self,
        target: str,
        value: float,
        description: Optional[str] = None
    ) -> 'QuestBuilder':
        obj_id = f"obj_{len(self._objectives)}"
        desc = description or f"Reach {target} level {int(value)}"

        self._objectives.append(Objective(
            id=obj_id,
            type=ObjectiveType.REACH_STAT,
            target=target,
            value=value,
            description=desc
        ))
        return self

    def deliver_objective(
        self,
        target: str,
        description: Optional[str] = None
    ) -> 'QuestBuilder':
        obj_id = f"obj_{len(self._objectives)}"
        desc = description or f"Deliver item to {target}"

        self._objectives.append(Objective(
            id=obj_id,
            type=ObjectiveType.DELIVER_ITEM,
            target=target,
            description=desc
        ))
        return self

    def duel_objective(
        self,
        quantity: int,
        target: str = "any",
        description: Optional[str] = None
    ) -> 'QuestBuilder':
        obj_id = f"obj_{len(self._objectives)}"
        desc = description or f"Win {quantity} duel(s)"

        self._objectives.append(Objective(
            id=obj_id,
            type=ObjectiveType.WIN_DUEL,
            target=target,
            quantity=quantity,
            description=desc
        ))
        return self

    def gold_objective(
        self,
        value: int,
        description: Optional[str] = None
    ) -> 'QuestBuilder':
        obj_id = f"obj_{len(self._objectives)}"
        desc = description or f"Earn {value} gold"

        self._objectives.append(Objective(
            id=obj_id,
            type=ObjectiveType.EARN_GOLD,
            target="any",
            value=float(value),
            description=desc
        ))
        return self

    def require_quest(self, quest_id: str) -> 'QuestBuilder':
        if "required_quests" not in self._prerequisites:
            self._prerequisites["required_quests"] = []
        self._prerequisites["required_quests"].append(quest_id)
        return self

    def require_quests(self, quest_ids: List[str]) -> 'QuestBuilder':
        if "required_quests" not in self._prerequisites:
            self._prerequisites["required_quests"] = []
        self._prerequisites["required_quests"].extend(quest_ids)
        return self

    def require_stat(self, stat: str, min_value: int) -> 'QuestBuilder':
        if "required_stats" not in self._prerequisites:
            self._prerequisites["required_stats"] = {}
        self._prerequisites["required_stats"][stat] = min_value
        return self

    def require_affinity(self, npc: str, min_value: float) -> 'QuestBuilder':
        if "required_affinity" not in self._prerequisites:
            self._prerequisites["required_affinity"] = {}
        self._prerequisites["required_affinity"][npc] = min_value
        return self

    def require_item(self, item: str) -> 'QuestBuilder':
        if "required_items" not in self._prerequisites:
            self._prerequisites["required_items"] = []
        self._prerequisites["required_items"].append(item)
        return self

    def require_reputation(self, region: str, min_value: int) -> 'QuestBuilder':
        if "required_reputation" not in self._prerequisites:
            self._prerequisites["required_reputation"] = {}
        self._prerequisites["required_reputation"][region] = min_value
        return self

    def build(self) -> Quest:
        if self._name is None:
            raise ValueError(f"Quest {self._id} must have a name")

        if self._description is None:
            raise ValueError(f"Quest {self._id} must have a description")

        if len(self._objectives) == 0:
            raise ValueError(f"Quest {self._id} must have at least one objective")

        for stat, value in self._prerequisites.get("required_stats", {}).items():
            if value < 0 or value > 100:
                raise ValueError(f"Stat requirement for {stat} must be 0-100, got {value}")

        for npc, value in self._prerequisites.get("required_affinity", {}).items():
            if value < -5.0 or value > 5.0:
                raise ValueError(f"Affinity requirement for {npc} must be -5.0 to 5.0, got {value}")

        return Quest(
            id=self._id,
            name=self._name,
            description=self._description,
            objectives=self._objectives,
            state=self._state,
            prerequisites=self._prerequisites,
            moral_choices=self._moral_choices
        )
