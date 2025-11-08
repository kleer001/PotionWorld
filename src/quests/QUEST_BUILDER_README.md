# QuestBuilder - Developer Guide

Clean, fluent API for creating quests in PotionWorld.

## Overview

QuestBuilder provides a declarative, chainable interface for quest creation with automatic ID generation and build-time validation. Create complex quests with minimal code while ensuring correctness.

**Example:**
```python
(QuestBuilder("my_quest")
 .name("The Trial")
 .description("Prove yourself")
 .craft_objective("healing_potion", 5)
 .gather_objective("moonleaf", 20)
 .require_stat("knowledge", 50)
 .build())
```

## Quick Start

```python
from src.quests.builder import QuestBuilder

quest = (QuestBuilder("intro_quest")
         .name("First Steps")
         .description("Learn the basics")
         .craft_objective("healing_potion", 1)
         .build())
```

That's it. No boilerplate, no manual ID assignment, clean and readable.

## Complete API Reference

### Required Methods

```python
QuestBuilder(quest_id: str)  # Constructor - quest ID
    .name(name: str)          # Quest name (required)
    .description(desc: str)   # Quest description (required)
    .build() -> Quest         # Build and validate
```

At minimum, every quest needs: **ID, name, description, and at least one objective**.

### Objective Methods

#### craft_objective
```python
.craft_objective(
    target: str,              # Recipe ID or "any"
    quantity: int,            # How many to craft
    description: str = None   # Optional custom description
)
```

**Auto-progression**: Listens to `PotionCreated` events

**Examples:**
```python
.craft_objective("healing_potion", 5)
.craft_objective("any", 20, "Craft 20 potions of any type")
```

#### gather_objective
```python
.gather_objective(
    target: str,              # Item ID
    quantity: int,            # How many to gather
    description: str = None
)
```

**Auto-progression**: Listens to `ItemAdded` events

**Examples:**
```python
.gather_objective("moonleaf", 50)
.gather_objective("rare_herb", 10, "Find 10 rare herbs in the forest")
```

#### talk_objective
```python
.talk_objective(
    target: str,              # NPC ID
    description: str = None
)
```

**Manual trigger**: Must be explicitly marked complete

**Examples:**
```python
.talk_objective("elder")
.talk_objective("mysterious_stranger", "Speak with the stranger")
```

#### affinity_objective
```python
.affinity_objective(
    target: str,              # NPC ID
    value: float,             # Required affinity (-5.0 to 5.0)
    description: str = None
)
```

**Auto-check**: Evaluated against current affinity

**Examples:**
```python
.affinity_objective("merchant", 2.0)
.affinity_objective("guild_master", 3.5, "Earn the guild master's trust")
```

#### stat_objective
```python
.stat_objective(
    target: str,              # Stat name
    value: float,             # Required level (0-100)
    description: str = None
)
```

**Auto-check**: Evaluated against current stat

**Examples:**
```python
.stat_objective("knowledge", 80)
.stat_objective("precision", 60, "Master the art of precision")
```

#### deliver_objective
```python
.deliver_objective(
    target: str,              # NPC ID to deliver to
    description: str = None
)
```

**Manual trigger**: Must be explicitly marked complete

**Examples:**
```python
.deliver_objective("elder")
.deliver_objective("captain", "Deliver the sealed orders")
```

#### duel_objective
```python
.duel_objective(
    quantity: int,            # Number of duels to win
    target: str = "any",      # Specific opponent or "any"
    description: str = None
)
```

**Auto-progression**: Listens to `CombatEnded` events

**Examples:**
```python
.duel_objective(3)
.duel_objective(5, "rival", "Defeat your rival 5 times")
```

#### gold_objective
```python
.gold_objective(
    value: int,               # Gold amount
    description: str = None
)
```

**Auto-progression**: Listens to `TransactionCompleted` events

**Examples:**
```python
.gold_objective(1000)
.gold_objective(5000, "Amass a fortune of 5000 gold")
```

### Prerequisite Methods

#### require_quest
```python
.require_quest(quest_id: str)
```

Requires a specific quest to be completed first.

**Examples:**
```python
.require_quest("intro_quest")
```

#### require_quests
```python
.require_quests(quest_ids: List[str])
```

Bulk add multiple quest prerequisites.

**Examples:**
```python
.require_quests(["quest_1", "quest_2", "quest_3"])
```

#### require_stat
```python
.require_stat(stat: str, min_value: int)
```

Requires minimum stat level (0-100).

**Validated**: Raises `ValueError` if not 0-100.

**Examples:**
```python
.require_stat("knowledge", 60)
.require_stat("precision", 50)
```

#### require_affinity
```python
.require_affinity(npc: str, min_value: float)
```

Requires minimum affinity with NPC (-5.0 to 5.0).

**Validated**: Raises `ValueError` if not -5.0 to 5.0.

**Examples:**
```python
.require_affinity("guild_master", 2.0)
.require_affinity("merchant", 1.5)
```

#### require_item
```python
.require_item(item: str)
```

Requires player to possess a specific item.

**Examples:**
```python
.require_item("guild_membership_card")
.require_item("sealed_letter")
```

#### require_reputation
```python
.require_reputation(region: str, min_value: int)
```

Requires minimum regional reputation.

**Examples:**
```python
.require_reputation("capital", 75)
.require_reputation("village", 50)
```

### Optional Methods

#### state
```python
.state(state: QuestState)
```

Set initial quest state. Defaults to `QuestState.AVAILABLE`.

**Examples:**
```python
.state(QuestState.LOCKED)
.state(QuestState.AVAILABLE)
```

## Common Patterns

### Simple Linear Quest
```python
quest = (QuestBuilder("tutorial_quest")
         .name("First Brew")
         .description("Craft your first potion")
         .craft_objective("healing_potion", 1)
         .build())
```

### Multi-Step Quest
```python
quest = (QuestBuilder("herb_delivery")
         .name("The Elder's Request")
         .description("Gather herbs and deliver them to the elder")
         .gather_objective("moonleaf", 20)
         .gather_objective("nightshade", 10)
         .deliver_objective("elder")
         .build())
```

### Quest Chain (Prerequisites)
```python
advanced_quest = (QuestBuilder("advanced_brewing")
                  .name("Advanced Techniques")
                  .description("Master advanced brewing")
                  .craft_objective("elixir", 5)
                  .require_quest("basic_brewing")
                  .require_quest("herb_lore")
                  .require_stat("knowledge", 50)
                  .build())
```

### Gated Quest (Locked Until Prerequisites Met)
```python
master_quest = (QuestBuilder("master_trial")
                .name("The Master's Trial")
                .description("Prove your mastery")
                .craft_objective("legendary_potion", 1)
                .duel_objective(10)
                .stat_objective("knowledge", 90)
                .require_quest("journeyman_quest")
                .require_stat("knowledge", 80)
                .require_stat("precision", 70)
                .require_affinity("guild_master", 3.0)
                .require_reputation("capital", 85)
                .state(QuestState.LOCKED)
                .build())
```

### Social Quest
```python
quest = (QuestBuilder("make_friends")
         .name("Winning Hearts")
         .description("Build relationships in town")
         .talk_objective("baker")
         .talk_objective("blacksmith")
         .talk_objective("innkeeper")
         .affinity_objective("merchant", 1.5)
         .affinity_objective("guard_captain", 1.0)
         .build())
```

### Economic Quest
```python
quest = (QuestBuilder("merchant_ambition")
         .name("Rise to Riches")
         .description("Build your fortune")
         .gold_objective(5000)
         .affinity_objective("merchant_guild", 2.0)
         .require_stat("business_acumen", 40)
         .build())
```

### Combat Quest
```python
quest = (QuestBuilder("tournament")
         .name("Arena Champion")
         .description("Win the tournament")
         .duel_objective(5)
         .stat_objective("combat_instinct", 70)
         .require_quest("training_complete")
         .build())
```

### Mixed Objectives Quest
```python
quest = (QuestBuilder("ultimate_challenge")
         .name("The Ultimate Test")
         .description("Prove yourself in all ways")
         .craft_objective("masterwork_potion", 3)
         .gather_objective("dragon_scale", 1)
         .duel_objective(10)
         .gold_objective(10000)
         .stat_objective("knowledge", 95)
         .stat_objective("combat_instinct", 85)
         .affinity_objective("king", 2.5)
         .require_quest("hero_of_village")
         .require_quest("master_alchemist")
         .require_reputation("kingdom", 90)
         .state(QuestState.LOCKED)
         .build())
```

## Build-Time Validation

The builder validates quests when `.build()` is called:

### Required Fields

```python
# Missing name
QuestBuilder("bad_quest")
    .description("Test")
    .craft_objective("x", 1)
    .build()
# ValueError: Quest bad_quest must have a name

# Missing description
QuestBuilder("bad_quest")
    .name("Bad Quest")
    .craft_objective("x", 1)
    .build()
# ValueError: Quest bad_quest must have a description

# Missing objectives
QuestBuilder("bad_quest")
    .name("Bad Quest")
    .description("Test")
    .build()
# ValueError: Quest bad_quest must have at least one objective
```

### Range Validation

```python
# Stat out of range (must be 0-100)
QuestBuilder("bad_quest")
    .name("Bad Quest")
    .description("Test")
    .craft_objective("x", 1)
    .require_stat("knowledge", 150)
    .build()
# ValueError: Stat requirement for knowledge must be 0-100, got 150

# Affinity out of range (must be -5.0 to 5.0)
QuestBuilder("bad_quest")
    .name("Bad Quest")
    .description("Test")
    .craft_objective("x", 1)
    .require_affinity("npc", 10.0)
    .build()
# ValueError: Affinity requirement for npc must be -5.0 to 5.0, got 10.0
```

## Best Practices

### 1. Use Descriptive Quest IDs
```python
# Good
QuestBuilder("village_healing_crisis")

# Bad
QuestBuilder("quest_1")
```

### 2. Custom Descriptions for Clarity
```python
# Auto-generated is fine for simple cases
.craft_objective("healing_potion", 5)  # "Craft 5x healing_potion"

# Custom for story/flavor
.craft_objective("healing_potion", 5, "Brew potions for the sick villagers")
```

### 3. Logical Prerequisite Ordering
```python
# Prerequisites should tell a story
(QuestBuilder("master_quest")
 .name("Master Alchemist")
 .description("Achieve mastery")
 .craft_objective("legendary_potion", 1)
 .require_quest("apprentice_quest")    # First
 .require_quest("journeyman_quest")    # Then
 .require_stat("knowledge", 80)        # Build skills
 .require_affinity("master", 2.0)      # Earn trust
 .build())
```

### 4. Lock High-Level Quests
```python
# Endgame quests should start LOCKED
(QuestBuilder("endgame_quest")
 .name("The Final Trial")
 .description("...")
 .craft_objective("ultimate_potion", 1)
 .require_quest("all_previous_quests")
 .state(QuestState.LOCKED)  # Player must unlock first
 .build())
```

### 5. Use Method Chaining Effectively
```python
# Good - readable groups
quest = (QuestBuilder("my_quest")
         .name("My Quest")
         .description("Description")

         # Objectives grouped
         .craft_objective("potion_a", 5)
         .craft_objective("potion_b", 3)
         .gather_objective("herb", 20)

         # Prerequisites grouped
         .require_quest("prev_quest")
         .require_stat("knowledge", 60)

         .build())

# Also fine - single line for simple quests
simple = QuestBuilder("simple").name("Simple").description("Desc").craft_objective("x", 1).build()
```

## Auto-Generated Features

### Objective IDs
Automatically assigned as `obj_0`, `obj_1`, `obj_2`, etc. in order added:

```python
quest = (QuestBuilder("my_quest")
         .name("Test")
         .description("Test")
         .craft_objective("a", 1)   # obj_0
         .gather_objective("b", 5)  # obj_1
         .talk_objective("c")       # obj_2
         .build())

# Access via quest.objectives[0].id == "obj_0"
```

### Default Descriptions
If no custom description provided, generates sensible defaults:

```python
.craft_objective("healing_potion", 5)
# description = "Craft 5x healing_potion"

.gather_objective("moonleaf", 20)
# description = "Gather 20x moonleaf"

.talk_objective("elder")
# description = "Talk to elder"

.stat_objective("knowledge", 80)
# description = "Reach knowledge level 80"

.affinity_objective("merchant", 2.0)
# description = "Reach 2.0 affinity with merchant"

.deliver_objective("elder")
# description = "Deliver item to elder"

.duel_objective(3)
# description = "Win 3 duel(s)"

.gold_objective(1000)
# description = "Earn 1000 gold"
```

### Default State
Quests default to `QuestState.AVAILABLE` unless explicitly set to `LOCKED`.

## Integration with QuestSystem

```python
from src.core.event_bus import EventBus
from src.quests.system import QuestSystem
from src.quests.builder import QuestBuilder

# Setup
bus = EventBus()
quest_system = QuestSystem(bus)

# Build quest
quest = (QuestBuilder("my_quest")
         .name("My Quest")
         .description("Complete objectives")
         .craft_objective("healing_potion", 5)
         .build())

# Use with system
player_state = {"knowledge": 50, "gold": 100}

success, reason = quest_system.start_quest(quest, "player_1", player_state)

if success:
    progress = quest_system.get_quest_progress(quest, player_state)
    print(f"{progress.objectives_complete}/{progress.objectives_total}")
```

## Comparison to Manual Construction

| Feature | Manual Quest() | QuestBuilder |
|---------|---------------|--------------|
| Objective IDs | Manual (`obj_0`, `obj_1`) | Auto-generated |
| Descriptions | Manual for each | Auto-generated or custom |
| Prerequisites | Dict syntax | Fluent methods |
| Validation | Runtime | Build-time |
| Readability | Verbose | Clean |
| Boilerplate | `progress={}`, `moral_choices=[]` | None |
| Error-prone | High (typos, indices) | Low (validated) |

## Testing with Builder

```python
import unittest
from src.quests.builder import QuestBuilder
from src.quests.data_structures import QuestState

class TestMyQuests(unittest.TestCase):
    def test_tutorial_quest(self):
        quest = (QuestBuilder("tutorial")
                 .name("Tutorial")
                 .description("Learn the basics")
                 .craft_objective("healing_potion", 1)
                 .build())

        self.assertEqual(quest.id, "tutorial")
        self.assertEqual(len(quest.objectives), 1)
        self.assertEqual(quest.state, QuestState.AVAILABLE)
```

Clean, simple, validated quest creation. That's the QuestBuilder philosophy.
