import unittest
from src.core.event_bus import EventBus
from src.core.data_structures import NPC, Personality, Action
from src.core.events import (
    AffinityChanged,
    ThresholdCrossed,
    MemoryCreated,
    RelationshipDecayed,
)
from src.relationships.system import RelationshipSystem


class TestRelationshipSystem(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()
        self.system = RelationshipSystem(self.bus)
        self.events = []
        self.bus.subscribe_all(lambda e: self.events.append(e))

    def test_apply_action_emits_affinity_changed(self):
        npc = NPC("test", "Test NPC", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0))
        action = Action("innovate", "Innovate", {"O": 1.0})

        result = self.system.apply_action(npc, action, current_day=1)

        self.assertEqual(result.new_affinity, 1.0)
        self.assertEqual(result.delta, 1.0)
        self.assertTrue(any(isinstance(e, AffinityChanged) for e in self.events))

    def test_threshold_crossing_emits_event(self):
        npc = NPC("test", "Test NPC", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=0.5)
        action = Action("big_help", "Big Help", {"O": 1.0})

        result = self.system.apply_action(npc, action, current_day=1)

        self.assertTrue(result.threshold_crossed)
        self.assertEqual(result.new_threshold_level, 1)

        threshold_events = [e for e in self.events if isinstance(e, ThresholdCrossed)]
        self.assertEqual(len(threshold_events), 1)
        self.assertEqual(threshold_events[0].new_level, 1)
        self.assertEqual(threshold_events[0].direction, "positive")

    def test_memory_creation_on_significant_event(self):
        npc = NPC("test", "Test NPC", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0))
        action = Action("huge_favor", "Huge Favor", {"O": 2.0})

        result = self.system.apply_action(npc, action, current_day=1)

        self.assertIsNotNone(result.memory_created)
        self.assertEqual(len(npc.memories), 1)
        self.assertTrue(any(isinstance(e, MemoryCreated) for e in self.events))

    def test_no_memory_on_small_event(self):
        npc = NPC("test", "Test NPC", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0))
        action = Action("small", "Small", {"O": 0.5})

        result = self.system.apply_action(npc, action, current_day=1)

        self.assertIsNone(result.memory_created)
        self.assertEqual(len(npc.memories), 0)

    def test_affinity_clamping(self):
        npc = NPC("test", "Test NPC", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=4.5)
        action = Action("extreme", "Extreme", {"O": 2.0})

        result = self.system.apply_action(npc, action, current_day=1)

        self.assertEqual(result.new_affinity, 5.0)

    def test_negative_affinity(self):
        npc = NPC("test", "Test NPC", Personality(openness=-1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0))
        action = Action("innovate", "Innovate", {"O": 1.0})

        result = self.system.apply_action(npc, action, current_day=1)

        self.assertEqual(result.new_affinity, -1.0)
        self.assertEqual(result.delta, -1.0)

    def test_last_interaction_updated(self):
        npc = NPC("test", "Test NPC", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0))
        action = Action("test", "Test", {"O": 0.5})

        self.system.apply_action(npc, action, current_day=5)

        self.assertEqual(npc.last_interaction, 5)


class TestTimeDecay(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()
        self.system = RelationshipSystem(self.bus)
        self.events = []
        self.bus.subscribe_all(lambda e: self.events.append(e))

    def test_decay_emits_event(self):
        npc = NPC("test", "Test NPC", Personality(openness=0, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=3.0, last_interaction=0)

        result = self.system.apply_time_decay(npc, current_day=7)

        self.assertIsNotNone(result)
        self.assertLess(result.new_affinity, 3.0)
        self.assertTrue(any(isinstance(e, RelationshipDecayed) for e in self.events))

    def test_no_decay_if_no_time_passed(self):
        npc = NPC("test", "Test NPC", Personality(openness=0, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=3.0, last_interaction=5)

        result = self.system.apply_time_decay(npc, current_day=5)

        self.assertIsNone(result)

    def test_memories_resist_decay(self):
        npc_with_memories = NPC("test1", "Test 1", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=3.0, last_interaction=0)
        npc_without_memories = NPC("test2", "Test 2", Personality(openness=0, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=3.0, last_interaction=0)

        action = Action("huge", "Huge", {"O": 2.0})
        self.system.apply_action(npc_with_memories, action, current_day=0)

        self.events.clear()

        result_with = self.system.apply_time_decay(npc_with_memories, current_day=7)
        result_without = self.system.apply_time_decay(npc_without_memories, current_day=7)

        self.assertGreater(result_with.new_affinity, result_without.new_affinity)


class TestThresholdDirection(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()
        self.system = RelationshipSystem(self.bus)
        self.events = []
        self.bus.subscribe_all(lambda e: self.events.append(e))

    def test_positive_direction(self):
        npc = NPC("test", "Test", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=0.5)
        action = Action("good", "Good", {"O": 1.0})

        self.system.apply_action(npc, action, current_day=1)

        threshold_events = [e for e in self.events if isinstance(e, ThresholdCrossed)]
        self.assertEqual(threshold_events[0].direction, "positive")

    def test_negative_direction(self):
        npc = NPC("test", "Test", Personality(openness=-1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=-0.5)
        action = Action("innovate", "Innovate", {"O": 1.0})

        self.system.apply_action(npc, action, current_day=1)

        threshold_events = [e for e in self.events if isinstance(e, ThresholdCrossed)]
        self.assertEqual(threshold_events[0].direction, "negative")


if __name__ == '__main__':
    unittest.main()
