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
