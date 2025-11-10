extends Node
## Global event bus using signals for decoupled communication
##
## This singleton provides a central place for all game-wide events.
## Systems emit signals here and other systems listen to them without
## needing direct references to each other.
##
## Usage:
##   Emit: GameEvents.ingredient_gathered.emit("common_mushroom", 3)
##   Listen: GameEvents.ingredient_gathered.connect(_on_ingredient_gathered)

# Gathering events
signal ingredient_gathered(ingredient_id: String, amount: int)
signal gathering_spot_depleted(spot_id: String)
signal gathering_spot_respawned(spot_id: String)

# Crafting events
signal potion_crafted(potion_name: String, quality: String)
signal crafting_started(recipe_id: String)
signal crafting_failed(reason: String)
signal recipe_learned(recipe_id: String)
signal recipe_mastery_increased(recipe_id: String, new_level: int)

# Relationship events
signal affinity_changed(npc_id: String, old_value: float, new_value: float)
signal dialogue_started(npc_id: String)
signal dialogue_ended(npc_id: String)
signal dialogue_choice_made(choice_id: String, option_selected: String)
signal trait_unlocked(trait_name: String)

# Progression events
signal stat_increased(stat_name: String, old_value: int, new_value: int)
signal xp_gained(stat_name: String, amount: int)
signal level_threshold_reached(stat_name: String, threshold: int)

# UI events
signal inventory_opened()
signal inventory_closed()
signal journal_opened()
signal journal_closed()
signal notification_requested(message: String, notification_type: String)

# Scene events
signal scene_transition_requested(scene_path: String)
signal scene_transition_started()
signal scene_transition_completed()
signal cutscene_started(cutscene_id: String)
signal cutscene_ended(cutscene_id: String)

# Save/Load events
signal game_saved(slot: int)
signal game_loaded(slot: int)
signal save_failed(reason: String)
signal load_failed(reason: String)

# Time events
signal day_changed(new_day: int)
signal time_of_day_changed(new_time: String)

# Audio events
signal music_change_requested(music_name: String)
signal sfx_play_requested(sfx_name: String)


func _ready() -> void:
	# Log that the event bus is ready
	print("GameEvents: Event bus initialized")
