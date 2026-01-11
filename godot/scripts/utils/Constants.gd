extends Node
## Global game constants
##
## Define all constant values here for easy tweaking.
## Accessible globally as Constants.STAT_CAP, etc.

# Stat caps and thresholds
const STAT_CAP: int = 100
const STAT_THRESHOLDS: Array[int] = [25, 50, 75, 100]

# Affinity limits
const AFFINITY_MIN: float = -5.0
const AFFINITY_MAX: float = 5.0
const AFFINITY_DECAY_RATE: float = 0.5  # Per week
const AFFINITY_DECAY_INTERVAL: int = 7  # Days

# Recipe mastery
const MASTERY_CAP: int = 100
const MASTERY_NOVICE: int = 20
const MASTERY_COMPETENT: int = 40
const MASTERY_PROFICIENT: int = 60
const MASTERY_EXPERT: int = 80
const MASTERY_MASTER: int = 100

# Crafting
const BASE_CRAFTING_SUCCESS: float = 0.5  # 50%
const QUALITY_TIERS: Array[String] = ["poor", "standard", "fine", "exceptional", "masterwork"]

# Inventory
const INVENTORY_STARTING_CAPACITY: int = 50
const POTION_STARTING_CAPACITY: int = 20

# Save system
const MAX_MANUAL_SAVE_SLOTS: int = 10
const AUTOSAVE_INTERVAL: float = 300.0  # 5 minutes in seconds

# Scene paths
const SCENE_MAIN_MENU: String = "res://scenes/main/MainMenu.tscn"
const SCENE_GARDEN: String = "res://scenes/locations/garden/IngredientGarden.tscn"
const SCENE_DORM: String = "res://scenes/locations/dorm/DormRoom.tscn"
const SCENE_CLASSROOM: String = "res://scenes/locations/classroom/Classroom.tscn"
const SCENE_COURTYARD: String = "res://scenes/locations/courtyard/Courtyard.tscn"
const SCENE_CART: String = "res://scenes/locations/cart/CartRide.tscn"

# Player
const PLAYER_MOVE_SPEED: float = 150.0
const PLAYER_INTERACTION_RANGE: float = 32.0

# Gathering
const GATHERING_DEFAULT_RESPAWN: float = 300.0  # 5 minutes in seconds
const GATHERING_MIN_YIELD: int = 2
const GATHERING_MAX_YIELD: int = 4

# Big 5 Personality scale
const PERSONALITY_LOW: int = -1
const PERSONALITY_MODERATE: int = 0
const PERSONALITY_HIGH: int = 1

# Time
const DAY_LENGTH_SECONDS: float = 1200.0  # 20 minutes per in-game day
const TIMES_OF_DAY: Array[String] = ["morning", "afternoon", "evening", "night"]

# Audio
const MUSIC_FADE_DURATION: float = 1.0
const DEFAULT_PITCH_VARIATION: float = 0.1

# Debug
const DEBUG_MODE: bool = true
const SHOW_FPS: bool = false
const LOG_EVENTS: bool = true
