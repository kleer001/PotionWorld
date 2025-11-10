extends Node2D
## Ingredient Garden Scene
##
## First playable location where player learns gathering.
## Contains multiple gathering spots and serves as the tutorial area.

@onready var player: Player = $Environment/Characters/Player
@onready var camera: Camera2D = $Environment/Characters/Player/Camera2D


func _ready() -> void:
	print("IngredientGarden: Scene loaded")

	# Set as current scene in GameState
	GameState.current_scene = scene_file_path
	GameState.current_phase = GameState.GamePhase.GAMEPLAY

	# Play garden music
	GameEvents.music_change_requested.emit("garden_theme")

	# Enable player controls
	GameState.can_move = true
	GameState.can_interact = true
	GameState.can_open_menus = true


func _exit_tree() -> void:
	print("IngredientGarden: Scene unloaded")
