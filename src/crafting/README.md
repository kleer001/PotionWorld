# Crafting System

Phase 1 implementation of PotionWorld's potion crafting system following the Hybrid API + Event Architecture.

## Features

- **Pure Logic**: Testable success formulas, quality determination, XP/mastery calculations
- **Event-Driven**: Emits events for cross-system integration (progression, inventory, quests)
- **Comprehensive Testing**: Unit tests for formulas and system behavior
- **Interactive Testbed**: CLI tool for testing and validation

## Architecture

### Core Components

1. **Formulas** (`formulas.py`): Pure functions for all game mechanics
   - Success chance calculation
   - D20 dice rolling with critical hits/failures
   - Quality determination based on success margin
   - Potency multipliers
   - XP rewards and mastery progression

2. **System** (`system.py`): CraftingSystem API with event emission
   - Main `craft()` API
   - Event emission for all state changes
   - Integration with event bus

3. **Tests** (`tests/`): Comprehensive test coverage
   - Formula validation
   - System integration tests
   - Event emission verification

4. **Testbed** (`testbed.py`): Interactive CLI for testing
   - God mode stat manipulation
   - Single craft with detailed breakdown
   - Batch crafting with statistics
   - Built-in test runner

## Quick Start

### Run the Testbed

```bash
python systest.py --crafting
```

Or directly:
```bash
python -m src.crafting.testbed
```

### Run Tests

```bash
python -m src.crafting.tests.test_formulas
python -m src.crafting.tests.test_system
```

### Basic Usage

```python
from src.core.event_bus import EventBus
from src.core.data_structures import *
from src.crafting.system import CraftingSystem

bus = EventBus()
crafting = CraftingSystem(bus)

recipe = Recipe(
    id="healing_potion",
    name="Healing Potion",
    difficulty=30,
    esens="H[+10]",
    base_potency=1.0,
    ingredients=["herb"]
)

input = CraftInput(
    recipe=recipe,
    ingredients=[IngredientInstance("herb_1", "herb", Quality.STANDARD)],
    crafter_stats=CrafterStats(knowledge=50, precision=40, intuition=30),
    tool_bonus=0.1
)

result = crafting.craft(input, crafter_id="player", current_mastery=0)

if result.success:
    print(f"Created {result.potion.quality.name} potion!")
    print(f"Potency: {result.potion.potency:.1%}")
```

## Events

The crafting system emits the following events:

- `CraftCompleted`: Every craft attempt (success or failure)
- `PotionCreated`: When potion successfully created
- `RecipeMasteryGained`: When recipe mastery increases
- `XPGained`: For each stat that gains XP
- `IngredientsConsumed`: When ingredients are used

## Testbed Commands

```
stats <K> <P> <I>    - Set crafter stats (god mode)
tool <bonus>         - Set tool bonus (0.0-0.3)
mastery <recipe> <n> - Set recipe mastery (god mode)
craft <recipe>       - Craft once with breakdown
batch <recipe> <n>   - Craft N times, show stats
recipes              - List available recipes
test                 - Run validation tests
events               - Show recent events
help                 - Show help
quit                 - Exit
```

## Formula Details

### Success Chance

```
Base: 50%
+ Knowledge/2 (0-50%)
+ Tool Bonus (0-30%)
+ Mastery Bonus (0-20%)
- Recipe Difficulty (0-100%)
+ D20 Roll modifier
```

Critical rolls:
- Natural 1: Always fails
- Natural 20: Always succeeds

### Quality Tiers

1. **Poor**: 75% potency
2. **Standard**: 100% potency
3. **Fine**: 110% potency
4. **Exceptional**: 125% potency
5. **Masterwork**: 150% potency

Quality determined by:
- Success margin (how much you beat the threshold)
- Ingredient quality (poor ingredients can downgrade)
- Precision (80+ has 20% chance to upgrade)

### XP Rewards

Base XP = Recipe Difficulty

Success multipliers:
- Poor: 0.8x
- Standard: 1.0x
- Fine: 1.2x
- Exceptional: 1.5x
- Masterwork: 2.0x

Failure: 10% knowledge, 5% intuition

### Mastery Progression

Gain per craft:
- Failure: +1
- Poor success: +3
- Standard: +5
- Fine: +8
- Exceptional: +12
- Masterwork: +15

Mastery bonuses:
- 0-24: No bonus
- 25-49: +10% success
- 50-74: +15% success
- 75-100: +20% success

## Design Principles

Following SOLID, DRY, and KISS principles:

- **Single Responsibility**: Each function does one thing
- **Pure Functions**: No side effects in formulas
- **Event-Driven**: Loose coupling through events
- **Testable**: All logic has comprehensive tests
- **Clean Code**: Self-documenting, no unnecessary comments
