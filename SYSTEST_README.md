# System Testbed Launcher

PotionWorld's unified launcher for all system testbeds.

## Usage

```bash
python systest.py --<system>
```

## Available Systems

### Phase 1 (Complete)
- `--crafting` - Potion crafting system testbed ✓

### Phase 2 (Complete)
- `--relationship` - NPC relationship and affinity ✓

### Coming Soon
- `--progression` - Character stat progression (Phase 3)
- `--quest` - Quest and objective tracking (Phase 3)
- `--combat` - Turn-based potion combat (Phase 4)
- `--economy` - Pricing and market dynamics (Phase 4)
- `--inventory` - Item storage and freshness (Phase 5)

## Examples

Launch crafting testbed:
```bash
python systest.py --crafting
```

View all options:
```bash
python systest.py --help
```

## Adding New Systems

When implementing a new system:

1. Create the testbed in `src/<system>/testbed.py`
2. Add the flag to `systest.py`
3. Import and launch in the appropriate elif block

Example:
```python
elif args.progression:
    from src.progression.testbed import ProgressionTestbed
    testbed = ProgressionTestbed()
    testbed.run()
```

## Why This Approach?

- **Simple**: One command for all systems
- **Consistent**: Same pattern for every testbed
- **Discoverable**: `--help` shows all options
- **Scalable**: Easy to add new systems
- **No path issues**: Works from project root
