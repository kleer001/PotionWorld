import unittest
from src.quests.builder import QuestBuilder
from src.quests.data_structures import QuestState, ObjectiveType


class TestQuestBuilderBasics(unittest.TestCase):

    def test_minimal_quest(self):
        quest = (QuestBuilder("test_quest")
                 .name("Test Quest")
                 .description("A simple test")
                 .craft_objective("healing_potion", 5)
                 .build())

        self.assertEqual(quest.id, "test_quest")
        self.assertEqual(quest.name, "Test Quest")
        self.assertEqual(quest.description, "A simple test")
        self.assertEqual(len(quest.objectives), 1)
        self.assertEqual(quest.state, QuestState.AVAILABLE)

    def test_multiple_objectives(self):
        quest = (QuestBuilder("multi_quest")
                 .name("Multi Quest")
                 .description("Multiple objectives")
                 .craft_objective("healing_potion", 5)
                 .gather_objective("moonleaf", 20)
                 .talk_objective("elder")
                 .build())

        self.assertEqual(len(quest.objectives), 3)
        self.assertEqual(quest.objectives[0].id, "obj_0")
        self.assertEqual(quest.objectives[1].id, "obj_1")
        self.assertEqual(quest.objectives[2].id, "obj_2")

    def test_custom_state(self):
        quest = (QuestBuilder("locked_quest")
                 .name("Locked")
                 .description("Test")
                 .craft_objective("potion", 1)
                 .state(QuestState.LOCKED)
                 .build())

        self.assertEqual(quest.state, QuestState.LOCKED)


class TestQuestBuilderObjectives(unittest.TestCase):

    def test_craft_objective(self):
        quest = (QuestBuilder("craft_quest")
                 .name("Craft Quest")
                 .description("Craft things")
                 .craft_objective("healing_potion", 5)
                 .build())

        obj = quest.objectives[0]
        self.assertEqual(obj.type, ObjectiveType.CRAFT_POTION)
        self.assertEqual(obj.target, "healing_potion")
        self.assertEqual(obj.quantity, 5)
        self.assertEqual(obj.description, "Craft 5x healing_potion")

    def test_craft_objective_custom_description(self):
        quest = (QuestBuilder("craft_quest")
                 .name("Craft Quest")
                 .description("Craft things")
                 .craft_objective("healing_potion", 5, "Make some potions")
                 .build())

        self.assertEqual(quest.objectives[0].description, "Make some potions")

    def test_gather_objective(self):
        quest = (QuestBuilder("gather_quest")
                 .name("Gather Quest")
                 .description("Gather things")
                 .gather_objective("moonleaf", 20)
                 .build())

        obj = quest.objectives[0]
        self.assertEqual(obj.type, ObjectiveType.GATHER_ITEM)
        self.assertEqual(obj.target, "moonleaf")
        self.assertEqual(obj.quantity, 20)

    def test_talk_objective(self):
        quest = (QuestBuilder("talk_quest")
                 .name("Talk Quest")
                 .description("Talk to people")
                 .talk_objective("elder")
                 .build())

        obj = quest.objectives[0]
        self.assertEqual(obj.type, ObjectiveType.TALK_TO_NPC)
        self.assertEqual(obj.target, "elder")

    def test_affinity_objective(self):
        quest = (QuestBuilder("affinity_quest")
                 .name("Affinity Quest")
                 .description("Build relationships")
                 .affinity_objective("merchant", 2.0)
                 .build())

        obj = quest.objectives[0]
        self.assertEqual(obj.type, ObjectiveType.REACH_AFFINITY)
        self.assertEqual(obj.target, "merchant")
        self.assertEqual(obj.value, 2.0)

    def test_stat_objective(self):
        quest = (QuestBuilder("stat_quest")
                 .name("Stat Quest")
                 .description("Level up")
                 .stat_objective("knowledge", 80)
                 .build())

        obj = quest.objectives[0]
        self.assertEqual(obj.type, ObjectiveType.REACH_STAT)
        self.assertEqual(obj.target, "knowledge")
        self.assertEqual(obj.value, 80)

    def test_deliver_objective(self):
        quest = (QuestBuilder("deliver_quest")
                 .name("Deliver Quest")
                 .description("Deliver items")
                 .deliver_objective("elder")
                 .build())

        obj = quest.objectives[0]
        self.assertEqual(obj.type, ObjectiveType.DELIVER_ITEM)
        self.assertEqual(obj.target, "elder")

    def test_duel_objective(self):
        quest = (QuestBuilder("duel_quest")
                 .name("Duel Quest")
                 .description("Fight people")
                 .duel_objective(3)
                 .build())

        obj = quest.objectives[0]
        self.assertEqual(obj.type, ObjectiveType.WIN_DUEL)
        self.assertEqual(obj.quantity, 3)

    def test_gold_objective(self):
        quest = (QuestBuilder("gold_quest")
                 .name("Gold Quest")
                 .description("Get rich")
                 .gold_objective(1000)
                 .build())

        obj = quest.objectives[0]
        self.assertEqual(obj.type, ObjectiveType.EARN_GOLD)
        self.assertEqual(obj.value, 1000.0)


class TestQuestBuilderPrerequisites(unittest.TestCase):

    def test_require_quest(self):
        quest = (QuestBuilder("sequel")
                 .name("Sequel")
                 .description("Requires previous quest")
                 .craft_objective("potion", 1)
                 .require_quest("intro_quest")
                 .build())

        self.assertIn("required_quests", quest.prerequisites)
        self.assertEqual(quest.prerequisites["required_quests"], ["intro_quest"])

    def test_require_multiple_quests(self):
        quest = (QuestBuilder("finale")
                 .name("Finale")
                 .description("Requires many quests")
                 .craft_objective("potion", 1)
                 .require_quest("quest_1")
                 .require_quest("quest_2")
                 .build())

        self.assertEqual(len(quest.prerequisites["required_quests"]), 2)

    def test_require_quests_bulk(self):
        quest = (QuestBuilder("finale")
                 .name("Finale")
                 .description("Requires many quests")
                 .craft_objective("potion", 1)
                 .require_quests(["quest_1", "quest_2", "quest_3"])
                 .build())

        self.assertEqual(len(quest.prerequisites["required_quests"]), 3)

    def test_require_stat(self):
        quest = (QuestBuilder("advanced")
                 .name("Advanced")
                 .description("Requires high stats")
                 .craft_objective("potion", 1)
                 .require_stat("knowledge", 60)
                 .build())

        self.assertIn("required_stats", quest.prerequisites)
        self.assertEqual(quest.prerequisites["required_stats"]["knowledge"], 60)

    def test_require_affinity(self):
        quest = (QuestBuilder("friendship")
                 .name("Friendship")
                 .description("Requires good relationship")
                 .craft_objective("potion", 1)
                 .require_affinity("merchant", 1.5)
                 .build())

        self.assertIn("required_affinity", quest.prerequisites)
        self.assertEqual(quest.prerequisites["required_affinity"]["merchant"], 1.5)

    def test_require_item(self):
        quest = (QuestBuilder("delivery")
                 .name("Delivery")
                 .description("Requires special item")
                 .deliver_objective("elder")
                 .require_item("special_package")
                 .build())

        self.assertIn("required_items", quest.prerequisites)
        self.assertIn("special_package", quest.prerequisites["required_items"])

    def test_require_reputation(self):
        quest = (QuestBuilder("prestigious")
                 .name("Prestigious")
                 .description("Requires reputation")
                 .craft_objective("potion", 1)
                 .require_reputation("village", 75)
                 .build())

        self.assertIn("required_reputation", quest.prerequisites)
        self.assertEqual(quest.prerequisites["required_reputation"]["village"], 75)


class TestQuestBuilderValidation(unittest.TestCase):

    def test_missing_name(self):
        builder = QuestBuilder("test").description("Test").craft_objective("potion", 1)
        with self.assertRaises(ValueError) as ctx:
            builder.build()
        self.assertIn("name", str(ctx.exception).lower())

    def test_missing_description(self):
        builder = QuestBuilder("test").name("Test").craft_objective("potion", 1)
        with self.assertRaises(ValueError) as ctx:
            builder.build()
        self.assertIn("description", str(ctx.exception).lower())

    def test_missing_objectives(self):
        builder = QuestBuilder("test").name("Test").description("Test")
        with self.assertRaises(ValueError) as ctx:
            builder.build()
        self.assertIn("objective", str(ctx.exception).lower())

    def test_invalid_stat_requirement_too_low(self):
        builder = (QuestBuilder("test")
                   .name("Test")
                   .description("Test")
                   .craft_objective("potion", 1)
                   .require_stat("knowledge", -1))
        with self.assertRaises(ValueError) as ctx:
            builder.build()
        self.assertIn("0-100", str(ctx.exception))

    def test_invalid_stat_requirement_too_high(self):
        builder = (QuestBuilder("test")
                   .name("Test")
                   .description("Test")
                   .craft_objective("potion", 1)
                   .require_stat("knowledge", 101))
        with self.assertRaises(ValueError) as ctx:
            builder.build()
        self.assertIn("0-100", str(ctx.exception))

    def test_invalid_affinity_requirement_too_low(self):
        builder = (QuestBuilder("test")
                   .name("Test")
                   .description("Test")
                   .craft_objective("potion", 1)
                   .require_affinity("npc", -6.0))
        with self.assertRaises(ValueError) as ctx:
            builder.build()
        self.assertIn("-5.0 to 5.0", str(ctx.exception))

    def test_invalid_affinity_requirement_too_high(self):
        builder = (QuestBuilder("test")
                   .name("Test")
                   .description("Test")
                   .craft_objective("potion", 1)
                   .require_affinity("npc", 6.0))
        with self.assertRaises(ValueError) as ctx:
            builder.build()
        self.assertIn("-5.0 to 5.0", str(ctx.exception))


class TestQuestBuilderChaining(unittest.TestCase):

    def test_complex_quest(self):
        quest = (QuestBuilder("master_quest")
                 .name("The Master's Trial")
                 .description("Prove your mastery")
                 .craft_objective("healing_potion", 10)
                 .craft_objective("mana_potion", 5)
                 .gather_objective("moonleaf", 50)
                 .talk_objective("grand_master")
                 .stat_objective("knowledge", 90)
                 .affinity_objective("guild_master", 3.0)
                 .duel_objective(5)
                 .gold_objective(5000)
                 .require_quest("apprentice_quest")
                 .require_quest("journeyman_quest")
                 .require_stat("knowledge", 80)
                 .require_stat("precision", 70)
                 .require_affinity("guild_master", 2.0)
                 .require_reputation("capital", 80)
                 .state(QuestState.LOCKED)
                 .build())

        self.assertEqual(len(quest.objectives), 8)
        self.assertEqual(len(quest.prerequisites["required_quests"]), 2)
        self.assertEqual(len(quest.prerequisites["required_stats"]), 2)
        self.assertEqual(quest.state, QuestState.LOCKED)


if __name__ == "__main__":
    unittest.main()
