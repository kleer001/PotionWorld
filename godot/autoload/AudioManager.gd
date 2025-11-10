extends Node
## Centralized audio management
##
## Handles music transitions and sound effect playback.
## Uses audio pools to prevent overlapping sounds.
## Reacts to game events automatically.
##
## Usage:
##   AudioManager.play_music("garden_theme")
##   AudioManager.play_sfx("gather_mushroom")

const MAX_SFX_PLAYERS: int = 8

var music_player: AudioStreamPlayer
var sfx_players: Array[AudioStreamPlayer] = []

var current_music: String = ""
var music_volume: float = 0.8
var sfx_volume: float = 1.0
var master_volume: float = 1.0

var is_music_muted: bool = false
var is_sfx_muted: bool = false

# Audio file paths
const MUSIC_PATH: String = "res://assets/audio/music/"
const SFX_PATH: String = "res://assets/audio/sfx/"


func _ready() -> void:
	print("AudioManager: Audio manager initialized")

	# Create music player
	music_player = AudioStreamPlayer.new()
	add_child(music_player)
	music_player.bus = "Music"
	music_player.volume_db = linear_to_db(music_volume)

	# Create SFX players pool
	for i in range(MAX_SFX_PLAYERS):
		var player := AudioStreamPlayer.new()
		add_child(player)
		player.bus = "SFX"
		player.volume_db = linear_to_db(sfx_volume)
		sfx_players.append(player)

	# Connect to game events for automatic audio feedback
	_connect_event_handlers()


## Play music track with fade
## @param music_name: Name of music file (without path or extension)
## @param fade_duration: Time to fade between tracks
func play_music(music_name: String, fade_duration: float = 1.0) -> void:
	if current_music == music_name:
		return

	if is_music_muted:
		print("AudioManager: Music is muted, not playing: " + music_name)
		return

	var music_file: String = MUSIC_PATH + music_name + ".ogg"

	if not FileAccess.file_exists(music_file):
		push_error("AudioManager: Music file not found: " + music_file)
		return

	var stream: AudioStream = load(music_file)
	if stream == null:
		push_error("AudioManager: Failed to load music: " + music_file)
		return

	# Fade out current music
	if music_player.playing:
		var tween := create_tween()
		tween.tween_property(music_player, "volume_db", -80.0, fade_duration)
		await tween.finished

	# Play new music
	music_player.stream = stream
	music_player.volume_db = linear_to_db(music_volume) if not is_music_muted else -80.0
	music_player.play()
	current_music = music_name

	# Fade in
	if fade_duration > 0:
		music_player.volume_db = -80.0
		var tween := create_tween()
		tween.tween_property(music_player, "volume_db", linear_to_db(music_volume), fade_duration)

	print("AudioManager: Playing music: " + music_name)


## Stop music with fade
func stop_music(fade_duration: float = 1.0) -> void:
	if not music_player.playing:
		return

	if fade_duration > 0:
		var tween := create_tween()
		tween.tween_property(music_player, "volume_db", -80.0, fade_duration)
		await tween.finished

	music_player.stop()
	current_music = ""
	print("AudioManager: Music stopped")


## Play sound effect
## @param sfx_name: Name of SFX file (without path or extension)
## @param pitch_variation: Random pitch variation (0.0 to 1.0)
func play_sfx(sfx_name: String, pitch_variation: float = 0.0) -> void:
	if is_sfx_muted:
		return

	var sfx_file: String = SFX_PATH + sfx_name + ".ogg"

	if not FileAccess.file_exists(sfx_file):
		# Try .wav extension
		sfx_file = SFX_PATH + sfx_name + ".wav"
		if not FileAccess.file_exists(sfx_file):
			push_error("AudioManager: SFX file not found: " + sfx_name)
			return

	var stream: AudioStream = load(sfx_file)
	if stream == null:
		push_error("AudioManager: Failed to load SFX: " + sfx_file)
		return

	# Find available SFX player
	for player in sfx_players:
		if not player.playing:
			player.stream = stream
			player.volume_db = linear_to_db(sfx_volume)
			player.pitch_scale = 1.0 + randf_range(-pitch_variation, pitch_variation)
			player.play()
			return

	# All players busy, play on first player (interrupts oldest sound)
	sfx_players[0].stream = stream
	sfx_players[0].volume_db = linear_to_db(sfx_volume)
	sfx_players[0].pitch_scale = 1.0 + randf_range(-pitch_variation, pitch_variation)
	sfx_players[0].play()


## Set music volume (0.0 to 1.0)
func set_music_volume(volume: float) -> void:
	music_volume = clampf(volume, 0.0, 1.0)
	if music_player:
		music_player.volume_db = linear_to_db(music_volume) if not is_music_muted else -80.0


## Set SFX volume (0.0 to 1.0)
func set_sfx_volume(volume: float) -> void:
	sfx_volume = clampf(volume, 0.0, 1.0)
	for player in sfx_players:
		player.volume_db = linear_to_db(sfx_volume) if not is_sfx_muted else -80.0


## Set master volume (0.0 to 1.0)
func set_master_volume(volume: float) -> void:
	master_volume = clampf(volume, 0.0, 1.0)
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Master"), linear_to_db(master_volume))


## Toggle music mute
func toggle_music_mute() -> void:
	is_music_muted = not is_music_muted
	if music_player:
		music_player.volume_db = linear_to_db(music_volume) if not is_music_muted else -80.0


## Toggle SFX mute
func toggle_sfx_mute() -> void:
	is_sfx_muted = not is_sfx_muted
	for player in sfx_players:
		player.volume_db = linear_to_db(sfx_volume) if not is_sfx_muted else -80.0


# Event handlers for automatic audio feedback
func _connect_event_handlers() -> void:
	GameEvents.ingredient_gathered.connect(_on_ingredient_gathered)
	GameEvents.potion_crafted.connect(_on_potion_crafted)
	GameEvents.crafting_failed.connect(_on_crafting_failed)
	GameEvents.affinity_changed.connect(_on_affinity_changed)
	GameEvents.stat_increased.connect(_on_stat_increased)
	GameEvents.level_threshold_reached.connect(_on_level_threshold_reached)
	GameEvents.music_change_requested.connect(_on_music_change_requested)
	GameEvents.sfx_play_requested.connect(_on_sfx_play_requested)


func _on_ingredient_gathered(ingredient_id: String, _amount: int) -> void:
	# Play gathering sound based on ingredient type
	var sfx_name := "gather_" + ingredient_id
	play_sfx(sfx_name, 0.1)


func _on_potion_crafted(_potion_name: String, quality: String) -> void:
	# Play different success sounds based on quality
	if quality in ["exceptional", "masterwork"]:
		play_sfx("craft_success_special")
	else:
		play_sfx("craft_success")


func _on_crafting_failed(_reason: String) -> void:
	play_sfx("craft_fail")


func _on_affinity_changed(_npc_id: String, old_value: float, new_value: float) -> void:
	if new_value > old_value and new_value - old_value >= 0.5:
		play_sfx("affinity_gain")
	elif new_value < old_value and old_value - new_value >= 0.5:
		play_sfx("affinity_loss")


func _on_stat_increased(_stat_name: String, _old_value: int, _new_value: int) -> void:
	play_sfx("stat_gain", 0.1)


func _on_level_threshold_reached(_stat_name: String, _threshold: int) -> void:
	play_sfx("level_up")


func _on_music_change_requested(music_name: String) -> void:
	play_music(music_name)


func _on_sfx_play_requested(sfx_name: String) -> void:
	play_sfx(sfx_name)
