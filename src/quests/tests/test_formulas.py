import unittest
from src.quests.formulas import (
    can_start_quest, calculate_next_state, check_objective_complete,
    calculate_quest_progress, are_all_objectives_complete,
    calculate_choice_consequences, apply_consequences_to_state,
    track_moral_pattern, analyze_moral_alignment, get_dominant_alignment
)
from src.quests.data_structures import QuestState, ObjectiveType


class TestQuestPrerequisites(unittest.TestCase):

    def test_quest_without_prerequisites(self):
        can_start, reason = can_start_quest("quest_1", {}, {})
        self.assertTrue(can_start)
        self.assertEqual(reason, "Prerequisites met")

    def test_required_quest_not_completed(self):
        can_start, reason = can_start_quest(
            "quest_2",
            {"quest_quest_1": "active"},
            {"quest_2": {"required_quests": ["quest_1"]}}
        )
        self.assertFalse(can_start)
        self.assertIn("quest_1", reason.lower())

    def test_required_quest_completed(self):
        can_start, reason = can_start_quest(
            "quest_2",
            {"quest_quest_1": "completed"},
            {"quest_2": {"required_quests": ["quest_1"]}}
        )
        self.assertTrue(can_start)

    def test_required_stat_insufficient(self):
        can_start, reason = can_start_quest(
            "quest_adv",
            {"knowledge": 30},
            {"quest_adv": {"required_stats": {"knowledge": 50}}}
        )
        self.assertFalse(can_start)
        self.assertIn("knowledge", reason.lower())

    def test_required_stat_sufficient(self):
        can_start, reason = can_start_quest(
            "quest_adv",
            {"knowledge": 60},
            {"quest_adv": {"required_stats": {"knowledge": 50}}}
        )
        self.assertTrue(can_start)

    def test_required_affinity_insufficient(self):
        can_start, reason = can_start_quest(
            "quest_npc",
            {"affinity_elder": 0.5},
            {"quest_npc": {"required_affinity": {"elder": 1.0}}}
        )
        self.assertFalse(can_start)
        self.assertIn("affinity", reason.lower())

    def test_required_affinity_sufficient(self):
        can_start, reason = can_start_quest(
            "quest_npc",
            {"affinity_elder": 1.5},
            {"quest_npc": {"required_affinity": {"elder": 1.0}}}
        )
        self.assertTrue(can_start)

    def test_required_item_missing(self):
        can_start, reason = can_start_quest(
            "quest_delivery",
            {"has_letter": False},
            {"quest_delivery": {"required_items": ["letter"]}}
        )
        self.assertFalse(can_start)
        self.assertIn("letter", reason.lower())

    def test_required_item_present(self):
        can_start, reason = can_start_quest(
            "quest_delivery",
            {"has_letter": True},
            {"quest_delivery": {"required_items": ["letter"]}}
        )
        self.assertTrue(can_start)

    def test_multiple_prerequisites(self):
        can_start, reason = can_start_quest(
            "quest_master",
            {
                "quest_quest_1": "completed",
                "knowledge": 70,
                "affinity_elder": 2.0,
                "has_key": True
            },
            {
                "quest_master": {
                    "required_quests": ["quest_1"],
                    "required_stats": {"knowledge": 60},
                    "required_affinity": {"elder": 1.5},
                    "required_items": ["key"]
                }
            }
        )
        self.assertTrue(can_start)


class TestQuestStateMachine(unittest.TestCase):

    def test_unlock_locked_quest(self):
        state = calculate_next_state(QuestState.LOCKED, "unlock", False)
        self.assertEqual(state, QuestState.AVAILABLE)

    def test_start_available_quest(self):
        state = calculate_next_state(QuestState.AVAILABLE, "start", False)
        self.assertEqual(state, QuestState.ACTIVE)

    def test_complete_with_objectives_done(self):
        state = calculate_next_state(QuestState.ACTIVE, "complete", True)
        self.assertEqual(state, QuestState.COMPLETED)

    def test_complete_without_objectives_done(self):
        state = calculate_next_state(QuestState.ACTIVE, "complete", False)
        self.assertEqual(state, QuestState.ACTIVE)

    def test_fail_active_quest(self):
        state = calculate_next_state(QuestState.ACTIVE, "fail", False)
        self.assertEqual(state, QuestState.FAILED)

    def test_abandon_active_quest(self):
        state = calculate_next_state(QuestState.ACTIVE, "abandon", False)
        self.assertEqual(state, QuestState.FAILED)

    def test_invalid_transition(self):
        state = calculate_next_state(QuestState.LOCKED, "complete", True)
        self.assertEqual(state, QuestState.LOCKED)


class TestObjectiveTracking(unittest.TestCase):

    def test_craft_potion_objective_incomplete(self):
        objective = {
            "type": ObjectiveType.CRAFT_POTION.value,
            "target": "healing_potion",
            "quantity": 5
        }
        complete = check_objective_complete(objective, 3, {})
        self.assertFalse(complete)

    def test_craft_potion_objective_complete(self):
        objective = {
            "type": ObjectiveType.CRAFT_POTION.value,
            "target": "healing_potion",
            "quantity": 5
        }
        complete = check_objective_complete(objective, 5, {})
        self.assertTrue(complete)

    def test_gather_item_objective(self):
        objective = {
            "type": ObjectiveType.GATHER_ITEM.value,
            "target": "moonleaf",
            "quantity": 20
        }
        self.assertFalse(check_objective_complete(objective, 15, {}))
        self.assertTrue(check_objective_complete(objective, 20, {}))

    def test_talk_to_npc_objective(self):
        objective = {
            "type": ObjectiveType.TALK_TO_NPC.value,
            "target": "elder"
        }
        self.assertFalse(check_objective_complete(objective, 0, {}))
        self.assertTrue(check_objective_complete(objective, 1, {}))

    def test_reach_affinity_objective(self):
        objective = {
            "type": ObjectiveType.REACH_AFFINITY.value,
            "target": "merchant",
            "value": 2.0
        }
        player_state = {"affinity_merchant": 1.5}
        self.assertFalse(check_objective_complete(objective, 0, player_state))

        player_state = {"affinity_merchant": 2.5}
        self.assertTrue(check_objective_complete(objective, 0, player_state))

    def test_reach_stat_objective(self):
        objective = {
            "type": ObjectiveType.REACH_STAT.value,
            "target": "knowledge",
            "value": 50
        }
        player_state = {"knowledge": 45}
        self.assertFalse(check_objective_complete(objective, 0, player_state))

        player_state = {"knowledge": 55}
        self.assertTrue(check_objective_complete(objective, 0, player_state))

    def test_deliver_item_objective(self):
        objective = {
            "type": ObjectiveType.DELIVER_ITEM.value,
            "target": "package"
        }
        self.assertFalse(check_objective_complete(objective, 0, {}))
        self.assertTrue(check_objective_complete(objective, 1, {}))

    def test_win_duel_objective(self):
        objective = {
            "type": ObjectiveType.WIN_DUEL.value,
            "target": "any",
            "quantity": 3
        }
        self.assertFalse(check_objective_complete(objective, 2, {}))
        self.assertTrue(check_objective_complete(objective, 3, {}))

    def test_earn_gold_objective(self):
        objective = {
            "type": ObjectiveType.EARN_GOLD.value,
            "value": 500
        }
        self.assertFalse(check_objective_complete(objective, 450, {}))
        self.assertTrue(check_objective_complete(objective, 500, {}))


class TestQuestProgress(unittest.TestCase):

    def test_quest_progress_none_complete(self):
        objectives = [
            {"type": ObjectiveType.CRAFT_POTION.value, "target": "healing", "quantity": 5},
            {"type": ObjectiveType.GATHER_ITEM.value, "target": "moonleaf", "quantity": 10}
        ]
        progress = {"obj_0": 0, "obj_1": 0}
        completed, total = calculate_quest_progress(objectives, progress, {})
        self.assertEqual(completed, 0)
        self.assertEqual(total, 2)

    def test_quest_progress_partial(self):
        objectives = [
            {"type": ObjectiveType.CRAFT_POTION.value, "target": "healing", "quantity": 5},
            {"type": ObjectiveType.GATHER_ITEM.value, "target": "moonleaf", "quantity": 10}
        ]
        progress = {"obj_0": 5, "obj_1": 7}
        completed, total = calculate_quest_progress(objectives, progress, {})
        self.assertEqual(completed, 1)
        self.assertEqual(total, 2)

    def test_quest_progress_all_complete(self):
        objectives = [
            {"type": ObjectiveType.CRAFT_POTION.value, "target": "healing", "quantity": 5},
            {"type": ObjectiveType.GATHER_ITEM.value, "target": "moonleaf", "quantity": 10}
        ]
        progress = {"obj_0": 5, "obj_1": 10}
        completed, total = calculate_quest_progress(objectives, progress, {})
        self.assertEqual(completed, 2)
        self.assertEqual(total, 2)

    def test_all_objectives_complete_check(self):
        objectives = [
            {"type": ObjectiveType.CRAFT_POTION.value, "target": "healing", "quantity": 5},
            {"type": ObjectiveType.TALK_TO_NPC.value, "target": "elder"}
        ]
        progress = {"obj_0": 5, "obj_1": 1}
        self.assertTrue(are_all_objectives_complete(objectives, progress, {}))

        progress = {"obj_0": 5, "obj_1": 0}
        self.assertFalse(are_all_objectives_complete(objectives, progress, {}))


class TestMoralChoices(unittest.TestCase):

    def test_calculate_choice_consequences(self):
        options = {
            "help_free": {
                "affinity_changes": {"villager": 1.0},
                "reputation_change": 10,
                "gold_change": 0
            },
            "charge_full": {
                "affinity_changes": {"villager": -1.0},
                "reputation_change": -5,
                "gold_change": 50
            }
        }
        consequences = calculate_choice_consequences("choice_1", options, "help_free")
        self.assertEqual(consequences["affinity_changes"]["villager"], 1.0)
        self.assertEqual(consequences["reputation_change"], 10)
        self.assertEqual(consequences["gold_change"], 0)

    def test_invalid_choice_option(self):
        options = {"option_a": {"gold_change": 10}}
        consequences = calculate_choice_consequences("choice_1", options, "option_b")
        self.assertEqual(consequences, {})

    def test_apply_consequences_affinity(self):
        state = {"affinity_npc1": 0, "gold": 100, "reputation": 50}
        consequences = {"affinity_changes": {"npc1": 1.5}}
        new_state = apply_consequences_to_state(state, consequences)
        self.assertEqual(new_state["affinity_npc1"], 1.5)
        self.assertEqual(new_state["gold"], 100)

    def test_apply_consequences_reputation(self):
        state = {"reputation": 50, "gold": 100}
        consequences = {"reputation_change": 15}
        new_state = apply_consequences_to_state(state, consequences)
        self.assertEqual(new_state["reputation"], 65)

    def test_apply_consequences_gold(self):
        state = {"gold": 100}
        consequences = {"gold_change": -30}
        new_state = apply_consequences_to_state(state, consequences)
        self.assertEqual(new_state["gold"], 70)

    def test_apply_consequences_world_flags(self):
        state = {}
        consequences = {"world_flags": {"village_saved": True, "merchant_angry": False}}
        new_state = apply_consequences_to_state(state, consequences)
        self.assertTrue(new_state["flag_village_saved"])
        self.assertFalse(new_state["flag_merchant_angry"])

    def test_track_moral_pattern(self):
        history = []
        new_history = track_moral_pattern(
            history, "choice_1", "help", ["altruistic", "lawful"]
        )
        self.assertEqual(len(new_history), 1)
        self.assertIn("choice_1", new_history[0])
        self.assertIn("altruistic", new_history[0])

    def test_analyze_moral_alignment(self):
        history = [
            "choice_1:help:altruistic,lawful",
            "choice_2:donate:altruistic",
            "choice_3:steal:greedy,chaotic"
        ]
        alignment = analyze_moral_alignment(history)
        self.assertEqual(alignment["altruistic"], 2)
        self.assertEqual(alignment["lawful"], 1)
        self.assertEqual(alignment["greedy"], 1)
        self.assertEqual(alignment["chaotic"], 1)

    def test_get_dominant_alignment_empty(self):
        alignment = get_dominant_alignment([])
        self.assertEqual(alignment, "neutral")

    def test_get_dominant_alignment(self):
        history = [
            "choice_1:help:altruistic",
            "choice_2:help:altruistic",
            "choice_3:steal:greedy"
        ]
        alignment = get_dominant_alignment(history)
        self.assertEqual(alignment, "altruistic")


if __name__ == "__main__":
    unittest.main()
