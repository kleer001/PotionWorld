from dataclasses import dataclass
from typing import Optional, List
from src.core.data_structures import Personality


@dataclass
class CombatStats:
    health: int
    max_health: int
    strength: int
    defense: int
    initiative: int
    resistance: int


@dataclass
class Trigger:
    trigger_type: str
    effect_esens: str


@dataclass
class StatusEffect:
    name: str
    source: str
    stat_affected: str
    modifier: float
    duration: int
    triggers: List[Trigger]
    removable: bool
    stackable: bool
    element: Optional[str] = None

    def __post_init__(self):
        if self.triggers is None:
            self.triggers = []


@dataclass
class Combatant:
    id: str
    name: str
    stats: CombatStats
    active_effects: List[StatusEffect]
    combat_belt: List
    personality: Optional[Personality] = None

    def __post_init__(self):
        if self.active_effects is None:
            self.active_effects = []
        if self.combat_belt is None:
            self.combat_belt = []


@dataclass
class CombatAction:
    action_type: str
    potion: Optional = None
    target_id: Optional[str] = None


@dataclass
class TurnResult:
    changes: List[str]
    actor_health: int
    target_health: int
    status_applied: List[StatusEffect]
    status_removed: List[str]
    victor: Optional[str]
