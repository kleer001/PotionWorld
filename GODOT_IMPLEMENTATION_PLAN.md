# PotionWorld: Godot 4.2 Isometric GUI MVP Implementation Plan
## High-Level Architecture - Birds Eye View

**Version:** 1.0
**Date:** 2025-11-10
**Target:** Season 0 Demo (60-minute vertical slice)
**Engine:** Godot 4.2 (stable)
**Platforms:** PC (Windows/Mac/Linux) + Web Export

---

## 🎯 EXECUTIVE SUMMARY

This document provides a comprehensive, high-level architecture for implementing PotionWorld's GUI MVP in Godot 4.2. The game uses:
- **Stardew Valley-style 3/4 isometric perspective** (not pure isometric)
- **Direct control movement** (WASD/gamepad for MVP, point-and-click later)
- **Dialogue Manager plugin** for character conversations with portraits
- **Minimal but elegant UI** with context-sensitive popups
- **Python ESENS parser** called via OS.execute
- **Full tactile crafting minigame** with simple graphics
- **Resource-based save system** with auto-save + manual slots

**Primary Goal:** Prove full gameplay loop (gather → craft → social) works and is fun, suitable for investor/publisher demos.

---

## 📁 PROJECT STRUCTURE

```
PotionWorld/
├── project.godot
├── .gitignore
│
├── autoload/              # Singleton systems (autoloaded)
│   ├── GameEvents.gd      # Event bus for global signals
│   ├── GameState.gd       # Current game state & session data
│   ├── SaveSystem.gd      # Save/load manager
│   ├── PlayerData.gd      # Player stats, inventory, relationships
│   ├── DialogueState.gd   # Dialogue history & choices
│   └── AudioManager.gd    # Music & SFX controller
│
├── scenes/                # All game scenes
│   ├── main/
│   │   ├── Main.tscn           # Root scene (loads others)
│   │   └── MainMenu.tscn       # Title screen
│   │
│   ├── locations/         # Playable locations
│   │   ├── cart/
│   │   │   ├── CartRide.tscn          # Opening scene
│   │   │   └── CartRide.gd
│   │   ├── dorm/
│   │   │   ├── DormRoom.tscn          # Player's room
│   │   │   ├── DormRoom.gd
│   │   │   └── InteractableObject.gd   # Clickable items
│   │   ├── garden/
│   │   │   ├── IngredientGarden.tscn   # Gathering location
│   │   │   ├── IngredientGarden.gd
│   │   │   └── GatheringSpot.gd        # Individual resource nodes
│   │   ├── classroom/
│   │   │   ├── Classroom.tscn          # Crafting tutorial
│   │   │   └── Classroom.gd
│   │   └── courtyard/
│   │       ├── Courtyard.tscn          # Social hub
│   │       └── Courtyard.gd
│   │
│   ├── characters/        # Character scenes
│   │   ├── Player.tscn             # Player character
│   │   ├── Player.gd
│   │   ├── NPCBase.tscn            # Base NPC scene (inherited)
│   │   ├── NPCBase.gd
│   │   └── npcs/
│   │       ├── Rachel.tscn
│   │       ├── Ezekiel.tscn
│   │       ├── Miriam.tscn
│   │       └── Thornwood.tscn
│   │
│   ├── ui/                # UI components
│   │   ├── hud/
│   │   │   ├── HUD.tscn                # Minimal persistent UI
│   │   │   └── HUD.gd
│   │   ├── inventory/
│   │   │   ├── InventoryUI.tscn        # Inventory popup
│   │   │   ├── InventoryUI.gd
│   │   │   └── ItemSlot.tscn           # Grid slot
│   │   ├── journal/
│   │   │   ├── JournalUI.tscn          # Stats/relationships
│   │   │   └── JournalUI.gd
│   │   ├── crafting/
│   │   │   ├── CraftingUI.tscn         # Crafting interface
│   │   │   ├── CraftingUI.gd
│   │   │   └── CraftingMinigame.tscn   # Mortar & pestle
│   │   ├── dialogue/
│   │   │   └── DialogueBox.tscn        # Custom wrapper for Dialogue Manager
│   │   └── notifications/
│   │       ├── Notification.tscn       # Popup notifications
│   │       └── NotificationManager.gd
│   │
│   └── minigames/         # Crafting minigame components
│       └── grinding/
│           ├── MortarPestle.tscn
│           ├── MortarPestle.gd
│           └── IngredientVisual.tscn
│
├── scripts/               # Non-node scripts (pure logic)
│   ├── data/
│   │   ├── IngredientData.gd      # Ingredient definitions
│   │   ├── RecipeData.gd          # Recipe definitions
│   │   ├── NPCData.gd             # NPC personality data
│   │   └── DialogueChoice.gd      # Choice consequence data
│   │
│   ├── systems/
│   │   ├── CraftingSystem.gd      # Crafting logic
│   │   ├── AffinitySystem.gd      # Relationship calculations
│   │   ├── StatSystem.gd          # XP & progression
│   │   ├── InventorySystem.gd     # Inventory management
│   │   └── ESENSParser.gd         # Wrapper for Python parser
│   │
│   └── utils/
│       ├── Constants.gd            # Game constants
│       └── Helpers.gd              # Utility functions
│
├── resources/             # Custom Resources (data containers)
│   ├── ingredients/
│   │   └── IngredientResource.gd   # Extends Resource
│   ├── recipes/
│   │   └── RecipeResource.gd       # Extends Resource
│   ├── npcs/
│   │   └── NPCResource.gd          # Big 5 personality + affinity
│   ├── dialogue/
│   │   └── (Dialogue Manager files)
│   └── save/
│       └── SaveData.gd             # Save file Resource
│
├── data/                  # JSON/CSV data files
│   ├── ingredients.json
│   ├── recipes.json
│   ├── npcs.json
│   ├── dialogue/
│   │   └── (Dialogue Manager .dialogue files)
│   └── choices.json       # Choice consequences
│
├── assets/                # Art, audio, fonts
│   ├── art/
│   │   ├── characters/
│   │   │   ├── portraits/         # Character portraits
│   │   │   └── sprites/           # Sprite sheets
│   │   ├── tilesets/
│   │   │   └── isometric/         # Tileset images
│   │   ├── ui/                    # UI textures
│   │   └── items/                 # Ingredient/potion icons
│   │
│   ├── audio/
│   │   ├── music/
│   │   └── sfx/
│   │
│   └── fonts/
│
├── addons/                # Godot plugins
│   └── dialogue_manager/   # Dialogue Manager plugin
│
├── python/                # Python scripts
│   └── esens_parser.py     # ESENS notation parser
│
└── exports/               # Build outputs
    ├── windows/
    ├── linux/
    ├── macos/
    └── web/
```

---

## 🏗️ CORE ARCHITECTURE

### Singleton Autoload System

Godot's autoload feature creates globally accessible singletons. These handle cross-scene systems:

#### 1. **GameEvents.gd** (Event Bus)
```gdscript
# Publisher/subscriber pattern for global events
extends Node

# Gathering events
signal ingredient_gathered(ingredient_type: String, amount: int)
signal gathering_spot_depleted(spot_id: String)

# Crafting events
signal potion_crafted(potion_name: String, quality: String)
signal crafting_failed(reason: String)
signal recipe_learned(recipe_id: String)

# Relationship events
signal affinity_changed(npc_id: String, old_value: float, new_value: float)
signal dialogue_choice_made(choice_id: String, npc_id: String)
signal trait_unlocked(trait_name: String)

# Progression events
signal stat_increased(stat_name: String, old_value: int, new_value: int)
signal xp_gained(stat_name: String, amount: int)
signal level_threshold_reached(stat_name: String, threshold: int)

# UI events
signal inventory_opened()
signal journal_opened()
signal notification_requested(message: String, type: String)

# Scene events
signal scene_transition_requested(scene_path: String)
signal cutscene_started(cutscene_id: String)
signal cutscene_ended(cutscene_id: String)

# Save/Load events
signal game_saved()
signal game_loaded()
```

**Why Event Bus?**
- Decouples systems (UI doesn't need reference to inventory system)
- Easy to add audio/visual feedback (AudioManager listens to events)
- Simplifies debugging (log all events from one place)
- Clean for collaboration

**Best Practices:**
- Only use for truly global events
- Don't overuse (prefer direct signals when nodes are close)
- Document what emits each signal

---

#### 2. **GameState.gd** (Current Session State)
```gdscript
# Tracks current game state (not saved data)
extends Node

# Current state
enum GamePhase { MENU, GAMEPLAY, DIALOGUE, CRAFTING, CUTSCENE, PAUSED }
var current_phase: GamePhase = GamePhase.MENU

# Current location
var current_scene: String = ""
var previous_scene: String = ""

# Time tracking
var current_day: int = 1
var current_time: String = "morning"  # morning, afternoon, evening, night
var elapsed_game_time: float = 0.0

# Current interaction state
var is_in_dialogue: bool = false
var is_crafting: bool = false
var is_gathering: bool = false

# UI state
var is_inventory_open: bool = false
var is_journal_open: bool = false
var is_paused: bool = false

# Input state
var can_move: bool = true
var can_interact: bool = true
var can_open_menus: bool = true

func enter_dialogue() -> void:
    current_phase = GamePhase.DIALOGUE
    is_in_dialogue = true
    can_move = false
    can_open_menus = false

func exit_dialogue() -> void:
    current_phase = GamePhase.GAMEPLAY
    is_in_dialogue = false
    can_move = true
    can_open_menus = true

# Similar methods for other state transitions...
```

**Purpose:**
- Single source of truth for current game state
- Controls what player can/cannot do
- Prevents bugs (can't open inventory during cutscene)
- Easy to query from any script

---

#### 3. **PlayerData.gd** (Persistent Player Data)
```gdscript
# Player's persistent data (this gets saved)
extends Node

# Character creation
var player_name: String = ""
var player_appearance: int = 0  # Index to appearance preset
var player_background: String = ""  # "rural_healer", "city_merchant", etc.

# Stats
var stats: Dictionary = {
    "precision": 0,
    "knowledge": 0,
    "intuition": 0,
    "business": 0,
    "reputation": 0,
    "combat_instinct": 0
}

# Inventory
var ingredients: Dictionary = {}  # {"common_mushroom": 5, "tree_sap": 2, ...}
var potions: Array[Dictionary] = []  # [{name, quality, potency, created_date}, ...]
var equipment: Dictionary = {}  # {mortar_pestle: "basic", cauldron: null, ...}

# Recipes
var known_recipes: Dictionary = {}  # {recipe_id: mastery_level (0-100)}
var discovered_recipes: Array[String] = []

# Relationships (NPC affinity)
var npc_affinity: Dictionary = {}  # {npc_id: affinity_value (-5.0 to 5.0)}
var npc_memories: Dictionary = {}  # {npc_id: [memory_strings]}

# Choices & Traits
var choices_made: Array[Dictionary] = []  # [{choice_id, option_selected, timestamp}, ...]
var unlocked_traits: Array[String] = []  # ["innovator", "diplomat", ...]
var personality_flags: Dictionary = {}  # {openness: 1, conscientiousness: 0, ...}

# Progression
var total_playtime: float = 0.0
var current_season: int = 0  # 0 for demo
var completed_quests: Array[String] = []

# Methods for common operations
func add_ingredient(ingredient_id: String, amount: int) -> void:
    if ingredients.has(ingredient_id):
        ingredients[ingredient_id] += amount
    else:
        ingredients[ingredient_id] = amount
    GameEvents.ingredient_gathered.emit(ingredient_id, amount)

func remove_ingredient(ingredient_id: String, amount: int) -> bool:
    if not ingredients.has(ingredient_id) or ingredients[ingredient_id] < amount:
        return false
    ingredients[ingredient_id] -= amount
    if ingredients[ingredient_id] <= 0:
        ingredients.erase(ingredient_id)
    return true

func has_ingredient(ingredient_id: String, amount: int = 1) -> bool:
    return ingredients.get(ingredient_id, 0) >= amount

func add_stat(stat_name: String, amount: int) -> void:
    var old_value = stats[stat_name]
    stats[stat_name] += amount
    GameEvents.stat_increased.emit(stat_name, old_value, stats[stat_name])
    GameEvents.xp_gained.emit(stat_name, amount)

    # Check thresholds (25, 50, 75, 100)
    for threshold in [25, 50, 75, 100]:
        if old_value < threshold and stats[stat_name] >= threshold:
            GameEvents.level_threshold_reached.emit(stat_name, threshold)

func add_affinity(npc_id: String, amount: float) -> void:
    var old_value = npc_affinity.get(npc_id, 0.0)
    var new_value = clamp(old_value + amount, -5.0, 5.0)
    npc_affinity[npc_id] = new_value
    GameEvents.affinity_changed.emit(npc_id, old_value, new_value)

func get_affinity(npc_id: String) -> float:
    return npc_affinity.get(npc_id, 0.0)

func learn_recipe(recipe_id: String) -> void:
    if not known_recipes.has(recipe_id):
        known_recipes[recipe_id] = 0  # Novice mastery
        GameEvents.recipe_learned.emit(recipe_id)

func add_recipe_mastery(recipe_id: String, amount: int) -> void:
    if known_recipes.has(recipe_id):
        known_recipes[recipe_id] = min(known_recipes[recipe_id] + amount, 100)

func make_choice(choice_id: String, option_selected: String) -> void:
    choices_made.append({
        "choice_id": choice_id,
        "option": option_selected,
        "day": GameState.current_day
    })
    GameEvents.dialogue_choice_made.emit(choice_id, option_selected)
```

**Purpose:**
- All saveable player data in one place
- Methods for common operations (add/remove items)
- Emits events when data changes (UI can react)

---

#### 4. **SaveSystem.gd** (Save/Load Manager)
```gdscript
# Handles saving and loading game data
extends Node

const SAVE_DIR = "user://saves/"
const AUTO_SAVE_FILE = "autosave.tres"
const MANUAL_SAVE_PREFIX = "manual_"

var current_save_slot: int = -1  # -1 for autosave

func _ready() -> void:
    # Create save directory if doesn't exist
    if not DirAccess.dir_exists_absolute(SAVE_DIR):
        DirAccess.make_dir_absolute(SAVE_DIR)

    # Connect to events for auto-save triggers
    GameEvents.scene_transition_requested.connect(_on_scene_transition)
    GameEvents.potion_crafted.connect(_on_potion_crafted)

func save_game(slot: int = -1) -> bool:
    var save_data = SaveData.new()

    # Populate save_data from PlayerData
    save_data.player_name = PlayerData.player_name
    save_data.player_appearance = PlayerData.player_appearance
    save_data.player_background = PlayerData.player_background
    save_data.stats = PlayerData.stats.duplicate(true)
    save_data.ingredients = PlayerData.ingredients.duplicate(true)
    save_data.potions = PlayerData.potions.duplicate(true)
    save_data.known_recipes = PlayerData.known_recipes.duplicate(true)
    save_data.npc_affinity = PlayerData.npc_affinity.duplicate(true)
    save_data.choices_made = PlayerData.choices_made.duplicate(true)
    save_data.unlocked_traits = PlayerData.unlocked_traits.duplicate(true)

    # Add metadata
    save_data.save_timestamp = Time.get_datetime_string_from_system()
    save_data.total_playtime = PlayerData.total_playtime
    save_data.current_day = GameState.current_day
    save_data.current_scene = GameState.current_scene

    # Determine save path
    var save_path = SAVE_DIR + (AUTO_SAVE_FILE if slot == -1 else MANUAL_SAVE_PREFIX + str(slot) + ".tres")

    # Save using ResourceSaver
    var result = ResourceSaver.save(save_data, save_path)

    if result == OK:
        current_save_slot = slot
        GameEvents.game_saved.emit()
        print("Game saved to: ", save_path)
        return true
    else:
        push_error("Failed to save game: ", result)
        return false

func load_game(slot: int = -1) -> bool:
    var save_path = SAVE_DIR + (AUTO_SAVE_FILE if slot == -1 else MANUAL_SAVE_PREFIX + str(slot) + ".tres")

    if not FileAccess.file_exists(save_path):
        push_error("Save file does not exist: ", save_path)
        return false

    # Load using ResourceLoader
    var save_data: SaveData = ResourceLoader.load(save_path)

    if save_data == null:
        push_error("Failed to load save file")
        return false

    # Restore PlayerData
    PlayerData.player_name = save_data.player_name
    PlayerData.player_appearance = save_data.player_appearance
    PlayerData.player_background = save_data.player_background
    PlayerData.stats = save_data.stats.duplicate(true)
    PlayerData.ingredients = save_data.ingredients.duplicate(true)
    PlayerData.potions = save_data.potions.duplicate(true)
    PlayerData.known_recipes = save_data.known_recipes.duplicate(true)
    PlayerData.npc_affinity = save_data.npc_affinity.duplicate(true)
    PlayerData.choices_made = save_data.choices_made.duplicate(true)
    PlayerData.unlocked_traits = save_data.unlocked_traits.duplicate(true)
    PlayerData.total_playtime = save_data.total_playtime

    # Restore GameState
    GameState.current_day = save_data.current_day

    current_save_slot = slot
    GameEvents.game_loaded.emit()
    print("Game loaded from: ", save_path)

    # Load the scene
    GameEvents.scene_transition_requested.emit(save_data.current_scene)

    return true

func get_save_info(slot: int = -1) -> Dictionary:
    var save_path = SAVE_DIR + (AUTO_SAVE_FILE if slot == -1 else MANUAL_SAVE_PREFIX + str(slot) + ".tres")

    if not FileAccess.file_exists(save_path):
        return {}

    var save_data: SaveData = ResourceLoader.load(save_path)
    if save_data == null:
        return {}

    return {
        "player_name": save_data.player_name,
        "timestamp": save_data.save_timestamp,
        "playtime": save_data.total_playtime,
        "day": save_data.current_day,
        "scene": save_data.current_scene
    }

func has_save(slot: int = -1) -> bool:
    var save_path = SAVE_DIR + (AUTO_SAVE_FILE if slot == -1 else MANUAL_SAVE_PREFIX + str(slot) + ".tres")
    return FileAccess.file_exists(save_path)

# Auto-save triggers
func _on_scene_transition(_scene_path: String) -> void:
    save_game(-1)  # Auto-save

func _on_potion_crafted(_potion_name: String, _quality: String) -> void:
    # Auto-save after successful crafting
    save_game(-1)
```

**SaveData.gd Resource:**
```gdscript
# resources/save/SaveData.gd
extends Resource
class_name SaveData

@export var player_name: String
@export var player_appearance: int
@export var player_background: String
@export var stats: Dictionary
@export var ingredients: Dictionary
@export var potions: Array[Dictionary]
@export var known_recipes: Dictionary
@export var npc_affinity: Dictionary
@export var choices_made: Array[Dictionary]
@export var unlocked_traits: Array[String]
@export var save_timestamp: String
@export var total_playtime: float
@export var current_day: int
@export var current_scene: String
```

**Why Resource-based saves?**
- Simple (one function call to save/load)
- Type-safe (knows Godot types)
- Compact binary format (.tres)
- Built-in versioning

---

#### 5. **AudioManager.gd** (Audio Controller)
```gdscript
# Centralized audio management
extends Node

var music_player: AudioStreamPlayer
var sfx_players: Array[AudioStreamPlayer] = []
const MAX_SFX_PLAYERS = 8

var current_music: String = ""
var music_volume: float = 0.8
var sfx_volume: float = 1.0

func _ready() -> void:
    # Create music player
    music_player = AudioStreamPlayer.new()
    add_child(music_player)
    music_player.bus = "Music"

    # Create SFX players pool
    for i in range(MAX_SFX_PLAYERS):
        var player = AudioStreamPlayer.new()
        add_child(player)
        player.bus = "SFX"
        sfx_players.append(player)

    # Connect to game events
    GameEvents.ingredient_gathered.connect(_on_ingredient_gathered)
    GameEvents.potion_crafted.connect(_on_potion_crafted)
    GameEvents.affinity_changed.connect(_on_affinity_changed)

func play_music(music_name: String, fade_duration: float = 1.0) -> void:
    if current_music == music_name:
        return

    var music_path = "res://assets/audio/music/" + music_name + ".ogg"
    var stream = load(music_path)

    if stream:
        # Fade out current music
        if music_player.playing:
            var tween = create_tween()
            tween.tween_property(music_player, "volume_db", -80, fade_duration)
            await tween.finished

        # Play new music
        music_player.stream = stream
        music_player.volume_db = linear_to_db(music_volume)
        music_player.play()
        current_music = music_name

func play_sfx(sfx_name: String, pitch_variation: float = 0.0) -> void:
    var sfx_path = "res://assets/audio/sfx/" + sfx_name + ".ogg"
    var stream = load(sfx_path)

    if not stream:
        return

    # Find available SFX player
    for player in sfx_players:
        if not player.playing:
            player.stream = stream
            player.volume_db = linear_to_db(sfx_volume)
            player.pitch_scale = 1.0 + randf_range(-pitch_variation, pitch_variation)
            player.play()
            return

# Event handlers
func _on_ingredient_gathered(ingredient_type: String, _amount: int) -> void:
    play_sfx("gather_" + ingredient_type, 0.1)

func _on_potion_crafted(_potion_name: String, quality: String) -> void:
    if quality in ["fine", "exceptional", "masterwork"]:
        play_sfx("craft_success_special")
    else:
        play_sfx("craft_success")

func _on_affinity_changed(_npc_id: String, old_value: float, new_value: float) -> void:
    if new_value > old_value:
        play_sfx("affinity_gain")
    else:
        play_sfx("affinity_loss")
```

**Purpose:**
- Centralized audio control
- Audio pools prevent overlapping sounds
- Reacts to game events automatically
- Easy volume/music transitions

---

## 🗺️ ISOMETRIC WORLD SETUP

### Stardew-Style 3/4 Perspective Implementation

**Key Differences from Pure Isometric:**
- Tiles are NOT 2:1 diamond ratio
- Uses 3/4 overhead perspective (like Stardew Valley, Zelda: ALTTP)
- Easier character animation (faces camera more)
- More forgiving depth sorting

### TileMap Configuration

**1. Base Tileset Setup**

Create `isometric_tileset.tres`:
- **Tile Shape:** Isometric (but will use custom size)
- **Tile Size:** 32x16 (or 64x32 for higher detail)
- **Tile Layout:** Diamond Down
- **Texture Filter:** Nearest (for pixel art) or Linear (for pre-rendered 3D)

**2. TileMapLayer Structure**

For each location scene (e.g., Garden, Dorm Room):

```
Scene Root (Node2D)
├── Environment (YSort enabled Node2D)
│   ├── GroundLayer (TileMapLayer)        # Floor tiles
│   │   └── Y Sort: Enabled
│   │
│   ├── WallsLayer (TileMapLayer)         # Walls, tall objects
│   │   └── Y Sort: Enabled
│   │
│   ├── DecorationLayer (TileMapLayer)    # Plants, furniture bases
│   │   └── Y Sort: Enabled
│   │
│   ├── Objects (Node2D)                   # Non-tile objects
│   │   ├── GatheringSpot (Sprite2D + Area2D)
│   │   ├── InteractableObject (Sprite2D + Area2D)
│   │   └── ... (more objects)
│   │
│   └── Characters (Node2D)
│       ├── Player (CharacterBody2D)
│       ├── Rachel (NPC)
│       └── ... (more NPCs)
│
├── Lighting (CanvasModulate)              # Global lighting tint
├── Camera2D                                # Follows player
└── UI Layer (CanvasLayer)                  # Location-specific UI
```

### Y-Sorting Setup

**Critical for depth ordering:**

1. **Enable Y-Sort on Environment Node:**
   - Inspector → CanvasItem → Ordering → Y Sort Enabled ✓

2. **All children must have Y-Sort enabled:**
   - Each TileMapLayer
   - All Sprite2D nodes
   - Character nodes

3. **Position = Sorting Key:**
   - Object's global Y position determines draw order
   - Higher Y = drawn in front

4. **Character Sorting:**
   - Set character's origin point at FEET
   - Character.position.y at ground level, not center

**Example Character Setup:**
```
Player (CharacterBody2D)
├── Sprite2D                    # Offset.y = -16 (sprite above feet)
│   └── Texture Offset: (0, -16)
├── CollisionShape2D            # At feet level
│   └── Position: (0, 0)
└── InteractionArea (Area2D)
    └── Position: (0, 0)
```

### Camera Setup

```gdscript
# Camera2D attached to Player
extends Camera2D

@export var smoothing_speed: float = 5.0
@export var zoom_level: float = 2.0  # Adjust for screen size

func _ready() -> void:
    zoom = Vector2(zoom_level, zoom_level)
    position_smoothing_enabled = true
    position_smoothing_speed = smoothing_speed

    # Optional: Set limits based on map size
    limit_left = 0
    limit_top = 0
    limit_right = 1920  # Map width in pixels
    limit_bottom = 1080  # Map height in pixels
```

---

## 🎮 PLAYER CONTROLLER

### Direct Control Movement (WASD/Gamepad)

**Player.gd:**
```gdscript
extends CharacterBody2D
class_name Player

@export var move_speed: float = 150.0

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var interaction_area: Area2D = $InteractionArea

var input_direction: Vector2 = Vector2.ZERO
var facing_direction: Vector2 = Vector2.DOWN

# Animation states: idle_down, idle_up, idle_left, idle_right
#                  walk_down, walk_up, walk_left, walk_right

func _physics_process(delta: float) -> void:
    # Check if player can move
    if not GameState.can_move:
        velocity = Vector2.ZERO
        play_idle_animation()
        move_and_slide()
        return

    # Get input
    input_direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")

    # Normalize diagonal movement
    if input_direction.length() > 0:
        input_direction = input_direction.normalized()
        facing_direction = input_direction

    # Set velocity
    velocity = input_direction * move_speed

    # Update animation
    if input_direction.length() > 0:
        play_walk_animation()
    else:
        play_idle_animation()

    # Move
    move_and_slide()

func play_walk_animation() -> void:
    if abs(input_direction.x) > abs(input_direction.y):
        # Horizontal movement
        if input_direction.x > 0:
            sprite.play("walk_right")
        else:
            sprite.play("walk_left")
    else:
        # Vertical movement
        if input_direction.y > 0:
            sprite.play("walk_down")
        else:
            sprite.play("walk_up")

func play_idle_animation() -> void:
    if abs(facing_direction.x) > abs(facing_direction.y):
        if facing_direction.x > 0:
            sprite.play("idle_right")
        else:
            sprite.play("idle_left")
    else:
        if facing_direction.y > 0:
            sprite.play("idle_down")
        else:
            sprite.play("idle_up")

func _unhandled_input(event: InputEvent) -> void:
    if not GameState.can_interact:
        return

    # Interact with nearby objects
    if event.is_action_pressed("interact"):
        var overlapping_areas = interaction_area.get_overlapping_areas()
        if overlapping_areas.size() > 0:
            # Interact with closest object
            var closest = overlapping_areas[0].get_parent()
            if closest.has_method("interact"):
                closest.interact()
```

**Input Map (Project Settings → Input Map):**
- `move_left`: A, Left Arrow, Gamepad Left Stick Left
- `move_right`: D, Right Arrow, Gamepad Left Stick Right
- `move_up`: W, Up Arrow, Gamepad Left Stick Up
- `move_down`: S, Down Arrow, Gamepad Left Stick Down
- `interact`: E, Space, Gamepad Button A
- `inventory`: I, Tab, Gamepad Button Y
- `journal`: J, Gamepad Button X
- `pause`: Esc, Gamepad Start

---

## 🎭 DIALOGUE SYSTEM

### Using Dialogue Manager Plugin

**Installation:**
1. Download from Asset Library or GitHub
2. Place in `addons/dialogue_manager/`
3. Enable in Project Settings → Plugins

**Structure:**

```
data/dialogue/
├── rachel.dialogue          # Rachel's conversations
├── ezekiel.dialogue         # Ezekiel's conversations
├── miriam.dialogue
├── thornwood.dialogue
└── choices.dialogue         # Major choice dialogues
```

**Sample Dialogue File (rachel.dialogue):**
```
~ first_meeting

Rachel: Oh! You're here! Hi! I'm Rachel!
[setExpression rachel excited]
Rachel: I got here yesterday and I've already explored EVERYTHING.
Rachel: The garden is amazing, the library has this restricted section—
Rachel: Oh, sorry, I'm talking too much, aren't I?
[setExpression rachel shy]

- Let's explore together!
    [addAffinity rachel 0.5]
    [set rachel_relationship friendly]
    Rachel: Really?! Yes! Come on!
    => go_to_garden

- I'll unpack first
    Rachel: Oh, of course! Take your time!
    => end

~ go_to_garden
[emit scene_transition garden]
=> end
```

**Custom Dialogue Box (wraps Dialogue Manager UI):**

```gdscript
# scenes/ui/dialogue/DialogueBox.gd
extends CanvasLayer

@onready var portrait: TextureRect = $Panel/Portrait
@onready var name_label: Label = $Panel/NameLabel
@onready var dialogue_label: RichTextLabel = $Panel/DialogueLabel
@onready var choice_container: VBoxContainer = $Panel/ChoiceContainer

var current_npc_id: String = ""
var portrait_textures: Dictionary = {}  # Preloaded portraits

func _ready() -> void:
    # Load all portraits
    portrait_textures = {
        "rachel_neutral": load("res://assets/art/characters/portraits/rachel_neutral.png"),
        "rachel_excited": load("res://assets/art/characters/portraits/rachel_excited.png"),
        "rachel_shy": load("res://assets/art/characters/portraits/rachel_shy.png"),
        # ... more portraits
    }

    # Connect to Dialogue Manager
    DialogueManager.dialogue_started.connect(_on_dialogue_started)
    DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

func start_dialogue(resource: DialogueResource, title: String, npc_id: String) -> void:
    current_npc_id = npc_id
    GameState.enter_dialogue()

    # Set NPC portrait and name
    set_portrait(npc_id, "neutral")
    name_label.text = get_npc_name(npc_id)

    # Start dialogue
    DialogueManager.show_dialogue_balloon(resource, title)

func set_portrait(npc_id: String, expression: String) -> void:
    var key = npc_id + "_" + expression
    if portrait_textures.has(key):
        portrait.texture = portrait_textures[key]

func get_npc_name(npc_id: String) -> String:
    match npc_id:
        "rachel": return "Rachel"
        "ezekiel": return "Ezekiel"
        "miriam": return "Miriam"
        "thornwood": return "Instructor Thornwood"
        _: return "Unknown"

func _on_dialogue_started() -> void:
    show()

func _on_dialogue_ended() -> void:
    hide()
    GameState.exit_dialogue()
```

**Dialogue Manager Custom Functions:**

Create `dialogue_manager_functions.gd` in autoload:

```gdscript
# Custom functions callable from .dialogue files
extends Node

func addAffinity(npc_id: String, amount: float) -> void:
    PlayerData.add_affinity(npc_id, amount)

func set_flag(flag_name: String, value: bool = true) -> void:
    PlayerData.personality_flags[flag_name] = value

func has_trait(trait_name: String) -> bool:
    return trait_name in PlayerData.unlocked_traits

func unlock_trait(trait_name: String) -> void:
    if not trait_name in PlayerData.unlocked_traits:
        PlayerData.unlocked_traits.append(trait_name)
        GameEvents.trait_unlocked.emit(trait_name)

func setExpression(npc_id: String, expression: String) -> void:
    # Tell DialogueBox to change portrait
    get_node("/root/DialogueBox").set_portrait(npc_id, expression)

func emit_scene_transition(scene_name: String) -> void:
    GameEvents.scene_transition_requested.emit("res://scenes/locations/" + scene_name + "/" + scene_name.capitalize() + ".tscn")
```

---

## 🎒 INVENTORY SYSTEM

### Data Structure

**IngredientResource.gd:**
```gdscript
extends Resource
class_name IngredientResource

@export var id: String = ""
@export var display_name: String = ""
@export var description: String = ""
@export var icon: Texture2D
@export var rarity: String = "common"  # common, uncommon, rare, very_rare, legendary
@export var category: String = "root"  # root, mushroom, berry, crystal, sap, etc.
@export var glow_color: Color = Color.WHITE
@export var base_value: int = 5  # Base sell price
@export var properties: Array[String] = []  # ["healing", "binding", "energy"]
```

**RecipeResource.gd:**
```gdscript
extends Resource
class_name RecipeResource

@export var id: String = ""
@export var display_name: String = ""
@export var description: String = ""
@export var icon: Texture2D
@export var difficulty: int = 5  # 0-100
@export var base_success_chance: int = 50
@export var ingredients: Dictionary = {}  # {"common_mushroom": 2, "tree_sap": 1}
@export var esens_notation: String = ""
@export var effects: Array[Dictionary] = []  # [{type: "heal", amount: 30, duration: 10}]
@export var quality_tiers: Array[String] = ["poor", "standard", "fine", "exceptional", "masterwork"]
@export var unlock_requirement: String = ""  # Optional: stat requirement
```

### Inventory UI

**InventoryUI.tscn structure:**
```
InventoryUI (Control, full screen, initially hidden)
├── Panel (NinePatchRect)
│   ├── TabContainer
│   │   ├── Ingredients Tab
│   │   │   ├── GridContainer (columns = 8)
│   │   │   │   └── ItemSlot x 50 (instances)
│   │   │   └── ItemDetails (RichTextLabel)
│   │   │
│   │   ├── Potions Tab
│   │   │   ├── GridContainer
│   │   │   └── ItemDetails
│   │   │
│   │   └── Equipment Tab
│   │       └── EquipmentSlots...
│   │
│   └── CloseButton (Button)
```

**InventoryUI.gd:**
```gdscript
extends Control

@onready var ingredient_grid: GridContainer = $Panel/TabContainer/Ingredients/GridContainer
@onready var potion_grid: GridContainer = $Panel/TabContainer/Potions/GridContainer

var ingredient_slots: Array[Control] = []
var potion_slots: Array[Control] = []

func _ready() -> void:
    # Get all item slot references
    for child in ingredient_grid.get_children():
        if child is ItemSlot:
            ingredient_slots.append(child)

    # Connect to player data changes
    GameEvents.ingredient_gathered.connect(_on_ingredients_changed)
    GameEvents.potion_crafted.connect(_on_potions_changed)

    # Initially hidden
    hide()

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("inventory") and GameState.can_open_menus:
        toggle()

func toggle() -> void:
    if visible:
        close()
    else:
        open()

func open() -> void:
    refresh_display()
    show()
    GameState.is_inventory_open = true
    GameState.can_move = false
    GameEvents.inventory_opened.emit()

func close() -> void:
    hide()
    GameState.is_inventory_open = false
    if not GameState.is_in_dialogue:
        GameState.can_move = true

func refresh_display() -> void:
    # Update ingredient slots
    var ingredient_list = PlayerData.ingredients.keys()
    for i in range(ingredient_slots.size()):
        if i < ingredient_list.size():
            var ingredient_id = ingredient_list[i]
            var amount = PlayerData.ingredients[ingredient_id]
            ingredient_slots[i].set_item(ingredient_id, amount)
        else:
            ingredient_slots[i].clear()

    # Similar for potions...

func _on_ingredients_changed(_type: String, _amount: int) -> void:
    if visible:
        refresh_display()

func _on_potions_changed(_name: String, _quality: String) -> void:
    if visible:
        refresh_display()
```

**ItemSlot.tscn:**
```gdscript
# Individual inventory slot
extends PanelContainer
class_name ItemSlot

@onready var icon: TextureRect = $MarginContainer/VBoxContainer/Icon
@onready var count_label: Label = $MarginContainer/VBoxContainer/CountLabel
@onready var hover_tooltip: Control = $HoverTooltip

var item_id: String = ""
var item_count: int = 0
var item_data: Resource = null

func set_item(id: String, count: int) -> void:
    item_id = id
    item_count = count

    # Load item data (ingredient or potion)
    item_data = load("res://data/ingredients/" + id + ".tres")
    if item_data:
        icon.texture = item_data.icon
        count_label.text = str(count) if count > 1 else ""
        show()
    else:
        clear()

func clear() -> void:
    item_id = ""
    item_count = 0
    item_data = null
    icon.texture = null
    count_label.text = ""
    hide()

func _on_mouse_entered() -> void:
    if item_data:
        hover_tooltip.show_tooltip(item_data)

func _on_mouse_exited() -> void:
    hover_tooltip.hide()
```

---

## ⚗️ CRAFTING SYSTEM

### ESENS Parser Integration

**python/esens_parser.py** (simplified example):
```python
#!/usr/bin/env python3
import sys
import json

def parse_esens(notation):
    """
    Parse ESENS notation and return effect data
    Example: P+H30%10s.ST -> Player healing, 30HP, 10 seconds, stackable
    """
    result = {
        "target": "player" if notation[0] == "P" else "enemy",
        "effect_type": "",
        "magnitude": 0,
        "duration": 0,
        "flags": []
    }

    # Simple parsing (replace with your actual parser)
    if "+H" in notation:
        result["effect_type"] = "heal"
        # Extract magnitude...

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No notation provided"}))
        sys.exit(1)

    notation = sys.argv[1]
    result = parse_esens(notation)
    print(json.dumps(result))
```

**scripts/systems/ESENSParser.gd:**
```gdscript
extends Node

const PYTHON_SCRIPT_PATH = "res://python/esens_parser.py"

func parse(notation: String) -> Dictionary:
    # Call Python script
    var output = []
    var exit_code = OS.execute("python3", [PYTHON_SCRIPT_PATH, notation], output, true)

    if exit_code != 0:
        push_error("ESENS parser failed: " + str(output))
        return {}

    # Parse JSON response
    var json = JSON.new()
    var parse_result = json.parse(output[0])

    if parse_result != OK:
        push_error("Failed to parse ESENS output")
        return {}

    return json.data

# Example usage:
# var effects = ESENSParser.parse("P+H30%10s.ST")
# print(effects)  # {target: "player", effect_type: "heal", magnitude: 30, ...}
```

### Crafting Minigame

**CraftingUI.tscn structure:**
```
CraftingUI (Control, full screen)
├── RecipePanel (Panel)
│   ├── RecipeTitle (Label)
│   ├── IngredientList (VBoxContainer)
│   ├── SuccessChance (ProgressBar)
│   └── CraftButton (Button)
│
├── MinigamePanel (Panel)
│   └── MortarPestle (embedded scene)
│
└── ResultPanel (Panel, initially hidden)
    ├── PotionIcon (TextureRect)
    ├── QualityLabel (Label)
    └── ContinueButton (Button)
```

**Crafting Minigame (MortarPestle.gd):**
```gdscript
extends Control

signal step_completed(quality: float)  # 0.0 to 1.0
signal minigame_completed(overall_quality: float)

enum CraftingStep { GRIND, ADD_SAP, ADD_BERRIES, DECANT }

var current_step: CraftingStep = CraftingStep.GRIND
var step_quality: Array[float] = []

@onready var mortar: Sprite2D = $Mortar
@onready var pestle: Sprite2D = $Pestle
@onready var ingredient_visuals: Node2D = $IngredientVisuals

var is_grinding: bool = false
var grind_circles_completed: int = 0
var grind_smoothness: float = 1.0  # 1.0 = perfect, 0.0 = jerky

func start_minigame(recipe: RecipeResource) -> void:
    current_step = CraftingStep.GRIND
    step_quality.clear()
    show_step_instructions()

func _input(event: InputEvent) -> void:
    match current_step:
        CraftingStep.GRIND:
            handle_grinding_input(event)
        CraftingStep.ADD_SAP:
            handle_dragging_input(event, "sap")
        CraftingStep.ADD_BERRIES:
            handle_dragging_input(event, "berries")
        CraftingStep.DECANT:
            handle_tilting_input(event)

func handle_grinding_input(event: InputEvent) -> void:
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT:
            is_grinding = event.pressed
            if event.pressed:
                start_grinding()

    if event is InputEventMouseMotion and is_grinding:
        process_grinding_motion(event.relative)

func process_grinding_motion(motion: Vector2) -> void:
    # Calculate circular motion
    var angle = motion.angle()
    # Check if continuing circular motion...

    # Update visual feedback
    pestle.rotation += motion.length() * 0.01

    # Check completion
    if grind_circles_completed >= 3:
        complete_step(grind_smoothness)

func handle_dragging_input(event: InputEvent, ingredient_type: String) -> void:
    # Drag ingredient to mortar
    # On release over mortar: add ingredient with animation
    pass

func handle_tilting_input(event: InputEvent) -> void:
    # Tilt mortar to pour into vial
    # Track steadiness
    pass

func complete_step(quality: float) -> void:
    step_quality.append(quality)
    step_completed.emit(quality)

    # Move to next step
    if current_step < CraftingStep.DECANT:
        current_step += 1
        show_step_instructions()
    else:
        # Calculate overall quality
        var avg_quality = 0.0
        for q in step_quality:
            avg_quality += q
        avg_quality /= step_quality.size()

        minigame_completed.emit(avg_quality)

func show_step_instructions() -> void:
    match current_step:
        CraftingStep.GRIND:
            # Show "Click and drag in circles to grind"
            pass
        CraftingStep.ADD_SAP:
            # Show "Drag tree sap to mortar"
            pass
        # etc...
```

**CraftingSystem.gd:**
```gdscript
extends Node

func craft_potion(recipe_id: String, minigame_quality: float) -> Dictionary:
    var recipe: RecipeResource = load("res://data/recipes/" + recipe_id + ".tres")

    if not recipe:
        return {success: false, reason: "Recipe not found"}

    # Check ingredients
    for ingredient_id in recipe.ingredients.keys():
        var required_amount = recipe.ingredients[ingredient_id]
        if not PlayerData.has_ingredient(ingredient_id, required_amount):
            return {success: false, reason: "Missing ingredient: " + ingredient_id}

    # Calculate success chance
    var success_chance = calculate_success_chance(recipe, minigame_quality)

    # Roll for success
    var roll = randf()
    if roll > success_chance:
        # Failure - lose ingredients
        consume_ingredients(recipe)
        return {success: false, reason: "Crafting failed"}

    # Success - determine quality
    var quality_tier = determine_quality(minigame_quality, PlayerData.stats.precision)

    # Consume ingredients
    consume_ingredients(recipe)

    # Create potion
    var potion = create_potion(recipe, quality_tier)
    PlayerData.potions.append(potion)

    # Grant XP
    PlayerData.add_stat("precision", 10)
    PlayerData.add_stat("knowledge", 25)

    # Add recipe mastery
    PlayerData.add_recipe_mastery(recipe_id, 5)

    GameEvents.potion_crafted.emit(recipe.display_name, quality_tier)

    return {
        success: true,
        potion: potion,
        quality: quality_tier
    }

func calculate_success_chance(recipe: RecipeResource, minigame_quality: float) -> float:
    var base = recipe.base_success_chance / 100.0
    var precision_bonus = PlayerData.stats.precision / 200.0  # Max +50%
    var minigame_bonus = minigame_quality * 0.3  # Max +30%

    return clamp(base + precision_bonus + minigame_bonus, 0.0, 1.0)

func determine_quality(minigame_quality: float, precision_stat: int) -> String:
    var quality_score = (minigame_quality * 0.7) + (precision_stat / 100.0 * 0.3)

    if quality_score >= 0.9:
        return "masterwork"
    elif quality_score >= 0.75:
        return "exceptional"
    elif quality_score >= 0.6:
        return "fine"
    elif quality_score >= 0.4:
        return "standard"
    else:
        return "poor"

func consume_ingredients(recipe: RecipeResource) -> void:
    for ingredient_id in recipe.ingredients.keys():
        var amount = recipe.ingredients[ingredient_id]
        PlayerData.remove_ingredient(ingredient_id, amount)

func create_potion(recipe: RecipeResource, quality: String) -> Dictionary:
    return {
        "id": recipe.id,
        "name": recipe.display_name,
        "quality": quality,
        "effects": recipe.effects.duplicate(true),
        "created_date": GameState.current_day,
        "icon": recipe.icon
    }
```

---

## 👥 NPC & RELATIONSHIP SYSTEM

**NPCResource.gd:**
```gdscript
extends Resource
class_name NPCResource

@export var id: String = ""
@export var display_name: String = ""
@export var portrait_neutral: Texture2D
@export var portrait_happy: Texture2D
@export var portrait_sad: Texture2D
@export var portrait_angry: Texture2D
@export var portrait_surprised: Texture2D

# Big 5 Personality (scale: -1, 0, +1)
@export_range(-1, 1, 1) var openness: int = 0
@export_range(-1, 1, 1) var conscientiousness: int = 0
@export_range(-1, 1, 1) var extraversion: int = 0
@export_range(-1, 1, 1) var agreeableness: int = 0
@export_range(-1, 1, 1) var neuroticism: int = 0

@export var initial_affinity: float = 0.0
@export var dialogue_file: String = ""  # Path to .dialogue file
```

**NPCBase.gd:**
```gdscript
extends CharacterBody2D
class_name NPCBase

@export var npc_data: NPCResource

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var interaction_area: Area2D = $InteractionArea

var current_affinity: float = 0.0

func _ready() -> void:
    if npc_data:
        current_affinity = PlayerData.get_affinity(npc_data.id)

        # Set initial affinity if first meeting
        if current_affinity == 0.0 and npc_data.initial_affinity != 0.0:
            PlayerData.add_affinity(npc_data.id, npc_data.initial_affinity)
            current_affinity = npc_data.initial_affinity

func interact() -> void:
    if not npc_data:
        return

    # Load dialogue file
    var dialogue_resource = load(npc_data.dialogue_file)
    if dialogue_resource:
        # Determine which dialogue based on affinity
        var dialogue_title = get_dialogue_title()

        # Start dialogue
        var dialogue_box = get_node("/root/Main/DialogueBox")
        dialogue_box.start_dialogue(dialogue_resource, dialogue_title, npc_data.id)

func get_dialogue_title() -> String:
    # Choose dialogue based on current affinity
    current_affinity = PlayerData.get_affinity(npc_data.id)

    if current_affinity >= 3.0:
        return "friendly_chat"
    elif current_affinity >= 0.0:
        return "neutral_chat"
    else:
        return "hostile_chat"
```

**AffinitySystem.gd:**
```gdscript
extends Node

const DECAY_RATE = 0.5  # Per week
const DECAY_INTERVAL = 7  # Days

func process_affinity_decay() -> void:
    # Called weekly by GameState
    for npc_id in PlayerData.npc_affinity.keys():
        var current = PlayerData.npc_affinity[npc_id]

        # Decay toward 0
        if current > 0:
            PlayerData.add_affinity(npc_id, -DECAY_RATE)
        elif current < 0:
            PlayerData.add_affinity(npc_id, DECAY_RATE)

func calculate_affinity_change(npc_id: String, action_type: String) -> float:
    # Load NPC personality
    var npc_data: NPCResource = load("res://data/npcs/" + npc_id + ".tres")
    if not npc_data:
        return 0.0

    # Match action to personality reaction
    var change = 0.0

    match action_type:
        "innovative_potion":
            change += npc_data.openness * 1.0
            change -= npc_data.conscientiousness * 0.5

        "traditional_potion":
            change -= npc_data.openness * 0.5
            change += npc_data.conscientiousness * 0.5

        "gift_giving":
            change += npc_data.extraversion * 1.0
            change += npc_data.agreeableness * 0.5

        "haggling":
            change -= npc_data.agreeableness * 1.0
            change += npc_data.extraversion * 0.5

        "share_knowledge":
            change += npc_data.openness * 0.5
            change += npc_data.agreeableness * 0.5

    return change

# Example usage:
# var affinity_delta = AffinitySystem.calculate_affinity_change("ezekiel", "innovative_potion")
# PlayerData.add_affinity("ezekiel", affinity_delta)
```

---

## 🌿 GATHERING SYSTEM

**GatheringSpot.gd:**
```gdscript
extends Area2D
class_name GatheringSpot

@export var ingredient_id: String = "common_mushroom"
@export var min_yield: int = 2
@export var max_yield: int = 4
@export var respawn_time: float = 300.0  # 5 minutes
@export var glow_color: Color = Color.BLUE

@onready var sprite: Sprite2D = $Sprite2D
@onready var particles: CPUParticles2D = $GlowParticles
@onready var label: Label = $Label

var is_depleted: bool = false
var respawn_timer: float = 0.0

func _ready() -> void:
    # Setup visual
    particles.color = glow_color
    label.text = "[E] Gather"
    label.hide()

    # Setup interaction
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)

func _process(delta: float) -> void:
    if is_depleted:
        respawn_timer += delta
        if respawn_timer >= respawn_time:
            respawn()

func _on_body_entered(body: Node2D) -> void:
    if body is Player and not is_depleted:
        label.show()

func _on_body_exited(body: Node2D) -> void:
    if body is Player:
        label.hide()

func interact() -> void:
    if is_depleted:
        return

    # Calculate yield
    var yield_amount = randi_range(min_yield, max_yield)

    # Add to player inventory
    PlayerData.add_ingredient(ingredient_id, yield_amount)

    # Show notification
    GameEvents.emit_signal("notification_requested",
        "Gathered %d x %s" % [yield_amount, get_ingredient_name()],
        "success")

    # Play animation
    play_gather_animation()

    # Deplete
    is_depleted = true
    sprite.modulate = Color(0.5, 0.5, 0.5)
    particles.emitting = false
    label.hide()

    GameEvents.gathering_spot_depleted.emit(name)

func respawn() -> void:
    is_depleted = false
    respawn_timer = 0.0
    sprite.modulate = Color.WHITE
    particles.emitting = true

func get_ingredient_name() -> String:
    var ingredient: IngredientResource = load("res://data/ingredients/" + ingredient_id + ".tres")
    return ingredient.display_name if ingredient else ingredient_id

func play_gather_animation() -> void:
    # Tween sprite up and fade
    var tween = create_tween()
    tween.tween_property(sprite, "position:y", sprite.position.y - 20, 0.5)
    tween.parallel().tween_property(sprite, "modulate:a", 0.0, 0.5)
    await tween.finished
    sprite.position.y += 20
    sprite.modulate.a = 1.0
```

---

## 📊 STATS & PROGRESSION

**StatSystem.gd:**
```gdscript
extends Node

const STAT_CAPS = {
    "precision": 100,
    "knowledge": 100,
    "intuition": 100,
    "business": 100,
    "reputation": 100,
    "combat_instinct": 100
}

const STAT_THRESHOLDS = [25, 50, 75, 100]

func check_stat_threshold(stat_name: String, old_value: int, new_value: int) -> void:
    for threshold in STAT_THRESHOLDS:
        if old_value < threshold and new_value >= threshold:
            trigger_threshold_bonus(stat_name, threshold)

func trigger_threshold_bonus(stat_name: String, threshold: int) -> void:
    match stat_name:
        "precision":
            if threshold == 25:
                GameEvents.notification_requested.emit(
                    "Precision 25: +5% crafting success chance",
                    "progression"
                )
        "knowledge":
            if threshold == 50:
                GameEvents.notification_requested.emit(
                    "Knowledge 50: Can create recipe variants",
                    "progression"
                )
        # etc...
```

---

## 🎨 UI SYSTEM

### Minimal Persistent HUD

**HUD.tscn:**
```
HUD (CanvasLayer)
└── MarginContainer (margins: 10px all sides)
    ├── TopLeft (VBoxContainer)
    │   ├── DayLabel (Label) - "Day 1 - Morning"
    │   └── QuestTracker (RichTextLabel) - Active quest hints
    │
    ├── TopRight (VBoxContainer)
    │   └── QuickStats (HBoxContainer) - Mini stat indicators
    │
    └── BottomRight (VBoxContainer)
        └── InteractionPrompt (Label) - "[E] Talk" when near NPC
```

**HUD.gd:**
```gdscript
extends CanvasLayer

@onready var day_label: Label = $MarginContainer/TopLeft/DayLabel
@onready var interaction_prompt: Label = $MarginContainer/BottomRight/InteractionPrompt

func _ready() -> void:
    interaction_prompt.hide()
    update_day_label()

func update_day_label() -> void:
    day_label.text = "Day %d - %s" % [GameState.current_day, GameState.current_time.capitalize()]

func show_interaction_prompt(text: String) -> void:
    interaction_prompt.text = text
    interaction_prompt.show()

func hide_interaction_prompt() -> void:
    interaction_prompt.hide()
```

### Notification System

**NotificationManager.gd:**
```gdscript
extends Node

const NOTIFICATION_SCENE = preload("res://scenes/ui/notifications/Notification.tscn")

@onready var container: VBoxContainer = $CanvasLayer/NotificationContainer

func _ready() -> void:
    GameEvents.notification_requested.connect(_on_notification_requested)

func _on_notification_requested(message: String, type: String) -> void:
    var notification = NOTIFICATION_SCENE.instantiate()
    container.add_child(notification)
    notification.show_notification(message, type)
```

**Notification.tscn (individual popup):**
```gdscript
extends PanelContainer

@onready var label: Label = $MarginContainer/Label
@onready var icon: TextureRect = $MarginContainer/HBoxContainer/Icon

const DISPLAY_TIME = 3.0
const FADE_TIME = 0.5

func show_notification(message: String, type: String) -> void:
    label.text = message

    # Set color based on type
    match type:
        "success":
            modulate = Color.GREEN
        "error":
            modulate = Color.RED
        "progression":
            modulate = Color.GOLD
        _:
            modulate = Color.WHITE

    # Animate in
    modulate.a = 0.0
    var tween = create_tween()
    tween.tween_property(self, "modulate:a", 1.0, FADE_TIME)

    # Wait then fade out
    await get_tree().create_timer(DISPLAY_TIME).timeout
    tween = create_tween()
    tween.tween_property(self, "modulate:a", 0.0, FADE_TIME)
    await tween.finished

    queue_free()
```

---

## 🎬 SCENE TRANSITIONS

**Main.gd (root scene manager):**
```gdscript
extends Node

@onready var scene_container: Node = $SceneContainer
@onready var transition: ColorRect = $TransitionLayer/ColorRect

var current_scene: Node = null

func _ready() -> void:
    GameEvents.scene_transition_requested.connect(_on_scene_transition_requested)

    # Load initial scene (main menu)
    load_scene("res://scenes/main/MainMenu.tscn", false)

func _on_scene_transition_requested(scene_path: String) -> void:
    load_scene(scene_path, true)

func load_scene(scene_path: String, use_transition: bool = true) -> void:
    if use_transition:
        await fade_out()

    # Unload current scene
    if current_scene:
        current_scene.queue_free()
        await current_scene.tree_exited

    # Load new scene
    var new_scene = load(scene_path).instantiate()
    scene_container.add_child(new_scene)
    current_scene = new_scene

    # Update game state
    GameState.current_scene = scene_path

    if use_transition:
        await fade_in()

func fade_out() -> void:
    transition.show()
    var tween = create_tween()
    tween.tween_property(transition, "modulate:a", 1.0, 0.5)
    await tween.finished

func fade_in() -> void:
    var tween = create_tween()
    tween.tween_property(transition, "modulate:a", 0.0, 0.5)
    await tween.finished
    transition.hide()
```

---

## 📋 IMPLEMENTATION PHASES

### **Phase 1: Foundation (Weeks 1-2)**
1. Setup Godot 4.2 project
2. Create autoload singletons (GameEvents, GameState, PlayerData, SaveSystem)
3. Setup input map
4. Create basic Player controller with movement
5. Create one test location (Garden) with isometric tilemap
6. Test Y-sorting with player and objects

**Deliverable:** Player can walk around garden with proper depth sorting

---

### **Phase 2: Gathering & Inventory (Week 3)**
1. Create IngredientResource and data files
2. Implement GatheringSpot scene
3. Build InventoryUI with tabs
4. Test gathering → inventory → save/load cycle

**Deliverable:** Can gather ingredients and see them in inventory

---

### **Phase 3: Dialogue System (Week 4)**
1. Install Dialogue Manager plugin
2. Create NPCResource and NPCBase scene
3. Write first dialogue file (Rachel introduction)
4. Create DialogueBox wrapper with portraits
5. Test NPC interaction

**Deliverable:** Can talk to Rachel with portraits and choices

---

### **Phase 4: Crafting Minigame (Weeks 5-6)**
1. Create RecipeResource
2. Build CraftingUI interface
3. Implement MortarPestle minigame (grinding step)
4. Integrate ESENS parser (call Python)
5. Add remaining minigame steps
6. Connect to CraftingSystem logic

**Deliverable:** Full crafting loop working (gather → craft → get potion)

---

### **Phase 5: Relationships & Stats (Week 7)**
1. Implement AffinitySystem
2. Create JournalUI showing stats and relationships
3. Connect dialogue choices to affinity changes
4. Implement StatSystem with thresholds
5. Add progression notifications

**Deliverable:** Choices affect relationships, stats increase, journal tracks progress

---

### **Phase 6: All Locations (Week 8)**
1. Build remaining locations (Dorm, Classroom, Courtyard, Cart)
2. Create scene transition system
3. Add all NPCs (Ezekiel, Miriam, Thornwood)
4. Write all dialogue files

**Deliverable:** All 5 locations accessible and populated

---

### **Phase 7: Content & Polish (Weeks 9-10)**
1. Write all 60 minutes of content
2. Create all art assets (or integrate placeholders)
3. Add music and SFX
4. Implement notification system
5. Polish UI/UX
6. Optimize performance

**Deliverable:** Complete 60-minute playable demo

---

### **Phase 8: Testing & Iteration (Weeks 11-12)**
1. Internal playtesting
2. Bug fixing
3. Friends & family testing
4. Iteration based on feedback
5. External playtesting
6. Final polish

**Deliverable:** Polished, tested MVP ready for investors/publishers

---

## 🔧 GODOT PROJECT SETTINGS

### Key Settings to Configure

**Project Settings → General:**
- **Application → Run → Main Scene:** `res://scenes/main/Main.tscn`
- **Display → Window → Size → Width:** 1920
- **Display → Window → Size → Height:** 1080
- **Display → Window → Stretch → Mode:** canvas_items
- **Display → Window → Stretch → Aspect:** keep

**Project Settings → Rendering:**
- **Textures → Canvas Textures → Default Texture Filter:** Nearest (for pixel art)
- **2D → Snap → Snap 2D Transforms to Pixel:** On
- **2D → Snap → Snap 2D Vertices to Pixel:** On

**Project Settings → Audio:**
- Create audio buses:
  - Master
  - Music (child of Master)
  - SFX (child of Master)
  - UI (child of Master)

**Project Settings → Autoload:**
Add in this order:
1. GameEvents → `res://autoload/GameEvents.gd`
2. GameState → `res://autoload/GameState.gd`
3. PlayerData → `res://autoload/PlayerData.gd`
4. SaveSystem → `res://autoload/SaveSystem.gd`
5. AudioManager → `res://autoload/AudioManager.gd`

---

## 📦 EXPORT SETTINGS

### PC Export (Windows/Mac/Linux)

**Export Presets:**
1. Create preset for each platform
2. **Runnable:** Check "Export with Debug"
3. **Resources → Export Mode:** Export selected resources (smaller builds)
4. Include `python/` folder in export

### Web Export (HTML5)

**Requirements:**
- Emscripten toolchain
- Python script won't work in browser - need to port ESENS parser to GDScript for web builds

**Export Settings:**
- **HTML → Export Type:** Regular
- **Variant → Extensions Support:** Enable if needed
- Test locally before deploying

---

## 🎯 SUCCESS METRICS

### Technical Goals
- [ ] 60 FPS on mid-range PC (2019+)
- [ ] Load times < 3 seconds between scenes
- [ ] Memory usage < 500MB
- [ ] No crashes during 60-minute playthrough
- [ ] Save/load works 100% reliably

### Gameplay Goals
- [ ] All 5 locations playable
- [ ] 4 NPCs with full dialogue and affinity tracking
- [ ] Gathering system works smoothly
- [ ] Crafting minigame is fun (playtest validated)
- [ ] Full gameplay loop (gather → craft → social) proven

### Content Goals
- [ ] 60 minutes of content
- [ ] 1 major choice (Ezekiel dilemma) with 4 outcomes
- [ ] 1 complete recipe (Simple Healing Tonic)
- [ ] 5 ingredient types collectible
- [ ] All stats and progression tracking working

---

## 📚 ADDITIONAL RESOURCES

### Godot 4 Tutorials Referenced
- **Isometric Tilemaps:** nightquestgames.com/introducing-isometric-tilemaps-in-godot/
- **Dialogue Manager:** github.com/nathanhoad/godot_dialogue_manager
- **Save System:** gdquest.com/library/save_game_godot4/
- **Event Bus:** gdquest.com/tutorial/godot/design-patterns/event-bus-singleton/

### Art Asset Sources (for MVP placeholders)
- **Kenny.nl** - Free game assets
- **OpenGameArt.org** - Community assets
- **itch.io** - Free/paid asset packs
- **Depth_strider** - Free isometric practice tiles

---

## 🎓 GODOT BEST PRACTICES SUMMARY

1. **Use Signals over direct function calls** when possible
2. **Use Resources for data** (ingredients, recipes, NPCs)
3. **Event Bus for global events only** - don't overuse
4. **Autoloads for true singletons** - keep minimal
5. **Scene composition over inheritance** when possible
6. **@onready for node references** instead of get_node in _ready
7. **@export for inspector editing** - makes designers happy
8. **Use typed GDScript** (var health: int = 100) for better errors
9. **Group related nodes** under common parents for organization
10. **Comment complex systems** - especially for Big 5 personality logic

---

## ✅ FINAL CHECKLIST

Before considering MVP complete:

- [ ] All 5 locations built and connected
- [ ] Player can move with WASD/gamepad
- [ ] Gathering spots work and respawn
- [ ] Inventory opens and displays items correctly
- [ ] Crafting minigame is playable and fun
- [ ] At least 1 potion can be crafted start to finish
- [ ] Dialogue system works with portraits
- [ ] NPC affinity changes based on choices
- [ ] Stats increase and thresholds trigger
- [ ] Journal displays all data correctly
- [ ] Auto-save and manual save both work
- [ ] Load game restores all data
- [ ] Scene transitions are smooth
- [ ] Audio plays correctly (music + SFX)
- [ ] No major bugs or crashes
- [ ] 60-minute playthrough is achievable
- [ ] Playtested by at least 5 people
- [ ] Feedback incorporated
- [ ] Builds successfully for PC + Web

---

**END OF IMPLEMENTATION PLAN**

This document provides the high-level architecture. Implementation details for each system should be expanded as needed during development. Iterate and adjust based on playtesting feedback!
