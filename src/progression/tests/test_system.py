import unittest
from src.core.event_bus import EventBus
from src.core.data_structures import Quality
from src.core.events import (
    XPGained, StatIncreased, MilestoneReached,
    SpecializationChosen, ReputationChanged, RecipeMasteryGained
)
from src.progression.system import ProgressionSystem
from src.progression.formulas import stat_to_xp


class TestProgressionSystem(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.system = ProgressionSystem(self.bus)
        self.events = []

        def capture_event(event):
            self.events.append(event)

        self.bus.subscribe(XPGained, capture_event)
        self.bus.subscribe(StatIncreased, capture_event)
        self.bus.subscribe(MilestoneReached, capture_event)
        self.bus.subscribe(SpecializationChosen, capture_event)
        self.bus.subscribe(ReputationChanged, capture_event)
        self.bus.subscribe(RecipeMasteryGained, capture_event)

    def test_add_xp_emits_xp_gained(self):
        result = self.system.add_xp("player", "knowledge", 100, 0)

        xp_events = [e for e in self.events if isinstance(e, XPGained)]
        self.assertEqual(len(xp_events), 1)
        self.assertEqual(xp_events[0].stat, "knowledge")
        self.assertEqual(xp_events[0].amount, 100)

    def test_add_xp_emits_stat_increased(self):
        current_xp = 0
        result = self.system.add_xp("player", "knowledge", 1000, current_xp)

        stat_events = [e for e in self.events if isinstance(e, StatIncreased)]
        self.assertEqual(len(stat_events), 1)
        self.assertEqual(stat_events[0].stat, "knowledge")
        self.assertGreater(stat_events[0].new_value, stat_events[0].old_value)

    def test_add_xp_no_stat_increase(self):
        current_xp = 10000
        result = self.system.add_xp("player", "knowledge", 10, current_xp)

        stat_events = [e for e in self.events if isinstance(e, StatIncreased)]
        self.assertEqual(len(stat_events), 0)

    def test_add_xp_milestone_reached(self):
        xp_at_19 = stat_to_xp(19)
        xp_needed = stat_to_xp(20) - xp_at_19

        result = self.system.add_xp("player", "knowledge", xp_needed, xp_at_19)

        self.assertTrue(result.milestone_reached)

        milestone_events = [e for e in self.events if isinstance(e, MilestoneReached)]
        self.assertEqual(len(milestone_events), 1)
        self.assertEqual(milestone_events[0].milestone, 20)
        self.assertIsInstance(milestone_events[0].unlocks, list)

    def test_add_xp_returns_stat_change(self):
        result = self.system.add_xp("player", "precision", 500, 100)

        self.assertEqual(result.stat, "precision")
        self.assertEqual(result.xp_gained, 500)
        self.assertEqual(result.old_xp, 100)
        self.assertEqual(result.new_xp, 600)
        self.assertIsInstance(result.old_stat, int)
        self.assertIsInstance(result.new_stat, int)

    def test_choose_specialization_success(self):
        stats = {"precision": 70}

        result = self.system.choose_specialization("player", "perfectionist", stats)

        self.assertTrue(result)

        spec_events = [e for e in self.events if isinstance(e, SpecializationChosen)]
        self.assertEqual(len(spec_events), 1)
        self.assertEqual(spec_events[0].specialization.id, "perfectionist")

    def test_choose_specialization_insufficient_stats(self):
        stats = {"precision": 30}

        result = self.system.choose_specialization("player", "perfectionist", stats)

        self.assertFalse(result)

        spec_events = [e for e in self.events if isinstance(e, SpecializationChosen)]
        self.assertEqual(len(spec_events), 0)

    def test_choose_specialization_invalid_id(self):
        stats = {"precision": 100}

        result = self.system.choose_specialization("player", "invalid_spec", stats)

        self.assertFalse(result)

        spec_events = [e for e in self.events if isinstance(e, SpecializationChosen)]
        self.assertEqual(len(spec_events), 0)

    def test_update_reputation(self):
        result = self.system.update_reputation("player", "village", 10, 30, "quest_completed")

        self.assertEqual(result, 40)

        rep_events = [e for e in self.events if isinstance(e, ReputationChanged)]
        self.assertEqual(len(rep_events), 1)
        self.assertEqual(rep_events[0].old_value, 30)
        self.assertEqual(rep_events[0].new_value, 40)
        self.assertEqual(rep_events[0].reason, "quest_completed")

    def test_update_reputation_clamped(self):
        result_max = self.system.update_reputation("player", "city", 50, 90, "heroic_deed")
        self.assertEqual(result_max, 100)

        self.events.clear()

        result_min = self.system.update_reputation("player", "city", -50, 10, "betrayal")
        self.assertEqual(result_min, 0)

    def test_update_reputation_no_change(self):
        result = self.system.update_reputation("player", "town", 0, 50, "nothing")

        self.assertEqual(result, 50)

        rep_events = [e for e in self.events if isinstance(e, ReputationChanged)]
        self.assertEqual(len(rep_events), 0)

    def test_update_recipe_mastery(self):
        result = self.system.update_recipe_mastery(
            "player", "healing_potion", 10, True, Quality.STANDARD
        )

        self.assertEqual(result, 15)

        mastery_events = [e for e in self.events if isinstance(e, RecipeMasteryGained)]
        self.assertEqual(len(mastery_events), 1)
        self.assertEqual(mastery_events[0].recipe_id, "healing_potion")
        self.assertEqual(mastery_events[0].old_mastery, 10)
        self.assertEqual(mastery_events[0].new_mastery, 15)

    def test_update_recipe_mastery_no_change(self):
        result = self.system.update_recipe_mastery(
            "player", "fire_potion", 100, True, Quality.MASTERWORK
        )

        self.assertEqual(result, 100)

        mastery_events = [e for e in self.events if isinstance(e, RecipeMasteryGained)]
        self.assertEqual(len(mastery_events), 0)

    def test_milestone_unlocks_knowledge(self):
        xp_needed = stat_to_xp(20)
        result = self.system.add_xp("player", "knowledge", xp_needed, 0)

        milestone_events = [e for e in self.events if isinstance(e, MilestoneReached)]
        self.assertEqual(len(milestone_events), 1)
        self.assertIn("basic_recipes", milestone_events[0].unlocks)

    def test_milestone_unlocks_combat(self):
        xp_needed = stat_to_xp(40)
        result = self.system.add_xp("player", "combat_instinct", xp_needed, 0)

        milestone_events = [e for e in self.events if isinstance(e, MilestoneReached)]
        self.assertGreater(len(milestone_events), 0)

        final_milestone = milestone_events[-1]
        self.assertIsInstance(final_milestone.unlocks, list)


if __name__ == "__main__":
    unittest.main()
