extends Resource
class_name SaveData
## Resource class for save game data
##
## This is used by SaveSystem to serialize player data to disk.
## Godot's Resource system handles type conversion automatically.

# Character creation
@export var player_name: String = ""
@export var player_appearance: int = 0
@export var player_background: String = ""

# Stats
@export var stats: Dictionary = {}

# Inventory
@export var ingredients: Dictionary = {}
@export var potions: Array[Dictionary] = []
@export var equipment: Dictionary = {}

# Recipes
@export var known_recipes: Dictionary = {}
@export var discovered_recipes: Array[String] = []

# Relationships
@export var npc_affinity: Dictionary = {}
@export var npc_memories: Dictionary = {}

# Choices & Traits
@export var choices_made: Array[Dictionary] = []
@export var unlocked_traits: Array[String] = []
@export var personality_flags: Dictionary = {}

# Progression
@export var total_playtime: float = 0.0
@export var current_season: int = 0
@export var completed_quests: Array[String] = []
@export var active_quests: Array[String] = []

# Save metadata
@export var save_timestamp: String = ""
@export var game_version: String = "0.1.0-mvp"
@export var current_day: int = 1
@export var current_time: String = "morning"
@export var current_scene: String = ""
