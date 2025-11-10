extends Resource
class_name IngredientResource
## Resource class for ingredient data
##
## Each ingredient type is defined as a separate .tres resource file
## that uses this class. Properties are editable in the Inspector.
##
## Usage:
##   var ingredient: IngredientResource = load("res://data/ingredients/common_mushroom.tres")
##   print(ingredient.display_name)  # "Common Mushroom"

@export_group("Basic Info")
@export var id: String = ""
@export var display_name: String = ""
@export_multiline var description: String = ""
@export var icon: Texture2D

@export_group("Classification")
@export_enum("Common", "Uncommon", "Rare", "Very Rare", "Legendary") var rarity: String = "Common"
@export_enum("Root", "Mushroom", "Berry", "Crystal", "Sap", "Seed", "Mineral", "Insect", "Oil", "Spore", "Feather", "Honey", "Scale", "Bone", "Flower", "Lichen", "Fruit") var category: String = "Mushroom"

@export_group("Visual")
@export var glow_color: Color = Color.WHITE
@export var particle_color: Color = Color.WHITE

@export_group("Economy")
@export var base_value: int = 5
@export var weight: float = 0.1

@export_group("Properties")
## Array of property strings like "healing", "binding", "energy", "transform", etc.
@export var properties: Array[String] = []

## Does this ingredient degrade over time?
@export var degrades: bool = false
@export var degradation_time: float = 0.0  # In game days

@export_group("Lore")
@export_multiline var lore: String = ""
@export var discovered_by: String = ""  # Historical flavor text


## Get rarity as integer (0-4)
func get_rarity_level() -> int:
	match rarity:
		"Common":
			return 0
		"Uncommon":
			return 1
		"Rare":
			return 2
		"Very Rare":
			return 3
		"Legendary":
			return 4
		_:
			return 0


## Get color based on rarity
func get_rarity_color() -> Color:
	match rarity:
		"Common":
			return Color.WHITE
		"Uncommon":
			return Color(0.3, 1.0, 0.3)  # Green
		"Rare":
			return Color(0.3, 0.6, 1.0)  # Blue
		"Very Rare":
			return Color(0.8, 0.3, 1.0)  # Purple
		"Legendary":
			return Color(1.0, 0.6, 0.0)  # Orange
		_:
			return Color.WHITE


## Check if has specific property
func has_property(property_name: String) -> bool:
	return property_name in properties
