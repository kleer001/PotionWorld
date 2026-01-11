# World Gameplay - Current State (MVP)

**Status**: Initial prototype working
**Last Updated**: 2026-01-11

## Overview

PotionWorld MVP is a 2D exploration and gathering game built with Python Arcade. The player explores a simple garden world, gathering ingredients while the game tracks stats and inventory.

## Current GUI/Gameplay Features

### 🎮 Core Gameplay Loop

1. **Exploration** - Player moves freely through a garden environment
2. **Gathering** - Interact with resource nodes to collect ingredients
3. **Progression** - Stats and inventory persist during session

### 🏃 Player Movement

- **Control Scheme**: WASD or Arrow Keys
- **Movement Type**: Continuous (hold to move)
- **Speed**: 180 pixels/second
- **Normalization**: Diagonal movement is properly normalized
- **Camera**: Smooth following camera (lerp factor: 0.2)
- **Camera Type**: Centered on player (Camera2D.position tracks player center)

### 🌿 Gathering System

**Gathering Spots**:
- 12 spots spawn in random positions around player start
- 4 ingredient types: Common Mushroom, Forest Berries, Earthen Root, Tree Sap
- Visual representation: Colored circles (30px radius)
- States: Normal (colored) / Depleted (dark gray)

**Interaction**:
- **Proximity Detection**: 100 pixel radius around player
- **Visual Feedback**: Yellow outline circle (40px radius) when in range
- **Input**: Press `E` to gather
- **Yield**: Random amount (1-3 per gather)
- **Respawn**: 30 second timer per spot

**Process**:
1. Move near a gathering spot (yellow outline appears)
2. Press E to interact
3. Notification shows what was gathered
4. Spot turns gray and begins respawn timer
5. Ingredients added to inventory

### 📊 UI Elements

**HUD (Always Visible)**:
- **Top Bar**: Controls reminder
  - "WASD: Move | E: Gather | I: Inventory (TODO) | ESC: Menu (TODO)"
- **Top Left Panel**:
  - Ingredient count summary
  - Individual ingredient amounts (shows first 5 types)
- **Left Side Panel (Lower)**:
  - Player stats display:
    - Intuition: 5 (starting value)
    - Precision: 3 (starting value)
    - Other stats: 0 (not yet used)

**Notifications**:
- **Position**: Top right corner
- **Duration**: 3 seconds
- **Fade**: Smooth fade-in/fade-out
- **Types**:
  - Info (blue background)
  - Success (green background)
  - Error (red background)
- **Examples**:
  - "Gathered 2x Common Mushroom"
  - "Gathered 1x Forest Berries"

### 🎨 Visual Design

**Color Scheme**:
- Background: Amazon green (#3B7A57)
- Ground: Dark green (drawn as large rectangle)
- UI Text: White/Light Gray
- Gathering spots: Brown, Red, Dark Green, Amber

**Layout**:
- Window: 1920x1080 (fixed, non-resizable)
- Player starts: Center of screen (960, 540)
- Camera starts: Centered on player
- World space: Unlimited (can move anywhere)

### 🏗️ Architecture

**View System**:
- Single view: `GameView` (exploration/gathering)
- Future views planned: Inventory, Crafting, Menu

**Entity System**:
- Player (arcade.Sprite with movement logic)
- GatheringSpot (arcade.Sprite with timer/respawn)
- SpriteLists for rendering

**Systems (Singletons)**:
- GameState - Phase management (MENU, GAMEPLAY, DIALOGUE, etc.)
- PlayerData - Persistent data (stats, inventory, progress)
- GameEvents - Event bus for decoupled communication
- AudioManager - Music/SFX (gracefully fails if no files)
- SaveSystem - JSON save/load (not yet used in MVP)

### 🎯 Player Stats

**Current Stats** (0-100 scale):
- **Precision**: 3 (from background: Rural Healer's Apprentice)
- **Intuition**: 5 (from background)
- **Knowledge**: 0
- **Business**: 0
- **Reputation**: 0
- **Combat Instinct**: 0

Stats are displayed but not yet used in gameplay mechanics.

### 📦 Inventory System

**Ingredients**:
- Dictionary: `{ingredient_id: amount}`
- Tracked in PlayerData singleton
- Displayed in UI (shows counts)
- No limits yet (infinite storage)

**Potions**:
- List of crafted potions (currently empty)
- Structure ready but no crafting system yet

### 🔧 Technical Details

**Performance**:
- Target: 60 FPS
- Delta-time scaled movement (frame-independent)
- Efficient sprite rendering

**Constants** (`constants.py`):
- WINDOW_WIDTH = 1920
- WINDOW_HEIGHT = 1080
- PLAYER_MOVE_SPEED = 180.0
- CAMERA_SPEED = 0.2
- GATHERING_INTERACTION_RANGE = 100
- GATHERING_RESPAWN_TIME = 30.0

### ⚙️ Debug Features

**Console Output**:
- Player position on startup
- Camera position on startup
- Game setup confirmation

**Debug Keys**:
- `P`: Add 5 precision stat (testing)

## Not Yet Implemented

### High Priority
- [ ] Inventory view (I key)
- [ ] Pause/Menu system (ESC key)
- [ ] Collision system (walls, boundaries)
- [ ] Save/Load functionality

### Medium Priority
- [ ] Crafting system
- [ ] NPC interactions
- [ ] Quest system
- [ ] Day/night cycle
- [ ] More ingredient types
- [ ] More gathering spot variations

### Low Priority
- [ ] Animations (player, gathering)
- [ ] Particle effects
- [ ] Sound effects
- [ ] Music tracks
- [ ] More complex map/tilemap
- [ ] Minimap

## Known Issues

✅ **RESOLVED**:
- ~~Player starting in upper right corner~~ - Fixed: Camera.position is center point, not bottom-left
- ~~Movement too slow~~ - Fixed: Increased to 180 px/s
- ~~Discrete tile movement~~ - Fixed: Restored continuous movement
- ~~`draw_lrtb` typo~~ - Fixed: Changed to `draw_lrbt`

**CURRENT**:
- None identified

## Testing Checklist

✅ Player spawns centered on screen
✅ WASD movement works smoothly
✅ Camera follows player
✅ Gathering spots visible
✅ Yellow outline appears when near spots
✅ E key gathers ingredients
✅ Notifications appear
✅ Inventory counts update
✅ Stats display on screen
✅ Spots deplete and show gray
⏳ Spots respawn after 30 seconds (needs verification)

## Next Steps

Focus on **world interactivity and UI improvements**:
1. Add visual polish to gathering interaction
2. Implement collision boundaries
3. Add more environmental objects
4. Improve visual feedback
5. Add debug overlay option

---

**Game Loop Summary**: Walk around → Find glowing spots → Press E → Collect ingredients → Watch inventory grow → Wait for respawn → Repeat
