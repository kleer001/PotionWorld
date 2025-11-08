from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Specialization:
    id: str
    name: str
    category: str
    bonuses: Dict[str, float]
    prerequisites: Dict[str, int]


@dataclass
class StatChange:
    stat: str
    xp_gained: int
    old_xp: int
    new_xp: int
    old_stat: int
    new_stat: int
    milestone_reached: bool


@dataclass
class PlayerStats:
    knowledge: int
    precision: int
    intuition: int
    business_acumen: int
    combat_instinct: int
    knowledge_xp: int
    precision_xp: int
    intuition_xp: int
    business_xp: int
    combat_xp: int


@dataclass
class MasteryRecord:
    recipe_id: str
    mastery: int
    crafts_attempted: int
    crafts_succeeded: int


@dataclass
class ReputationRecord:
    region: str
    reputation: int
    level_name: str
