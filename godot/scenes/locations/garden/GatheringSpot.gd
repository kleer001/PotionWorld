extends Node2D
class_name GatheringSpot
## Gathering spot for ingredients
##
## Player walks up and presses E to gather.
## Respawns after a configurable timer.

@export_group("Ingredient Settings")
@export var ingredient_id: String = "common_mushroom"
@export var min_yield: int = 2
@export var max_yield: int = 4
@export var respawn_time: float = 300.0  # 5 minutes

@export_group("Visual Settings")
@export var glow_color: Color = Color(0.5, 0.8, 1.0, 0.8)

@onready var sprite: Sprite2D = $Sprite2D
@onready var particles: CPUParticles2D = $GlowParticles
@onready var interaction_area: Area2D = $InteractionArea
@onready var collision_shape: CollisionShape2D = $InteractionArea/CollisionShape2D

var is_depleted: bool = false
var respawn_timer: float = 0.0
var ingredient_data: IngredientResource = null


func _ready() -> void:
	# Load ingredient data
	var ingredient_path := "res://data/ingredients/" + ingredient_id + ".tres"
	if FileAccess.file_exists(ingredient_path):
		ingredient_data = load(ingredient_path)

		if ingredient_data and particles:
			# Use ingredient's glow color
			particles.color = ingredient_data.glow_color
	else:
		push_error("GatheringSpot: Ingredient data not found: " + ingredient_path)

	# Setup particles
	if particles:
		particles.color = glow_color
		particles.emitting = true


func _process(delta: float) -> void:
	if is_depleted:
		respawn_timer += delta

		if respawn_timer >= respawn_time:
			respawn()


## Called when player interacts
func interact() -> void:
	if is_depleted:
		return

	# Calculate yield
	var yield_amount := randi_range(min_yield, max_yield)

	# Add to player inventory
	PlayerData.add_ingredient(ingredient_id, yield_amount)

	# Show notification
	var ingredient_name := _get_ingredient_name()
	GameEvents.notification_requested.emit(
		"Gathered %d x %s" % [yield_amount, ingredient_name],
		"success"
	)

	# Play gather animation
	play_gather_animation()

	# Deplete this spot
	deplete()


## Deplete the gathering spot
func deplete() -> void:
	is_depleted = true
	respawn_timer = 0.0

	# Visual feedback
	if sprite:
		sprite.modulate = Color(0.5, 0.5, 0.5, 0.7)  # Gray out

	if particles:
		particles.emitting = false

	# Disable interaction
	if collision_shape:
		collision_shape.set_deferred("disabled", true)

	GameEvents.gathering_spot_depleted.emit(name)


## Respawn the gathering spot
func respawn() -> void:
	is_depleted = false
	respawn_timer = 0.0

	# Restore visuals
	if sprite:
		sprite.modulate = Color.WHITE

	if particles:
		particles.emitting = true

	# Re-enable interaction
	if collision_shape:
		collision_shape.set_deferred("disabled", false)

	GameEvents.gathering_spot_respawned.emit(name)


## Play gathering animation
func play_gather_animation() -> void:
	if not sprite:
		return

	# Animate sprite upward and fade
	var tween := create_tween()
	tween.set_parallel(true)
	tween.tween_property(sprite, "position:y", sprite.position.y - 20, 0.5)
	tween.tween_property(sprite, "modulate:a", 0.0, 0.5)

	await tween.finished

	# Reset for respawn
	sprite.position.y += 20
	sprite.modulate.a = 1.0


## Get ingredient display name
func _get_ingredient_name() -> String:
	if ingredient_data:
		return ingredient_data.display_name
	return ingredient_id


## Get interaction prompt text
func get_interaction_prompt() -> String:
	if is_depleted:
		return ""

	var ingredient_name := _get_ingredient_name()
	return "[E] Gather %s" % ingredient_name
