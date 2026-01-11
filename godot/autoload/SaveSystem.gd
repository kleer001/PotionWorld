extends Node
## Handles saving and loading game data
##
## Uses Godot's Resource system for easy serialization.
## Auto-saves on certain triggers, plus manual save slots.
##
## Usage:
##   SaveSystem.save_game(-1)  # Auto-save
##   SaveSystem.save_game(1)   # Manual save to slot 1
##   SaveSystem.load_game(1)   # Load from slot 1

const SAVE_DIR: String = "user://saves/"
const AUTO_SAVE_FILE: String = "autosave.tres"
const MANUAL_SAVE_PREFIX: String = "manual_"
const SAVE_EXTENSION: String = ".tres"

var current_save_slot: int = -1  # -1 for autosave, 0+ for manual slots


func _ready() -> void:
	print("SaveSystem: Save/load manager initialized")

	# Create save directory if it doesn't exist
	if not DirAccess.dir_exists_absolute(SAVE_DIR):
		DirAccess.make_dir_absolute(SAVE_DIR)
		print("SaveSystem: Created save directory at: " + SAVE_DIR)

	# Connect to events for auto-save triggers
	GameEvents.scene_transition_completed.connect(_on_scene_transition)
	GameEvents.potion_crafted.connect(_on_potion_crafted)


## Save game to specified slot
## @param slot: -1 for autosave, 0+ for manual slots
## @return: true if successful
func save_game(slot: int = -1) -> bool:
	print("SaveSystem: Saving game to slot %d..." % slot)

	var save_data := SaveData.new()

	# Populate save_data from PlayerData
	save_data.player_name = PlayerData.player_name
	save_data.player_appearance = PlayerData.player_appearance
	save_data.player_background = PlayerData.player_background

	save_data.stats = PlayerData.stats.duplicate(true)
	save_data.ingredients = PlayerData.ingredients.duplicate(true)
	save_data.potions = PlayerData.potions.duplicate(true)
	save_data.equipment = PlayerData.equipment.duplicate(true)

	save_data.known_recipes = PlayerData.known_recipes.duplicate(true)
	save_data.discovered_recipes = PlayerData.discovered_recipes.duplicate(true)

	save_data.npc_affinity = PlayerData.npc_affinity.duplicate(true)
	save_data.npc_memories = PlayerData.npc_memories.duplicate(true)

	save_data.choices_made = PlayerData.choices_made.duplicate(true)
	save_data.unlocked_traits = PlayerData.unlocked_traits.duplicate(true)
	save_data.personality_flags = PlayerData.personality_flags.duplicate(true)

	save_data.total_playtime = PlayerData.total_playtime + GameState.real_time_played
	save_data.current_season = PlayerData.current_season
	save_data.completed_quests = PlayerData.completed_quests.duplicate(true)
	save_data.active_quests = PlayerData.active_quests.duplicate(true)

	# Add metadata
	save_data.save_timestamp = Time.get_datetime_string_from_system()
	save_data.current_day = GameState.current_day
	save_data.current_time = GameState.current_time
	save_data.current_scene = GameState.current_scene

	# Determine save path
	var save_path: String = _get_save_path(slot)

	# Save using ResourceSaver
	var result := ResourceSaver.save(save_data, save_path)

	if result == OK:
		current_save_slot = slot
		GameEvents.game_saved.emit(slot)
		print("SaveSystem: Game saved successfully to: " + save_path)
		return true
	else:
		var error_msg := "Failed to save game (error code: %d)" % result
		push_error("SaveSystem: " + error_msg)
		GameEvents.save_failed.emit(error_msg)
		return false


## Load game from specified slot
## @param slot: -1 for autosave, 0+ for manual slots
## @return: true if successful
func load_game(slot: int = -1) -> bool:
	print("SaveSystem: Loading game from slot %d..." % slot)

	var save_path: String = _get_save_path(slot)

	if not FileAccess.file_exists(save_path):
		var error_msg := "Save file does not exist: " + save_path
		push_error("SaveSystem: " + error_msg)
		GameEvents.load_failed.emit(error_msg)
		return false

	# Load using ResourceLoader
	var save_data: SaveData = ResourceLoader.load(save_path)

	if save_data == null:
		var error_msg := "Failed to load save file: " + save_path
		push_error("SaveSystem: " + error_msg)
		GameEvents.load_failed.emit(error_msg)
		return false

	# Restore PlayerData
	PlayerData.player_name = save_data.player_name
	PlayerData.player_appearance = save_data.player_appearance
	PlayerData.player_background = save_data.player_background

	PlayerData.stats = save_data.stats.duplicate(true)
	PlayerData.ingredients = save_data.ingredients.duplicate(true)
	PlayerData.potions = save_data.potions.duplicate(true)
	PlayerData.equipment = save_data.equipment.duplicate(true)

	PlayerData.known_recipes = save_data.known_recipes.duplicate(true)
	PlayerData.discovered_recipes = save_data.discovered_recipes.duplicate(true)

	PlayerData.npc_affinity = save_data.npc_affinity.duplicate(true)
	PlayerData.npc_memories = save_data.npc_memories.duplicate(true)

	PlayerData.choices_made = save_data.choices_made.duplicate(true)
	PlayerData.unlocked_traits = save_data.unlocked_traits.duplicate(true)
	PlayerData.personality_flags = save_data.personality_flags.duplicate(true)

	PlayerData.total_playtime = save_data.total_playtime
	PlayerData.current_season = save_data.current_season
	PlayerData.completed_quests = save_data.completed_quests.duplicate(true)
	PlayerData.active_quests = save_data.active_quests.duplicate(true)

	# Restore GameState
	GameState.current_day = save_data.current_day
	GameState.current_time = save_data.current_time

	current_save_slot = slot
	GameEvents.game_loaded.emit(slot)
	print("SaveSystem: Game loaded successfully from: " + save_path)

	# Request scene transition to saved location
	if save_data.current_scene != "":
		GameEvents.scene_transition_requested.emit(save_data.current_scene)

	return true


## Get save file information without loading the whole file
## @return: Dictionary with save info, or empty dict if save doesn't exist
func get_save_info(slot: int = -1) -> Dictionary:
	var save_path: String = _get_save_path(slot)

	if not FileAccess.file_exists(save_path):
		return {}

	var save_data: SaveData = ResourceLoader.load(save_path)
	if save_data == null:
		return {}

	return {
		"player_name": save_data.player_name,
		"timestamp": save_data.save_timestamp,
		"playtime": save_data.total_playtime,
		"playtime_formatted": _format_playtime(save_data.total_playtime),
		"day": save_data.current_day,
		"time": save_data.current_time,
		"scene": save_data.current_scene,
		"game_version": save_data.game_version
	}


## Check if save exists for slot
func has_save(slot: int = -1) -> bool:
	var save_path: String = _get_save_path(slot)
	return FileAccess.file_exists(save_path)


## Delete save file for slot
func delete_save(slot: int = -1) -> bool:
	var save_path: String = _get_save_path(slot)

	if not FileAccess.file_exists(save_path):
		return false

	var result := DirAccess.remove_absolute(save_path)
	if result == OK:
		print("SaveSystem: Deleted save file: " + save_path)
		return true
	else:
		push_error("SaveSystem: Failed to delete save file: " + save_path)
		return false


## Get list of all available manual save slots (0-9)
func get_available_saves() -> Array[int]:
	var available: Array[int] = []

	# Check autosave
	if has_save(-1):
		available.append(-1)

	# Check manual slots 0-9
	for i in range(10):
		if has_save(i):
			available.append(i)

	return available


## Get path for save slot
func _get_save_path(slot: int) -> String:
	if slot == -1:
		return SAVE_DIR + AUTO_SAVE_FILE
	else:
		return SAVE_DIR + MANUAL_SAVE_PREFIX + str(slot) + SAVE_EXTENSION


## Format playtime seconds into readable string
func _format_playtime(seconds: float) -> String:
	var hours := int(seconds / 3600)
	var minutes := int((seconds - hours * 3600) / 60)

	if hours > 0:
		return "%d hr %d min" % [hours, minutes]
	else:
		return "%d min" % minutes


# Auto-save event handlers
func _on_scene_transition() -> void:
	# Auto-save after scene transitions
	save_game(-1)


func _on_potion_crafted(_potion_name: String, _quality: String) -> void:
	# Auto-save after successful crafting
	save_game(-1)
