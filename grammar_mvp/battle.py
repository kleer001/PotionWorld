"""Battle engine — turn resolution, potion application, effect ticking."""

import random

from grammar_mvp.game_state import Character, GameState

# Map ESENS stat codes → Character attribute names
STAT_MAP = {
    "H": "hp",
    "S": "strength",
    "D": "defense",
}

# Map ESENS target codes → GameState attribute names
TARGET_MAP = {
    "P": "hero",
    "E": "enemy",
}


def resolve_turn(attacker: Character, defender: Character) -> str:
    """One attack: attacker hits defender. Returns a log string."""
    hit = random.randint(1, attacker.strength)
    block = random.randint(0, defender.defense)
    damage = max(1, hit - block)
    defender.hp = max(0, defender.hp - damage)
    return (
        f"{attacker.name} attacks! {hit} hit - {block} block = {damage} dmg. "
        f"{defender.name}: {defender.hp}/{defender.max_hp}"
    )


def apply_potion(parsed_dict: dict, state: GameState) -> str:
    """Apply a parsed ESENS effect to the game state. Returns a log string.

    ``parsed_dict`` is the ``result["dict"]`` from ``parse_esens``.
    For now this does immediate stat mutation only.
    """
    target_code = parsed_dict.get("target", "P")
    effect_type = parsed_dict.get("effect_type", "+")
    stat_code = parsed_dict.get("stat_affected", "H")
    magnitude = 0
    mag_info = parsed_dict.get("magnitude")
    if mag_info:
        magnitude = mag_info.get("value", 0)

    attr = STAT_MAP.get(stat_code)
    target_attr = TARGET_MAP.get(target_code)
    if not attr or not target_attr:
        return "Potion fizzles…"

    character: Character = getattr(state, target_attr)

    if effect_type == "+":
        old = getattr(character, attr)
        new = old + magnitude
        if attr == "hp":
            new = min(new, character.max_hp)
        setattr(character, attr, new)
        return f"{character.name} +{magnitude} {attr.upper()}! ({old}→{new})"
    elif effect_type == "-":
        old = getattr(character, attr)
        new = max(0, old - magnitude)
        setattr(character, attr, new)
        return f"{character.name} -{magnitude} {attr.upper()}! ({old}→{new})"
    else:
        return "Potion fizzles…"


def tick_effects(character: Character):
    """Decrement active effect durations, remove expired ones.

    Placeholder for future duration-based effects.
    """
    still_active = []
    for effect in character.active_effects:
        effect["remaining"] -= 1
        if effect["remaining"] > 0:
            still_active.append(effect)
        # TODO: reverse stat change on expiry
    character.active_effects = still_active


def check_battle_end(state: GameState) -> str | None:
    """Return 'win', 'lose', or None."""
    if state.hero.hp <= 0:
        return "lose"
    if state.enemy.hp <= 0:
        return "win"
    return None
