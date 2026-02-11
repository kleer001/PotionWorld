import random
import tomllib
from pathlib import Path

import arcade

CARD_WIDTH = 80
CARD_HEIGHT = 120


def _hex_to_color(hex_str):
    """Convert '#RRGGBB' to an (R, G, B) tuple."""
    h = hex_str.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def load_cards(path=None):
    """Parse cards.toml → dict keyed by card ID.

    Resolves ``ref`` fields: if a card has ``ref``, load that file's
    ``[card]`` table, then overlay the inline fields on top (inline wins).
    """
    if path is None:
        path = Path(__file__).parent / "data" / "cards.toml"
    else:
        path = Path(path)

    with open(path, "rb") as f:
        data = tomllib.load(f)

    card_db = {}
    for card_id, card_data in data.get("cards", {}).items():
        card = dict(card_data)
        card["id"] = card_id

        if "ref" in card:
            ref_path = path.parent / card["ref"]
            with open(ref_path, "rb") as rf:
                ref_data = tomllib.load(rf)
            base = dict(ref_data.get("card", {}))
            base.update(card)
            del base["ref"]
            card = base

        card_db[card_id] = card

    return card_db


def load_starter_deck(card_db, path=None):
    """Read [starter_deck] from TOML → list of card dicts (with dupes)."""
    if path is None:
        path = Path(__file__).parent / "data" / "cards.toml"
    with open(path, "rb") as f:
        data = tomllib.load(f)
    card_ids = data.get("starter_deck", {}).get("cards", [])
    return [dict(card_db[cid]) for cid in card_ids]


def build_deck(card_ids, card_db):
    """Turn a list of card ID strings into a shuffled list of card dicts."""
    deck = [dict(card_db[cid]) for cid in card_ids]
    random.shuffle(deck)
    return deck


# ---------------------------------------------------------------------------
# Action dispatch — M8
# ---------------------------------------------------------------------------


def redraw_hand(state, args):
    """Discard current hand, draw a fresh hand."""
    state.deck.extend(state.hand)
    state.hand.clear()
    random.shuffle(state.deck)
    for _ in range(min(state.hand_size, len(state.deck))):
        state.hand.append(state.deck.pop())


def draw_cards(state, args):
    """Draw extra cards from deck to hand."""
    for _ in range(args.get("count", 1)):
        if state.deck:
            state.hand.append(state.deck.pop())


def modify_state(state, args):
    """Apply *delta* to a named *field* on state."""
    field = args["field"]
    setattr(state, field, getattr(state, field) + args["delta"])


def recycle_card(state, args):
    """Undock the rightmost locked card back to hand, refund 1 mana."""
    for i in range(len(state.lock) - 1, -1, -1):
        if state.lock[i] is not None:
            state.hand.append(state.lock[i])
            state.lock[i] = None
            state.mana = min(state.mana + 1, state.max_mana)
            return


ACTION_REGISTRY = {
    "redraw_hand": redraw_hand,
    "draw_cards": draw_cards,
    "modify_state": modify_state,
    "recycle_card": recycle_card,
}


def dispatch_action(card_data, state):
    """Look up and call the action/on_draw function for a card."""
    action_name = card_data.get("action") or card_data.get("on_draw")
    if not action_name or action_name not in ACTION_REGISTRY:
        return
    args = card_data.get("args") or card_data.get("on_draw_args", {})
    ACTION_REGISTRY[action_name](state, args)


class CardSprite(arcade.SpriteSolidColor):
    """An 80×120 solid-color rectangle representing one card."""

    def __init__(self, card_data):
        color = _hex_to_color(card_data.get("color", "#888888"))
        super().__init__(CARD_WIDTH, CARD_HEIGHT, color=color)
        self.card_data = card_data
        self.home_position = (0.0, 0.0)
        self.is_locked = False
        self.slot_index = -1

        self.token_text = arcade.Text(
            card_data.get("token", "?"),
            0, 0,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="center",
            anchor_y="center",
        )
        self.label_text = arcade.Text(
            card_data.get("label", ""),
            0, 0,
            color=arcade.color.WHITE,
            font_size=9,
            anchor_x="center",
            anchor_y="center",
        )
