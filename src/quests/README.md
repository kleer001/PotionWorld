# Quest System

Phase 7 implementation of PotionWorld's quest system with state management, objective tracking, moral choices, and cross-system integration following the Hybrid API + Event Architecture.

## Features

- **Quest State Machine**: LOCKED → AVAILABLE → ACTIVE → COMPLETED/FAILED
- **8 Objective Types**: Craft, gather, talk, affinity, stats, delivery, duels, gold
- **Prerequisite System**: Quest chains, stat requirements, affinity gates, item requirements
- **Moral Choice System**: Consequence tracking with world state persistence
- **Auto-Progression**: Automatic objective updates from game events
- **Event-Driven**: Emits events for cross-system integration

## Architecture

### Core Components

1. **Formulas** (`formulas.py`): Pure functions for quest mechanics
   - Quest prerequisite checking
   - State machine transitions
   - Objective completion logic
   - Moral choice consequences

2. **System** (`system.py`): QuestSystem API with event emission
   - `unlock_quest()` - Unlock locked quests
   - `start_quest()` - Start quests with prerequisite checks
   - `update_objective()` - Progress quest objectives
   - `complete_quest()` - Complete quests with validation
   - `fail_quest()` / `abandon_quest()` - Handle quest failure
   - `make_choice()` - Process moral choices
   - `get_quest_progress()` - Query quest status
   - Event listeners for auto-progression

3. **Tests** (`tests/`): Comprehensive test coverage
   - Formula validation
   - System integration tests
   - Event emission verification
   - Auto-progression tests

4. **Testbed** (`testbed.py`): Interactive CLI for testing
   - Quest management
   - Objective manipulation
   - Moral choice simulation
   - Built-in test runner

## Quick Start

### Run the Testbed

```bash
python systest.py --quests
```

Or directly:
```bash
python -m src.quests.testbed
```

### Run Tests

```bash
python -m src.quests.tests.test_formulas
python -m src.quests.tests.test_system
```

### Basic Usage

```python
from src.core.event_bus import EventBus
from src.quests.system import QuestSystem
from src.quests.data_structures import Quest, QuestState, Objective, ObjectiveType

bus = EventBus()
quest_system = QuestSystem(bus)

quest = Quest(
    id="first_quest",
    name="The Apprentice's Trial",
    description="Craft 5 healing potions",
    objectives=[
        Objective(
            id="obj_0",
            type=ObjectiveType.CRAFT_POTION,
            target="healing_potion",
            quantity=5,
            description="Craft 5 healing potions"
        )
    ],
    state=QuestState.AVAILABLE,
    prerequisites={}
)

success, reason = quest_system.start_quest(quest, "player", {})

if success:
    quest_system.update_objective(quest, "obj_0", 1, "player", {})

    progress = quest_system.get_quest_progress(quest, {})
    print(f"Progress: {progress.objectives_complete}/{progress.objectives_total}")
```

## Events

The quest system emits the following events:

- `QuestUnlocked`: When a locked quest becomes available
- `QuestStarted`: When a player starts a quest
- `ObjectiveUpdated`: When objective progress changes
- `QuestCompleted`: When all objectives are complete
- `QuestFailed`: When a quest fails or is abandoned
- `MoralChoiceMade`: When a player makes a moral choice
- `WorldStateChanged`: When a choice modifies world flags

## Quest State Machine

```
LOCKED ──unlock──> AVAILABLE ──start──> ACTIVE ──complete──> COMPLETED
                                           │
                                           └──fail/abandon──> FAILED
```

### State Transitions

**LOCKED → AVAILABLE**
- Prerequisites not met
- Use `unlock_quest()` to make available

**AVAILABLE → ACTIVE**
- Prerequisites checked
- Use `start_quest()`

**ACTIVE → COMPLETED**
- All objectives must be complete
- Use `complete_quest()`

**ACTIVE → FAILED**
- Quest failed or abandoned
- Use `fail_quest()` or `abandon_quest()`

## Objective Types

### 1. CRAFT_POTION
Track potion crafting:
```python
Objective(
    type=ObjectiveType.CRAFT_POTION,
    target="healing_potion",  # or "any"
    quantity=5
)
```

**Auto-Progress**: Listens to `PotionCreated` events

### 2. GATHER_ITEM
Track item collection:
```python
Objective(
    type=ObjectiveType.GATHER_ITEM,
    target="moonleaf",
    quantity=20
)
```

**Auto-Progress**: Listens to `ItemAdded` events

### 3. TALK_TO_NPC
Require NPC interaction:
```python
Objective(
    type=ObjectiveType.TALK_TO_NPC,
    target="elder"
)
```

**Manual**: Must be triggered explicitly

### 4. REACH_AFFINITY
Affinity threshold:
```python
Objective(
    type=ObjectiveType.REACH_AFFINITY,
    target="merchant",
    value=2.0
)
```

**Auto-Check**: Checked against player state

### 5. REACH_STAT
Stat threshold:
```python
Objective(
    type=ObjectiveType.REACH_STAT,
    target="knowledge",
    value=80
)
```

**Auto-Check**: Checked against player state

### 6. DELIVER_ITEM
Item delivery:
```python
Objective(
    type=ObjectiveType.DELIVER_ITEM,
    target="package"
)
```

**Manual**: Must be triggered explicitly

### 7. WIN_DUEL
Combat victories:
```python
Objective(
    type=ObjectiveType.WIN_DUEL,
    target="any",
    quantity=3
)
```

**Auto-Progress**: Listens to `CombatEnded` events

### 8. EARN_GOLD
Gold accumulation:
```python
Objective(
    type=ObjectiveType.EARN_GOLD,
    value=1000
)
```

**Auto-Progress**: Listens to `TransactionCompleted` events

## Prerequisites

### Required Quests
```python
quest.prerequisites = {
    "required_quests": ["intro_quest", "tutorial_quest"]
}
```

### Required Stats
```python
quest.prerequisites = {
    "required_stats": {
        "knowledge": 50,
        "precision": 40
    }
}
```

### Required Affinity
```python
quest.prerequisites = {
    "required_affinity": {
        "elder": 1.0,
        "merchant": 0.5
    }
}
```

### Required Items
```python
quest.prerequisites = {
    "required_items": ["key", "letter"]
}
```

### Required Reputation
```python
quest.prerequisites = {
    "required_reputation": {
        "village": 50,
        "city": 30
    }
}
```

## Moral Choice System

### Defining Choices

```python
choice = MoralChoice(
    id="help_villager",
    quest_id="village_quest",
    description="A sick villager needs a potion but cannot pay. What do you do?",
    options={
        "help_free": {
            "affinity_changes": {"villager": 1.0, "elder": 0.5},
            "reputation_change": 10,
            "gold_change": 0,
            "world_flags": {"village_saved": True}
        },
        "charge_half": {
            "affinity_changes": {"villager": 0.5},
            "reputation_change": 5,
            "gold_change": 25
        },
        "charge_full": {
            "affinity_changes": {"villager": -0.5, "merchant": 0.5},
            "reputation_change": -5,
            "gold_change": 50
        },
        "refuse": {
            "affinity_changes": {"villager": -1.0, "elder": -0.5},
            "reputation_change": -15,
            "gold_change": 0,
            "world_flags": {"village_saved": False}
        }
    },
    }
)
```

### Making Choices

```python
consequences = quest_system.make_choice(
    choice,
    selected_option="help_free",
    player_id="player",
    player_state=current_state
)
```

### Consequence Types

**Affinity Changes**
```python
"affinity_changes": {"npc_id": delta}
```

**Reputation Changes**
```python
"reputation_change": delta
```

**Gold Changes**
```python
"gold_change": delta
```

**World Flags**
```python
"world_flags": {"flag_name": value}
```

The system tracks player choices and determines dominant alignment:

```python
alignment = quest_system.get_player_alignment("player")
```

## Auto-Progression

The quest system automatically updates objectives by listening to game events:

### Crafting Events
```python
event_bus.emit(PotionCreated(...))
# Auto-updates CRAFT_POTION objectives
```

### Gathering Events
```python
event_bus.emit(ItemAdded(...))
# Auto-updates GATHER_ITEM objectives
```

### Combat Events
```python
event_bus.emit(CombatEnded(...))
# Auto-updates WIN_DUEL objectives
```

### Economy Events
```python
event_bus.emit(TransactionCompleted(...))
# Auto-updates EARN_GOLD objectives
```

## Configuration

Quest behavior is tunable via `config/quests.ini`:

```ini
[Limits]
max_active_quests = 10
max_daily_quests = 5
max_total_quests = 100

[Timeouts]
deliver_item = 86400  # 1 day in seconds

[Base_Rewards]
gold_easy = 50
gold_medium = 100
gold_hard = 250
xp_easy = 100
xp_medium = 250
xp_hard = 500
reputation_easy = 5
reputation_medium = 10
reputation_hard = 20

[Moral_Choices]
track_patterns = true
affect_reputation = true
min_impact = 0.5

[Auto_Progression]
enabled = true
track_crafting = true
track_gathering = true
track_combat = true
track_economy = true
track_social = true
```

## Integration Examples

### Progression System

```python
class ProgressionIntegration:
    def __init__(self, event_bus):
        event_bus.subscribe(QuestCompleted, self.on_quest_completed)

    def on_quest_completed(self, event):
        progression.add_xp(
            event.player_id,
            "knowledge",
            100,
            current_xp
        )
```

### Inventory System

```python
class InventoryIntegration:
    def __init__(self, event_bus):
        event_bus.subscribe(QuestCompleted, self.on_quest_completed)

    def on_quest_completed(self, event):
        reward_item = ItemStack("quest_reward", "item", 1, Quality.FINE)
        inventory.add_item(event.player_id, reward_item)
```

### Relationship System

```python
class RelationshipIntegration:
    def __init__(self, event_bus):
        event_bus.subscribe(MoralChoiceMade, self.on_choice_made)

    def on_choice_made(self, event):
        for npc, delta in event.consequences.get("affinity_changes", {}).items():
            relationship.apply_affinity_change(npc, delta)
```

## Testbed Commands

```
list                       - List all quests
start <quest_id>           - Start a quest
progress                   - Show active quest progress
obj <id> <amount>          - Increment objective (god mode)
choice <id> <option>       - Make a moral choice
complete                   - Complete active quest
abandon                    - Abandon active quest
unlock <quest_id>          - Unlock a locked quest (god mode)
state <stat> <value>       - Set player stat (god mode)
affinity <npc> <value>     - Set NPC affinity (god mode)
events [n]                 - Show recent n events
test                       - Run scenario tests
help                       - Show help
quit                       - Exit
```

## Example Testbed Session

```
QUEST SYSTEM TESTBED
============================================================
God mode enabled - full control over quest states

------------------------------------------------------------
PLAYER STATE
------------------------------------------------------------
Knowledge: 50   Precision: 40   Intuition: 30
Business:  25   Combat:    35
Gold: 100   Reputation: 50

Affinities:
  Elder:      0.0
  Merchant:   0.0
  Rival:      0.0


> list

============================================================
AVAILABLE QUESTS
============================================================

📋 [AVAILABLE] The Apprentice's Trial
   ID: craft_quest
   Craft 5 healing potions to prove your skill
   Objectives: 1

📋 [AVAILABLE] Herb Collector
   ID: gather_quest
   Gather ingredients for the elder
   Objectives: 2

> start craft_quest

✓ Started: The Apprentice's Trial

============================================================
QUEST: The Apprentice's Trial
============================================================
State: active
Progress: 0/1

Objectives:
  [ ] Craft 5 healing potions (0/5)

> obj obj_0 3

✓ Incremented obj_0 by 3

Progress: 0/1

Objectives:
  [ ] Craft 5 healing potions (3/5)

> obj obj_0 2

✓ Incremented obj_0 by 2

Progress: 1/1

Objectives:
  [✓] Craft 5 healing potions (5/5)

  → Quest can be completed! Use 'complete' command.

> complete

✓ Quest completed: The Apprentice's Trial
```

## Design Principles

Following SOLID, DRY, and KISS principles:

- **Single Responsibility**: Each function does one thing
- **Pure Functions**: No side effects in formulas
- **Event-Driven**: Loose coupling through events
- **Testable**: All logic has comprehensive tests
- **Clean Code**: Self-documenting, no unnecessary comments

## Success Criteria

✅ **Quest states transition correctly** - State machine enforces valid transitions
✅ **Prerequisites work properly** - Can't bypass requirements
✅ **Objectives track accurately** - Progress counts correctly across all types
✅ **Parallel objectives work** - Can complete in any order
✅ **Moral choices create consequences** - Affinity/reputation/gold changes apply
✅ **World state flags persist** - Choices affect future gameplay
✅ **Auto-progression works** - Events trigger objective updates
✅ **Moral choices create consequences** - Choices persist in world state
✅ **Testbed validates all flows** - Can test complex scenarios
✅ **Events integrate properly** - Other systems respond to quest events
✅ **Tests pass completely** - 100% formula and system coverage
