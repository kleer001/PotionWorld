# Scene Building Guide - Phase 1
## Step-by-Step Instructions for Godot Editor

This guide provides exact steps to build each scene in Godot 4.2.
Follow these specifications precisely at first, then customize as needed.

---

## 🎮 Scene 1: Player.tscn

**Location:** `godot/scenes/characters/Player.tscn`
**Script:** Already created at `godot/scenes/characters/Player.gd`

### Node Structure

```
Player (CharacterBody2D)  ← ROOT
├── AnimatedSprite2D
├── CollisionShape2D
├── Camera2D
├── InteractionArea (Area2D)
│   └── CollisionShape2D
└── InteractionPrompt (Label)
```

### Building Steps

1. **Create Root Node:**
   - Scene → New Scene
   - Click "Other Node"
   - Search for "CharacterBody2D"
   - Rename to "Player"
   - Attach script: `res://scenes/characters/Player.gd`

2. **Add AnimatedSprite2D:**
   - Right-click Player → Add Child Node
   - Search "AnimatedSprite2D"
   - Inspector settings:
     - Position: (0, 0)
     - Offset: (0, -16) ← This offsets sprite above feet

3. **Add CollisionShape2D:**
   - Right-click Player → Add Child Node
   - Search "CollisionShape2D"
   - Inspector → Shape → New CircleShape2D
   - Click the shape, set Radius: 8
   - Position: (0, 0) ← At player's feet

4. **Add Camera2D:**
   - Right-click Player → Add Child Node
   - Search "Camera2D"
   - Inspector settings:
     - Enabled: ✓
     - Zoom: (2.0, 2.0)
     - Position Smoothing → Enabled: ✓
     - Position Smoothing → Speed: 5.0

5. **Add InteractionArea (Area2D):**
   - Right-click Player → Add Child Node
   - Search "Area2D"
   - Rename to "InteractionArea"
   - Add child CollisionShape2D to InteractionArea:
     - Shape → New CircleShape2D
     - Radius: 32 (larger than player collision)

6. **Add InteractionPrompt (Label):**
   - Right-click Player → Add Child Node
   - Search "Label"
   - Rename to "InteractionPrompt"
   - Inspector settings:
     - Position: (-40, -40) ← Above player's head
     - Text: "[E] Interact"
     - Horizontal Alignment: Center
     - Vertical Alignment: Top

7. **Save Scene:**
   - Scene → Save Scene As
   - Save to: `res://scenes/characters/Player.tscn`

### Placeholder Art

For now, add a simple colored sprite:
- Select AnimatedSprite2D
- Inspector → Animation → Frames → New SpriteFrames
- Click the SpriteFrames resource
- Bottom panel → SpriteFrames editor opens
- Add a default animation called "idle_down"
- You can draw a simple colored rectangle or use a placeholder texture

**Proper setup will require:**
- 8 animations: idle_down, idle_up, idle_left, idle_right, walk_down, walk_up, walk_left, walk_right
- These can be added later when you have art assets

---

## 🌿 Scene 2: GatheringSpot.tscn

**Location:** `godot/scenes/locations/garden/GatheringSpot.tscn`
**Script:** Already created at `godot/scenes/locations/garden/GatheringSpot.gd`

### Node Structure

```
GatheringSpot (Node2D)  ← ROOT
├── Sprite2D
├── CPUParticles2D (name: GlowParticles)
└── InteractionArea (Area2D)
    └── CollisionShape2D
```

### Building Steps

1. **Create Root:**
   - New Scene → Other Node → Node2D
   - Rename to "GatheringSpot"
   - Attach script: `res://scenes/locations/garden/GatheringSpot.gd`

2. **Add Sprite2D:**
   - Add Child → Sprite2D
   - Position: (0, 0)
   - For now, use a placeholder texture or colored rectangle
   - Inspector → Texture → Quick Load → (find a placeholder image)

3. **Add CPUParticles2D:**
   - Add Child → CPUParticles2D
   - Rename to "GlowParticles"
   - Inspector settings:
     - Emitting: ✓ (checked)
     - Amount: 20
     - Lifetime: 2.0
     - Emission Shape → Shape: Sphere
     - Emission Shape → Sphere Radius: 16.0
     - Direction → Spread: 180.0
     - Gravity: (0, -20, 0)
     - Initial Velocity → Velocity Min: 10.0
     - Initial Velocity → Velocity Max: 20.0
     - Scale Amount Min: 0.5
     - Scale Amount Max: 1.5
     - Color: Light blue (0.5, 0.8, 1.0, 0.8)

4. **Add InteractionArea:**
   - Add Child → Area2D
   - Rename to "InteractionArea"
   - Add child: CollisionShape2D
     - Shape → New CircleShape2D
     - Radius: 24

5. **Configure Script Exports:**
   - Select GatheringSpot root
   - Inspector → Script Variables:
     - Ingredient Id: "common_mushroom"
     - Min Yield: 2
     - Max Yield: 4
     - Respawn Time: 300.0
     - Glow Color: (0.5, 0.8, 1.0, 0.8)

6. **Save Scene:**
   - Save to: `res://scenes/locations/garden/GatheringSpot.tscn`

---

## 🗺️ Scene 3: IngredientGarden.tscn

**Location:** `godot/scenes/locations/garden/IngredientGarden.tscn`
**Script:** Already created at `godot/scenes/locations/garden/IngredientGarden.gd`

### Node Structure

```
IngredientGarden (Node2D)  ← ROOT
├── Environment (Node2D) ← Y-Sort Enabled!
│   ├── GroundLayer (TileMapLayer)
│   ├── DecorationLayer (TileMapLayer)
│   ├── Objects (Node2D)
│   │   ├── GatheringSpot_Mushroom (instance)
│   │   ├── GatheringSpot_Berries (instance)
│   │   ├── GatheringSpot_Roots (instance)
│   │   └── GatheringSpot_Sap (instance)
│   └── Characters (Node2D)
│       └── Player (instance)
└── CanvasModulate (for lighting tint)
```

### Building Steps

1. **Create Root:**
   - New Scene → Node2D
   - Rename to "IngredientGarden"
   - Attach script: `res://scenes/locations/garden/IngredientGarden.gd`

2. **Add Environment Node:**
   - Add Child → Node2D
   - Rename to "Environment"
   - **CRITICAL:** Inspector → CanvasItem → Ordering:
     - ✅ Y Sort Enabled (MUST BE CHECKED!)

3. **Add TileMapLayers:**

   **GroundLayer:**
   - Right-click Environment → Add Child → TileMapLayer
   - Rename to "GroundLayer"
   - Inspector settings:
     - Tile Set → New TileSet
     - Y Sort Origin: 0
     - ✅ Y Sort Enabled

   **DecorationLayer:**
   - Right-click Environment → Add Child → TileMapLayer
   - Rename to "DecorationLayer"
   - Inspector:
     - Tile Set → Use same TileSet as GroundLayer
     - ✅ Y Sort Enabled

   **Note:** You'll need to configure the TileSet with isometric tiles:
   - Select GroundLayer
   - Inspector → Tile Set → (click the TileSet resource)
   - Bottom panel → TileSet editor
   - Add tileset texture
   - Configure tile shape: Isometric (in TileSet settings)
   - This is advanced - can do later with proper art

4. **Add Objects Container:**
   - Right-click Environment → Add Child → Node2D
   - Rename to "Objects"

5. **Add GatheringSpots (instances):**
   - Right-click Objects → Instantiate Child Scene
   - Select `res://scenes/locations/garden/GatheringSpot.tscn`
   - Rename to "GatheringSpot_Mushroom"
   - Position: (100, 100) ← Place somewhere visible
   - Inspector → Script Variables:
     - Ingredient Id: "common_mushroom"

   - Repeat for berries, roots, sap:
     - "GatheringSpot_Berries" at (200, 150), ingredient: "common_berries"
     - "GatheringSpot_Roots" at (150, 200), ingredient: "common_roots"
     - "GatheringSpot_Sap" at (250, 100), ingredient: "tree_sap"

6. **Add Characters Container:**
   - Right-click Environment → Add Child → Node2D
   - Rename to "Characters"

7. **Add Player (instance):**
   - Right-click Characters → Instantiate Child Scene
   - Select `res://scenes/characters/Player.tscn`
   - Position: (320, 240) ← Center of a 640x480 area

8. **Add CanvasModulate (optional lighting):**
   - Right-click IngredientGarden → Add Child → CanvasModulate
   - Inspector → Color: (1.0, 1.0, 0.9, 1.0) ← Slightly warm tint

9. **Save Scene:**
   - Save to: `res://scenes/locations/garden/IngredientGarden.tscn`

---

## ✅ Testing Checklist

### Test Player.tscn

1. Open Player.tscn
2. Press F6 (Run Current Scene)
3. Verify:
   - [ ] No errors in console
   - [ ] Player appears (even if just a colored square)
   - [ ] Camera follows player

### Test GatheringSpot.tscn

1. Open GatheringSpot.tscn
2. Press F6
3. Verify:
   - [ ] No errors
   - [ ] Sprite visible
   - [ ] Particles emitting (glowing effect)

### Test IngredientGarden.tscn

1. Open IngredientGarden.tscn
2. Press F6
3. Verify:
   - [ ] No errors
   - [ ] Player spawns
   - [ ] Can move with WASD
   - [ ] Camera follows player smoothly
   - [ ] Gathering spots visible
   - [ ] Can walk to gathering spot
   - [ ] Press E near spot
   - [ ] Should see "Gathered X x Common Mushroom" (check console)
   - [ ] Gathering spot should gray out
   - [ ] Open inventory with I - should see ingredient

### Expected Issues (OK for now)

- ❓ Player has no animations (just default sprite)
- ❓ Gathering spots have placeholder graphics
- ❓ No tilemap painted (just empty gray)
- ❓ No music plays (audio files don't exist yet)
- ❓ Console warnings about missing audio files (expected)

### Real Issues (need fixing)

- ❌ Errors in Output console
- ❌ Player can't move at all
- ❌ Pressing E doesn't gather
- ❌ Crashes or freezes

---

## 🎨 Art Asset Placeholders

For now, you can use simple colored rectangles:

**Player sprite:**
- 32x32 pixels
- Blue colored square
- Later: animated sprite sheets

**Gathering spots:**
- Mushrooms: Brown/tan circle
- Berries: Red circle
- Roots: Brown/green
- Sap: Amber/yellow

**Tiles:**
- Ground: Green
- Decoration: Dark green

You can create these quickly in any image editor (even MS Paint!), or download free placeholder assets from:
- Kenny.nl (free game assets)
- OpenGameArt.org
- itch.io (search "free isometric tiles")

---

## 📝 Next Steps After Phase 1

Once these 3 scenes are built and tested:

1. Report any errors to Claude
2. Take screenshots of the working game
3. Confirm all features work:
   - Player movement
   - Gathering interaction
   - Inventory system
4. Move to Phase 2 (Inventory UI)

---

## 🆘 Troubleshooting

### "Script class 'Player' could not be found"
- Solution: Project → Reload Current Project
- Godot needs to reparse scripts to recognize class_name

### "Invalid call. Nonexistent function 'emit'"
- Solution: Make sure all autoloads are configured in Project Settings
- Project → Project Settings → Autoload → verify all 5 are there

### "Y-sorting not working / depth issues"
- Solution:
  - Environment node MUST have Y Sort Enabled
  - ALL TileMapLayers must have Y Sort Enabled
  - Player's origin MUST be at feet (position 0,0, sprite offset up)

### "Can't interact with gathering spots"
- Solution:
  - Check InteractionArea on both Player and GatheringSpot
  - Both need CollisionShape2D with proper radius
  - Player script calls interact() method

### "Nothing happens when I press E"
- Solution:
  - Verify Input Map has "interact" action defined
  - Project → Project Settings → Input Map → "interact"
  - Should have E, Space, and Gamepad Button 0

---

**Good luck building! Report back when scenes are working!** 🚀
