"""Level loader — parse levels.toml, auto-build decks, track progression."""

import random
import tomllib
from pathlib import Path

from grammar_mvp.game_state import Character


_DATA_DIR = Path(__file__).parent / "data"
_LEVELS_PATH = _DATA_DIR / "levels.toml"


# ------------------------------------------------------------------
# Parsing
# ------------------------------------------------------------------

def _parse_symbol(symbol_str: str) -> tuple[str, int]:
    """Parse 'H@3' → ('H', 3).  No count defaults to 2."""
    if "@" in symbol_str:
        token, count_str = symbol_str.rsplit("@", 1)
        return token, int(count_str)
    return symbol_str, 2


def _parse_implied(implied_str: str) -> tuple[str, int]:
    """Parse 'P@0' → ('P', 0) — token and slot index."""
    token, slot_str = implied_str.rsplit("@", 1)
    return token, int(slot_str)


def _char_from_dict(d: dict) -> Character:
    """Build a Character from a TOML inline table."""
    return Character(
        name=d["name"],
        hp=d["hp"],
        max_hp=d["hp"],
        strength=d["strength"],
        defense=d["defense"],
    )


def load_levels(path: Path | None = None) -> list[dict]:
    """Load all levels from TOML, return list of level dicts.

    Each level dict has:
        id, title, hint, implied_cards, symbols, deck_extras,
        mana, slot_count, hand_size, heroes, enemies
    Heroes carry forward: if a level omits ``heroes``, it inherits
    from the previous level.
    """
    if path is None:
        path = _LEVELS_PATH
    with open(path, "rb") as f:
        data = tomllib.load(f)

    raw_levels = data.get("levels", [])
    levels: list[dict] = []
    last_heroes = None

    for raw in raw_levels:
        level = {
            "id": raw["id"],
            "title": raw.get("title", ""),
            "hint": raw.get("hint", ""),
            "mana": raw.get("mana", 10),
            "slot_count": raw.get("slot_count", 5),
            "hand_size": raw.get("hand_size", 5),
            "deck_extras": raw.get("deck_extras", []),
            "smooth_draw_n": raw.get("smooth_draw_n", 1),
        }

        # Implied cards
        level["implied_cards"] = [
            _parse_implied(s) for s in raw.get("implied_cards", [])
        ]

        # Symbols → (token, count) pairs
        level["symbols"] = [
            _parse_symbol(s) for s in raw.get("symbols", [])
        ]

        # Heroes — carry forward if omitted
        if "heroes" in raw:
            last_heroes = [_char_from_dict(h) for h in raw["heroes"]]
        level["heroes"] = last_heroes or []

        # Enemies
        level["enemies"] = [_char_from_dict(e) for e in raw.get("enemies", [])]

        levels.append(level)

    return levels


# ------------------------------------------------------------------
# Deck building
# ------------------------------------------------------------------

def build_level_deck(level: dict, card_db: dict) -> list[dict]:
    """Auto-build a shuffled deck from level symbols + deck_extras.

    For each (token, count) in ``level["symbols"]``, find the matching
    card in card_db by token and add *count* copies.  Then append any
    deck_extras by card ID.
    """
    # Index card_db by token for grammar card lookup
    token_to_id: dict[str, str] = {}
    for card_id, card_data in card_db.items():
        if card_data.get("type") == "grammar":
            tok = card_data["token"]
            if tok not in token_to_id:
                token_to_id[tok] = card_id

    deck: list[dict] = []

    # Grammar cards from symbols
    for token, count in level["symbols"]:
        card_id = token_to_id.get(token)
        if card_id and card_id in card_db:
            for _ in range(count):
                deck.append(dict(card_db[card_id]))

    # Extra cards (action, curse) by ID
    for card_id in level["deck_extras"]:
        if card_id in card_db:
            deck.append(dict(card_db[card_id]))

    random.shuffle(deck)
    return deck


# ------------------------------------------------------------------
# Progression
# ------------------------------------------------------------------

class LevelManager:
    """Tracks which level the player is on and provides level data."""

    def __init__(self, levels: list[dict] | None = None):
        self.levels = levels if levels is not None else load_levels()
        self.current_index: int = 0

    @property
    def current_level(self) -> dict:
        return self.levels[self.current_index]

    @property
    def is_last_level(self) -> bool:
        return self.current_index >= len(self.levels) - 1

    def advance(self) -> bool:
        """Move to next level. Returns False if already at the last level."""
        if self.is_last_level:
            return False
        self.current_index += 1
        return True

    def restart_level(self):
        """Reset to replay the current level (on defeat)."""
        pass  # current_index stays the same; BattleView re-reads it

    def restart_game(self):
        """Reset to the very first level."""
        self.current_index = 0
