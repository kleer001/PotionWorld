import time
import uuid
from typing import Dict, Optional

from src.core.event_bus import EventBus
from src.core.data_structures import Quality
from src.crafting.data_structures import Potion
from src.economy.data_structures import (
    Wallet,
    Transaction,
    PriceModifiers,
    MarketCondition,
)
from src.core.events import (
    TransactionCompleted,
    GoldChanged,
    PriceCalculated,
    MarketShifted,
    ReputationEarned,
)
from src.economy.formulas import (
    calculate_ingredient_base_price,
    calculate_potion_base_price,
    apply_quality_modifier,
    calculate_reputation_modifier,
    calculate_affinity_modifier,
    calculate_demand_multiplier,
    calculate_final_price,
    calculate_bulk_discount,
    calculate_combat_reward,
    update_market_demand,
    update_market_supply,
)


class EconomySystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.wallets: Dict[str, Wallet] = {}
        self.market_conditions: Dict[str, MarketCondition] = {}

    def get_wallet(self, owner_id: str) -> Wallet:
        if owner_id not in self.wallets:
            self.wallets[owner_id] = Wallet(owner_id=owner_id, gold=0)
        return self.wallets[owner_id]

    def add_gold(self, owner_id: str, amount: int, reason: str) -> int:
        wallet = self.get_wallet(owner_id)
        wallet.gold += amount

        self.event_bus.emit(GoldChanged(
            owner_id=owner_id,
            delta=amount,
            new_balance=wallet.gold,
            reason=reason
        ))

        return wallet.gold

    def deduct_gold(self, owner_id: str, amount: int, reason: str) -> bool:
        wallet = self.get_wallet(owner_id)

        if wallet.gold < amount:
            return False

        wallet.gold -= amount

        self.event_bus.emit(GoldChanged(
            owner_id=owner_id,
            delta=-amount,
            new_balance=wallet.gold,
            reason=reason
        ))

        return True

    def calculate_potion_price(
        self,
        potion: Potion,
        ingredient_cost: int,
        difficulty: int,
        buyer_reputation: int = 50,
        seller_affinity: float = 0.0,
        demand: float = 1.0,
        supply: float = 1.0
    ) -> tuple[int, PriceModifiers]:
        base_price = calculate_potion_base_price(ingredient_cost, difficulty)

        quality_multiplier = apply_quality_modifier(100, potion.quality) / 100.0

        modifiers = PriceModifiers(
            base_multiplier=1.0,
            quality_multiplier=quality_multiplier,
            reputation_modifier=calculate_reputation_modifier(buyer_reputation),
            affinity_modifier=calculate_affinity_modifier(seller_affinity),
            demand_multiplier=calculate_demand_multiplier(demand, supply),
            rarity_multiplier=1.0
        )

        final_price = calculate_final_price(base_price, modifiers)

        return final_price, modifiers

    def calculate_ingredient_price(
        self,
        ingredient_id: str,
        rarity: str,
        quantity: int = 1,
        buyer_reputation: int = 50,
        seller_affinity: float = 0.0,
        demand: float = 1.0,
        supply: float = 1.0
    ) -> tuple[int, PriceModifiers]:
        base_price = calculate_ingredient_base_price(rarity)

        rarity_multipliers = {
            "common": 1.0,
            "uncommon": 1.5,
            "rare": 2.0,
            "very_rare": 2.5,
            "legendary": 3.0
        }

        modifiers = PriceModifiers(
            base_multiplier=1.0,
            quality_multiplier=1.0,
            reputation_modifier=calculate_reputation_modifier(buyer_reputation),
            affinity_modifier=calculate_affinity_modifier(seller_affinity),
            demand_multiplier=calculate_demand_multiplier(demand, supply),
            rarity_multiplier=rarity_multipliers.get(rarity.lower(), 1.0)
        )

        unit_price = calculate_final_price(base_price, modifiers)

        if quantity > 1:
            unit_price = calculate_bulk_discount(quantity, unit_price)

        total_price = unit_price * quantity

        self.event_bus.emit(PriceCalculated(
            item_id=ingredient_id,
            base_price=base_price,
            final_price=total_price,
            buyer_id="",
            seller_id="",
            modifiers=modifiers
        ))

        return total_price, modifiers

    def execute_transaction(
        self,
        buyer_id: str,
        seller_id: str,
        item_id: str,
        item_type: str,
        quantity: int,
        unit_price: int,
        modifiers: PriceModifiers
    ) -> Optional[Transaction]:
        total_price = unit_price * quantity

        if not self.deduct_gold(buyer_id, total_price, f"Purchase {item_type}"):
            return None

        self.add_gold(seller_id, total_price, f"Sold {item_type}")

        transaction = Transaction(
            id=self._generate_transaction_id(),
            buyer_id=buyer_id,
            seller_id=seller_id,
            item_id=item_id,
            item_type=item_type,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            timestamp=time.time(),
            modifiers=modifiers
        )

        buyer_wallet = self.get_wallet(buyer_id)
        seller_wallet = self.get_wallet(seller_id)
        buyer_wallet.transaction_history.append(transaction.id)
        seller_wallet.transaction_history.append(transaction.id)

        self.event_bus.emit(TransactionCompleted(
            transaction_id=transaction.id,
            buyer_id=buyer_id,
            seller_id=seller_id,
            item_type=item_type,
            quantity=quantity,
            total_price=total_price,
            timestamp=transaction.timestamp
        ))

        return transaction

    def award_combat_reward(
        self,
        winner_id: str,
        turn_count: int,
        difficulty: int,
        victory_margin: float
    ) -> int:
        reward = calculate_combat_reward(turn_count, difficulty, victory_margin)
        self.add_gold(winner_id, reward, "Combat victory")
        return reward

    def update_market(
        self,
        item_id: str,
        transactions_today: int = 0,
        items_added: int = 0,
        items_sold: int = 0,
        reason: str = "market_update"
    ) -> MarketCondition:
        if item_id not in self.market_conditions:
            self.market_conditions[item_id] = MarketCondition(
                item_id=item_id,
                demand_level=1.0,
                supply_level=1.0,
                base_price=100,
                current_multiplier=1.0
            )

        condition = self.market_conditions[item_id]
        old_demand = condition.demand_level
        old_supply = condition.supply_level

        condition.demand_level = update_market_demand(
            condition.demand_level,
            transactions_today
        )

        condition.supply_level = update_market_supply(
            condition.supply_level,
            items_added,
            items_sold
        )

        condition.current_multiplier = calculate_demand_multiplier(
            condition.demand_level,
            condition.supply_level
        )

        self.event_bus.emit(MarketShifted(
            item_id=item_id,
            old_demand=old_demand,
            new_demand=condition.demand_level,
            old_supply=old_supply,
            new_supply=condition.supply_level,
            reason=reason
        ))

        return condition

    def get_market_condition(self, item_id: str) -> MarketCondition:
        if item_id not in self.market_conditions:
            return MarketCondition(
                item_id=item_id,
                demand_level=1.0,
                supply_level=1.0,
                base_price=100,
                current_multiplier=1.0
            )
        return self.market_conditions[item_id]

    def _generate_transaction_id(self) -> str:
        return f"txn_{uuid.uuid4().hex[:8]}"
