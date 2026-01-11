extends Node
## Manages all persistent player data (stats, inventory, relationships, etc.)
##
## This singleton stores all data that should be saved to disk.
## All saveable data lives here, and SaveSystem reads from this.
##
## Usage:
##   PlayerData.add_ingredient("common_mushroom", 3)
##   PlayerData.add_stat("precision", 10)
##   PlayerData.add_affinity("rachel", 0.5)

# Character creation
var player_name: String = ""
var player_appearance: int = 0  # Index to appearance preset (0-3)
var player_background: String = ""  # "rural_healer", "city_merchant", etc.

# Stats (0-100)
var stats: Dictionary = {
	"precision": 0,
	"knowledge": 0,
	"intuition": 0,
	"business": 0,
	"reputation": 0,
	"combat_instinct": 0
}

# Inventory - Ingredients
## Key: ingredient_id (String), Value: amount (int)
var ingredients: Dictionary = {}

# Inventory - Potions
## Array of potion dictionaries with properties
var potions: Array[Dictionary] = []

# Inventory - Equipment
## Key: equipment_slot (String), Value: equipment_id (String)
var equipment: Dictionary = {
	"mortar_pestle": "basic",
	"cauldron": "",
	"vials": "basic",
	"travel_gear": ""
}

# Recipes
## Key: recipe_id (String), Value: mastery_level (int 0-100)
var known_recipes: Dictionary = {}

## Array of recipe IDs that have been discovered but not mastered
var discovered_recipes: Array[String] = []

# Relationships - NPC Affinity
## Key: npc_id (String), Value: affinity (float -5.0 to 5.0)
var npc_affinity: Dictionary = {}

# Relationships - NPC Memories
## Key: npc_id (String), Value: Array of memory strings
var npc_memories: Dictionary = {}

# Choices & Traits
## Array of choice records
var choices_made: Array[Dictionary] = []

## Array of unlocked trait names
var unlocked_traits: Array[String] = []

## Personality flags from choices
var personality_flags: Dictionary = {
	"openness": 0,
	"conscientiousness": 0,
	"extraversion": 0,
	"agreeableness": 0,
	"neuroticism": 0
}

# Progression
var total_playtime: float = 0.0
var current_season: int = 0  # 0 for demo
var completed_quests: Array[String] = []
var active_quests: Array[String] = []


func _ready() -> void:
	print("PlayerData: Player data manager initialized")


## Add ingredient to inventory
func add_ingredient(ingredient_id: String, amount: int) -> void:
	if ingredients.has(ingredient_id):
		ingredients[ingredient_id] += amount
	else:
		ingredients[ingredient_id] = amount

	GameEvents.ingredient_gathered.emit(ingredient_id, amount)
	print("PlayerData: Added %d x %s (total: %d)" % [amount, ingredient_id, ingredients[ingredient_id]])


## Remove ingredient from inventory
## Returns true if successful, false if not enough
func remove_ingredient(ingredient_id: String, amount: int) -> bool:
	if not ingredients.has(ingredient_id) or ingredients[ingredient_id] < amount:
		return false

	ingredients[ingredient_id] -= amount
	if ingredients[ingredient_id] <= 0:
		ingredients.erase(ingredient_id)

	return true


## Check if player has ingredient
func has_ingredient(ingredient_id: String, amount: int = 1) -> bool:
	return ingredients.get(ingredient_id, 0) >= amount


## Get ingredient count
func get_ingredient_count(ingredient_id: String) -> int:
	return ingredients.get(ingredient_id, 0)


## Add potion to inventory
func add_potion(potion_data: Dictionary) -> void:
	potions.append(potion_data)
	print("PlayerData: Added potion: %s (Quality: %s)" % [potion_data.get("name", "Unknown"), potion_data.get("quality", "Unknown")])


## Remove potion from inventory
func remove_potion(index: int) -> bool:
	if index >= 0 and index < potions.size():
		potions.remove_at(index)
		return true
	return false


## Add stat points and trigger events
func add_stat(stat_name: String, amount: int) -> void:
	if not stats.has(stat_name):
		push_error("PlayerData: Unknown stat: " + stat_name)
		return

	var old_value: int = stats[stat_name]
	stats[stat_name] = min(stats[stat_name] + amount, 100)  # Cap at 100
	var new_value: int = stats[stat_name]

	if old_value != new_value:
		GameEvents.stat_increased.emit(stat_name, old_value, new_value)
		GameEvents.xp_gained.emit(stat_name, amount)

		# Check thresholds (25, 50, 75, 100)
		for threshold in [25, 50, 75, 100]:
			if old_value < threshold and new_value >= threshold:
				GameEvents.level_threshold_reached.emit(stat_name, threshold)
				print("PlayerData: %s reached threshold %d!" % [stat_name, threshold])


## Get stat value
func get_stat(stat_name: String) -> int:
	return stats.get(stat_name, 0)


## Add affinity with NPC
func add_affinity(npc_id: String, amount: float) -> void:
	var old_value: float = npc_affinity.get(npc_id, 0.0)
	var new_value: float = clampf(old_value + amount, -5.0, 5.0)
	npc_affinity[npc_id] = new_value

	GameEvents.affinity_changed.emit(npc_id, old_value, new_value)

	# Log significant changes
	if abs(amount) >= 0.5:
		print("PlayerData: %s affinity changed: %.1f -> %.1f (%.1f)" % [npc_id, old_value, new_value, amount])


## Get affinity with NPC
func get_affinity(npc_id: String) -> float:
	return npc_affinity.get(npc_id, 0.0)


## Get affinity level name
func get_affinity_level(npc_id: String) -> String:
	var affinity: float = get_affinity(npc_id)

	if affinity >= 4.0:
		return "Devoted"
	elif affinity >= 3.0:
		return "Loyal"
	elif affinity >= 2.0:
		return "Friendly"
	elif affinity >= 1.0:
		return "Warm"
	elif affinity > -1.0:
		return "Neutral"
	elif affinity > -2.0:
		return "Cool"
	elif affinity > -3.0:
		return "Unfriendly"
	elif affinity > -4.0:
		return "Hostile"
	else:
		return "Nemesis"


## Add memory for NPC
func add_npc_memory(npc_id: String, memory: String) -> void:
	if not npc_memories.has(npc_id):
		npc_memories[npc_id] = []

	npc_memories[npc_id].append(memory)


## Learn a recipe
func learn_recipe(recipe_id: String) -> void:
	if not known_recipes.has(recipe_id):
		known_recipes[recipe_id] = 0  # Novice mastery (0/100)
		GameEvents.recipe_learned.emit(recipe_id)
		print("PlayerData: Learned recipe: %s" % recipe_id)


## Add recipe mastery
func add_recipe_mastery(recipe_id: String, amount: int) -> void:
	if not known_recipes.has(recipe_id):
		push_error("PlayerData: Cannot add mastery to unknown recipe: " + recipe_id)
		return

	var old_level: int = known_recipes[recipe_id]
	known_recipes[recipe_id] = min(known_recipes[recipe_id] + amount, 100)
	var new_level: int = known_recipes[recipe_id]

	if old_level != new_level:
		GameEvents.recipe_mastery_increased.emit(recipe_id, new_level)


## Get recipe mastery
func get_recipe_mastery(recipe_id: String) -> int:
	return known_recipes.get(recipe_id, 0)


## Get recipe mastery level name
func get_recipe_mastery_name(recipe_id: String) -> String:
	var mastery: int = get_recipe_mastery(recipe_id)

	if mastery >= 81:
		return "Master"
	elif mastery >= 61:
		return "Expert"
	elif mastery >= 41:
		return "Proficient"
	elif mastery >= 21:
		return "Competent"
	else:
		return "Novice"


## Record a choice
func make_choice(choice_id: String, option_selected: String) -> void:
	choices_made.append({
		"choice_id": choice_id,
		"option": option_selected,
		"day": GameState.current_day
	})
	GameEvents.dialogue_choice_made.emit(choice_id, option_selected)


## Check if choice was made
func has_made_choice(choice_id: String) -> bool:
	for choice in choices_made:
		if choice["choice_id"] == choice_id:
			return true
	return false


## Get option selected for a choice
func get_choice_option(choice_id: String) -> String:
	for choice in choices_made:
		if choice["choice_id"] == choice_id:
			return choice["option"]
	return ""


## Unlock a trait
func unlock_trait(trait_name: String) -> void:
	if not trait_name in unlocked_traits:
		unlocked_traits.append(trait_name)
		GameEvents.trait_unlocked.emit(trait_name)
		print("PlayerData: Unlocked trait: %s" % trait_name)


## Check if trait is unlocked
func has_trait(trait_name: String) -> bool:
	return trait_name in unlocked_traits


## Reset all data (for new game)
func reset_data() -> void:
	player_name = ""
	player_appearance = 0
	player_background = ""

	stats = {
		"precision": 0,
		"knowledge": 0,
		"intuition": 0,
		"business": 0,
		"reputation": 0,
		"combat_instinct": 0
	}

	ingredients.clear()
	potions.clear()
	equipment = {
		"mortar_pestle": "basic",
		"cauldron": "",
		"vials": "basic",
		"travel_gear": ""
	}

	known_recipes.clear()
	discovered_recipes.clear()
	npc_affinity.clear()
	npc_memories.clear()
	choices_made.clear()
	unlocked_traits.clear()

	personality_flags = {
		"openness": 0,
		"conscientiousness": 0,
		"extraversion": 0,
		"agreeableness": 0,
		"neuroticism": 0
	}

	total_playtime = 0.0
	current_season = 0
	completed_quests.clear()
	active_quests.clear()

	print("PlayerData: All data reset for new game")
