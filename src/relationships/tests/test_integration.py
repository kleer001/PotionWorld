import unittest
from src.core.event_bus import EventBus
from src.core.data_structures import Personality
from src.relationships.data_structures import NPC, Action
from src.core.events import ThresholdCrossed
from src.relationships.system import RelationshipSystem


class TestCrossSystemIntegration(unittest.TestCase):

    def test_economy_price_adjustment_by_affinity(self):
        bus = EventBus()
        relationships = RelationshipSystem(bus)

        merchant = NPC("merchant", "Merchant",
                      Personality(openness=0, conscientiousness=0, extraversion=1, agreeableness=1, neuroticism=0))

        base_price = 100

        price_neutral = base_price * (1.0 - merchant.affinity / 20.0)
        self.assertEqual(price_neutral, 100)

        gift = Action("gift", "Gift", {"E": 1.0, "A": 1.0})
        result = relationships.apply_action(merchant, gift, current_day=1)

        price_friendly = base_price * (1.0 - merchant.affinity / 20.0)
        self.assertLess(price_friendly, price_neutral)
        self.assertAlmostEqual(price_friendly, 90.0, places=1)

    def test_quest_unlock_on_threshold(self):
        bus = EventBus()
        relationships = RelationshipSystem(bus)

        unlocked_quests = []

        def on_threshold(event):
            if event.new_level >= 3:
                unlocked_quests.append(f"friendship_{event.npc_id}")

        bus.subscribe(ThresholdCrossed, on_threshold)

        npc = NPC("quest_giver", "Quest Giver",
                 Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=1, neuroticism=0))

        help_action = Action("help", "Help", {"O": 1.5, "A": 1.5})

        relationships.apply_action(npc, help_action, current_day=1)
        self.assertEqual(len(unlocked_quests), 0)

        relationships.apply_action(npc, help_action, current_day=2)
        self.assertEqual(len(unlocked_quests), 1)
        self.assertEqual(unlocked_quests[0], "friendship_quest_giver")

    def test_dialogue_options_by_affinity_level(self):
        bus = EventBus()
        relationships = RelationshipSystem(bus)

        npc = NPC("npc", "NPC",
                 Personality(openness=0, conscientiousness=0, extraversion=0, agreeableness=1, neuroticism=0))

        def get_dialogue_options(affinity):
            options = ["Talk"]
            if affinity >= 1:
                options.append("Ask about family")
            if affinity >= 2:
                options.append("Share secret")
            if affinity >= 3:
                options.append("Request favor")
            if affinity >= 4:
                options.append("Deep conversation")
            return options

        self.assertEqual(get_dialogue_options(npc.affinity), ["Talk"])

        help_action = Action("help", "Help", {"A": 1.5})
        relationships.apply_action(npc, help_action, current_day=1)

        self.assertIn("Ask about family", get_dialogue_options(npc.affinity))

    def test_reputation_affects_all_faction_npcs(self):
        bus = EventBus()
        relationships = RelationshipSystem(bus)

        guild_members = [
            NPC(f"member_{i}", f"Guild Member {i}",
                Personality(openness=0, conscientiousness=1, extraversion=0, agreeableness=0, neuroticism=0))
            for i in range(5)
        ]

        faction_reputation = 0.0

        help_guild = Action("help_guild", "Help Guild", {"C": 1.0})

        for member in guild_members:
            result = relationships.apply_action(member, help_guild, current_day=1)
            faction_reputation += result.delta / len(guild_members)

        self.assertGreater(faction_reputation, 0)
        self.assertAlmostEqual(faction_reputation, 1.0, places=1)


class TestMultipleNPCInteractions(unittest.TestCase):

    def test_same_action_different_npcs(self):
        bus = EventBus()
        relationships = RelationshipSystem(bus)

        action = Action("innovate", "Show innovation", {"O": 1.5})

        traditional = NPC("t", "Traditional",
                         Personality(openness=-1, conscientiousness=1, extraversion=0, agreeableness=0, neuroticism=0))
        innovative = NPC("i", "Innovative",
                        Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0))

        result_t = relationships.apply_action(traditional, action, current_day=1)
        result_i = relationships.apply_action(innovative, action, current_day=1)

        self.assertLess(result_t.delta, 0)
        self.assertGreater(result_i.delta, 0)
        self.assertEqual(abs(result_t.delta), abs(result_i.delta))

    def test_relationship_independence(self):
        bus = EventBus()
        relationships = RelationshipSystem(bus)

        npc1 = NPC("1", "NPC1", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0))
        npc2 = NPC("2", "NPC2", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0))

        action = Action("help", "Help", {"O": 1.0})

        relationships.apply_action(npc1, action, current_day=1)

        self.assertEqual(npc1.affinity, 1.0)
        self.assertEqual(npc2.affinity, 0.0)


class TestLongTermRelationshipArcs(unittest.TestCase):

    def test_full_relationship_lifecycle(self):
        bus = EventBus()
        relationships = RelationshipSystem(bus)

        npc = NPC("npc", "NPC",
                 Personality(openness=1, conscientiousness=0, extraversion=1, agreeableness=1, neuroticism=0))

        positive_action = Action("help", "Help", {"O": 1.0, "E": 0.5, "A": 0.5})

        for day in range(3):
            relationships.apply_action(npc, positive_action, current_day=day)

        peak_affinity = npc.affinity
        self.assertGreater(peak_affinity, 4.0)
        memory_count = len(npc.memories)

        relationships.apply_time_decay(npc, current_day=30)

        self.assertLessEqual(npc.affinity, peak_affinity)
        self.assertEqual(len(npc.memories), memory_count)

    def test_oscillating_relationship(self):
        bus = EventBus()
        relationships = RelationshipSystem(bus)

        npc = NPC("npc", "NPC",
                 Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=1, neuroticism=0))

        positive = Action("help", "Help", {"O": 1.0, "A": 0.5})
        negative = Action("insult", "Insult", {"O": -1.0, "A": -0.5})

        for day in range(10):
            if day % 2 == 0:
                relationships.apply_action(npc, positive, current_day=day)
            else:
                relationships.apply_action(npc, negative, current_day=day)

        self.assertAlmostEqual(npc.affinity, 0, delta=0.5)


if __name__ == '__main__':
    unittest.main()
