# Relationship System

Phase 2 implementation of PotionWorld's NPC relationship system following the Hybrid API + Event Architecture.

## Features

- **Big 5 Personality Model**: NPCs react differently based on personality traits
- **Affinity Tracking**: Range from -5 (Nemesis) to +5 (Devoted)
- **Memory System**: Significant events create lasting memories that resist decay
- **Time Decay**: Relationships naturally decay toward neutral without interaction
- **Threshold Events**: Cross affinity levels to unlock new interactions
- **Event-Driven**: Emits events for cross-system integration (quests, economy, dialogue)

## Architecture

### Core Components

1. **Formulas** (`formulas.py`): Pure functions for relationship mechanics
   - Personality-based reaction calculation
   - Time-based affinity decay
   - Memory resistance to decay
   - Threshold detection

2. **System** (`system.py`): RelationshipSystem API with event emission
   - `apply_action()` - Apply NPC interaction
   - `apply_time_decay()` - Process time-based decay
   - Event emission for all relationship changes

3. **Tests** (`tests/`): Comprehensive test coverage
   - Formula validation
   - System integration tests
   - Event emission verification

4. **Testbed** (`testbed.py`): Interactive CLI for testing
   - Apply actions to NPCs
   - Advance time and observe decay
   - View memories and affinity levels
   - Built-in scenario tests

## Quick Start

### Run the Testbed

```bash
python systest.py --relationship
```

Or directly:
```bash
python -m src.relationships.testbed
```

### Run Tests

```bash
python -m src.relationships.tests.test_formulas
python -m src.relationships.tests.test_system
```

### Basic Usage

```python
from src.core.event_bus import EventBus
from src.core.data_structures import NPC, Personality, Action
from src.relationships.system import RelationshipSystem

bus = EventBus()
relationships = RelationshipSystem(bus)

npc = NPC(
    id="thornwood",
    name="Instructor Thornwood",
    personality=Personality(
        openness=-1,
        conscientiousness=1,
        extraversion=0,
        agreeableness=-1,
        neuroticism=0
    )
)

action = Action(
    id="innovative",
    name="Show innovative potion",
    personality_impacts={"O": 1.0, "E": 0.5}
)

result = relationships.apply_action(npc, action, current_day=1)

print(f"Affinity change: {result.delta:+.1f}")
print(f"New affinity: {result.new_affinity:+.1f}")
```

## Events

The relationship system emits the following events:

- `AffinityChanged`: When any action affects affinity
- `ThresholdCrossed`: When crossing integer affinity boundaries
- `MemoryCreated`: When significant events create memories
- `RelationshipDecayed`: When time causes affinity to decay

## Personality System

NPCs have Big 5 personality traits, each ranging from -1 to +1:

### Openness (O)
- **+1**: Innovative, creative, curious
- **-1**: Traditional, conservative, practical

### Conscientiousness (C)
- **+1**: Meticulous, organized, careful
- **-1**: Casual, spontaneous, flexible

### Extraversion (E)
- **+1**: Outgoing, social, energetic
- **-1**: Introverted, reserved, quiet

### Agreeableness (A)
- **+1**: Cooperative, compassionate, trusting
- **-1**: Competitive, skeptical, direct

### Neuroticism (N)
- **+1**: Anxious, sensitive, cautious
- **-1**: Stable, calm, confident

## Reaction Calculation

When you perform an action, the NPC's reaction is calculated by:

```
delta = Σ(personality_trait × action_impact)
```

Example:
```python
# Innovative action
action = Action("innovate", "Show innovation", {"O": 1.0, "E": 0.5})

# Traditional NPC (O=-1)
# delta = (-1 × 1.0) + (0 × 0.5) = -1.0

# Innovative NPC (O=+1, E=+1)
# delta = (1 × 1.0) + (1 × 0.5) = +1.5
```

## Affinity Levels

Affinity ranges from -5 to +5:

- **+5**: Devoted - Would sacrifice for you
- **+4**: Loyal - Actively supports you
- **+3**: Friendly - Helps willingly, discounts
- **+2**: Warm - Positive interactions
- **+1**: Positive - Slightly favorable
- **0**: Neutral - Professional, transactional
- **-1**: Cool - Mild dislike
- **-2**: Unfriendly - Reluctant, price increases
- **-3**: Hostile - May refuse service
- **-4**: Antagonistic - Works against you indirectly
- **-5**: Nemesis - Actively sabotages you

## Memory System

Significant interactions (|delta| ≥ 1.0) create memories that:
- Persist across game sessions
- Resist affinity decay
- Have decay resistance = min(1.0, |delta| / 2.0)

Example:
```python
# Major favor: delta = +2.0
# Creates memory with 1.0 (100%) decay resistance

# Minor favor: delta = +0.5
# No memory created (below threshold)
```

## Time Decay

Without interaction, affinity gradually returns to neutral:

```
decay_per_week = 0.5
```

Memories reduce decay proportionally to their resistance:
```python
# No memories: 3.0 → 2.5 after 1 week
# 50% resistance: 3.0 → 2.75 after 1 week
# 100% resistance: 3.0 → 3.0 (no decay)
```

## Testbed Commands

```
apply <npc> <action>  - Apply action to NPC
time <days>           - Advance time and apply decay
npcs                  - List all NPCs with personalities
actions               - List available actions
memories <npc>        - Show NPC's memories
test                  - Run scenario tests
events                - Show recent events
help                  - Show help
quit                  - Exit
```

## Example Testbed Session

```
> npcs
thornwood: Instructor Thornwood (O:-1, C:+1, E:0, A:-1, N:0)
wisteria: Healer Wisteria (O:0, C:+1, E:-1, A:+1, N:-1)
kael: Rival Kael (O:+1, C:0, E:+1, A:-1, N:0)

> apply thornwood traditional
Applying 'Follow traditional method' to Instructor Thornwood
Openness:          -1 × -0.5 = +0.5
Conscientiousness: +1 × +0.5 = +0.5
Delta: +1.0

Result: Affinity 0.0 → +1.0
⚠️  THRESHOLD CROSSED: +1

> time 7
Advancing 7 days...
Thornwood: +1.0 → +0.5 (decay)
```

## Integration Examples

### Quest System
```python
class QuestSystem:
    def __init__(self, event_bus):
        event_bus.subscribe(ThresholdCrossed, self.on_threshold)

    def on_threshold(self, event):
        if event.new_level >= 3:
            self.unlock_quest(f"friendship_{event.npc_id}")
```

### Economy System
```python
class EconomySystem:
    def calculate_price(self, item, npc_affinity):
        base_price = item.value
        affinity_modifier = 1.0 - (npc_affinity / 20.0)
        return base_price * affinity_modifier
```

## Design Principles

Following SOLID, DRY, and KISS principles:

- **Single Responsibility**: Each function does one thing
- **Pure Functions**: No side effects in formulas
- **Event-Driven**: Loose coupling through events
- **Testable**: All logic has comprehensive tests
- **Clean Code**: Self-documenting, no unnecessary comments
