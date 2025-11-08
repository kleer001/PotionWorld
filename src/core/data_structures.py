from dataclasses import dataclass
from typing import Optional, List
from enum import IntEnum


class Quality(IntEnum):
    POOR = 1
    STANDARD = 2
    FINE = 3
    EXCEPTIONAL = 4
    MASTERWORK = 5


@dataclass
class Recipe:
    id: str
    name: str
    difficulty: int
    esens: str
    base_potency: float
    ingredients: List[str]


@dataclass
class IngredientInstance:
    id: str
    type: str
    quality: Quality
    freshness: float = 1.0


@dataclass
class CrafterStats:
    knowledge: int = 0
    precision: int = 0
    intuition: int = 0


@dataclass
class CraftInput:
    recipe: Recipe
    ingredients: List[IngredientInstance]
    crafter_stats: CrafterStats
    tool_bonus: float = 0.0
    prep_bonus: float = 0.0
    mastery_bonus: float = 0.0


@dataclass
class Potion:
    id: str
    recipe_id: str
    esens_notation: str
    quality: Quality
    potency: float
    created_by: str
    created_at: float


@dataclass
class FormulaBreakdown:
    base_chance: float
    knowledge_bonus: float
    tool_bonus: float
    mastery_bonus: float
    difficulty_penalty: float
    dice_roll: int
    final_chance: float
    success_threshold: float


@dataclass
class CraftResult:
    success: bool
    quality: Optional[Quality]
    potion: Optional[Potion]
    xp_rewards: dict
    mastery_gain: int
    formula_breakdown: FormulaBreakdown


@dataclass
class Personality:
    openness: int
    conscientiousness: int
    extraversion: int
    agreeableness: int
    neuroticism: int


@dataclass
class Memory:
    event: str
    affinity_change: float
    day_created: int
    decay_resistance: float


@dataclass
class Action:
    id: str
    name: str
    personality_impacts: dict
    creates_memory_threshold: float = 1.0


@dataclass
class NPC:
    id: str
    name: str
    personality: Personality
    affinity: float = 0.0
    memories: List[Memory] = None
    last_interaction: int = 0

    def __post_init__(self):
        if self.memories is None:
            self.memories = []


@dataclass
class AffinityChange:
    npc_id: str
    delta: float
    new_affinity: float
    old_affinity: float
    threshold_crossed: bool
    new_threshold_level: int
    memory_created: Optional[Memory]
    reason: str


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
    combat_belt: List[Potion]
    personality: Optional[Personality] = None

    def __post_init__(self):
        if self.active_effects is None:
            self.active_effects = []
        if self.combat_belt is None:
            self.combat_belt = []


@dataclass
class CombatAction:
    action_type: str
    potion: Optional[Potion] = None
    target_id: Optional[str] = None


@dataclass
class TurnResult:
    changes: List[str]
    actor_health: int
    target_health: int
    status_applied: List[StatusEffect]
    status_removed: List[str]
    victor: Optional[str]
