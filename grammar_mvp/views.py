import random
import sys
from pathlib import Path

import arcade
import arcade.gui

# Ensure project root is on path for ESENS_Parser import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ESENS_Parser import ESENSParseError, parse_esens

from grammar_mvp.battle import apply_potion, check_battle_end, resolve_turn, tick_effects
from grammar_mvp.cards import (
    CARD_HEIGHT,
    CARD_WIDTH,
    CardSprite,
    dispatch_action,
    load_cards,
    load_starter_deck,
    redraw_hand,
)
from grammar_mvp.display import BattleLog, create_hero_panel, create_enemy_panel, create_lock_slots
from grammar_mvp.game_state import Character, GameState

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
HAND_Y = 100
SLOT_Y = 280
HAND_GAP = 10
CAST_X = SCREEN_WIDTH // 2 + 300
DECK_X = 1060
DECK_PILE_COUNT = 5
DECK_OFFSET = 2
DECK_BROWNS = [
    (85, 55, 25),
    (101, 67, 33),
    (120, 80, 40),
    (139, 90, 43),
    (160, 110, 60),
]

# Layout — character panels (top third)
PANEL_Y = 570
HERO_PANEL_X = 300
ENEMY_PANEL_X = SCREEN_WIDTH - 300

# Battle log sits between the two panels
LOG_X = SCREEN_WIDTH // 2
LOG_Y = 520

# Timing
TURN_DELAY = 5.0          # seconds between auto-played turns
PREVIEW_TURN_COUNT = 3     # how many turns auto-play in preview phase
POST_CAST_TURNS = 2        # auto-play turns after a cast


class BattleView(arcade.View):

    def __init__(self):
        super().__init__()
        self.state: GameState | None = None
        self.card_db: dict = {}

        # Sprite lists
        self.hand_list: arcade.SpriteList = arcade.SpriteList()
        self.slot_list: arcade.SpriteList = arcade.SpriteList()
        self.lock_list: arcade.SpriteList = arcade.SpriteList()
        self.deck_pile: arcade.SpriteList = arcade.SpriteList()

        # Drag state
        self.held_card: CardSprite | None = None
        self.held_offset_x: float = 0.0
        self.held_offset_y: float = 0.0

        # Persistent text objects
        self.feedback_text: arcade.Text | None = None
        self.mana_text: arcade.Text | None = None
        self.mana_label_text: arcade.Text | None = None

        # Character panels (M10)
        self.hero_panel = None
        self.enemy_panel = None

        # Battle log display (M10)
        self.battle_log_display: BattleLog | None = None

        # Turn timer (M9)
        self.turn_timer: float = 0.0
        self.turns_remaining: int = 0
        self.hero_attacks_next: bool = True

        # End-of-battle overlay text
        self.end_text: arcade.Text | None = None

        # GUI
        self.ui_manager = arcade.gui.UIManager()

    # ------------------------------------------------------------------
    # View lifecycle
    # ------------------------------------------------------------------

    def on_show_view(self):
        self.window.background_color = (30, 30, 40)

        # Load card data
        self.card_db = load_cards()
        starter = load_starter_deck(self.card_db)
        random.shuffle(starter)

        self.state = GameState(
            hero=Character("Stable Boy", 15, 15, 3, 1),
            enemy=Character("Goblin", 25, 25, 7, 3),
            mana=10,
            max_mana=10,
            deck=starter,
            hand=[],
            lock=[None] * 5,
            slot_count=5,
            hand_size=5,
            phase="preview",
        )

        # Draw initial hand from deck
        self._draw_cards_from_deck(self.state.hand_size)
        self._sync_hand()
        self._build_deck_pile()

        # Lock slots
        self.slot_list = create_lock_slots(
            self.state.slot_count, SCREEN_WIDTH, SLOT_Y,
        )

        # Text
        self.feedback_text = arcade.Text(
            "",
            SCREEN_WIDTH / 2, SLOT_Y + CARD_HEIGHT // 2 + 15,
            color=arcade.color.GRAY,
            font_size=14,
            anchor_x="center",
        )
        self.mana_text = arcade.Text(
            f"{self.state.mana}/{self.state.max_mana}",
            CAST_X, SLOT_Y - 45,
            color=arcade.color.LIGHT_BLUE,
            font_size=16,
            anchor_x="center",
        )
        self.mana_label_text = arcade.Text(
            "Mana",
            CAST_X, SLOT_Y - 65,
            color=arcade.color.LIGHT_BLUE,
            font_size=12,
            anchor_x="center",
        )

        # CAST button — positioned to the right of the lock area
        cast_button = arcade.gui.UIFlatButton(text="CAST", width=120, height=50)
        cast_button.on_click = self._on_cast_click
        cast_anchor = arcade.gui.UIAnchorLayout()
        cast_anchor.add(
            child=cast_button,
            anchor_x="center",
            anchor_y="center",
            align_x=300,
            align_y=SLOT_Y - SCREEN_HEIGHT // 2,
        )
        self.ui_manager.add(cast_anchor)

        # REDRAW button — below the hand, costs 2 mana
        redraw_button = arcade.gui.UIFlatButton(
            text="REDRAW (2 Mana)", width=160, height=40,
        )
        redraw_button.on_click = self._on_redraw_click
        redraw_anchor = arcade.gui.UIAnchorLayout()
        redraw_anchor.add(
            child=redraw_button,
            anchor_x="center",
            anchor_y="center",
            align_x=0,
            align_y=HAND_Y - CARD_HEIGHT // 2 - 40 - SCREEN_HEIGHT // 2,
        )
        self.ui_manager.add(redraw_anchor)

        self.ui_manager.enable()

        # Character panels (M10)
        self.hero_panel = create_hero_panel(self.state.hero, HERO_PANEL_X, PANEL_Y)
        self.enemy_panel = create_enemy_panel(self.state.enemy, ENEMY_PANEL_X, PANEL_Y)

        # Battle log display (M10)
        self.battle_log_display = BattleLog(LOG_X, LOG_Y)

        # End-of-battle overlay
        self.end_text = arcade.Text(
            "",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            color=arcade.color.YELLOW,
            font_size=32,
            anchor_x="center",
            anchor_y="center",
        )

        # Start preview phase
        self.turns_remaining = PREVIEW_TURN_COUNT
        self.turn_timer = 0.0
        self.hero_attacks_next = True

    def on_hide_view(self):
        self.ui_manager.disable()

    # ------------------------------------------------------------------
    # Update (phase-driven timer)
    # ------------------------------------------------------------------

    def on_update(self, delta_time):
        state = self.state
        phase = state.phase

        # Tick hit animations every frame
        if self.hero_panel:
            self.hero_panel.update_animation(delta_time)
        if self.enemy_panel:
            self.enemy_panel.update_animation(delta_time)

        # If stuck in build with nothing to play, auto-resolve
        if phase == "build" and not state.hand and not state.deck:
            state.phase = "resolve"
            self.turns_remaining = 999
            phase = "resolve"

        if phase in ("preview", "build", "resolve", "post_cast"):
            self.turn_timer += delta_time
            if self.turn_timer >= TURN_DELAY:
                self.turn_timer -= TURN_DELAY
                self._play_one_turn()

    def _play_one_turn(self):
        """Resolve one attack turn and check for phase transitions."""
        state = self.state

        # Pick attacker/defender
        if self.hero_attacks_next:
            log = resolve_turn(state.hero, state.enemy)
            if self.enemy_panel:
                self.enemy_panel.shake()
        else:
            log = resolve_turn(state.enemy, state.hero)
            if self.hero_panel:
                self.hero_panel.shake()
        self.hero_attacks_next = not self.hero_attacks_next

        state.turn += 1
        tick_effects(state.hero)
        tick_effects(state.enemy)

        state.battle_log.append(log)
        self.battle_log_display.push(log)
        self._sync_panels()

        # Check win/lose
        result = check_battle_end(state)
        if result:
            self._enter_end_phase(result)
            return

        self.turns_remaining -= 1

        if state.phase == "preview" and self.turns_remaining <= 0:
            state.phase = "build"

        elif state.phase == "post_cast" and self.turns_remaining <= 0:
            # After post-cast turns, check mana
            if state.mana > 0:
                state.phase = "build"
            else:
                state.phase = "resolve"
                self.turns_remaining = 999  # keep going until someone dies

        # If we just entered build but there's nothing to play, auto-resolve
        if state.phase == "build" and not state.hand and not state.deck:
            state.phase = "resolve"
            self.turns_remaining = 999

    def _enter_end_phase(self, result: str):
        if result == "win":
            self.state.phase = "reward"
            self.end_text.text = "VICTORY!"
            self.end_text.color = arcade.color.GOLD
        else:
            self.state.phase = "gameover"
            self.end_text.text = "DEFEAT"
            self.end_text.color = arcade.color.RED

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def on_draw(self):
        self.clear()

        # Character panels (M10)
        if self.hero_panel:
            self.hero_panel.draw()
        if self.enemy_panel:
            self.enemy_panel.draw()

        # Battle log (M10)
        if self.battle_log_display:
            self.battle_log_display.draw()

        # Lock slot backgrounds
        self.slot_list.draw()

        # Locked cards (cards that sit in slots)
        self.lock_list.draw()
        self._draw_card_texts(self.lock_list)

        # Deck pile (decorative)
        self.deck_pile.draw()

        # Hand cards
        self.hand_list.draw()
        self._draw_card_texts(self.hand_list)

        # Held card (on top of everything)
        if self.held_card:
            held_list = arcade.SpriteList()
            held_list.append(self.held_card)
            held_list.draw()
            self._draw_card_texts(held_list)

        # HUD
        self.feedback_text.draw()
        self.mana_text.draw()
        self.mana_label_text.draw()

        # GUI (CAST button)
        self.ui_manager.draw()

        # End-of-battle overlay
        if self.state.phase in ("reward", "gameover"):
            self.end_text.draw()

    @staticmethod
    def _draw_card_texts(sprite_list: arcade.SpriteList):
        for card in sprite_list:
            card.token_text.x = card.center_x
            card.token_text.y = card.center_y + 10
            card.token_text.draw()
            card.label_text.x = card.center_x
            card.label_text.y = card.center_y - 30
            card.label_text.draw()

    def _sync_panels(self):
        """Update panel HP text from current Character data."""
        if self.hero_panel:
            self.hero_panel.update(self.state.hero)
        if self.enemy_panel:
            self.enemy_panel.update(self.state.enemy)

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self.state.phase != "build":
            return

        # Try lifting a locked card out of its slot
        cards = arcade.get_sprites_at_point((x, y), self.lock_list)
        if cards:
            card = cards[-1]
            self._lift_from_slot(card)
            self.held_card = card
            self.held_offset_x = card.center_x - x
            self.held_offset_y = card.center_y - y
            return

        # Try picking up a hand card — remove from hand so the gap closes
        cards = arcade.get_sprites_at_point((x, y), self.hand_list)
        if cards:
            card = cards[-1]
            self.hand_list.remove(card)
            if card.card_data in self.state.hand:
                self.state.hand.remove(card.card_data)
            self._recompute_hand_positions()
            self.held_card = card
            self.held_offset_x = card.center_x - x
            self.held_offset_y = card.center_y - y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.held_card:
            self.held_card.center_x = x + self.held_offset_x
            self.held_card.center_y = y + self.held_offset_y

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.held_card:
            return

        card = self.held_card
        self.held_card = None

        # Attempt to dock into a slot
        if self.state.mana >= 1:
            hits = arcade.check_for_collision_with_list(card, self.slot_list)
            for slot in hits:
                if slot.card is None:
                    self._dock_card(card, slot)
                    return

        # Return to hand at the closest position
        self._insert_into_hand(card)

    # ------------------------------------------------------------------
    # Dock / undock helpers
    # ------------------------------------------------------------------

    def _dock_card(self, card: CardSprite, slot):
        """Snap *card* into *slot*, deduct mana, update parser feedback.

        Card must already be removed from hand (picked-up cards are
        taken out of hand_list/state.hand on mouse press).
        """
        card.position = slot.position
        self.lock_list.append(card)
        slot.card = card
        card.is_locked = True
        card.slot_index = slot.slot_index
        self.state.lock[slot.slot_index] = card.card_data
        self.state.mana -= 1
        self._update_feedback()

    def _lift_from_slot(self, card: CardSprite):
        """Lift *card* out of its slot and refund mana. Does NOT return to hand."""
        for slot in self.slot_list:
            if slot.card is card:
                slot.card = None
                self.state.lock[slot.slot_index] = None
                break
        self.lock_list.remove(card)
        card.is_locked = False
        card.slot_index = -1
        self.state.mana = min(self.state.mana + 1, self.state.max_mana)
        self._update_feedback()

    def _insert_into_hand(self, card: CardSprite):
        """Insert *card* into hand at the position closest to its x-coordinate."""
        count = len(self.state.hand)
        new_count = count + 1
        total_width = new_count * CARD_WIDTH + (new_count - 1) * HAND_GAP
        start_x = (SCREEN_WIDTH - total_width) / 2 + CARD_WIDTH / 2

        # Within a card's height of the hand row → pick nearest gap
        best_idx = count
        if abs(card.center_y - HAND_Y) <= CARD_HEIGHT:
            best_dist = float("inf")
            for i in range(new_count):
                pos_x = start_x + i * (CARD_WIDTH + HAND_GAP)
                dist = abs(card.center_x - pos_x)
                if dist < best_dist:
                    best_dist = dist
                    best_idx = i

        self.state.hand.insert(best_idx, card.card_data)
        self._sync_hand()

    # ------------------------------------------------------------------
    # CAST
    # ------------------------------------------------------------------

    def _on_cast_click(self, _event):
        if self.state.phase != "build":
            return

        # Nothing docked?
        has_cards = any(slot.card for slot in self.slot_list)
        if not has_cards:
            self.feedback_text.text = "Nothing to cast!"
            self.feedback_text.color = arcade.color.RED
            return

        # Separate action cards from grammar cards
        action_cards = []
        grammar_tokens = []
        for slot in self.slot_list:
            if not slot.card:
                continue
            if slot.card.card_data.get("type") == "action":
                action_cards.append(slot.card.card_data)
            else:
                grammar_tokens.append(slot.card.card_data["token"])

        # Dispatch action cards
        for card_data in action_cards:
            dispatch_action(card_data, self.state)
            msg = f"PLAYED: {card_data['label']}"
            self.state.battle_log.append(msg)
            self.battle_log_display.push(msg)

        # Parse grammar cards as ESENS and apply potion
        cast_text = None
        if grammar_tokens:
            esens_string = "".join(grammar_tokens)
            try:
                result = parse_esens(esens_string)
                potion_log = apply_potion(result["dict"], self.state)
                self.state.battle_log.append(f"CAST: {result['explanation']}")
                self.battle_log_display.push(f"CAST: {result['explanation']}")
                if potion_log:
                    self.state.battle_log.append(potion_log)
                    self.battle_log_display.push(potion_log)
                cast_text = f"Cast: {result['explanation']}"
            except ESENSParseError:
                self.feedback_text.text = "Invalid potion!"
                self.feedback_text.color = arcade.color.RED
                return

        # Clear lock slots
        for slot in self.slot_list:
            if slot.card:
                self.lock_list.remove(slot.card)
                slot.card = None
        self.state.lock = [None] * self.state.slot_count

        # Refill hand from deck
        self._draw_cards_from_deck(self.state.hand_size - len(self.state.hand))
        self._full_sync()

        # Show result
        if cast_text:
            self.feedback_text.text = cast_text
            self.feedback_text.color = arcade.color.YELLOW_GREEN
        elif action_cards:
            names = ", ".join(c["label"] for c in action_cards)
            self.feedback_text.text = f"Played: {names}"
            self.feedback_text.color = arcade.color.YELLOW_GREEN

        # Sync panels after potion effects
        self._sync_panels()

        # Transition to post_cast auto-play turns
        self.state.phase = "post_cast"
        self.turns_remaining = POST_CAST_TURNS
        self.turn_timer = 0.0

    # ------------------------------------------------------------------
    # REDRAW
    # ------------------------------------------------------------------

    def _on_redraw_click(self, _event):
        if self.state.phase != "build":
            return
        if self.state.mana < 2:
            self.feedback_text.text = "Not enough mana to redraw!"
            self.feedback_text.color = arcade.color.RED
            return

        self.state.mana -= 2
        redraw_hand(self.state, {})
        self._full_sync()
        self.feedback_text.text = "Hand redrawn!"
        self.feedback_text.color = arcade.color.YELLOW_GREEN

    # ------------------------------------------------------------------
    # Action cards — M8
    # ------------------------------------------------------------------

    def _full_sync(self):
        """Rebuild all sprites from state (after action cards / curses)."""
        # Rebuild slots if slot_count changed (Extra Slot / Shattered Slot)
        if len(self.slot_list) != self.state.slot_count:
            self.slot_list = create_lock_slots(
                self.state.slot_count, SCREEN_WIDTH, SLOT_Y,
            )
            # Trim or extend the lock list to match
            self.state.lock = self.state.lock[:self.state.slot_count]
            while len(self.state.lock) < self.state.slot_count:
                self.state.lock.append(None)
        self._sync_lock()
        self._sync_hand()
        self._update_feedback()

    # ------------------------------------------------------------------
    # State ↔ sprite helpers
    # ------------------------------------------------------------------

    def _build_deck_pile(self):
        """Build the decorative deck pile to the right of the hand."""
        self.deck_pile = arcade.SpriteList()
        colors = [random.choice(DECK_BROWNS) for _ in range(DECK_PILE_COUNT)]
        random.shuffle(colors)
        for i, color in enumerate(colors):
            card = arcade.SpriteSolidColor(CARD_WIDTH, CARD_HEIGHT, color=color)
            card.center_x = DECK_X + i * DECK_OFFSET
            card.center_y = HAND_Y + i * DECK_OFFSET
            self.deck_pile.append(card)

    def _draw_cards_from_deck(self, count):
        """Move up to *count* cards from deck to hand. Curses fire on draw."""
        for _ in range(count):
            if not self.state.deck:
                break
            card = self.state.deck.pop()
            if card.get("type") == "curse" and card.get("on_draw"):
                dispatch_action(card, self.state)
                msg = f"CURSE: {card['label']}!"
                self.state.battle_log.append(msg)
                if self.battle_log_display:
                    self.battle_log_display.push(msg)
                continue  # curse fires and vanishes
            self.state.hand.append(card)

    def _sync_hand(self):
        """Rebuild hand_list sprites from state.hand."""
        self.hand_list = arcade.SpriteList()
        count = len(self.state.hand)
        if count == 0:
            return
        total_width = count * CARD_WIDTH + (count - 1) * HAND_GAP
        start_x = (SCREEN_WIDTH - total_width) / 2 + CARD_WIDTH / 2
        for i, card_data in enumerate(self.state.hand):
            sprite = CardSprite(card_data)
            sprite.center_x = start_x + i * (CARD_WIDTH + HAND_GAP)
            sprite.center_y = HAND_Y
            sprite.home_position = (sprite.center_x, sprite.center_y)
            self.hand_list.append(sprite)

    def _sync_lock(self):
        """Rebuild lock_list and slot.card references from state.lock."""
        self.lock_list = arcade.SpriteList()
        for slot in self.slot_list:
            card_data = self.state.lock[slot.slot_index]
            if card_data:
                sprite = CardSprite(card_data)
                sprite.position = slot.position
                sprite.is_locked = True
                sprite.slot_index = slot.slot_index
                slot.card = sprite
                self.lock_list.append(sprite)
            else:
                slot.card = None

    def _recompute_hand_positions(self):
        """Re-space hand cards without rebuilding sprites."""
        count = len(self.hand_list)
        if count == 0:
            return
        total_width = count * CARD_WIDTH + (count - 1) * HAND_GAP
        start_x = (SCREEN_WIDTH - total_width) / 2 + CARD_WIDTH / 2
        for i, card in enumerate(self.hand_list):
            pos = (start_x + i * (CARD_WIDTH + HAND_GAP), HAND_Y)
            card.home_position = pos
            if card is not self.held_card:
                card.position = pos

    def _update_feedback(self):
        """Re-parse lock contents and update feedback + mana text."""
        tokens = []
        for slot in self.slot_list:
            if slot.card:
                tokens.append(slot.card.card_data["token"])
        esens_string = "".join(tokens)

        if not esens_string:
            self.feedback_text.text = ""
            self.feedback_text.color = arcade.color.GRAY
        else:
            try:
                result = parse_esens(esens_string, explain=True)
                self.feedback_text.text = result["explanation"]
                self.feedback_text.color = arcade.color.GREEN
            except ESENSParseError:
                self.feedback_text.text = "Incomplete notation..."
                self.feedback_text.color = arcade.color.GRAY

        self.mana_text.text = f"{self.state.mana}/{self.state.max_mana}"
