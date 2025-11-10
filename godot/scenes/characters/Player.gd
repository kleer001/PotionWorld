extends CharacterBody2D
class_name Player
## Player character controller
##
## Handles player movement (WASD/gamepad), interactions, and animation.
## Origin point is at the FEET for proper Y-sorting.

@export var move_speed: float = 150.0

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var interaction_area: Area2D = $InteractionArea
@onready var interaction_prompt: Label = $InteractionPrompt

var input_direction: Vector2 = Vector2.ZERO
var facing_direction: Vector2 = Vector2.DOWN

# Animation states we need:
# idle_down, idle_up, idle_left, idle_right
# walk_down, walk_up, walk_left, walk_right


func _ready() -> void:
	# Hide interaction prompt by default
	if interaction_prompt:
		interaction_prompt.hide()

	# Connect to interaction area
	if interaction_area:
		interaction_area.area_entered.connect(_on_interaction_area_entered)
		interaction_area.area_exited.connect(_on_interaction_area_exited)


func _physics_process(_delta: float) -> void:
	# Check if player can move
	if not GameState.can_move:
		velocity = Vector2.ZERO
		play_idle_animation()
		move_and_slide()
		return

	# Get input direction
	input_direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")

	# Normalize diagonal movement (prevent faster diagonal speed)
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

	# Move the player
	move_and_slide()


func _unhandled_input(event: InputEvent) -> void:
	if not GameState.can_interact:
		return

	# Interact with nearby objects
	if event.is_action_pressed("interact"):
		interact_with_nearby()


## Play walking animation based on direction
func play_walk_animation() -> void:
	if not sprite:
		return

	# Determine direction (prioritize horizontal)
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


## Play idle animation based on facing direction
func play_idle_animation() -> void:
	if not sprite:
		return

	# Use last facing direction
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


## Interact with nearby interactable objects
func interact_with_nearby() -> void:
	if not interaction_area:
		return

	var overlapping_areas := interaction_area.get_overlapping_areas()

	if overlapping_areas.is_empty():
		return

	# Find closest interactable
	var closest: Area2D = null
	var closest_dist := INF

	for area in overlapping_areas:
		var dist := global_position.distance_to(area.global_position)
		if dist < closest_dist:
			closest_dist = dist
			closest = area

	# Interact with closest object
	if closest:
		var parent = closest.get_parent()
		if parent and parent.has_method("interact"):
			parent.interact()


## Called when something enters interaction range
func _on_interaction_area_entered(area: Area2D) -> void:
	var parent = area.get_parent()

	if parent and parent.has_method("interact"):
		# Show interaction prompt
		update_interaction_prompt(true, parent)


## Called when something exits interaction range
func _on_interaction_area_exited(area: Area2D) -> void:
	# Check if any other interactables are still in range
	var overlapping := interaction_area.get_overlapping_areas()

	if overlapping.is_empty():
		update_interaction_prompt(false)
	else:
		# Show prompt for remaining object
		var parent = overlapping[0].get_parent()
		if parent and parent.has_method("interact"):
			update_interaction_prompt(true, parent)


## Update interaction prompt visibility and text
func update_interaction_prompt(show: bool, interactable: Node = null) -> void:
	if not interaction_prompt:
		return

	if show and interactable:
		# Get prompt text from interactable
		var prompt_text := "[E] Interact"

		if interactable.has_method("get_interaction_prompt"):
			prompt_text = interactable.get_interaction_prompt()

		interaction_prompt.text = prompt_text
		interaction_prompt.show()
	else:
		interaction_prompt.hide()
