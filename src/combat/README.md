# Combat System

Phase 3 implementation of PotionWorld's turn-based combat system following the Hybrid API + Event Architecture.

## Features

- **Turn-Based Combat**: Strategic potion usage in combat encounters
- **ESENS-Driven Effects**: Potions apply damage, healing, buffs, and debuffs via ESENS notation
- **Status Effect Management**: Stackable/non-stackable effects with duration tracking
- **Trigger System**: Effects that activate at specific phases (start/end turn, on attack/defend)
- **Personality-Based AI**: NPCs make combat decisions based on Big 5 personality traits
- **Event-Driven**: Emits events for cross-system integration (progression, quests, economy)

## Architecture

### Core Components

1. **Formulas** (`formulas.py`): Pure functions for combat mechanics
   - Damage calculation with strength/defense modifiers
   - Status effect application and stacking
   - Trigger evaluation and phase matching
   - Duration tracking and expiration
   - AI decision-making based on personality
   - Simple ESENS parsing for combat effects

2. **System** (`system.py`): CombatSystem API with event emission
   - `execute_turn()` - Main combat turn execution
   - `create_ai_action()` - AI opponent decision making
   - Event emission for all combat actions
   - Integration with event bus

3. **Tests** (`tests/`): Comprehensive test coverage
   - Formula validation
   - System integration tests
   - Event emission verification
   - AI behavior testing

4. **Testbed** (`testbed.py`): Interactive CLI for testing
   - Live combat simulation
   - Health bars and status display
   - AI opponent with personality
   - Built-in test runner

## Quick Start

### Run the Testbed

```bash
python systest.py --combat
```

Or directly:
```bash
python -m src.combat.testbed
```

### Run Tests

```bash
python -m src.combat.tests.test_formulas
python -m src.combat.tests.test_system
```

### Basic Usage

```python
from src.core.event_bus import EventBus
from src.core.data_structures import *
from src.combat.system import CombatSystem

bus = EventBus()
combat = CombatSystem(bus)

player = Combatant(
    id="player",
    name="Player",
    stats=CombatStats(
        health=100,
        max_health=100,
        strength=50,
        defense=30,
        initiative=10,
        resistance=5
    ),
    active_effects=[],
    combat_belt=[damage_potion, heal_potion],
    personality=None
)

enemy = Combatant(
    id="enemy",
    name="Dark Alchemist",
    stats=CombatStats(health=80, max_health=80, strength=40, defense=25, ...),
    active_effects=[],
    combat_belt=[enemy_potions],
    personality=Personality(O=1, C=0, E=1, A=-1, N=0)
)

action = CombatAction(action_type="USE_POTION", potion=damage_potion)

result = combat.execute_turn("combat_1", 1, player, action, enemy)

print(f"Victor: {result.victor}")
for change in result.changes:
    print(change)
```

## Events

The combat system emits the following events:

- `TurnExecuted`: Every turn execution
- `DamageDealt`: When damage is dealt to a combatant
- `StatusApplied`: When status effects are applied
- `TriggerActivated`: When triggers fire (start/end turn, etc.)
- `CombatEnded`: When combat concludes with a victor

## Combat Mechanics

### Damage Calculation

```
modified_damage = base_damage × (1 + attacker_strength / 100)
damage_reduction = defender_defense / 100
final_damage = modified_damage × (1 - damage_reduction)
minimum = 1 damage
```

Example:
```python
# Attacker: 50 strength, Base: 20 damage
# Defender: 30 defense
# Result: 20 × 1.5 × 0.7 = 21 damage
```

### Status Effects

Status effects modify combatant stats temporarily:

**Stackable Effects**: Multiple instances accumulate
- Strength Boost × 2 = both bonuses apply
- Used for buffs that should compound

**Non-Stackable Effects**: Latest replaces previous
- Shield effect updates to newest
- Used for exclusive states

**Effect Modifiers**:
- `modifier > 1.0`: Buff (e.g., 1.3 = +30%)
- `modifier < 1.0`: Debuff (e.g., 0.7 = -30%)

**Duration**:
- `n > 0`: Decreases each turn, removed at 0
- `-1`: Permanent, never expires
- `0`: Immediate/instant effect

### Trigger System

Triggers activate effects at specific combat phases:

- `^S`: Start of turn
- `vE`: End of turn
- `>A`: On attack
- `<D`: On defend
- `>Sprd`: On spread/area effect

Example:
```python
# Regeneration: heals at start of each turn
trigger = Trigger("^S", "P+H10")
regen = StatusEffect(
    name="Regeneration",
    triggers=[trigger],
    duration=5
)
```

### Actions

**USE_POTION**: Apply potion effects
- Damage potions target opponent
- Healing/buff potions target self
- Consumes potion from combat belt

**GUARD**: Defensive stance
- +50% defense for 1 turn
- Useful when low on potions

**OBSERVE**: Skip turn
- No effect, useful for testing
- AI rarely chooses this

## AI Decision Making

AI chooses potions based on personality and situation:

### Personality Influences

**Extraversion (+)**: Prefers aggressive damage
```python
if personality.extraversion > 0:
    damage_score *= 1.5
```

**Agreeableness (+)**: Prefers defensive/healing
```python
if personality.agreeableness > 0:
    defensive_score *= 1.3
```

**Neuroticism (+)**: Panic when low health
```python
if health < 30% and neuroticism > 0:
    healing_score *= 2.0
```

**Openness (+)**: Likes complex status effects
```python
if personality.openness > 0:
    status_effect_score += 20
```

**Conscientiousness (+)**: Consistent best choice
```python
if personality.conscientiousness > 0:
    return best_potion
else:
    return weighted_random_potion
```

## ESENS Combat Effects

The system parses simple ESENS notation for combat:

### Damage Effects
- `E#Damage30`: Deal 30 base damage to enemy
- `E-H25`: Reduce enemy health by 25

### Healing Effects
- `P+H20`: Restore 20 health to self
- `P+H50`: Restore 50 health to self

### Buff Effects
- `P+S30%3T`: +30% strength for 3 turns
- `P+D25%2T`: +25% defense for 2 turns

### Debuff Effects
- `E-S20%2T`: Enemy -20% strength for 2 turns
- `E-D30%3T`: Enemy -30% defense for 3 turns

## Testbed Commands

```
1-4        - Use potion from belt
guard      - Boost defense (+50% this turn)
observe    - Skip turn
status     - Show detailed combat stats
events     - Show recent events
test       - Run validation tests
reset      - Reset combat
help       - Show help
quit       - Exit
```

## Example Testbed Session

```
COMBAT TESTBED
==============================================================

Turn 1
--------------------------------------------------------------

Player
  HP: [██████████████████████████████] 100/100

Dark Alchemist
  HP: [██████████████████████████████] 100/100

Your Potions:
  1. fire_blast      - E#Damage30
  2. healing         - P+H25
  3. strength_boost  - P+S30%3T
  4. weaken          - E-D25%2T

[Turn 1] > 1

>>> Player's turn
    Player dealt 27 damage to Dark Alchemist

>>> Dark Alchemist's turn
    Uses shadow_strike
    Dark Alchemist dealt 22 damage to Player

Turn 2
--------------------------------------------------------------

Player
  HP: [███████████████████████░░░░░░░] 78/100

Dark Alchemist
  HP: [██████████████████████░░░░░░░░] 73/100

[Turn 2] > 3

>>> Player's turn
    Player gains Enhanced Strength for 3 turns

>>> Dark Alchemist's turn
    Uses dark_heal
    Dark Alchemist restored 20 health
```

## Integration Examples

### Progression System
```python
class ProgressionSystem:
    def __init__(self, event_bus):
        event_bus.subscribe(CombatEnded, self.on_combat_ended)

    def on_combat_ended(self, event):
        if event.winner_id == "player":
            xp = 100 + (20 - event.turn_count) * 5
            self.add_xp("player", "combat_instinct", xp)
```

### Quest System
```python
class QuestSystem:
    def __init__(self, event_bus):
        event_bus.subscribe(CombatEnded, self.on_combat_ended)

    def on_combat_ended(self, event):
        if event.winner_id == "player":
            self.update_objective("defeat_alchemists", progress=+1)
```

### Economy System
```python
class EconomySystem:
    def __init__(self, event_bus):
        event_bus.subscribe(CombatEnded, self.on_combat_ended)

    def on_combat_ended(self, event):
        if event.winner_id == "player":
            loot = calculate_loot(event.turn_count)
            self.add_gold("player", loot)
```

## Design Principles

Following SOLID, DRY, and KISS principles:

- **Single Responsibility**: Each function does one thing
- **Pure Functions**: No side effects in formulas
- **Event-Driven**: Loose coupling through events
- **Testable**: All logic has comprehensive tests
- **Clean Code**: Self-documenting, no unnecessary comments

## Success Criteria

✅ **Turn structure flows correctly** - Start triggers → action → end triggers → durations
✅ **Damage calculation works** - Strength/defense modifiers apply correctly
✅ **Status effects apply/stack properly** - Stackable and non-stackable flags work
✅ **Triggers fire at correct times** - Phase matching works for ^S, vE, >A, <D
✅ **Durations update properly** - Effects expire at 0, permanent effects persist
✅ **AI makes personality-based choices** - Different personalities show distinct behavior
✅ **Combat feels strategic** - Player choices matter
✅ **Events integrate with other systems** - XP, quests, economy can react
✅ **Testbed validates all mechanics** - Can play full combat manually
