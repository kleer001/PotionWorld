# PotionWorld - Godot 4.2 Implementation

This folder contains the complete Godot 4.2 implementation of PotionWorld's GUI MVP (Season 0 Demo).

## 🚀 Quick Start

### Prerequisites
- **Godot 4.2** (stable) - [Download here](https://godotengine.org/download)
- **Python 3.8+** - For ESENS parser
- **Git** - For version control

### Opening the Project

1. Launch Godot 4.2
2. Click "Import"
3. Navigate to this `godot/` folder
4. Select `project.godot`
5. Click "Import & Edit"

### First Time Setup

The project will import assets automatically. This may take a few minutes on first load.

**Required Addons:**
- [ ] Dialogue Manager plugin - Install from Asset Library or [GitHub](https://github.com/nathanhoad/godot_dialogue_manager)

---

## 📁 Project Structure

```
godot/
├── project.godot           # Main project configuration
├── .gitignore             # Git ignore rules
│
├── autoload/              # Singleton systems (globally accessible)
│   ├── GameEvents.gd      # Event bus for global signals
│   ├── GameState.gd       # Current game state & session data
│   ├── PlayerData.gd      # Player stats, inventory, relationships
│   ├── SaveSystem.gd      # Save/load manager
│   └── AudioManager.gd    # Music & SFX controller
│
├── scenes/                # All .tscn scene files
│   ├── main/              # Root scenes (Main, MainMenu)
│   ├── locations/         # Playable locations (Garden, Dorm, etc.)
│   ├── characters/        # Player and NPC character scenes
│   ├── ui/                # UI components (HUD, Inventory, Journal, etc.)
│   └── minigames/         # Crafting minigame components
│
├── scripts/               # Pure GDScript logic (no scene nodes)
│   ├── data/              # Data structure definitions
│   ├── systems/           # Game system implementations
│   └── utils/             # Helper functions and constants
│
├── resources/             # Custom Resource classes
│   ├── ingredients/       # IngredientResource.gd + data files
│   ├── recipes/           # RecipeResource.gd + data files
│   ├── npcs/              # NPCResource.gd + data files
│   ├── dialogue/          # Dialogue Manager files
│   └── save/              # SaveData.gd
│
├── data/                  # JSON/CSV game data
│   ├── ingredients.json   # All ingredient definitions
│   ├── recipes.json       # All recipe definitions
│   ├── npcs.json          # NPC personality data
│   ├── choices.json       # Dialogue choice consequences
│   └── dialogue/          # .dialogue files for Dialogue Manager
│
├── assets/                # Art, audio, fonts
│   ├── art/               # All visual assets
│   ├── audio/             # Music and SFX
│   └── fonts/             # Text fonts
│
├── addons/                # Third-party plugins
│   └── dialogue_manager/  # Dialogue Manager plugin
│
├── python/                # Python scripts (ESENS parser)
│   ├── ESENS_Parser.py    # Core ESENS notation parser
│   ├── esens_godot_wrapper.py  # Godot integration wrapper
│   └── ESENS_README.md    # Parser documentation
│
└── exports/               # Build outputs (gitignored)
```

---

## 🎮 Controls

### Keyboard & Mouse
- **WASD** / **Arrow Keys** - Move player
- **E** / **Space** - Interact with objects/NPCs
- **I** / **Tab** - Open inventory
- **J** - Open journal
- **Esc** - Pause menu

### Gamepad
- **Left Stick** - Move player
- **A Button** (Xbox) / **X** (PlayStation) - Interact
- **Y Button** (Xbox) / **Triangle** (PlayStation) - Inventory
- **X Button** (Xbox) / **Square** (PlayStation) - Journal
- **Start** - Pause menu

---

## 🏗️ Architecture Overview

### Autoload Singletons

PotionWorld uses Godot's autoload system for globally accessible managers:

1. **GameEvents** - Event bus (publish/subscribe pattern)
   - All systems emit signals here
   - Decouples systems (UI doesn't need reference to inventory)

2. **GameState** - Current session state
   - What scene we're in
   - What phase of gameplay (dialogue, crafting, etc.)
   - Input restrictions based on context

3. **PlayerData** - Persistent player data
   - Stats, inventory, relationships
   - All saveable data lives here

4. **SaveSystem** - Save/load management
   - Resource-based saves (.tres format)
   - Auto-save + manual save slots

5. **AudioManager** - Audio playback
   - Music transitions
   - SFX pooling
   - Reacts to game events

### Event-Driven Communication

Systems communicate via signals emitted through **GameEvents**:

```gdscript
# Example: Gathering an ingredient
PlayerData.add_ingredient("common_mushroom", 3)
# → Emits: GameEvents.ingredient_gathered("common_mushroom", 3)
# → AudioManager plays gather SFX
# → InventoryUI refreshes display
# → NotificationManager shows popup
```

### Resource-Based Data

All game content is defined as Resources:
- **IngredientResource** - Each ingredient type
- **RecipeResource** - Each craftable potion
- **NPCResource** - Each character with Big 5 personality
- **SaveData** - Player save file

Resources are loaded from `data/` or `resources/` folders.

---

## 🎨 Isometric Setup

### Stardew-Style 3/4 Perspective

- **NOT** pure isometric (2:1 diamond)
- Uses 3/4 overhead perspective (like Stardew Valley)
- Easier for character animation
- More forgiving depth sorting

### Y-Sorting Configuration

**Critical for proper depth rendering:**

All visual elements must have **Y Sort Enabled**:
- Environment root node: Y Sort ✓
- Each TileMapLayer: Y Sort ✓
- All Sprite2D nodes: Y Sort ✓
- Character nodes: Y Sort ✓

**Character Origin Point:**
- Must be at FEET, not center
- `CharacterBody2D.position` = ground level
- `Sprite2D` offset above feet

### TileMap Layers

Locations use multiple TileMapLayers for depth:
1. **Ground** - Floor tiles
2. **Walls** - Vertical structures
3. **Decoration** - Furniture, plants
4. **Characters** - Player + NPCs (not tilemap)

---

## 🗣️ Dialogue System

Uses **Dialogue Manager** plugin for branching conversations.

### Dialogue Files

Located in `data/dialogue/`, written in Dialogue Manager format:

```
~ first_meeting

Rachel: Oh! You're here! Hi! I'm Rachel!
[setExpression rachel excited]

- Let's explore together!
    [addAffinity rachel 0.5]
    Rachel: Really?! Yes! Come on!
    => go_to_garden

- I'll unpack first
    Rachel: Oh, of course! Take your time!
    => end
```

### Custom Functions

Custom functions in `autoload/DialogueManagerFunctions.gd`:
- `addAffinity(npc_id, amount)` - Change relationship
- `unlock_trait(trait_name)` - Unlock player trait
- `has_trait(trait_name)` - Check if player has trait
- `setExpression(npc_id, expression)` - Change portrait

### Big 5 Integration

NPCs have personality traits that affect dialogue:
- Openness (-1, 0, +1)
- Conscientiousness (-1, 0, +1)
- Extraversion (-1, 0, +1)
- Agreeableness (-1, 0, +1)
- Neuroticism (-1, 0, +1)

Dialogue can branch based on these traits and player choices.

---

## ⚗️ Crafting System

### ESENS Parser Integration

The Python ESENS parser is called from Godot via `OS.execute()`:

```gdscript
# scripts/systems/ESENSParser.gd
var output = []
var notation = "P+H30%10s.ST"
OS.execute("python3",
    ["res://python/esens_godot_wrapper.py", notation],
    output, true)

var json = JSON.parse_string(output[0])
# Returns: {success: true, notation: "...", effects: {...}}
```

### Crafting Minigame

Full tactile interaction:
1. **Grind** - Circular mouse motion (3 circles)
2. **Add Sap** - Drag ingredient to mortar
3. **Add Berries** - Drag berries one by one
4. **Decant** - Tilt mortar to pour into vial

Quality determined by:
- Smoothness of grinding
- Timing accuracy
- Player's Precision stat

---

## 💾 Save System

### Resource-Based Saves

Uses Godot's Resource system (not JSON):
- Simpler (one function call)
- Type-safe (handles Vector2, Color, etc.)
- Compact binary format

### Save Locations

```
user://saves/
├── autosave.tres           # Auto-save
├── manual_1.tres           # Manual slot 1
├── manual_2.tres           # Manual slot 2
└── manual_3.tres           # Manual slot 3
```

On **Windows**: `%APPDATA%\Godot\app_userdata\PotionWorld\saves\`
On **macOS**: `~/Library/Application Support/Godot/app_userdata/PotionWorld/saves/`
On **Linux**: `~/.local/share/godot/app_userdata/PotionWorld/saves/`

### Auto-Save Triggers

Automatic saves occur:
- Scene transitions
- After crafting a potion
- After major dialogue choices
- Every 5 minutes (planned)

---

## 🧪 Testing

### Running the Game

Press **F5** or click the **Play** button in Godot editor.

### Debug Tools

Built-in debug features:
- Press **F3** for FPS counter
- Press **F4** for performance monitor
- Console outputs game events

### Unit Testing

(Planned for later phases)

---

## 📦 Exporting

### PC Builds (Windows/Mac/Linux)

1. Project → Export
2. Select platform preset
3. Export with Debug (for testing)
4. Builds output to `exports/`

### Web Export (HTML5)

**Note:** Python ESENS parser won't work in web builds. For web export, the ESENS parser must be ported to GDScript.

Web export settings:
- Export Type: Regular
- Test locally before deploying

---

## 🐛 Troubleshooting

### "Autoload scripts not found"

Check Project → Project Settings → Autoload and verify paths:
- `res://autoload/GameEvents.gd`
- `res://autoload/GameState.gd`
- etc.

### "Python script fails to execute"

- Ensure Python 3.8+ is installed
- Verify `python3` is in system PATH
- Test manually: `python3 godot/python/esens_godot_wrapper.py "P+H30%10s.ST"`

### "Tilemap Y-sorting issues"

- Verify Y Sort Enabled on Environment node
- Verify Y Sort Enabled on each TileMapLayer
- Check character origin is at feet
- Ensure characters are children of Environment node

### "Dialogue Manager not working"

- Install Dialogue Manager plugin from Asset Library
- Enable in Project → Project Settings → Plugins
- Restart Godot after installing

---

## 📚 Additional Resources

### Documentation
- [Full Implementation Plan](../GODOT_IMPLEMENTATION_PLAN.md) - High-level architecture
- [Season 0 Game Design Doc](../Season_0/Season_0_GameDesignDoc.md) - Game design
- [ESENS Parser Documentation](python/ESENS_README.md) - Notation system

### Godot Learning
- [Official Godot Docs](https://docs.godotengine.org/en/stable/)
- [GDQuest](https://www.gdquest.com/) - Tutorials and patterns
- [Godot Asset Library](https://godotengine.org/asset-library/asset) - Plugins and tools

### Community
- [Godot Discord](https://discord.gg/godotengine)
- [r/godot](https://reddit.com/r/godot)

---

## 🎯 Current Status

### ✅ Completed
- [x] Project structure setup
- [x] Folder organization
- [x] Input map configuration
- [x] ESENS parser integration

### 🚧 In Progress
- [ ] Autoload singletons implementation
- [ ] Player controller
- [ ] First location (Garden)
- [ ] Basic gathering system

### 📋 Planned (12-Week Timeline)
See [GODOT_IMPLEMENTATION_PLAN.md](../GODOT_IMPLEMENTATION_PLAN.md) for full roadmap.

**Phase 1 (Weeks 1-2):** Foundation - Core systems and player movement
**Phase 2 (Week 3):** Gathering & Inventory
**Phase 3 (Week 4):** Dialogue System
**Phase 4 (Weeks 5-6):** Crafting Minigame
**Phase 5 (Week 7):** Relationships & Stats
**Phase 6 (Week 8):** All Locations
**Phase 7 (Weeks 9-10):** Content & Polish
**Phase 8 (Weeks 11-12):** Testing & Iteration

---

## 📝 Contributing

This is a solo dev project, but contributions welcome! See main repo README for guidelines.

---

## 📄 License

See main repository for license information.

---

**Happy Brewing! 🧪✨**
