import arcade

from grammar_mvp.animation import DamageFloat, HitAnimation
from grammar_mvp.cards import CARD_WIDTH, CARD_HEIGHT

SLOT_COLOR = (50, 50, 50)
SLOT_GAP = 10

# Character panel colours
PORTRAIT_COLOR = (70, 70, 90)
HERO_COLOR = (0, 204, 204)     # robin's egg blue
ENEMY_COLOR = (139, 0, 0)      # deep red
PORTRAIT_W = 100
PORTRAIT_H = 120

# Battle log
LOG_LINE_COUNT = 4
LOG_FONT_SIZE = 12
LOG_LINE_SPACING = 20


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


# ------------------------------------------------------------------
# Character panels
# ------------------------------------------------------------------

class CharacterPanel:
    """Holds draw objects for one combatant (name, portrait, HP)."""

    def __init__(self, character, x, y, color=PORTRAIT_COLOR):
        self.x = x
        self.y = y
        portrait = arcade.SpriteSolidColor(
            PORTRAIT_W, PORTRAIT_H, color=color,
        )
        portrait.center_x = x
        portrait.center_y = y
        self.portrait_list = arcade.SpriteList()
        self.portrait_list.append(portrait)

        self.name_text = arcade.Text(
            character.name,
            x, y + PORTRAIT_H // 2 + 15,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="center",
        )
        self.hp_text = arcade.Text(
            f"{character.hp}/{character.max_hp}",
            x, y - PORTRAIT_H // 2 - 20,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
        )

        self.hit_anim = HitAnimation()
        self.dmg_float = DamageFloat()
        self.dmg_text = arcade.Text(
            "", x, y,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    def shake(self):
        """Trigger the hit-bounce animation."""
        self.hit_anim.start()

    def show_damage(self, amount: int):
        """Spawn a floating damage number (e.g. ``-5``)."""
        self.dmg_float.start(f"-{amount}")

    def update_animation(self, dt: float):
        """Advance the hit animation by *dt* seconds."""
        self.hit_anim.update(dt)
        self.dmg_float.update(dt)

    def draw(self):
        offset = self.hit_anim.offset
        portrait = self.portrait_list[0]
        portrait.center_x = self.x + offset
        self.name_text.x = self.x + offset
        self.hp_text.x = self.x + offset

        self.portrait_list.draw()
        self.name_text.draw()
        self.hp_text.draw()

        # Floating damage number
        if self.dmg_float.active:
            self.dmg_text.text = self.dmg_float.label
            self.dmg_text.x = self.x + self.dmg_float.x_offset
            self.dmg_text.y = self.y + self.dmg_float.y_offset
            a = self.dmg_float.alpha
            self.dmg_text.color = (255, 80, 80, a)
            self.dmg_text.draw()

    def update(self, character):
        """Sync displayed HP from Character data."""
        self.hp_text.text = f"{character.hp}/{character.max_hp}"


def create_hero_panel(character, x, y):
    return CharacterPanel(character, x, y, color=HERO_COLOR)


def create_enemy_panel(character, x, y):
    return CharacterPanel(character, x, y, color=ENEMY_COLOR)


# ------------------------------------------------------------------
# Battle log
# ------------------------------------------------------------------

class BattleLog:
    """Displays the most recent log lines stacked vertically."""

    def __init__(self, x, y):
        self.lines: list[arcade.Text] = []
        self.x = x
        self.y = y
        for i in range(LOG_LINE_COUNT):
            t = arcade.Text(
                "",
                x, y - i * LOG_LINE_SPACING,
                color=arcade.color.LIGHT_GRAY,
                font_size=LOG_FONT_SIZE,
                anchor_x="center",
            )
            self.lines.append(t)

    def push(self, message: str):
        """Shift existing lines up, newest appears at the bottom."""
        for i in range(len(self.lines) - 1):
            self.lines[i].text = self.lines[i + 1].text
        self.lines[-1].text = message

    def draw(self):
        for line in self.lines:
            line.draw()


# ------------------------------------------------------------------
# Mana pips
# ------------------------------------------------------------------

PIP_RADIUS = 7
PIP_GAP = 6
PIP_COLOR_REMAINING = arcade.color.WHITE
PIP_COLOR_COST = (220, 40, 40)          # red — pending cast cost
PIP_COLOR_SPENT_FILL = (30, 30, 30)     # near-black interior
PIP_COLOR_SPENT_OUTLINE = arcade.color.WHITE


class ManaPips:
    """Visual mana pips: white=remaining, red=cast cost, hollow=spent.

    Pips are laid out right-to-left so remaining mana is anchored to the
    right side and spent mana drains from the left.
    """

    def __init__(self, right_x: float, y: float, max_mana: int):
        self.right_x = right_x
        self.y = y
        self.max_mana = max_mana
        self.mana = max_mana
        self.cast_cost = 0
        self.label = arcade.Text(
            "Mana",
            right_x, y - 20,
            color=arcade.color.LIGHT_BLUE,
            font_size=12,
            anchor_x="right",
        )

    def update(self, mana: int, max_mana: int, cast_cost: int):
        self.mana = mana
        self.max_mana = max_mana
        self.cast_cost = cast_cost

    def draw(self):
        # Pips are drawn right-to-left: rightmost pip = pip index 0 = first
        # "remaining" pip.  Walking left: remaining → cost → spent.
        for i in range(self.max_mana):
            cx = self.right_x - i * (PIP_RADIUS * 2 + PIP_GAP)
            # Which bucket does this pip fall into?
            # Right-to-left order: remaining (mana), then cost, then spent.
            if i < self.mana:
                # Remaining — solid white
                arcade.draw_circle_filled(cx, self.y, PIP_RADIUS,
                                          PIP_COLOR_REMAINING)
            elif i < self.mana + self.cast_cost:
                # Will be spent on cast — solid red
                arcade.draw_circle_filled(cx, self.y, PIP_RADIUS,
                                          PIP_COLOR_COST)
            else:
                # Already spent — hollow (outline only)
                arcade.draw_circle_filled(cx, self.y, PIP_RADIUS,
                                          PIP_COLOR_SPENT_FILL)
                arcade.draw_circle_outline(cx, self.y, PIP_RADIUS,
                                           PIP_COLOR_SPENT_OUTLINE, 2)
        self.label.draw()
