import unittest
from src.core.event_bus import EventBus
from src.core.events import (
    QuestUnlocked, QuestStarted, ObjectiveUpdated, QuestCompleted,
    QuestFailed, MoralChoiceMade, WorldStateChanged,
    PotionCreated, ItemAdded, CombatEnded, TransactionCompleted
)
from src.core.data_structures import Quality
from src.quests.system import QuestSystem
from src.quests.data_structures import (
    Quest, QuestState, Objective, ObjectiveType, MoralChoice
)


class TestQuestSystemBasics(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()
        self.quest_system = QuestSystem(self.bus)
        self.events = []

        def capture_event(event):
            self.events.append(event)

        self.bus.subscribe_all(capture_event)

    def test_unlock_quest(self):
        quest = Quest(
            id="quest_1",
            name="First Quest",
            description="A simple quest",
            objectives=[],
            state=QuestState.LOCKED
        )

        success = self.quest_system.unlock_quest(quest, "player_1")

        self.assertTrue(success)
        self.assertEqual(quest.state, QuestState.AVAILABLE)

        unlocked_events = [e for e in self.events if isinstance(e, QuestUnlocked)]
        self.assertEqual(len(unlocked_events), 1)
        self.assertEqual(unlocked_events[0].quest_id, "quest_1")

    def test_start_quest_success(self):
        quest = Quest(
            id="quest_1",
            name="First Quest",
            description="A simple quest",
            objectives=[],
            state=QuestState.AVAILABLE,
            prerequisites={}
        )

        success, reason = self.quest_system.start_quest(
            quest, "player_1", {}
        )

        self.assertTrue(success)
        self.assertEqual(quest.state, QuestState.ACTIVE)

        started_events = [e for e in self.events if isinstance(e, QuestStarted)]
        self.assertEqual(len(started_events), 1)

    def test_start_quest_with_prerequisites(self):
        quest = Quest(
            id="quest_2",
            name="Advanced Quest",
            description="Requires prerequisites",
            objectives=[],
            state=QuestState.AVAILABLE,
            prerequisites={"required_stats": {"knowledge": 50}}
        )

        success, reason = self.quest_system.start_quest(
            quest, "player_1", {"knowledge": 30}
        )

        self.assertFalse(success)
        self.assertIn("knowledge", reason.lower())

    def test_update_objective(self):
        quest = Quest(
            id="quest_1",
            name="Craft Quest",
            description="Craft potions",
            objectives=[
                Objective(
                    id="obj_0",
                    type=ObjectiveType.CRAFT_POTION,
                    target="healing_potion",
                    quantity=5,
                    description="Craft 5 healing potions"
                )
            ],
            state=QuestState.ACTIVE
        )

        self.quest_system.update_objective(
            quest, "obj_0", 3, "player_1", {}
        )

        self.assertEqual(quest.progress.get("obj_0"), 3)

        updated_events = [e for e in self.events if isinstance(e, ObjectiveUpdated)]
        self.assertEqual(len(updated_events), 1)
        self.assertEqual(updated_events[0].new_progress, 3)

    def test_complete_quest_success(self):
        quest = Quest(
            id="quest_1",
            name="Simple Quest",
            description="Complete objectives",
            objectives=[
                Objective(
                    id="obj_0",
                    type=ObjectiveType.CRAFT_POTION,
                    target="healing_potion",
                    quantity=5
                )
            ],
            state=QuestState.ACTIVE,
            progress={"obj_0": 5}
        )

        self.quest_system.active_quests["player_1"] = {"quest_1": quest}

        success, reason = self.quest_system.complete_quest(
            quest, "player_1", {}
        )

        self.assertTrue(success)
        self.assertEqual(quest.state, QuestState.COMPLETED)

        completed_events = [e for e in self.events if isinstance(e, QuestCompleted)]
        self.assertEqual(len(completed_events), 1)

    def test_complete_quest_objectives_incomplete(self):
        quest = Quest(
            id="quest_1",
            name="Simple Quest",
            description="Complete objectives",
            objectives=[
                Objective(
                    id="obj_0",
                    type=ObjectiveType.CRAFT_POTION,
                    target="healing_potion",
                    quantity=5
                )
            ],
            state=QuestState.ACTIVE,
            progress={"obj_0": 3}
        )

        success, reason = self.quest_system.complete_quest(
            quest, "player_1", {}
        )

        self.assertFalse(success)
        self.assertIn("objectives", reason.lower())

    def test_fail_quest(self):
        quest = Quest(
            id="quest_1",
            name="Failed Quest",
            description="This will fail",
            objectives=[],
            state=QuestState.ACTIVE
        )

        self.quest_system.active_quests["player_1"] = {"quest_1": quest}

        success = self.quest_system.fail_quest(
            quest, "player_1", "timeout"
        )

        self.assertTrue(success)
        self.assertEqual(quest.state, QuestState.FAILED)

        failed_events = [e for e in self.events if isinstance(e, QuestFailed)]
        self.assertEqual(len(failed_events), 1)

    def test_abandon_quest(self):
        quest = Quest(
            id="quest_1",
            name="Abandoned Quest",
            description="Will be abandoned",
            objectives=[],
            state=QuestState.ACTIVE
        )

        self.quest_system.active_quests["player_1"] = {"quest_1": quest}

        success = self.quest_system.abandon_quest(quest, "player_1")

        self.assertTrue(success)
        self.assertEqual(quest.state, QuestState.FAILED)


class TestMoralChoiceSystem(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()
        self.quest_system = QuestSystem(self.bus)
        self.events = []

        def capture_event(event):
            self.events.append(event)

        self.bus.subscribe_all(capture_event)

    def test_make_moral_choice(self):
        choice = MoralChoice(
            id="choice_1",
            quest_id="quest_1",
            description="Help the villager?",
            options={
                "help": {
                    "affinity_changes": {"villager": 1.0},
                    "reputation_change": 10,
                    "gold_change": 0
                },
                "ignore": {
                    "affinity_changes": {"villager": -0.5},
                    "reputation_change": 0,
                    "gold_change": 10
                }
            },
            option_tags={
                "help": ["altruistic", "lawful"],
                "ignore": ["selfish", "neutral"]
            }
        )

        consequences = self.quest_system.make_choice(
            choice, "help", "player_1", {}
        )

        self.assertEqual(consequences["affinity_changes"]["villager"], 1.0)
        self.assertEqual(consequences["reputation_change"], 10)

        choice_events = [e for e in self.events if isinstance(e, MoralChoiceMade)]
        self.assertEqual(len(choice_events), 1)

    def test_moral_choice_with_world_flags(self):
        choice = MoralChoice(
            id="choice_2",
            quest_id="quest_2",
            description="Save the village?",
            options={
                "save": {
                    "world_flags": {"village_saved": True},
                    "gold_change": -100
                }
            },
            option_tags={"save": ["heroic"]}
        )

        consequences = self.quest_system.make_choice(
            choice, "save", "player_1", {}
        )

        world_state_events = [e for e in self.events if isinstance(e, WorldStateChanged)]
        self.assertEqual(len(world_state_events), 1)
        self.assertEqual(world_state_events[0].flag, "village_saved")
        self.assertTrue(world_state_events[0].new_value)

    def test_track_moral_alignment(self):
        choice1 = MoralChoice(
            id="choice_1",
            quest_id="quest_1",
            description="Help?",
            options={"help": {}},
            option_tags={"help": ["altruistic"]}
        )

        choice2 = MoralChoice(
            id="choice_2",
            quest_id="quest_2",
            description="Donate?",
            options={"donate": {}},
            option_tags={"donate": ["altruistic"]}
        )

        self.quest_system.make_choice(choice1, "help", "player_1", {})
        self.quest_system.make_choice(choice2, "donate", "player_1", {})

        alignment = self.quest_system.get_player_alignment("player_1")
        self.assertEqual(alignment, "altruistic")


class TestAutoProgression(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()
        self.quest_system = QuestSystem(self.bus)

    def test_auto_progress_on_potion_created(self):
        quest = Quest(
            id="quest_craft",
            name="Crafting Quest",
            description="Craft potions",
            objectives=[
                Objective(
                    id="obj_0",
                    type=ObjectiveType.CRAFT_POTION,
                    target="healing_potion",
                    quantity=5
                )
            ],
            state=QuestState.ACTIVE,
            progress={}
        )

        self.quest_system.active_quests["crafter_1"] = {"quest_craft": quest}

        class MockPotion:
            def __init__(self):
                self.recipe_id = "healing_potion"

        self.bus.emit(PotionCreated(
            potion=MockPotion(),
            quality=Quality.STANDARD,
            potency=1.0,
            crafter_id="crafter_1"
        ))

        self.assertEqual(quest.progress.get("obj_0", 0), 1)

    def test_auto_progress_on_item_added(self):
        quest = Quest(
            id="quest_gather",
            name="Gathering Quest",
            description="Gather items",
            objectives=[
                Objective(
                    id="obj_0",
                    type=ObjectiveType.GATHER_ITEM,
                    target="moonleaf",
                    quantity=20
                )
            ],
            state=QuestState.ACTIVE,
            progress={}
        )

        self.quest_system.active_quests["gatherer_1"] = {"quest_gather": quest}

        self.bus.emit(ItemAdded(
            owner_id="gatherer_1",
            item_id="moonleaf",
            item_type="ingredient",
            quantity=5,
            slot_index=0
        ))

        self.assertEqual(quest.progress.get("obj_0", 0), 5)

    def test_auto_progress_on_combat_ended(self):
        quest = Quest(
            id="quest_duel",
            name="Combat Quest",
            description="Win duels",
            objectives=[
                Objective(
                    id="obj_0",
                    type=ObjectiveType.WIN_DUEL,
                    target="any",
                    quantity=3
                )
            ],
            state=QuestState.ACTIVE,
            progress={}
        )

        self.quest_system.active_quests["fighter_1"] = {"quest_duel": quest}

        self.bus.emit(CombatEnded(
            combat_id="duel_1",
            winner_id="fighter_1",
            turn_count=10
        ))

        self.assertEqual(quest.progress.get("obj_0", 0), 1)

    def test_auto_progress_on_transaction(self):
        quest = Quest(
            id="quest_gold",
            name="Gold Quest",
            description="Earn gold",
            objectives=[
                Objective(
                    id="obj_0",
                    type=ObjectiveType.EARN_GOLD,
                    target="any",
                    value=500
                )
            ],
            state=QuestState.ACTIVE,
            progress={}
        )

        self.quest_system.active_quests["merchant_1"] = {"quest_gold": quest}

        self.bus.emit(TransactionCompleted(
            transaction_id="tx_1",
            buyer_id="customer_1",
            seller_id="merchant_1",
            item_type="potion",
            quantity=1,
            total_price=150,
            timestamp=12345.0
        ))

        self.assertEqual(quest.progress.get("obj_0", 0), 150)


class TestQuestProgress(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()
        self.quest_system = QuestSystem(self.bus)

    def test_get_quest_progress(self):
        quest = Quest(
            id="quest_1",
            name="Multi-Objective Quest",
            description="Complete multiple objectives",
            objectives=[
                Objective(
                    id="obj_0",
                    type=ObjectiveType.CRAFT_POTION,
                    target="healing_potion",
                    quantity=5
                ),
                Objective(
                    id="obj_1",
                    type=ObjectiveType.GATHER_ITEM,
                    target="moonleaf",
                    quantity=10
                )
            ],
            state=QuestState.ACTIVE,
            progress={"obj_0": 5, "obj_1": 7}
        )

        progress = self.quest_system.get_quest_progress(quest, {})

        self.assertEqual(progress.objectives_complete, 1)
        self.assertEqual(progress.objectives_total, 2)
        self.assertFalse(progress.can_complete)

    def test_get_active_quests(self):
        quest1 = Quest(
            id="quest_1",
            name="Quest 1",
            description="First quest",
            objectives=[],
            state=QuestState.ACTIVE
        )

        quest2 = Quest(
            id="quest_2",
            name="Quest 2",
            description="Second quest",
            objectives=[],
            state=QuestState.ACTIVE
        )

        self.quest_system.active_quests["player_1"] = {
            "quest_1": quest1,
            "quest_2": quest2
        }

        active = self.quest_system.get_active_quests("player_1")
        self.assertEqual(len(active), 2)


if __name__ == "__main__":
    unittest.main()
