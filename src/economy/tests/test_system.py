import unittest
from src.core.event_bus import EventBus
from src.core.data_structures import Quality, Potion, PriceModifiers
from src.core.events import (
    TransactionCompleted,
    GoldChanged,
    MarketShifted,
)
from src.economy.system import EconomySystem


class TestWalletOperations(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.economy = EconomySystem(self.bus)

    def test_create_wallet_on_first_access(self):
        wallet = self.economy.get_wallet("player1")
        self.assertEqual(wallet.owner_id, "player1")
        self.assertEqual(wallet.gold, 0)

    def test_add_gold_increases_balance(self):
        new_balance = self.economy.add_gold("player1", 100, "test")
        self.assertEqual(new_balance, 100)

    def test_add_gold_emits_event(self):
        events = []
        self.bus.subscribe(GoldChanged, lambda e: events.append(e))

        self.economy.add_gold("player1", 100, "test")

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].delta, 100)
        self.assertEqual(events[0].new_balance, 100)

    def test_deduct_gold_succeeds_with_sufficient_funds(self):
        self.economy.add_gold("player1", 100, "setup")
        success = self.economy.deduct_gold("player1", 50, "test")
        self.assertTrue(success)

        wallet = self.economy.get_wallet("player1")
        self.assertEqual(wallet.gold, 50)

    def test_deduct_gold_fails_with_insufficient_funds(self):
        self.economy.add_gold("player1", 30, "setup")
        success = self.economy.deduct_gold("player1", 50, "test")
        self.assertFalse(success)

        wallet = self.economy.get_wallet("player1")
        self.assertEqual(wallet.gold, 30)


class TestPricingCalculations(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.economy = EconomySystem(self.bus)

    def test_potion_price_calculation(self):
        potion = Potion(
            id="potion_1",
            recipe_id="healing",
            esens_notation="P+H20",
            quality=Quality.STANDARD,
            potency=1.0,
            created_by="player1",
            created_at=0.0
        )

        price, modifiers = self.economy.calculate_potion_price(
            potion=potion,
            ingredient_cost=50,
            difficulty=30
        )

        self.assertGreater(price, 50)
        self.assertIsInstance(modifiers, PriceModifiers)

    def test_quality_affects_potion_price(self):
        standard_potion = Potion(
            id="p1", recipe_id="r1", esens_notation="",
            quality=Quality.STANDARD, potency=1.0,
            created_by="", created_at=0.0
        )

        masterwork_potion = Potion(
            id="p2", recipe_id="r1", esens_notation="",
            quality=Quality.MASTERWORK, potency=1.5,
            created_by="", created_at=0.0
        )

        standard_price, _ = self.economy.calculate_potion_price(
            standard_potion, 50, 30
        )
        masterwork_price, _ = self.economy.calculate_potion_price(
            masterwork_potion, 50, 30
        )

        self.assertGreater(masterwork_price, standard_price)

    def test_ingredient_price_with_bulk_discount(self):
        single_price, _ = self.economy.calculate_ingredient_price(
            "herb_1", "common", quantity=1
        )
        bulk_price, _ = self.economy.calculate_ingredient_price(
            "herb_1", "common", quantity=10
        )

        price_per_unit_bulk = bulk_price / 10
        self.assertLess(price_per_unit_bulk, single_price)

    def test_affinity_affects_pricing(self):
        potion = Potion(
            id="p1", recipe_id="r1", esens_notation="",
            quality=Quality.STANDARD, potency=1.0,
            created_by="", created_at=0.0
        )

        neutral_price, _ = self.economy.calculate_potion_price(
            potion, 50, 30, seller_affinity=0.0
        )
        friendly_price, _ = self.economy.calculate_potion_price(
            potion, 50, 30, seller_affinity=5.0
        )

        self.assertLess(friendly_price, neutral_price)


class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.economy = EconomySystem(self.bus)

    def test_successful_transaction(self):
        self.economy.add_gold("buyer", 200, "setup")
        self.economy.add_gold("seller", 0, "setup")

        modifiers = PriceModifiers()
        transaction = self.economy.execute_transaction(
            buyer_id="buyer",
            seller_id="seller",
            item_id="potion_1",
            item_type="potion",
            quantity=1,
            unit_price=100,
            modifiers=modifiers
        )

        self.assertIsNotNone(transaction)
        self.assertEqual(self.economy.get_wallet("buyer").gold, 100)
        self.assertEqual(self.economy.get_wallet("seller").gold, 100)

    def test_failed_transaction_insufficient_funds(self):
        self.economy.add_gold("buyer", 50, "setup")
        self.economy.add_gold("seller", 0, "setup")

        modifiers = PriceModifiers()
        transaction = self.economy.execute_transaction(
            buyer_id="buyer",
            seller_id="seller",
            item_id="potion_1",
            item_type="potion",
            quantity=1,
            unit_price=100,
            modifiers=modifiers
        )

        self.assertIsNone(transaction)
        self.assertEqual(self.economy.get_wallet("buyer").gold, 50)
        self.assertEqual(self.economy.get_wallet("seller").gold, 0)

    def test_transaction_emits_event(self):
        events = []
        self.bus.subscribe(TransactionCompleted, lambda e: events.append(e))

        self.economy.add_gold("buyer", 200, "setup")
        modifiers = PriceModifiers()
        self.economy.execute_transaction(
            "buyer", "seller", "item1", "potion", 1, 100, modifiers
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].total_price, 100)

    def test_transaction_history_tracked(self):
        self.economy.add_gold("buyer", 200, "setup")
        modifiers = PriceModifiers()

        transaction = self.economy.execute_transaction(
            "buyer", "seller", "item1", "potion", 1, 100, modifiers
        )

        buyer_wallet = self.economy.get_wallet("buyer")
        seller_wallet = self.economy.get_wallet("seller")

        self.assertIn(transaction.id, buyer_wallet.transaction_history)
        self.assertIn(transaction.id, seller_wallet.transaction_history)


class TestCombatRewards(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.economy = EconomySystem(self.bus)

    def test_combat_reward_increases_gold(self):
        initial_gold = self.economy.get_wallet("player1").gold
        reward = self.economy.award_combat_reward(
            winner_id="player1",
            turn_count=10,
            difficulty=50,
            victory_margin=0.5
        )

        final_gold = self.economy.get_wallet("player1").gold
        self.assertEqual(final_gold, initial_gold + reward)

    def test_combat_reward_emits_gold_changed(self):
        events = []
        self.bus.subscribe(GoldChanged, lambda e: events.append(e))

        self.economy.award_combat_reward("player1", 10, 50, 0.5)

        gold_events = [e for e in events if e.owner_id == "player1"]
        self.assertGreater(len(gold_events), 0)


class TestMarketDynamics(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.economy = EconomySystem(self.bus)

    def test_market_update_changes_demand(self):
        condition = self.economy.update_market(
            item_id="healing_potion",
            transactions_today=10
        )

        self.assertGreater(condition.demand_level, 1.0)

    def test_market_update_changes_supply(self):
        condition = self.economy.update_market(
            item_id="healing_potion",
            items_added=5,
            items_sold=10
        )

        self.assertLess(condition.supply_level, 1.0)

    def test_market_update_emits_event(self):
        events = []
        self.bus.subscribe(MarketShifted, lambda e: events.append(e))

        self.economy.update_market("healing_potion", transactions_today=5)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].item_id, "healing_potion")

    def test_get_market_condition_creates_default(self):
        condition = self.economy.get_market_condition("new_item")
        self.assertEqual(condition.item_id, "new_item")
        self.assertEqual(condition.demand_level, 1.0)
        self.assertEqual(condition.supply_level, 1.0)


if __name__ == "__main__":
    unittest.main()
