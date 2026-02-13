import random
import sys
from itertools import permutations
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
)
from grammar_mvp.animation import BurnAnimation
from grammar_mvp.display import BattleLog, ManaPips, create_hero_panel, create_enemy_panel, create_lock_slots
from grammar_mvp.game_state import Character, GameState
from grammar_mvp import levels as levels_mod
from grammar_mvp.levels import LevelManager, build_level_deck

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

# Timing — turn_delay is read from levels.toml at runtime
POST_CAST_TURNS = 2        # auto-play turns after a cast


class BattleView(arcade.View):

    def __init__(self, level_manager: LevelManager | None = None):
        super().__init__()
        self.level_mgr = level_manager or LevelManager()
        self.state: GameState | None = None
        self.card_db: dict = {}

        # Implied card tracking: slot_index → card_data dict
        self.implied_slots: dict[int, dict] = {}

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
        self.mana_pips: ManaPips | None = None
        self.level_title_text: arcade.Text | None = None
        self.hint_text: arcade.Text | None = None

        # Character panels (M10)
        self.hero_panel = None
        self.enemy_panel = None

        # Battle log display (M10)
        self.battle_log_display: BattleLog | None = None

        # Turn timer (M9)
        self.turn_timer: float = 0.0
        self.turns_remaining: int = 0
        self.hero_attacks_next: bool = True

        # Burn animation queue: [(CardSprite, BurnAnimation), ...]
        self.burn_queue: list[tuple[CardSprite, BurnAnimation]] = []

        # End-of-battle overlay text
        self.end_text: arcade.Text | None = None

        # GUI
        self.ui_manager = arcade.gui.UIManager()

    # ------------------------------------------------------------------
    # View lifecycle
    # ------------------------------------------------------------------

    def on_show_view(self):
        self.window.background_color = (30, 30, 40)

        # Load card database
        self.card_db = load_cards()

        # Build game state from current level
        level = self.level_mgr.current_level
        deck = build_level_deck(level, self.card_db)

        hero_src = level["heroes"][0]
        enemy_src = level["enemies"][0]
        hero = Character(hero_src.name, hero_src.hp, hero_src.max_hp,
                         hero_src.strength, hero_src.defense)
        enemy = Character(enemy_src.name, enemy_src.hp, enemy_src.max_hp,
                          enemy_src.strength, enemy_src.defense)

        self.state = GameState(
            hero=hero,
            enemy=enemy,
            mana=level["mana"],
            max_mana=level["mana"],
            deck=deck,
            hand=[],
            lock=[None] * level["slot_count"],
            slot_count=level["slot_count"],
            hand_size=level["hand_size"],
            phase="build",
            smooth_draws=level.get("smooth_draws", 0),
            smooth_draws_left=level.get("smooth_draws", 0),
        )

        # Build implied card data from level definition
        self.implied_slots = {}
        for token, slot_idx in level["implied_cards"]:
            for card_id, card_data in self.card_db.items():
                if card_data.get("token") == token and card_data.get("type") == "grammar":
                    self.implied_slots[slot_idx] = dict(card_data)
                    break

        # Draw initial hand from deck (smoothed for tutorial levels)
        self._smoothed_draw(self.state.hand_size)
        self._sync_hand()
        self._build_deck_pile()

        # Lock slots
        self.slot_list = create_lock_slots(
            self.state.slot_count, SCREEN_WIDTH, SLOT_Y,
        )

        # Place implied cards into their lock slots
        self._place_implied_cards()
        self._sync_lock()

        # Level title and hint
        self.level_title_text = arcade.Text(
            f"{level['id']}: {level['title']}",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20,
            color=arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
            anchor_y="center",
        )
        self.hint_text = arcade.Text(
            level.get("hint", ""),
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 45,
            color=arcade.color.YELLOW,
            font_size=12,
            anchor_x="center",
        )

        # HUD text
        self.feedback_text = arcade.Text(
            "",
            SCREEN_WIDTH / 2, SLOT_Y + CARD_HEIGHT // 2 + 15,
            color=arcade.color.GRAY,
            font_size=14,
            anchor_x="center",
        )
        self.mana_pips = ManaPips(
            right_x=CAST_X + 50,
            y=SLOT_Y - 45,
            max_mana=self.state.max_mana,
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

        # REDRAW button — to the right of CAST
        redraw_button = arcade.gui.UIFlatButton(
            text="REDRAW (2)", width=120, height=50,
        )
        redraw_button.on_click = self._on_redraw_click
        redraw_anchor = arcade.gui.UIAnchorLayout()
        redraw_anchor.add(
            child=redraw_button,
            anchor_x="center",
            anchor_y="center",
            align_x=440,
            align_y=SLOT_Y - SCREEN_HEIGHT // 2,
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

        # Start combat timer
        self.turn_timer = 0.0
        self.hero_attacks_next = True

    def on_hide_view(self):
        self.ui_manager.disable()

    # ------------------------------------------------------------------
    # Implied cards
    # ------------------------------------------------------------------

    def _place_implied_cards(self):
        """Populate state.lock with implied card data (marked with 'implied' flag)."""
        for slot_idx, card_data in self.implied_slots.items():
            if slot_idx >= self.state.slot_count:
                continue
            implied_data = dict(card_data)
            implied_data["implied"] = True
            self.state.lock[slot_idx] = implied_data

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

        # Tick burn animations
        self._tick_burns(delta_time)

        if phase not in ("reward", "gameover", "gamecomplete"):
            self.turn_timer += delta_time
            if self.turn_timer >= levels_mod.turn_delay:
                self.turn_timer -= levels_mod.turn_delay
                self._play_one_turn()

    def _play_one_turn(self):
        """Resolve one attack turn and check for phase transitions."""
        state = self.state

        # Pick attacker/defender
        if self.hero_attacks_next:
            hp_before = state.enemy.hp
            log = resolve_turn(state.hero, state.enemy)
            damage = hp_before - state.enemy.hp
            if self.enemy_panel:
                self.enemy_panel.shake()
                self.enemy_panel.show_damage(damage)
        else:
            hp_before = state.hero.hp
            log = resolve_turn(state.enemy, state.hero)
            damage = hp_before - state.hero.hp
            if self.hero_panel:
                self.hero_panel.shake()
                self.hero_panel.show_damage(damage)
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

        if state.phase == "post_cast":
            self.turns_remaining -= 1
            if self.turns_remaining <= 0:
                state.phase = "build"

    def _enter_end_phase(self, result: str):
        if result == "win":
            if self.level_mgr.is_last_level:
                self.state.phase = "gamecomplete"
                self.end_text.text = "GAME COMPLETE!"
                self.end_text.color = arcade.color.GOLD
                self._add_end_button("PLAY AGAIN", self._on_restart_game)
            else:
                self.state.phase = "reward"
                self.end_text.text = "VICTORY!"
                self.end_text.color = arcade.color.GOLD
                self._add_end_button("NEXT LEVEL", self._on_next_level)
        else:
            self.state.phase = "gameover"
            self.end_text.text = "DEFEAT"
            self.end_text.color = arcade.color.RED
            self._add_end_button("START OVER", self._on_restart_game, align_x=-220)
            self._add_end_button("REPLAY", self._on_retry, align_x=0)
            self._add_end_button("QUIT", self._on_quit, align_x=220)

    def _add_end_button(self, text: str, callback, *, align_x: int = 0):
        """Add a button below the end-of-battle text."""
        btn = arcade.gui.UIFlatButton(text=text, width=200, height=50)
        btn.on_click = callback
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=btn,
            anchor_x="center",
            anchor_y="center",
            align_x=align_x,
            align_y=-60,
        )
        self.ui_manager.add(anchor)

    def _on_next_level(self, _event):
        self.level_mgr.advance()
        self.window.show_view(BattleView(self.level_mgr))

    def _on_retry(self, _event):
        self.level_mgr.restart_level()
        self.window.show_view(BattleView(self.level_mgr))

    def _on_restart_game(self, _event):
        self.level_mgr.restart_game()
        self.window.show_view(BattleView(self.level_mgr))

    def _on_quit(self, _event):
        arcade.close_window()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def on_draw(self):
        self.clear()

        # Level title and hint
        if self.level_title_text:
            self.level_title_text.draw()
        if self.hint_text:
            self.hint_text.draw()

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

        # Burning cards (on top of hand, below held card)
        self._draw_burns()

        # Held card (on top of everything)
        if self.held_card:
            held_list = arcade.SpriteList()
            held_list.append(self.held_card)
            held_list.draw()
            self._draw_card_texts(held_list)

        # HUD
        self.feedback_text.draw()
        self.mana_pips.draw()

        # GUI (CAST button)
        self.ui_manager.draw()

        # End-of-battle overlay
        if self.state.phase in ("reward", "gameover", "gamecomplete"):
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
    # Burn animation
    # ------------------------------------------------------------------

    # Burn orange target colour (R, G, B)
    _BURN_COLOR = (255, 140, 40)

    def _start_burn(self, card_data: dict, x: float, y: float):
        """Spawn a card sprite at (*x*, *y*) and start its burn animation."""
        sprite = CardSprite(card_data)
        sprite.center_x = x
        sprite.center_y = y
        # Stash the origin so we can apply offsets each frame
        sprite._burn_origin = (x, y)
        anim = BurnAnimation()
        anim.start()
        self.burn_queue.append((sprite, anim))

    def _tick_burns(self, dt: float):
        """Advance all active burns; discard finished ones."""
        alive = []
        for sprite, anim in self.burn_queue:
            anim.update(dt)
            if anim.active:
                ox, oy = sprite._burn_origin
                sprite.center_x = ox + anim.x_offset
                sprite.center_y = oy + anim.y_offset
                sprite.alpha = anim.alpha
                # Blend original colour toward burn orange
                orig = sprite.color[:3]
                t = anim.tint
                r = int(orig[0] * (1 - t) + self._BURN_COLOR[0] * t)
                g = int(orig[1] * (1 - t) + self._BURN_COLOR[1] * t)
                b = int(orig[2] * (1 - t) + self._BURN_COLOR[2] * t)
                sprite.color = (r, g, b, anim.alpha)
                alive.append((sprite, anim))
        self.burn_queue = alive

    def _draw_burns(self):
        """Draw all currently-burning card sprites."""
        for sprite, anim in self.burn_queue:
            burn_list = arcade.SpriteList()
            burn_list.append(sprite)
            burn_list.draw()
            # Fade card text to match
            sprite.token_text.x = sprite.center_x
            sprite.token_text.y = sprite.center_y + 10
            sprite.token_text.color = (255, 255, 255, anim.alpha)
            sprite.token_text.draw()
            sprite.label_text.x = sprite.center_x
            sprite.label_text.y = sprite.center_y - 30
            sprite.label_text.color = (255, 255, 255, anim.alpha)
            sprite.label_text.draw()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self.state.phase in ("reward", "gameover", "gamecomplete"):
            return

        # Try lifting a locked card out of its slot (skip implied cards)
        cards = arcade.get_sprites_at_point((x, y), self.lock_list)
        if cards:
            card = cards[-1]
            if getattr(card, "is_implied", False):
                return  # implied cards cannot be picked up
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
        if self.state.phase in ("reward", "gameover", "gamecomplete"):
            return

        # Check for player-placed cards (not just implied)
        has_player_cards = any(
            slot.card and not getattr(slot.card, "is_implied", False)
            for slot in self.slot_list
        )
        if not has_player_cards:
            self.feedback_text.text = "Nothing to cast!"
            self.feedback_text.color = arcade.color.RED
            return

        # Separate action cards from grammar cards (all slots, including implied)
        action_cards = []
        grammar_tokens = []
        has_player_grammar = False
        for slot in self.slot_list:
            if not slot.card:
                continue
            if slot.card.card_data.get("type") == "action":
                action_cards.append(slot.card.card_data)
            else:
                grammar_tokens.append(slot.card.card_data["token"])
                if not getattr(slot.card, "is_implied", False):
                    has_player_grammar = True

        # Dispatch action cards
        for card_data in action_cards:
            dispatch_action(card_data, self.state)
            msg = f"PLAYED: {card_data['label']}"
            self.state.battle_log.append(msg)
            self.battle_log_display.push(msg)

        # Parse grammar cards as ESENS — only if player placed grammar cards
        cast_text = None
        if grammar_tokens and has_player_grammar:
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
                if not action_cards:
                    # No valid grammar AND no actions — reject entirely
                    self.feedback_text.text = "Invalid potion!"
                    self.feedback_text.color = arcade.color.RED
                    return
                # Actions fired; potion fizzled but cast proceeds
                cast_text = "Potion fizzles... but actions played!"

        # Clear non-implied lock slots from state
        for i in range(self.state.slot_count):
            if self.state.lock[i] and not self.state.lock[i].get("implied"):
                self.state.lock[i] = None

        # Refill hand from deck (plain draw — smoothing is for full hands only)
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
        if self.state.phase in ("reward", "gameover", "gamecomplete"):
            return
        if self.state.mana < 2:
            self.feedback_text.text = "Not enough mana to redraw!"
            self.feedback_text.color = arcade.color.RED
            return

        self.state.mana -= 2
        # Return hand to deck, then smoothed redraw
        self.state.deck.extend(self.state.hand)
        self.state.hand.clear()
        self._smoothed_draw(self.state.hand_size)
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
                # Burn animation: card appears near deck then burns away
                self._start_burn(card, DECK_X, HAND_Y)
                continue  # curse fires and vanishes
            self.state.hand.append(card)

    def _score_hand(self, hand_cards):
        """Score a candidate hand by counting valid potions composable
        from these cards combined with the implied cards in lock slots.

        Returns the number of distinct valid ESENS strings that can be
        formed by placing grammar cards from *hand_cards* into open slots.
        """
        grammar_tokens = [
            c["token"] for c in hand_cards if c.get("type") == "grammar"
        ]
        if not grammar_tokens:
            return 0

        # Implied tokens keyed by slot index
        implied_tokens = {
            idx: cd["token"] for idx, cd in self.implied_slots.items()
        }

        # Open slot indices (not occupied by implied cards)
        open_slots = [
            i for i in range(self.state.slot_count)
            if i not in implied_tokens
        ]
        if not open_slots:
            return 0

        tried: set[str] = set()
        valid = 0
        max_place = min(len(grammar_tokens), len(open_slots))

        for size in range(1, max_place + 1):
            for perm in permutations(grammar_tokens, size):
                slots = dict(implied_tokens)
                for i, token in enumerate(perm):
                    slots[open_slots[i]] = token
                esens = "".join(
                    slots.get(idx, "") for idx in range(self.state.slot_count)
                )
                if esens in tried:
                    continue
                tried.add(esens)
                try:
                    parse_esens(esens)
                    valid += 1
                except ESENSParseError:
                    pass
        return valid

    def _smoothed_draw(self, count):
        """Arena-style hand smoothing for full-hand draws only.

        While ``smooth_draws_left > 0``, shuffle the deck 3 times, peek
        at what would be drawn, score for potion viability, and keep the
        best shuffle.  Each call decrements the budget by one.

        Once the budget is spent (or was zero to begin with), this is a
        plain draw — honest RNG.
        """
        if self.state.smooth_draws_left <= 0 or not self.state.deck:
            self._draw_cards_from_deck(count)
            return

        self.state.smooth_draws_left -= 1
        n_candidates = 3

        best_score = -1
        best_order = None
        peek_count = min(count, len(self.state.deck))

        for _ in range(n_candidates):
            random.shuffle(self.state.deck)
            # Peek at the top cards (drawn via pop from end)
            top = self.state.deck[-peek_count:]
            score = self._score_hand(
                [c for c in top if c.get("type") != "curse"]
            )
            if score > best_score:
                best_score = score
                best_order = list(self.state.deck)

        self.state.deck = best_order
        self._draw_cards_from_deck(count)

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
                # Dim implied cards so the player knows they're fixed
                if card_data.get("implied"):
                    sprite.is_implied = True
                    sprite.alpha = 140
                    sprite.token_text.color = (200, 200, 200, 140)
                    sprite.label_text.color = (200, 200, 200, 140)
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
            if slot.card and slot.card.card_data.get("type") != "action":
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

        # Count docked (non-implied) cards as pending cast cost
        docked = sum(
            1 for s in self.slot_list
            if s.card and not getattr(s.card, "is_implied", False)
        )
        self.mana_pips.update(self.state.mana, self.state.max_mana, docked)
