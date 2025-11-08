from dataclasses import dataclass
from typing import Optional, List
from src.core.data_structures import Potion, Quality


@dataclass
class CraftCompleted:
    success: bool
    recipe_id: str
    quality: Optional[Quality]
    potion_id: Optional[str]
    crafter_id: str
    timestamp: int


@dataclass
class PotionCreated:
    potion: Potion
    quality: Quality
    potency: float
    crafter_id: str


@dataclass
class RecipeMasteryGained:
    recipe_id: str
    old_mastery: int
    new_mastery: int
    crafter_id: str


@dataclass
class XPGained:
    stat: str
    amount: int
    crafter_id: str


@dataclass
class IngredientsConsumed:
    ingredient_ids: List[str]
    recipe_id: str
    crafter_id: str


@dataclass
class AffinityChanged:
    npc_id: str
    delta: float
    new_affinity: float
    reason: str
    timestamp: int


@dataclass
class ThresholdCrossed:
    npc_id: str
    old_level: int
    new_level: int
    direction: str


@dataclass
class MemoryCreated:
    npc_id: str
    memory: 'Memory'


@dataclass
class RelationshipDecayed:
    npc_id: str
    old_affinity: float
    new_affinity: float
    days_passed: int


@dataclass
class TurnExecuted:
    combat_id: str
    turn_number: int
    actor_id: str
    action_type: str
    result_changes: List[str]


@dataclass
class DamageDealt:
    source_id: str
    target_id: str
    amount: int
    element: Optional[str]


@dataclass
class StatusApplied:
    target_id: str
    effect_name: str
    source_id: str
    duration: int


@dataclass
class TriggerActivated:
    combatant_id: str
    trigger_type: str
    effect_name: str


@dataclass
class CombatEnded:
    combat_id: str
    winner_id: str
    turn_count: int
