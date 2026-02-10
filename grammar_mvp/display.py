import arcade

from grammar_mvp.cards import CARD_WIDTH, CARD_HEIGHT

SLOT_COLOR = (50, 50, 50)
SLOT_GAP = 10


def create_lock_slots(slot_count, screen_width, y_center):
    """Create ``slot_count`` dark-gray slot sprites, evenly spaced."""
    slot_list = arcade.SpriteList()
    total_width = slot_count * CARD_WIDTH + (slot_count - 1) * SLOT_GAP
    start_x = (screen_width - total_width) / 2 + CARD_WIDTH / 2

    for i in range(slot_count):
        slot = arcade.SpriteSolidColor(CARD_WIDTH, CARD_HEIGHT, color=SLOT_COLOR)
        slot.center_x = start_x + i * (CARD_WIDTH + SLOT_GAP)
        slot.center_y = y_center
        slot.slot_index = i
        slot.card = None
        slot_list.append(slot)

    return slot_list
