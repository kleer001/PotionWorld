# Quest System: 3-Step Implementation

## Overview
Quest structure, objective tracking, state management, moral choices with consequences.

**Core Validation:** Quest state machine works reliably, objectives track progress correctly, moral choices create meaningful consequences, prerequisites unlock properly.

---

## Step 1: Core Logic

### 1.1 Quest State Machine
```python
from enum import Enum

class QuestState(Enum):
    LOCKED = "locked"          # Prerequisites not met
    AVAILABLE = "available"    # Can be started
    ACTIVE = "active"          # In progress
    COMPLETED = "completed"    # Finished successfully
    FAILED = "failed"          # Failed or abandoned

def can_start_quest(
    quest_id: str,
    player_state: dict,
    quest_prerequisites: dict
) -> tuple[bool, str]:
    """
    Pure function: Check if quest can be started

    Returns: (can_start, reason)
    """
    prereqs = quest_prerequisites.get(quest_id, {})

    # Check required quests completed
    if "required_quests" in prereqs:
        for req_quest in prereqs["required_quests"]:
            if player_state.get(f"quest_{req_quest}") != "completed":
                return (False, f"Requires quest: {req_quest}")

    # Check stat requirements
    if "required_stats" in prereqs:
        for stat, min_value in prereqs["required_stats"].items():
            if player_state.get(stat, 0) < min_value:
                return (False, f"Requires {stat} >= {min_value}")

    # Check affinity requirements
    if "required_affinity" in prereqs:
        for npc, min_affinity in prereqs["required_affinity"].items():
            if player_state.get(f"affinity_{npc}", 0) < min_affinity:
                return (False, f"Requires affinity with {npc} >= {min_affinity}")

    # Check item requirements
    if "required_items" in prereqs:
        for item in prereqs["required_items"]:
            if not player_state.get(f"has_{item}", False):
                return (False, f"Requires item: {item}")

    return (True, "Prerequisites met")

def calculate_next_state(
    current_state: QuestState,
    action: str,
    objectives_complete: bool
) -> QuestState:
    """
    Pure function: Determine next quest state

    Returns: new state
    """
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
        return current_state  # Can't complete without objectives

    return transitions.get(current_state, {}).get(action, current_state)
```

### 1.2 Objective Tracking
```python
from typing import List, Dict, Any

class ObjectiveType(Enum):
    CRAFT_POTION = "craft_potion"
    GATHER_ITEM = "gather_item"
    TALK_TO_NPC = "talk_to_npc"
    REACH_AFFINITY = "reach_affinity"
    REACH_STAT = "reach_stat"
    DELIVER_ITEM = "deliver_item"
    WIN_DUEL = "win_duel"
    EARN_GOLD = "earn_gold"

def check_objective_complete(
    objective: dict,
    progress: int,
    player_state: dict
) -> bool:
    """
    Pure function: Check if objective is complete

    objective = {
        "type": ObjectiveType.CRAFT_POTION,
        "target": "healing_potion",
        "quantity": 5
    }
    """
    obj_type = ObjectiveType(objective["type"])

    if obj_type in [ObjectiveType.CRAFT_POTION, ObjectiveType.GATHER_ITEM]:
        # Count-based objectives
        required = objective.get("quantity", 1)
        return progress >= required

    elif obj_type == ObjectiveType.TALK_TO_NPC:
        # Boolean objectives
        return progress >= 1

    elif obj_type == ObjectiveType.REACH_AFFINITY:
        # Threshold objectives
        npc = objective["target"]
        required = objective["value"]
        current = player_state.get(f"affinity_{npc}", 0)
        return current >= required

    elif obj_type == ObjectiveType.REACH_STAT:
        # Stat threshold
        stat = objective["target"]
        required = objective["value"]
        current = player_state.get(stat, 0)
        return current >= required

    elif obj_type == ObjectiveType.DELIVER_ITEM:
        # Delivery complete when progress marked
        return progress >= 1

    elif obj_type == ObjectiveType.WIN_DUEL:
        # Win count
        required = objective.get("quantity", 1)
        return progress >= required

    elif obj_type == ObjectiveType.EARN_GOLD:
        # Gold threshold
        required = objective.get("value", 100)
        return progress >= required

    return False

def calculate_quest_progress(
    objectives: List[dict],
    objective_progress: Dict[str, int],
    player_state: dict
) -> tuple[int, int]:
    """
    Pure function: Calculate overall quest progress

    Returns: (completed_count, total_count)
    """
    total = len(objectives)
    completed = 0

    for i, obj in enumerate(objectives):
        progress = objective_progress.get(f"obj_{i}", 0)
        if check_objective_complete(obj, progress, player_state):
            completed += 1

    return (completed, total)

def are_all_objectives_complete(
    objectives: List[dict],
    objective_progress: Dict[str, int],
    player_state: dict
) -> bool:
    """
    Pure function: Check if quest can be completed
    """
    completed, total = calculate_quest_progress(
        objectives,
        objective_progress,
        player_state
    )
    return completed == total
```

### 1.3 Moral Choice Logic
```python
def calculate_choice_consequences(
    choice_id: str,
    choice_options: dict,
    selected_option: str
) -> dict:
    """
    Pure function: Calculate consequences of moral choice

    choice_options = {
        "help_free": {
            "affinity_changes": {"villager": +1.0, "merchant": +0.5},
            "reputation_change": +10,
            "gold_change": 0
        },
        "charge_full": {
            "affinity_changes": {"villager": -1.0, "merchant": +0.5},
            "reputation_change": -5,
            "gold_change": +50
        }
    }

    Returns: consequences dict
    """
    if selected_option not in choice_options:
        return {}

    return choice_options[selected_option]

def apply_consequences_to_state(
    player_state: dict,
    consequences: dict
) -> dict:
    """
    Pure function: Apply consequences to player state

    Returns: new state (doesn't mutate input)
    """
    new_state = player_state.copy()

    # Apply affinity changes
    for npc, change in consequences.get("affinity_changes", {}).items():
        key = f"affinity_{npc}"
        new_state[key] = new_state.get(key, 0) + change

    # Apply reputation change
    if "reputation_change" in consequences:
        new_state["reputation"] = new_state.get("reputation", 0) + consequences["reputation_change"]

    # Apply gold change
    if "gold_change" in consequences:
        new_state["gold"] = new_state.get("gold", 0) + consequences["gold_change"]

    # Set world state flags
    for flag, value in consequences.get("world_flags", {}).items():
        new_state[f"flag_{flag}"] = value

    return new_state

def track_moral_pattern(
    choice_history: List[str],
    choice_id: str,
    selected_option: str,
    option_tags: List[str]
) -> List[str]:
    """
    Pure function: Track player's moral choices for patterns

    option_tags = ["altruistic", "lawful"] or ["greedy", "pragmatic"]

    Returns: updated history
    """
    new_history = choice_history.copy()
    new_history.append(f"{choice_id}:{selected_option}:{','.join(option_tags)}")
    return new_history
```

### Tests (Step 1)
```python
def test_quest_prerequisites():
    """Test prerequisite checking"""
    # Missing required quest
    can_start, reason = can_start_quest(
        "quest_2",
        {"quest_quest_1": "active"},  # Quest 1 not completed
        {"quest_2": {"required_quests": ["quest_1"]}}
    )
    assert not can_start
    assert "quest_1" in reason.lower()

    # Prerequisites met
    can_start, reason = can_start_quest(
        "quest_2",
        {"quest_quest_1": "completed"},
        {"quest_2": {"required_quests": ["quest_1"]}}
    )
    assert can_start

def test_state_transitions():
    """Test quest state machine"""
    # Can't complete without objectives done
    state = calculate_next_state(
        QuestState.ACTIVE,
        "complete",
        objectives_complete=False
    )
    assert state == QuestState.ACTIVE

    # Can complete with objectives done
    state = calculate_next_state(
        QuestState.ACTIVE,
        "complete",
        objectives_complete=True
    )
    assert state == QuestState.COMPLETED

def test_objective_progress():
    """Test objective tracking"""
    objectives = [
        {"type": "craft_potion", "target": "healing", "quantity": 3},
        {"type": "talk_to_npc", "target": "elder"}
    ]

    progress = {"obj_0": 3, "obj_1": 1}
    completed, total = calculate_quest_progress(objectives, progress, {})

    assert completed == 2
    assert total == 2

def test_moral_choices():
    """Test choice consequences"""
    options = {
        "help": {"affinity_changes": {"npc1": +1.0}, "gold_change": 0},
        "ignore": {"affinity_changes": {"npc1": -0.5}, "gold_change": +10}
    }

    consequences = calculate_choice_consequences("choice_1", options, "help")
    assert consequences["affinity_changes"]["npc1"] == 1.0

    state = {"affinity_npc1": 0, "gold": 50}
    new_state = apply_consequences_to_state(state, consequences)

    assert new_state["affinity_npc1"] == 1.0
    assert new_state["gold"] == 50  # No change
```

---

## Step 2: API + Events

### 2.1 Data Structures
```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class Objective:
    id: str
    type: ObjectiveType
    target: str
    quantity: int = 1
    value: Optional[float] = None
    description: str = ""

@dataclass
class Quest:
    id: str
    name: str
    description: str
    objectives: List[Objective]
    state: QuestState
    progress: Dict[str, int] = field(default_factory=dict)
    moral_choices: List[str] = field(default_factory=list)

@dataclass
class MoralChoice:
    id: str
    quest_id: str
    description: str
    options: Dict[str, dict]  # option_id -> consequences
    option_tags: Dict[str, List[str]]  # option_id -> ["altruistic", "greedy", etc.]

@dataclass
class QuestProgress:
    quest_id: str
    objectives_complete: int
    objectives_total: int
    can_complete: bool
```

### 2.2 Events
```python
@dataclass
class QuestUnlocked:
    quest_id: str
    quest_name: str
    player_id: str

@dataclass
class QuestStarted:
    quest_id: str
    quest_name: str
    player_id: str
    timestamp: int

@dataclass
class ObjectiveUpdated:
    quest_id: str
    objective_id: str
    old_progress: int
    new_progress: int
    complete: bool
    player_id: str

@dataclass
class QuestCompleted:
    quest_id: str
    quest_name: str
    player_id: str
    timestamp: int
    choices_made: List[str]

@dataclass
class QuestFailed:
    quest_id: str
    quest_name: str
    reason: str
    player_id: str

@dataclass
class MoralChoiceMade:
    quest_id: str
    choice_id: str
    selected_option: str
    consequences: dict
    player_id: str

@dataclass
class WorldStateChanged:
    flag: str
    old_value: Any
    new_value: Any
    source_quest: str
```

### 2.3 QuestSystem Class
```python
class QuestSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

        # Listen to game events that might progress quests
        event_bus.subscribe(PotionCreated, self.on_potion_created)
        event_bus.subscribe(ItemAdded, self.on_item_added)
        event_bus.subscribe(AffinityChanged, self.on_affinity_changed)

    def start_quest(
        self,
        quest: Quest,
        player_id: str,
        player_state: dict,
        prerequisites: dict
    ) -> tuple[bool, str]:
        """
        API: Attempt to start a quest

        1. Check prerequisites
        2. Update quest state
        3. Emit events
        """
        # Check if can start
        can_start, reason = can_start_quest(quest.id, player_state, prerequisites)

        if not can_start:
            return (False, reason)

        # Update state
        quest.state = calculate_next_state(quest.state, "start", False)

        # Emit event
        self.event_bus.emit(QuestStarted(
            quest_id=quest.id,
            quest_name=quest.name,
            player_id=player_id,
            timestamp=int(time.time())
        ))

        return (True, "Quest started")

    def update_objective(
        self,
        quest: Quest,
        objective_id: str,
        increment: int,
        player_id: str,
        player_state: dict
    ):
        """
        API: Update objective progress

        1. Increment progress
        2. Check completion
        3. Emit events
        """
        old_progress = quest.progress.get(objective_id, 0)
        new_progress = old_progress + increment
        quest.progress[objective_id] = new_progress

        # Find objective
        obj_index = int(objective_id.split("_")[1])
        objective = quest.objectives[obj_index]

        # Check if complete
        complete = check_objective_complete(
            {
                "type": objective.type.value,
                "target": objective.target,
                "quantity": objective.quantity,
                "value": objective.value
            },
            new_progress,
            player_state
        )

        # Emit event
        self.event_bus.emit(ObjectiveUpdated(
            quest_id=quest.id,
            objective_id=objective_id,
            old_progress=old_progress,
            new_progress=new_progress,
            complete=complete,
            player_id=player_id
        ))

    def complete_quest(
        self,
        quest: Quest,
        player_id: str,
        player_state: dict
    ) -> tuple[bool, str]:
        """
        API: Attempt to complete quest

        1. Check all objectives complete
        2. Update state
        3. Emit events
        """
        # Check if all objectives done
        all_complete = are_all_objectives_complete(
            [
                {
                    "type": obj.type.value,
                    "target": obj.target,
                    "quantity": obj.quantity,
                    "value": obj.value
                }
                for obj in quest.objectives
            ],
            quest.progress,
            player_state
        )

        if not all_complete:
            return (False, "Not all objectives complete")

        # Update state
        quest.state = calculate_next_state(quest.state, "complete", True)

        # Emit event
        self.event_bus.emit(QuestCompleted(
            quest_id=quest.id,
            quest_name=quest.name,
            player_id=player_id,
            timestamp=int(time.time()),
            choices_made=quest.moral_choices
        ))

        return (True, "Quest completed")

    def make_choice(
        self,
        choice: MoralChoice,
        selected_option: str,
        player_id: str,
        player_state: dict
    ) -> dict:
        """
        API: Make a moral choice

        1. Calculate consequences
        2. Apply to state
        3. Track pattern
        4. Emit events
        """
        # Calculate consequences
        consequences = calculate_choice_consequences(
            choice.id,
            choice.options,
            selected_option
        )

        # Emit choice made
        self.event_bus.emit(MoralChoiceMade(
            quest_id=choice.quest_id,
            choice_id=choice.id,
            selected_option=selected_option,
            consequences=consequences,
            player_id=player_id
        ))

        # Emit world state changes
        for flag, value in consequences.get("world_flags", {}).items():
            self.event_bus.emit(WorldStateChanged(
                flag=flag,
                old_value=player_state.get(f"flag_{flag}"),
                new_value=value,
                source_quest=choice.quest_id
            ))

        return consequences

    def get_quest_progress(
        self,
        quest: Quest,
        player_state: dict
    ) -> QuestProgress:
        """
        API: Get quest progress summary
        """
        completed, total = calculate_quest_progress(
            [
                {
                    "type": obj.type.value,
                    "target": obj.target,
                    "quantity": obj.quantity,
                    "value": obj.value
                }
                for obj in quest.objectives
            ],
            quest.progress,
            player_state
        )

        can_complete = are_all_objectives_complete(
            [
                {
                    "type": obj.type.value,
                    "target": obj.target,
                    "quantity": obj.quantity,
                    "value": obj.value
                }
                for obj in quest.objectives
            ],
            quest.progress,
            player_state
        )

        return QuestProgress(
            quest_id=quest.id,
            objectives_complete=completed,
            objectives_total=total,
            can_complete=can_complete
        )

    # Event handlers for auto-progress
    def on_potion_created(self, event: PotionCreated):
        """Auto-progress craft objectives"""
        # Find active quests with craft objectives
        # Increment progress for matching recipe
        pass

    def on_item_added(self, event: ItemAdded):
        """Auto-progress gather objectives"""
        # Find active quests with gather objectives
        # Increment progress for matching item
        pass

    def on_affinity_changed(self, event: AffinityChanged):
        """Check affinity threshold objectives"""
        # Find active quests with affinity objectives
        # Check if threshold reached
        pass
```

---

## Step 3: Testbed + Integration

### 3.1 Quest Testbed
```python
class QuestTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.quest_sys = QuestSystem(self.event_bus)

        # God mode: instant state manipulation
        self.player_state = {
            "knowledge": 50,
            "gold": 100,
            "reputation": 0
        }

        self.quests = self._create_test_quests()
        self.active_quest = None

        # Track events
        self.event_bus.subscribe(self._on_event)

    def run(self):
        """Main CLI loop"""
        print("QUEST TESTBED (God Mode)")
        print("=" * 60)

        while True:
            self._display_status()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "list":
                self._list_quests()
            elif cmd[0] == "start":
                self._start_quest(cmd[1])
            elif cmd[0] == "progress":
                self._show_progress()
            elif cmd[0] == "obj":
                # God mode: manually increment objective
                self._increment_objective(cmd[1], int(cmd[2]))
            elif cmd[0] == "choice":
                self._make_choice(cmd[1], cmd[2])
            elif cmd[0] == "complete":
                self._complete_quest()
            elif cmd[0] == "state":
                # God mode: set player state
                self._set_state(cmd[1:])
            elif cmd[0] == "test":
                self._run_scenario_tests()
            elif cmd[0] == "help":
                self._show_help()
            elif cmd[0] == "quit":
                break

    def _start_quest(self, quest_id: str):
        """Start a quest"""
        quest = next((q for q in self.quests if q.id == quest_id), None)
        if not quest:
            print(f"Quest {quest_id} not found")
            return

        success, reason = self.quest_sys.start_quest(
            quest,
            player_id="testbed",
            player_state=self.player_state,
            prerequisites={}  # God mode: no prerequisites
        )

        if success:
            self.active_quest = quest
            print(f"✓ Started: {quest.name}")
            self._show_progress()
        else:
            print(f"✗ Cannot start: {reason}")

    def _show_progress(self):
        """Show current quest progress"""
        if not self.active_quest:
            print("No active quest")
            return

        progress = self.quest_sys.get_quest_progress(
            self.active_quest,
            self.player_state
        )

        print(f"\n{'=' * 60}")
        print(f"QUEST: {self.active_quest.name}")
        print(f"{'=' * 60}")
        print(f"State: {self.active_quest.state.value}")
        print(f"Progress: {progress.objectives_complete}/{progress.objectives_total}")

        print(f"\nObjectives:")
        for i, obj in enumerate(self.active_quest.objectives):
            obj_id = f"obj_{i}"
            current = self.active_quest.progress.get(obj_id, 0)
            complete = check_objective_complete(
                {
                    "type": obj.type.value,
                    "target": obj.target,
                    "quantity": obj.quantity,
                    "value": obj.value
                },
                current,
                self.player_state
            )

            status = "✓" if complete else " "
            print(f"  [{status}] {obj.description} ({current}/{obj.quantity})")

        if progress.can_complete:
            print(f"\n  → Quest can be completed!")

    def _increment_objective(self, obj_id: str, amount: int):
        """God mode: manually increment objective"""
        if not self.active_quest:
            print("No active quest")
            return

        self.quest_sys.update_objective(
            self.active_quest,
            obj_id,
            amount,
            player_id="testbed",
            player_state=self.player_state
        )

        print(f"Incremented {obj_id} by {amount}")
        self._show_progress()

    def _make_choice(self, choice_id: str, option: str):
        """Make a moral choice"""
        # Find choice in test data
        choice = self._get_choice(choice_id)
        if not choice:
            print(f"Choice {choice_id} not found")
            return

        consequences = self.quest_sys.make_choice(
            choice,
            option,
            player_id="testbed",
            player_state=self.player_state
        )

        # Apply consequences (god mode: show but don't persist)
        print(f"\nChoice made: {option}")
        print(f"\nConsequences:")
        for key, value in consequences.items():
            print(f"  {key}: {value}")

    def _complete_quest(self):
        """Complete the active quest"""
        if not self.active_quest:
            print("No active quest")
            return

        success, reason = self.quest_sys.complete_quest(
            self.active_quest,
            player_id="testbed",
            player_state=self.player_state
        )

        if success:
            print(f"✓ Quest completed: {self.active_quest.name}")
            self.active_quest = None
        else:
            print(f"✗ Cannot complete: {reason}")

    def _run_scenario_tests(self):
        """Run predefined quest scenarios"""
        print("\n" + "=" * 60)
        print("RUNNING SCENARIO TESTS")
        print("=" * 60)

        # Scenario 1: Linear quest completion
        print("\nScenario 1: Complete linear quest")
        quest = self._create_simple_quest()
        self.quest_sys.start_quest(quest, "test", {}, {})

        for i in range(len(quest.objectives)):
            self.quest_sys.update_objective(
                quest, f"obj_{i}", 999, "test", {}
            )

        success, _ = self.quest_sys.complete_quest(quest, "test", {})
        print(f"  Result: {'✓ PASS' if success else '✗ FAIL'}")

        # Scenario 2: Prerequisites
        print("\nScenario 2: Quest prerequisites")
        can_start, reason = can_start_quest(
            "locked_quest",
            {"quest_prereq_quest": "active"},
            {"locked_quest": {"required_quests": ["prereq_quest"]}}
        )
        print(f"  Locked (correct): {'✓ PASS' if not can_start else '✗ FAIL'}")

        # Scenario 3: Moral choice consequences
        print("\nScenario 3: Moral choice")
        choice = MoralChoice(
            id="test_choice",
            quest_id="test",
            description="Help or profit?",
            options={
                "help": {"gold_change": 0, "affinity_changes": {"npc": +1.0}},
                "profit": {"gold_change": +50, "affinity_changes": {"npc": -1.0}}
            },
            option_tags={}
        )
        consequences = self.quest_sys.make_choice(choice, "help", "test", {})
        print(f"  Consequences applied: {'✓ PASS' if consequences else '✗ FAIL'}")

    def _set_state(self, args):
        """God mode: set player state"""
        # state gold 500
        if len(args) >= 2:
            key = args[0]
            value = int(args[1])
            self.player_state[key] = value
            print(f"Set {key} = {value}")

    def _show_help(self):
        print("\nCommands:")
        print("  list                 - List all quests")
        print("  start <id>           - Start a quest")
        print("  progress             - Show active quest progress")
        print("  obj <id> <amount>    - Increment objective (god mode)")
        print("  choice <id> <option> - Make a moral choice")
        print("  complete             - Complete active quest")
        print("  state <key> <value>  - Set player state (god mode)")
        print("  test                 - Run scenario tests")
        print("  help                 - Show this help")
        print("  quit                 - Exit")

    def _on_event(self, event):
        """Log events"""
        print(f"  [Event] {event.__class__.__name__}")
```

### 3.2 Integration with Other Systems
```python
# Quest system listens to game events to auto-progress objectives

class QuestSystem:
    # ... existing code ...

    def on_potion_created(self, event: PotionCreated):
        """Auto-progress craft objectives when potion created"""
        for quest in self._get_active_quests():
            for i, obj in enumerate(quest.objectives):
                if obj.type == ObjectiveType.CRAFT_POTION:
                    if obj.target == event.potion.recipe_id or obj.target == "any":
                        self.update_objective(
                            quest,
                            f"obj_{i}",
                            1,
                            event.crafter_id,
                            {}
                        )

    def on_affinity_changed(self, event: AffinityChanged):
        """Check affinity threshold objectives"""
        for quest in self._get_active_quests():
            for i, obj in enumerate(quest.objectives):
                if obj.type == ObjectiveType.REACH_AFFINITY:
                    if obj.target == event.npc_id:
                        # Threshold check handled in check_objective_complete
                        pass
```

---

## Success Criteria

This system is complete when:

✅ **Quest states transition correctly** - Locked → Available → Active → Completed
✅ **Prerequisites work properly** - Can't start quests early
✅ **Objectives track accurately** - Progress counts correctly
✅ **Parallel objectives work** - Can complete in any order
✅ **Sequential objectives work** - Must complete in order (if flagged)
✅ **Moral choices create consequences** - Affinity/reputation/gold changes apply
✅ **World state flags persist** - Choices affect future quests
✅ **Auto-progression works** - Crafting/gathering triggers objective updates
✅ **Testbed validates all flows** - Can test complex quest scenarios
✅ **Events integrate properly** - Other systems respond to quest events
