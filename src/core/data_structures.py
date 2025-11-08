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
