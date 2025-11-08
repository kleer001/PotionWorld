from dataclasses import dataclass
from typing import List


@dataclass
class PriceModifiers:
    base_multiplier: float = 1.0
    quality_multiplier: float = 1.0
    reputation_modifier: float = 0.0
    affinity_modifier: float = 0.0
    demand_multiplier: float = 1.0
    rarity_multiplier: float = 1.0


@dataclass
class Transaction:
    id: str
    buyer_id: str
    seller_id: str
    item_id: str
    item_type: str
    quantity: int
    unit_price: int
    total_price: int
    timestamp: float
    modifiers: PriceModifiers


@dataclass
class Wallet:
    owner_id: str
    gold: int = 0
    transaction_history: List[str] = None

    def __post_init__(self):
        if self.transaction_history is None:
            self.transaction_history = []


@dataclass
class MarketCondition:
    item_id: str
    demand_level: float
    supply_level: float
    base_price: int
    current_multiplier: float


@dataclass
class ShopInventory:
    shop_id: str
    items: dict
    display_slots: int = 10
    storage_capacity: int = 50
