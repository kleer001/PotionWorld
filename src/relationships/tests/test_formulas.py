import unittest
from src.core.data_structures import Personality
from src.relationships.data_structures import Action, Memory
from src.relationships.formulas import (
    calculate_reaction,
    calculate_decay,
    calculate_decay_with_memories,
    should_create_memory,
    check_threshold_crossed,
)


class TestPersonalityReaction(unittest.TestCase):

    def test_high_openness_likes_innovation(self):
        action = Action("innovate", "Innovate", {"O": 1.0})
        high_o = Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0)
        low_o = Personality(openness=-1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0)

        self.assertEqual(calculate_reaction(high_o, action), 1.0)
        self.assertEqual(calculate_reaction(low_o, action), -1.0)

    def test_multiple_traits_combine(self):
        action = Action("social_gift", "Give social gift", {"E": 1.0, "A": 0.5})
        npc = Personality(openness=0, conscientiousness=0, extraversion=1, agreeableness=1, neuroticism=0)
        delta = calculate_reaction(npc, action)

        self.assertEqual(delta, 1.5)

    def test_negative_reactions(self):
        action = Action("haggle", "Haggle aggressively", {"A": -1.0})
        agreeable = Personality(openness=0, conscientiousness=0, extraversion=0, agreeableness=1, neuroticism=0)
        disagreeable = Personality(openness=0, conscientiousness=0, extraversion=0, agreeableness=-1, neuroticism=0)

        self.assertEqual(calculate_reaction(agreeable, action), -1.0)
        self.assertEqual(calculate_reaction(disagreeable, action), 1.0)

    def test_clamping_at_boundaries(self):
        action = Action("extreme", "Extreme action", {"O": 3.0})
        high_o = Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0)

        delta = calculate_reaction(high_o, action)
        self.assertEqual(delta, 2.0)

    def test_full_trait_name_support(self):
        action = Action("test", "Test", {"openness": 1.0, "extraversion": 0.5})
        npc = Personality(openness=1, conscientiousness=0, extraversion=1, agreeableness=0, neuroticism=0)

        delta = calculate_reaction(npc, action)
        self.assertEqual(delta, 1.5)


class TestAffinityDecay(unittest.TestCase):

    def test_positive_affinity_decays_toward_zero(self):
        positive = calculate_decay(current_affinity=3.0, days_passed=7)
        self.assertGreater(positive, 0)
        self.assertLess(positive, 3.0)

    def test_negative_affinity_decays_toward_zero(self):
        negative = calculate_decay(current_affinity=-3.0, days_passed=7)
        self.assertLess(negative, 0)
        self.assertGreater(negative, -3.0)

    def test_zero_affinity_stays_zero(self):
        zero = calculate_decay(current_affinity=0.0, days_passed=7)
        self.assertEqual(zero, 0.0)

    def test_no_time_passed_no_decay(self):
        no_decay = calculate_decay(current_affinity=3.0, days_passed=0)
        self.assertEqual(no_decay, 3.0)

    def test_decay_rate_affects_speed(self):
        slow = calculate_decay(current_affinity=3.0, days_passed=7, decay_rate=0.25)
        fast = calculate_decay(current_affinity=3.0, days_passed=7, decay_rate=1.0)

        self.assertGreater(slow, fast)

    def test_two_weeks_decay(self):
        result = calculate_decay(current_affinity=3.0, days_passed=14, decay_rate=0.5)
        expected = 3.0 - (14 / 7.0) * 0.5
        self.assertAlmostEqual(result, expected, places=5)


class TestDecayWithMemories(unittest.TestCase):

    def test_memories_resist_decay(self):
        memories = [Memory("helped", 2.0, 0, decay_resistance=0.5)]

        with_memories = calculate_decay_with_memories(3.0, 7, memories)
        without_memories = calculate_decay(3.0, 7)

        self.assertGreater(with_memories, without_memories)

    def test_no_memories_same_as_base_decay(self):
        with_empty = calculate_decay_with_memories(3.0, 7, [])
        without = calculate_decay(3.0, 7)

        self.assertEqual(with_empty, without)

    def test_multiple_memories_average_resistance(self):
        memories = [
            Memory("help1", 1.5, 0, decay_resistance=0.3),
            Memory("help2", 1.2, 5, decay_resistance=0.7),
        ]

        result = calculate_decay_with_memories(3.0, 7, memories)
        self.assertGreater(result, calculate_decay(3.0, 7))

    def test_full_resistance_no_decay(self):
        memories = [Memory("epic", 2.0, 0, decay_resistance=1.0)]

        result = calculate_decay_with_memories(3.0, 7, memories)
        self.assertEqual(result, 3.0)


class TestMemoryCreation(unittest.TestCase):

    def test_significant_event_creates_memory(self):
        self.assertTrue(should_create_memory(1.5, threshold=1.0))
        self.assertTrue(should_create_memory(-1.5, threshold=1.0))

    def test_insignificant_event_no_memory(self):
        self.assertFalse(should_create_memory(0.5, threshold=1.0))
        self.assertFalse(should_create_memory(-0.5, threshold=1.0))

    def test_exact_threshold(self):
        self.assertTrue(should_create_memory(1.0, threshold=1.0))

    def test_custom_threshold(self):
        self.assertTrue(should_create_memory(0.5, threshold=0.3))
        self.assertFalse(should_create_memory(0.2, threshold=0.3))


class TestThresholdDetection(unittest.TestCase):

    def test_crossing_positive_boundary(self):
        crossed, level = check_threshold_crossed(0.9, 1.1)
        self.assertTrue(crossed)
        self.assertEqual(level, 1)

    def test_crossing_negative_boundary(self):
        crossed, level = check_threshold_crossed(-0.9, -1.1)
        self.assertTrue(crossed)
        self.assertEqual(level, -1)

    def test_not_crossing_boundary(self):
        crossed, level = check_threshold_crossed(1.1, 1.3)
        self.assertFalse(crossed)
        self.assertEqual(level, 1)

    def test_crossing_from_zero(self):
        crossed_pos, level_pos = check_threshold_crossed(0.5, 1.1)
        self.assertTrue(crossed_pos)
        self.assertEqual(level_pos, 1)

        crossed_neg, level_neg = check_threshold_crossed(-0.5, -1.1)
        self.assertTrue(crossed_neg)
        self.assertEqual(level_neg, -1)

    def test_crossing_multiple_levels(self):
        crossed, level = check_threshold_crossed(1.5, 3.2)
        self.assertTrue(crossed)
        self.assertEqual(level, 3)


if __name__ == '__main__':
    unittest.main()
