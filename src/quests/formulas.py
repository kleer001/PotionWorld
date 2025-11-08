from typing import Dict, List, Any, Tuple
from src.quests.data_structures import QuestState, ObjectiveType


def can_start_quest(
    quest_id: str,
    player_state: Dict[str, Any],
    quest_prerequisites: Dict[str, Any]
) -> Tuple[bool, str]:
    prereqs = quest_prerequisites.get(quest_id, {})

    if "required_quests" in prereqs:
        for req_quest in prereqs["required_quests"]:
            if player_state.get(f"quest_{req_quest}") != "completed":
                return (False, f"Requires quest: {req_quest}")

    if "required_stats" in prereqs:
        for stat, min_value in prereqs["required_stats"].items():
            if player_state.get(stat, 0) < min_value:
                return (False, f"Requires {stat} >= {min_value}")

    if "required_affinity" in prereqs:
        for npc, min_affinity in prereqs["required_affinity"].items():
            if player_state.get(f"affinity_{npc}", 0) < min_affinity:
                return (False, f"Requires affinity with {npc} >= {min_affinity}")

    if "required_items" in prereqs:
        for item in prereqs["required_items"]:
            if not player_state.get(f"has_{item}", False):
                return (False, f"Requires item: {item}")

    if "required_reputation" in prereqs:
        for region, min_rep in prereqs["required_reputation"].items():
            if player_state.get(f"reputation_{region}", 0) < min_rep:
                return (False, f"Requires reputation in {region} >= {min_rep}")

    return (True, "Prerequisites met")


def calculate_next_state(
    current_state: QuestState,
    action: str,
    objectives_complete: bool
) -> QuestState:
    transitions = {
        QuestState.LOCKED: {
            "unlock": QuestState.AVAILABLE
        },
        QuestState.AVAILABLE: {
            "start": QuestState.ACTIVE
        },
        QuestState.ACTIVE: {
            "complete": QuestState.COMPLETED,
            "fail": QuestState.FAILED,
            "abandon": QuestState.FAILED
        }
    }

    if action == "complete" and not objectives_complete:
        return current_state

    return transitions.get(current_state, {}).get(action, current_state)


def check_objective_complete(
    objective: Dict[str, Any],
    progress: int,
    player_state: Dict[str, Any]
) -> bool:
    obj_type = ObjectiveType(objective["type"])

    if obj_type in [ObjectiveType.CRAFT_POTION, ObjectiveType.GATHER_ITEM]:
        required = objective.get("quantity", 1)
        return progress >= required

    elif obj_type == ObjectiveType.TALK_TO_NPC:
        return progress >= 1

    elif obj_type == ObjectiveType.REACH_AFFINITY:
        npc = objective["target"]
        required = objective["value"]
        current = player_state.get(f"affinity_{npc}", 0)
        return current >= required

    elif obj_type == ObjectiveType.REACH_STAT:
        stat = objective["target"]
        required = objective["value"]
        current = player_state.get(stat, 0)
        return current >= required

    elif obj_type == ObjectiveType.DELIVER_ITEM:
        return progress >= 1

    elif obj_type == ObjectiveType.WIN_DUEL:
        required = objective.get("quantity", 1)
        return progress >= required

    elif obj_type == ObjectiveType.EARN_GOLD:
        required = objective.get("value", 100)
        return progress >= required

    return False


def calculate_quest_progress(
    objectives: List[Dict[str, Any]],
    objective_progress: Dict[str, int],
    player_state: Dict[str, Any]
) -> Tuple[int, int]:
    total = len(objectives)
    completed = 0

    for i, obj in enumerate(objectives):
        progress = objective_progress.get(f"obj_{i}", 0)
        if check_objective_complete(obj, progress, player_state):
            completed += 1

    return (completed, total)


def are_all_objectives_complete(
    objectives: List[Dict[str, Any]],
    objective_progress: Dict[str, int],
    player_state: Dict[str, Any]
) -> bool:
    completed, total = calculate_quest_progress(
        objectives,
        objective_progress,
        player_state
    )
    return completed == total


def calculate_choice_consequences(
    choice_id: str,
    choice_options: Dict[str, dict],
    selected_option: str
) -> Dict[str, Any]:
    if selected_option not in choice_options:
        return {}

    return choice_options[selected_option]


def apply_consequences_to_state(
    player_state: Dict[str, Any],
    consequences: Dict[str, Any]
) -> Dict[str, Any]:
    new_state = player_state.copy()

    for npc, change in consequences.get("affinity_changes", {}).items():
        key = f"affinity_{npc}"
        new_state[key] = new_state.get(key, 0) + change

    if "reputation_change" in consequences:
        new_state["reputation"] = new_state.get("reputation", 0) + consequences["reputation_change"]

    if "gold_change" in consequences:
        new_state["gold"] = new_state.get("gold", 0) + consequences["gold_change"]

    for flag, value in consequences.get("world_flags", {}).items():
        new_state[f"flag_{flag}"] = value

    return new_state
