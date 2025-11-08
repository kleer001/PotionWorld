# Configuration Files

PotionWorld uses .ini files for high-level game balance tuning without code changes.

## Files

### `progression.ini`

Controls all progression system parameters:

**XP Curve:**
- `max_xp` - Maximum XP value (default: 100000)
- `max_stat` - Maximum stat value (default: 100)
- `curve_scale` - Logarithmic curve scaling (default: 40)
- `curve_offset` - Logarithmic curve offset (default: 100)

Formula: `stat = curve_scale * log10(xp) - curve_offset`

**Mastery Gains:**
- `failure` through `masterwork` - Mastery points per craft quality

**Mastery Diminishing Returns:**
- `threshold_high` / `threshold_mid` - Where gains reduce
- `multiplier_high` / `multiplier_mid` - Reduction multipliers

**Mastery Bonuses:**
- Success/quality bonuses at each mastery level
- Waste reduction percentage

**Reputation:**
- Thresholds for Known/Respected/Renowned/Legendary
- Price modifiers per reputation level
- Quest access tiers
- NPC initial affinity bonuses

**Specializations:**
- Each specialization has its own section
- `prereq_*` - Stat prerequisites
- `bonus_*` - Bonuses granted
- Supports int, float, and boolean values

## Making Changes

1. Edit the .ini file
2. Restart the game/testbed
3. No code changes needed
4. All formulas automatically use new values

## Example: Rebalancing XP Curve

Want faster early progression?

```ini
[XP_Curve]
curve_scale = 50  # Was 40 - makes early levels faster
curve_offset = 80 # Was 100 - lowers the floor
```

## Example: New Specialization

Add to `progression.ini`:

```ini
[Specializations.AlchemistSupreme]
category = crafting
prereq_knowledge = 80
prereq_precision = 80
bonus_knowledge = 10
bonus_precision = 10
bonus_quality_bonus = 0.20
```

Then update `formulas.py` to load it.

## Fallback Values

All config values have hardcoded defaults in `config.py`. If the .ini file is missing or malformed, the system falls back to defaults automatically.
