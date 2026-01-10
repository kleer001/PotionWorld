# PotionWorld - Arcade Prototype

**Season 0 MVP** - Phase 1: Foundation

A cozy alchemy RPG built with Python Arcade.

## Quick Start

```bash
# Make sure you're in the arcade_prototype directory
cd arcade_prototype

# Install dependencies
pip install arcade==3.3.3

# Run the game
python main.py
```

## Controls

- **WASD** or **Arrow Keys**: Move player
- **E**: Gather from nearby gathering spots
- **I**: Open inventory (coming soon)
- **P**: Debug - increase precision stat
- **ESC**: Menu (coming soon)

## What's Implemented (Phase 1)

✅ **Core Systems**:
- GameEvents: Event bus for decoupled communication
- GameState: Session state management
- PlayerData: Persistent player data (stats, inventory, relationships)
- SaveSystem: JSON-based save/load (not yet wired to UI)
- AudioManager: Music and SFX (placeholder - no audio files yet)

✅ **Gameplay**:
- Player movement (WASD)
- Gathering spots with respawn timers
- Ingredient collection
- Notification system
- Simple inventory tracking
- Camera following player

✅ **Entities**:
- Player character
- Gathering spots (4 types: mushrooms, berries, roots, sap)

## Project Structure

```
arcade_prototype/
├── main.py                  # Entry point
├── constants.py             # Game configuration
│
├── systems/                 # Core game systems
│   ├── game_events.py       # Event bus
│   ├── game_state.py        # State manager
│   ├── player_data.py       # Persistent data
│   ├── save_system.py       # Save/load
│   └── audio_manager.py     # Audio
│
├── entities/                # Game entities
│   ├── player.py            # Player character
│   └── gathering_spot.py    # Resource nodes
│
├── views/                   # Game screens
│   └── game_view.py         # Main gameplay
│
├── ui/                      # UI components
│   └── notification.py      # Toast notifications
│
├── resources/               # Data files (JSON)
│   └── ingredients.json     # (TODO)
│
└── assets/                  # Art and audio
    ├── sprites/             # (Placeholder)
    ├── audio/               # (Placeholder)
    └── fonts/               # (Placeholder)
```

## What's Next (Phase 2)

🔜 **Inventory UI**:
- Visual inventory panel
- Ingredient icons
- Sorting and filtering

🔜 **Dialogue System**:
- Named NPCs (Rachel, Ezekiel, Miriam, Thornwood)
- Dialogue boxes with choices
- Affinity tracking

🔜 **Crafting Minigame**:
- Tactile mortar & pestle interaction
- Recipe system
- Quality calculation

## Current Known Issues

- ⚠️ No audio files yet (AudioManager will fail gracefully)
- ⚠️ Using placeholder graphics (colored circles)
- ⚠️ Inventory UI not implemented yet
- ⚠️ Save/Load not wired to UI
- ⚠️ No main menu yet

## Architecture Notes

- **Traditional OOP**: No ECS complexity
- **Event-driven**: Systems communicate via GameEvents
- **Singleton patterns**: For global managers (GameState, PlayerData, etc.)
- **Composition**: Player has systems, not inheritance
- **All Python**: 100% code-based, no editor required

## Development

This prototype follows the transition plan from Godot to Arcade. Key advantages:

- ✅ Native Python (direct ESENS parser integration)
- ✅ 100% code-based (no scene editor)
- ✅ Faster iteration (just run `python main.py`)
- ✅ Traditional OOP (simpler than ECS)
- ✅ Easy debugging

## Testing

Walk around the garden and gather ingredients. You should see:
- Notifications when gathering
- Ingredient counts in top-left
- Stats display in bottom-left
- Yellow circles around interactable spots
- Spots turn gray when depleted and respawn after 5 minutes

## Credits

- **Game Engine**: Python Arcade 3.3.3
- **Game Design**: Based on PROTOTYPE_A_PRODUCTION_GUIDE.md
- **Architecture**: See GODOT_TO_ARCADE_TRANSITION_PLAN.md
