from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


class QuestState(Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class ObjectiveType(Enum):
    CRAFT_POTION = "craft_potion"
    GATHER_ITEM = "gather_item"
    TALK_TO_NPC = "talk_to_npc"
    REACH_AFFINITY = "reach_affinity"
    REACH_STAT = "reach_stat"
    DELIVER_ITEM = "deliver_item"
    WIN_DUEL = "win_duel"
    EARN_GOLD = "earn_gold"


@dataclass
class Objective:
    id: str
    type: ObjectiveType
    target: str
    quantity: int = 1
    value: Optional[float] = None
    description: str = ""


@dataclass
class Quest:
    id: str
    name: str
    description: str
    objectives: List[Objective]
    state: QuestState
    progress: Dict[str, int] = field(default_factory=dict)
    moral_choices: List[str] = field(default_factory=list)
    prerequisites: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MoralChoice:
    id: str
    quest_id: str
    description: str
    options: Dict[str, dict]


@dataclass
class QuestProgress:
    quest_id: str
    objectives_complete: int
    objectives_total: int
    can_complete: bool


@dataclass
class XPReward:
    stat: str
    amount: int


@dataclass
class QuestRewards:
    gold: int = 0
    xp_rewards: List[XPReward] = field(default_factory=list)
    reputation: int = 0
    items: List[str] = field(default_factory=list)
    unlocks: List[str] = field(default_factory=list)
