extends Node
## Global utility/helper functions
##
## Collection of useful functions accessible globally as Helpers.function_name()

## Format seconds into human-readable time string
## @param seconds: Time in seconds
## @param show_seconds: Whether to include seconds in output
## @return: Formatted string like "2 hrs 15 min" or "45 min 30 sec"
static func format_time(seconds: float, show_seconds: bool = false) -> String:
	var hours := int(seconds / 3600)
	var minutes := int((seconds - hours * 3600) / 60)
	var secs := int(seconds - hours * 3600 - minutes * 60)

	var result := ""

	if hours > 0:
		result += "%d hr " % hours

	if minutes > 0 or hours > 0:
		result += "%d min " % minutes

	if show_seconds and (secs > 0 or (hours == 0 and minutes == 0)):
		result += "%d sec" % secs

	return result.strip_edges()


## Format a number with thousands separators
## @param number: Number to format
## @return: Formatted string like "1,234,567"
static func format_number(number: int) -> String:
	var str_number := str(number)
	var result := ""
	var count := 0

	for i in range(str_number.length() - 1, -1, -1):
		if count == 3:
			result = "," + result
			count = 0
		result = str_number[i] + result
		count += 1

	return result


## Get color based on affinity value
## @param affinity: Affinity value (-5.0 to 5.0)
## @return: Color ranging from red (negative) to green (positive)
static func get_affinity_color(affinity: float) -> Color:
	if affinity >= 3.0:
		return Color(0.2, 1.0, 0.2)  # Bright green (Loyal/Devoted)
	elif affinity >= 1.0:
		return Color(0.6, 1.0, 0.6)  # Light green (Warm/Friendly)
	elif affinity > -1.0:
		return Color(0.8, 0.8, 0.8)  # Gray (Neutral)
	elif affinity > -3.0:
		return Color(1.0, 0.6, 0.4)  # Orange (Cool/Unfriendly)
	else:
		return Color(1.0, 0.2, 0.2)  # Red (Hostile/Nemesis)


## Get quality color
## @param quality: Quality tier name
## @return: Color for that quality tier
static func get_quality_color(quality: String) -> Color:
	match quality:
		"poor":
			return Color(0.6, 0.6, 0.6)  # Gray
		"standard":
			return Color.WHITE
		"fine":
			return Color(0.3, 1.0, 0.3)  # Green
		"exceptional":
			return Color(0.4, 0.6, 1.0)  # Blue
		"masterwork":
			return Color(1.0, 0.7, 0.0)  # Gold
		_:
			return Color.WHITE


## Clamp affinity to valid range
static func clamp_affinity(value: float) -> float:
	return clampf(value, Constants.AFFINITY_MIN, Constants.AFFINITY_MAX)


## Clamp stat to valid range
static func clamp_stat(value: int) -> int:
	return clampi(value, 0, Constants.STAT_CAP)


## Get random element from array
static func random_from_array(array: Array) -> Variant:
	if array.is_empty():
		return null
	return array[randi() % array.size()]


## Shuffle array in place
static func shuffle_array(array: Array) -> void:
	for i in range(array.size() - 1, 0, -1):
		var j := randi() % (i + 1)
		var temp = array[i]
		array[i] = array[j]
		array[j] = temp


## Get percentage as string
static func format_percentage(value: float) -> String:
	return "%d%%" % int(value * 100)


## Check if value is within range
static func in_range(value: float, min_val: float, max_val: float) -> bool:
	return value >= min_val and value <= max_val


## Linear interpolation between two values
static func lerp_custom(from: float, to: float, weight: float) -> float:
	return from + (to - from) * weight


## Get sign of number (-1, 0, or 1)
static func sign_of(value: float) -> int:
	if value > 0:
		return 1
	elif value < 0:
		return -1
	else:
		return 0


## Convert Big 5 personality value to string
static func personality_to_string(value: int) -> String:
	match value:
		Constants.PERSONALITY_LOW:
			return "Low"
		Constants.PERSONALITY_MODERATE:
			return "Moderate"
		Constants.PERSONALITY_HIGH:
			return "High"
		_:
			return "Unknown"


## Get full personality description
static func get_personality_description(trait: String, value: int) -> String:
	var level := personality_to_string(value)

	match trait.to_lower():
		"openness":
			if value == Constants.PERSONALITY_HIGH:
				return "High Openness: Creative, curious, experimental"
			elif value == Constants.PERSONALITY_LOW:
				return "Low Openness: Traditional, practical, prefers routine"
			else:
				return "Moderate Openness: Balanced creativity and tradition"

		"conscientiousness":
			if value == Constants.PERSONALITY_HIGH:
				return "High Conscientiousness: Organized, reliable, rule-following"
			elif value == Constants.PERSONALITY_LOW:
				return "Low Conscientiousness: Flexible, spontaneous, casual"
			else:
				return "Moderate Conscientiousness: Reasonably organized"

		"extraversion":
			if value == Constants.PERSONALITY_HIGH:
				return "High Extraversion: Outgoing, energetic, social"
			elif value == Constants.PERSONALITY_LOW:
				return "Low Extraversion: Reserved, quiet, reflective"
			else:
				return "Moderate Extraversion: Socially adaptable"

		"agreeableness":
			if value == Constants.PERSONALITY_HIGH:
				return "High Agreeableness: Cooperative, compassionate, kind"
			elif value == Constants.PERSONALITY_LOW:
				return "Low Agreeableness: Competitive, direct, skeptical"
			else:
				return "Moderate Agreeableness: Diplomatically balanced"

		"neuroticism":
			if value == Constants.PERSONALITY_HIGH:
				return "High Neuroticism: Emotionally reactive, worried, sensitive"
			elif value == Constants.PERSONALITY_LOW:
				return "Low Neuroticism: Calm, stable, resilient"
			else:
				return "Moderate Neuroticism: Generally stable"

		_:
			return "Unknown trait"


## Debug print with timestamp
static func debug_log(message: String) -> void:
	if Constants.DEBUG_MODE and Constants.LOG_EVENTS:
		var time := Time.get_ticks_msec() / 1000.0
		print("[%.2f] %s" % [time, message])
