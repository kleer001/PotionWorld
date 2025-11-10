extends Node
## Manages current game session state (not saved data)
##
## This singleton tracks what's happening RIGHT NOW in the game:
## - What scene we're in
## - What the player can/cannot do
## - What phase of gameplay we're in
##
## This is separate from PlayerData (which is saved).

enum GamePhase {
	MENU,        ## Main menu or title screen
	GAMEPLAY,    ## Normal gameplay (walking around, gathering)
	DIALOGUE,    ## In conversation with NPC
	CRAFTING,    ## Using crafting UI
	CUTSCENE,    ## Watching a cutscene
	PAUSED       ## Game paused
}

# Current state
var current_phase: GamePhase = GamePhase.MENU
var previous_phase: GamePhase = GamePhase.MENU

# Scene tracking
var current_scene: String = ""
var previous_scene: String = ""

# Time tracking
var current_day: int = 1
var current_time: String = "morning"  # morning, afternoon, evening, night
var elapsed_game_time: float = 0.0
var real_time_played: float = 0.0

# Interaction state
var is_in_dialogue: bool = false
var is_crafting: bool = false
var is_gathering: bool = false
var current_interacting_npc: String = ""

# UI state
var is_inventory_open: bool = false
var is_journal_open: bool = false
var is_paused: bool = false

# Input state (what player can do)
var can_move: bool = true
var can_interact: bool = true
var can_open_menus: bool = true
var can_pause: bool = true


func _ready() -> void:
	print("GameState: Session state manager initialized")

	# Connect to relevant events
	GameEvents.dialogue_started.connect(_on_dialogue_started)
	GameEvents.dialogue_ended.connect(_on_dialogue_ended)
	GameEvents.inventory_opened.connect(_on_inventory_opened)
	GameEvents.inventory_closed.connect(_on_inventory_closed)
	GameEvents.journal_opened.connect(_on_journal_opened)
	GameEvents.journal_closed.connect(_on_journal_closed)


func _process(delta: float) -> void:
	# Track playtime
	if current_phase != GamePhase.MENU and current_phase != GamePhase.PAUSED:
		real_time_played += delta
		elapsed_game_time += delta


## Enter dialogue mode - restricts player actions
func enter_dialogue(npc_id: String = "") -> void:
	previous_phase = current_phase
	current_phase = GamePhase.DIALOGUE
	is_in_dialogue = true
	current_interacting_npc = npc_id
	can_move = false
	can_interact = false
	can_open_menus = false


## Exit dialogue mode - restores player actions
func exit_dialogue() -> void:
	current_phase = GamePhase.GAMEPLAY
	is_in_dialogue = false
	current_interacting_npc = ""
	can_move = true
	can_interact = true
	can_open_menus = true


## Enter crafting mode
func enter_crafting() -> void:
	previous_phase = current_phase
	current_phase = GamePhase.CRAFTING
	is_crafting = true
	can_move = false
	can_interact = false
	can_open_menus = false


## Exit crafting mode
func exit_crafting() -> void:
	current_phase = GamePhase.GAMEPLAY
	is_crafting = false
	can_move = true
	can_interact = true
	can_open_menus = true


## Enter cutscene mode
func enter_cutscene() -> void:
	previous_phase = current_phase
	current_phase = GamePhase.CUTSCENE
	can_move = false
	can_interact = false
	can_open_menus = false
	can_pause = false


## Exit cutscene mode
func exit_cutscene() -> void:
	current_phase = previous_phase
	can_move = true
	can_interact = true
	can_open_menus = true
	can_pause = true


## Pause the game
func pause_game() -> void:
	if not can_pause:
		return

	previous_phase = current_phase
	current_phase = GamePhase.PAUSED
	is_paused = true
	get_tree().paused = true


## Unpause the game
func unpause_game() -> void:
	current_phase = previous_phase
	is_paused = false
	get_tree().paused = false


## Advance to next day
func advance_day() -> void:
	current_day += 1
	current_time = "morning"
	GameEvents.day_changed.emit(current_day)


## Change time of day
func set_time_of_day(new_time: String) -> void:
	if new_time in ["morning", "afternoon", "evening", "night"]:
		current_time = new_time
		GameEvents.time_of_day_changed.emit(current_time)


## Get current phase as string (for debugging)
func get_phase_name() -> String:
	match current_phase:
		GamePhase.MENU:
			return "Menu"
		GamePhase.GAMEPLAY:
			return "Gameplay"
		GamePhase.DIALOGUE:
			return "Dialogue"
		GamePhase.CRAFTING:
			return "Crafting"
		GamePhase.CUTSCENE:
			return "Cutscene"
		GamePhase.PAUSED:
			return "Paused"
		_:
			return "Unknown"


# Event handlers
func _on_dialogue_started(npc_id: String) -> void:
	enter_dialogue(npc_id)


func _on_dialogue_ended(_npc_id: String) -> void:
	exit_dialogue()


func _on_inventory_opened() -> void:
	is_inventory_open = true
	can_move = false


func _on_inventory_closed() -> void:
	is_inventory_open = false
	if not is_in_dialogue and not is_crafting:
		can_move = true


func _on_journal_opened() -> void:
	is_journal_open = true
	can_move = false


func _on_journal_closed() -> void:
	is_journal_open = false
	if not is_in_dialogue and not is_crafting:
		can_move = true
