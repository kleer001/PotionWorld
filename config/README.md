# Configuration Files

PotionWorld uses .ini files for high-level game balance tuning without code changes.

## Philosophy

Only **essential balance knobs** that playtesters need. Not every magic number - just the ones that affect game feel.

## Files

### `crafting.ini`

**Success_Chance:**
- Base chance and stat modifiers
- Critical roll values (natural 1/20)

**Quality_Thresholds:**
- Margins for each quality tier

**XP_Rewards:**
- Failure XP percentages
- Quality multipliers

### `relationships.ini`

**Affinity:**
- Min/max affinity bounds

**Memory:**
- Significance threshold (when memories form)
- Decay resistance calculation

**Decay:**
- Time-based affinity decay rate

### `combat.ini`

**Damage:**
- Strength/defense divisors
- Minimum damage floor

**AI_Personality:**
- Personality trait multipliers for AI decisions

### `economy.ini`

**Base_Prices:**
- Ingredient prices by rarity

**Potion_Pricing:**
- Base multiplier and difficulty scaling

**Quality_Multipliers:**
- Price modifiers per quality tier

**Market:**
- Supply/demand min/max bounds
- Decay rates

**Bulk_Discounts:**
- Quantity thresholds and discount percentages

**Combat_Rewards:**
- Base reward and bonus calculations

### `progression.ini`

**XP_Curve:**
- Logarithmic curve parameters

**Mastery:**
- Gains per quality tier
- Diminishing returns thresholds

**Reputation:**
- Thresholds and modifiers

**Specializations:**
- Prerequisites and bonuses

## Making Changes

1. Edit the .ini file
2. Restart the game/testbed
3. Changes apply immediately
4. All formulas use new values automatically

## Example: Easier Crafting

Make crafting more forgiving for early players:

```ini
[Success_Chance]
base_chance = 0.6        # Was 0.5 - +10% success
difficulty_divisor = 120.0  # Was 100.0 - reduces penalty
```

## Example: Faster Relationships

Speed up relationship building:

```ini
[Decay]
decay_per_week = 0.3     # Was 0.5 - slower decay

[Memory]
significance_threshold = 0.8  # Was 1.0 - easier to create memories
```

## Fallback Values

All config values have hardcoded defaults. If .ini files are missing or malformed, systems fall back to defaults automatically.

## Playtester Workflow

1. Playtest and identify balance issues
2. Designer edits relevant .ini section
3. Playtesters restart and verify
4. Iterate until balanced

No code changes. No recompilation. Pure data-driven tuning.
