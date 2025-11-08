import unittest
from src.core.data_structures import Quality
from src.progression.formulas import (
    xp_to_stat, stat_to_xp, xp_for_next_milestone,
    update_mastery, get_mastery_bonuses,
    calculate_reputation_level, get_reputation_modifiers,
    can_choose_specialization, apply_specialization_bonuses,
    get_specialization_by_id, SPECIALIZATIONS
)


class TestXPConversion(unittest.TestCase):
    def test_xp_to_stat_boundaries(self):
        self.assertEqual(xp_to_stat(0), 0)
        self.assertEqual(xp_to_stat(100000), 100)
        self.assertGreater(xp_to_stat(1000), 0)
        self.assertLess(xp_to_stat(1000), 100)

    def test_xp_to_stat_progression(self):
        self.assertEqual(xp_to_stat(1000), 20)
        self.assertAlmostEqual(xp_to_stat(5000), 40, delta=10)
        self.assertAlmostEqual(xp_to_stat(15000), 60, delta=10)
        self.assertAlmostEqual(xp_to_stat(40000), 80, delta=10)

    def test_stat_to_xp_boundaries(self):
        self.assertEqual(stat_to_xp(0), 0)
        self.assertEqual(stat_to_xp(100), 100000)

    def test_xp_stat_round_trip(self):
        for stat in [0, 20, 40, 60, 80, 100]:
            xp = stat_to_xp(stat)
            result = xp_to_stat(xp)
            self.assertAlmostEqual(result, stat, delta=2)

    def test_logarithmic_curve(self):
        xp_20 = stat_to_xp(20)
        xp_40 = stat_to_xp(40)
        xp_60 = stat_to_xp(60)
        xp_80 = stat_to_xp(80)

        self.assertLess(xp_40 - xp_20, xp_60 - xp_40)
        self.assertLess(xp_60 - xp_40, xp_80 - xp_60)

    def test_xp_for_next_milestone(self):
        xp_at_18 = stat_to_xp(18)
        needed = xp_for_next_milestone(xp_at_18)
        self.assertGreater(needed, 0)
        self.assertGreaterEqual(xp_to_stat(xp_at_18 + needed), 20)

    def test_xp_for_next_milestone_at_max(self):
        xp_at_100 = stat_to_xp(100)
        needed = xp_for_next_milestone(xp_at_100)
        self.assertEqual(needed, 0)


class TestMasterySystem(unittest.TestCase):
    def test_mastery_failure_gain(self):
        result = update_mastery(0, False, Quality.POOR)
        self.assertEqual(result, 1)

    def test_mastery_quality_gains(self):
        poor = update_mastery(0, True, Quality.POOR)
        standard = update_mastery(0, True, Quality.STANDARD)
        fine = update_mastery(0, True, Quality.FINE)
        exceptional = update_mastery(0, True, Quality.EXCEPTIONAL)
        masterwork = update_mastery(0, True, Quality.MASTERWORK)

        self.assertEqual(poor, 3)
        self.assertEqual(standard, 5)
        self.assertEqual(fine, 8)
        self.assertEqual(exceptional, 12)
        self.assertEqual(masterwork, 15)

    def test_mastery_diminishing_returns(self):
        low_gain = update_mastery(10, True, Quality.STANDARD) - 10
        mid_gain = update_mastery(65, True, Quality.STANDARD) - 65
        high_gain = update_mastery(85, True, Quality.STANDARD) - 85

        self.assertGreater(low_gain, mid_gain)
        self.assertGreater(mid_gain, high_gain)

    def test_mastery_cap(self):
        result = update_mastery(99, True, Quality.MASTERWORK)
        self.assertEqual(result, 100)

        result = update_mastery(100, True, Quality.MASTERWORK)
        self.assertEqual(result, 100)

    def test_mastery_bonuses_levels(self):
        novice = get_mastery_bonuses(0)
        competent = get_mastery_bonuses(25)
        proficient = get_mastery_bonuses(50)
        expert = get_mastery_bonuses(75)
        master = get_mastery_bonuses(95)

        self.assertEqual(novice["success_bonus"], 0.0)
        self.assertEqual(competent["success_bonus"], 0.10)
        self.assertEqual(proficient["success_bonus"], 0.20)
        self.assertEqual(expert["success_bonus"], 0.30)
        self.assertEqual(master["success_bonus"], 0.40)

    def test_mastery_bonuses_abilities(self):
        novice = get_mastery_bonuses(10)
        expert = get_mastery_bonuses(70)
        master = get_mastery_bonuses(90)

        self.assertFalse(novice["can_teach"])
        self.assertTrue(expert["can_teach"])
        self.assertTrue(master["can_innovate"])
        self.assertFalse(expert["can_innovate"])


class TestReputationSystem(unittest.TestCase):
    def test_reputation_levels(self):
        self.assertEqual(calculate_reputation_level(0), "Unknown")
        self.assertEqual(calculate_reputation_level(20), "Unknown")
        self.assertEqual(calculate_reputation_level(21), "Known")
        self.assertEqual(calculate_reputation_level(41), "Respected")
        self.assertEqual(calculate_reputation_level(61), "Renowned")
        self.assertEqual(calculate_reputation_level(81), "Legendary")
        self.assertEqual(calculate_reputation_level(100), "Legendary")

    def test_reputation_modifiers(self):
        unknown = get_reputation_modifiers(10)
        known = get_reputation_modifiers(30)
        legendary = get_reputation_modifiers(90)

        self.assertEqual(unknown["price_modifier"], 0.90)
        self.assertEqual(known["price_modifier"], 1.0)
        self.assertEqual(legendary["price_modifier"], 1.20)

        self.assertEqual(unknown["quest_access"], 1)
        self.assertEqual(legendary["quest_access"], 5)

    def test_reputation_affinity_bonuses(self):
        unknown = get_reputation_modifiers(10)
        legendary = get_reputation_modifiers(90)

        self.assertEqual(unknown["npc_initial_affinity"], -0.5)
        self.assertEqual(legendary["npc_initial_affinity"], 1.5)


class TestSpecializations(unittest.TestCase):
    def test_get_specialization_by_id(self):
        spec = get_specialization_by_id("perfectionist")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.name, "Perfectionist")

        spec = get_specialization_by_id("invalid")
        self.assertIsNone(spec)

    def test_can_choose_specialization_insufficient_stats(self):
        perfectionist = get_specialization_by_id("perfectionist")
        low_stats = {"precision": 30}

        result = can_choose_specialization(perfectionist, low_stats)
        self.assertFalse(result)

    def test_can_choose_specialization_sufficient_stats(self):
        perfectionist = get_specialization_by_id("perfectionist")
        high_stats = {"precision": 70}

        result = can_choose_specialization(perfectionist, high_stats)
        self.assertTrue(result)

    def test_can_choose_specialization_multiple_prerequisites(self):
        analyst = get_specialization_by_id("analyst")
        insufficient = {"knowledge": 50}
        sufficient = {"knowledge": 75}

        self.assertFalse(can_choose_specialization(analyst, insufficient))
        self.assertTrue(can_choose_specialization(analyst, sufficient))

    def test_apply_specialization_bonuses(self):
        perfectionist = get_specialization_by_id("perfectionist")
        base_stats = {"precision": 50.0, "quality_bonus": 0.0}

        modified = apply_specialization_bonuses(base_stats, [perfectionist])

        self.assertEqual(modified["precision"], 70.0)
        self.assertEqual(modified["quality_bonus"], 0.10)

    def test_apply_multiple_specializations(self):
        perfectionist = get_specialization_by_id("perfectionist")
        innovator = get_specialization_by_id("innovator")

        base_stats = {"precision": 50.0, "intuition": 50.0, "quality_bonus": 0.0}
        modified = apply_specialization_bonuses(base_stats, [perfectionist, innovator])

        self.assertEqual(modified["precision"], 70.0)
        self.assertEqual(modified["intuition"], 65.0)

    def test_all_specializations_exist(self):
        self.assertEqual(len(SPECIALIZATIONS), 7)

        categories = set(spec.category for spec in SPECIALIZATIONS)
        self.assertIn("crafting", categories)
        self.assertIn("social", categories)
        self.assertIn("research", categories)


if __name__ == "__main__":
    unittest.main()
