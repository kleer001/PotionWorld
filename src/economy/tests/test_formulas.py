import unittest
from src.core.data_structures import Quality, PriceModifiers
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
    calculate_profit_margin,
)


class TestIngredientPricing(unittest.TestCase):
    def test_common_ingredient_price(self):
        price = calculate_ingredient_base_price("common")
        self.assertEqual(price, 10)

    def test_rare_ingredient_price(self):
        price = calculate_ingredient_base_price("rare")
        self.assertEqual(price, 200)

    def test_legendary_ingredient_price(self):
        price = calculate_ingredient_base_price("legendary")
        self.assertEqual(price, 2000)

    def test_unknown_rarity_defaults_to_common(self):
        price = calculate_ingredient_base_price("unknown")
        self.assertEqual(price, 10)


class TestPotionPricing(unittest.TestCase):
    def test_simple_potion_price(self):
        price = calculate_potion_base_price(ingredient_cost=100, difficulty=30)
        self.assertEqual(price, 180)

    def test_difficult_potion_price(self):
        price = calculate_potion_base_price(ingredient_cost=100, difficulty=80)
        self.assertGreaterEqual(price, 225)
        self.assertLessEqual(price, 235)

    def test_masterwork_quality_modifier(self):
        price = apply_quality_modifier(100, Quality.MASTERWORK)
        self.assertEqual(price, 200)

    def test_poor_quality_modifier(self):
        price = apply_quality_modifier(100, Quality.POOR)
        self.assertEqual(price, 75)


class TestReputationAndAffinity(unittest.TestCase):
    def test_neutral_reputation_no_modifier(self):
        modifier = calculate_reputation_modifier(50)
        self.assertAlmostEqual(modifier, 0.0, places=2)

    def test_high_reputation_positive_modifier(self):
        modifier = calculate_reputation_modifier(100)
        self.assertAlmostEqual(modifier, 0.20, places=2)

    def test_low_reputation_negative_modifier(self):
        modifier = calculate_reputation_modifier(0)
        self.assertAlmostEqual(modifier, -0.20, places=2)

    def test_neutral_affinity_no_modifier(self):
        modifier = calculate_affinity_modifier(0.0)
        self.assertAlmostEqual(modifier, 0.0, places=2)

    def test_high_affinity_discount(self):
        modifier = calculate_affinity_modifier(5.0)
        self.assertAlmostEqual(modifier, -0.20, places=2)

    def test_low_affinity_penalty(self):
        modifier = calculate_affinity_modifier(-5.0)
        self.assertAlmostEqual(modifier, 0.20, places=2)


class TestMarketDynamics(unittest.TestCase):
    def test_high_demand_increases_price(self):
        multiplier = calculate_demand_multiplier(demand=2.0, supply=1.0)
        self.assertEqual(multiplier, 2.0)

    def test_low_demand_decreases_price(self):
        multiplier = calculate_demand_multiplier(demand=0.5, supply=1.0)
        self.assertEqual(multiplier, 0.5)

    def test_zero_supply_max_multiplier(self):
        multiplier = calculate_demand_multiplier(demand=1.0, supply=0.0)
        self.assertEqual(multiplier, 2.0)

    def test_demand_update_increases_with_transactions(self):
        new_demand = update_market_demand(
            current_demand=1.0,
            transactions_today=10
        )
        self.assertGreater(new_demand, 1.0)

    def test_supply_update_reflects_sales(self):
        new_supply = update_market_supply(
            current_supply=1.0,
            items_added=5,
            items_sold=10
        )
        self.assertLess(new_supply, 1.0)


class TestFinalPriceCalculation(unittest.TestCase):
    def test_base_price_with_no_modifiers(self):
        modifiers = PriceModifiers()
        final = calculate_final_price(100, modifiers)
        self.assertEqual(final, 100)

    def test_all_modifiers_applied(self):
        modifiers = PriceModifiers(
            base_multiplier=1.0,
            quality_multiplier=1.5,
            reputation_modifier=0.10,
            affinity_modifier=-0.10,
            demand_multiplier=1.2,
            rarity_multiplier=1.5
        )
        final = calculate_final_price(100, modifiers)
        self.assertGreater(final, 100)

    def test_minimum_price_is_one(self):
        modifiers = PriceModifiers(
            base_multiplier=0.01,
            quality_multiplier=0.01
        )
        final = calculate_final_price(1, modifiers)
        self.assertEqual(final, 1)


class TestBulkDiscounts(unittest.TestCase):
    def test_no_discount_for_single_item(self):
        price = calculate_bulk_discount(1, 100)
        self.assertEqual(price, 100)

    def test_small_discount_for_three_items(self):
        price = calculate_bulk_discount(3, 100)
        self.assertEqual(price, 95)

    def test_medium_discount_for_five_items(self):
        price = calculate_bulk_discount(5, 100)
        self.assertEqual(price, 90)

    def test_large_discount_for_ten_items(self):
        price = calculate_bulk_discount(10, 100)
        self.assertEqual(price, 85)


class TestCombatRewards(unittest.TestCase):
    def test_base_combat_reward(self):
        reward = calculate_combat_reward(
            turn_count=10,
            difficulty=50,
            victory_margin=0.5
        )
        self.assertGreater(reward, 100)

    def test_fast_victory_bonus(self):
        fast_reward = calculate_combat_reward(5, 50, 0.5)
        slow_reward = calculate_combat_reward(15, 50, 0.5)
        self.assertGreater(fast_reward, slow_reward)

    def test_difficulty_affects_reward(self):
        hard_reward = calculate_combat_reward(10, 80, 0.5)
        easy_reward = calculate_combat_reward(10, 20, 0.5)
        self.assertGreater(hard_reward, easy_reward)


class TestProfitMargin(unittest.TestCase):
    def test_profit_margin_calculation(self):
        margin = calculate_profit_margin(150, 100)
        self.assertAlmostEqual(margin, 0.5, places=2)

    def test_loss_margin(self):
        margin = calculate_profit_margin(80, 100)
        self.assertAlmostEqual(margin, -0.2, places=2)

    def test_zero_cost_basis(self):
        margin = calculate_profit_margin(100, 0)
        self.assertEqual(margin, 1.0)


if __name__ == "__main__":
    unittest.main()
