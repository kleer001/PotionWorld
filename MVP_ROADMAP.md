# MVP Implementation Roadmap

Step-by-step build plan for the Guardian Angel card battler.
Each milestone is playable. Ship early, iterate.

Reference: `MVP_GAME_DOC.md` (design), `CLAUDE.md` (architecture),
`GRAMMAR_LADDER.md` (grammar sequence), `cards.toml` (card data).

---

## Milestone 0 — Skeleton Window

**Goal:** An Arcade window opens. A View draws something. We can close it.

**Files:**
- `grammar_mvp/main.py`
- `grammar_mvp/views.py`

**Build:**
- `main.py`: create `arcade.Window(1280, 720, "Potion Primer")`,
  call `window.run(view=BattleView())`
- `BattleView(arcade.View)`:
  - `on_show_view()` → set `self.window.background_color`
  - `on_draw()` → `self.clear()`, draw a single `arcade.Text("Potion Primer")`
  - `on_key_press()` → ESC to close

**Done when:** Window opens, shows text, closes on ESC.

---

## Milestone 1 — GameState + Card Loading

**Goal:** Game state exists. Cards load from TOML. Nothing drawn yet beyond
a debug print.

**Files:**
- `grammar_mvp/game_state.py`
- `grammar_mvp/cards.py`
- `grammar_mvp/data/cards.toml` (already exists)

**Build:**

`game_state.py`:
```
@dataclass
class Character:
    name: str
    hp: int
    max_hp: int
    strength: int
    defense: int

@dataclass
class GameState:
    hero: Character
    enemy: Character
    mana: int
    max_mana: int
    deck: list          # Card dicts remaining in deck
    hand: list          # Card dicts in hand
    lock: list          # [Card|None] per slot
    slot_count: int
    hand_size: int
    phase: str          # "preview", "build", "resolve", "reward"
    battle_log: list    # recent message strings
    turn: int
```

`cards.py`:
- `load_cards(path) -> dict[str, dict]` — parse `cards.toml` with
  `tomllib` (stdlib in 3.11+). Resolve `ref` fields: if a card has
  `ref`, load that file's `[card]` table, then overlay the inline fields
  on top (inline wins). Return a dict keyed by card ID.
- `load_starter_deck(card_db) -> list[dict]` — read `[starter_deck]`
  from TOML, return list of card dicts (with duplicates).
- `build_deck(card_ids, card_db) -> list[dict]` — turn a list of card
  ID strings into a list of card dicts, shuffled.

**Done when:** `python -c "from grammar_mvp.cards import load_cards; print(load_cards())"` prints all 56 cards.

---

## Milestone 2 — Cards On Screen

**Goal:** Hand of cards drawn on screen. No interaction yet.

**Files:**
- `grammar_mvp/cards.py` (add CardSprite)
- `grammar_mvp/views.py` (update BattleView)

**Build:**

`CardSprite(arcade.SpriteSolidColor)`:
- Constructor takes a card dict. Creates an 80x120 solid color
  rectangle using the card's `color` field.
- Stores: `self.card_data` (the dict), `self.home_position`,
  `self.is_locked`, `self.slot_index`
- Two `arcade.Text` objects attached: token (large, centered) and
  label (small, bottom). These are drawn manually in `BattleView.on_draw()`
  at the sprite's current position — they are NOT children of the sprite.
  Store them as `self.token_text` and `self.label_text`.

`BattleView` updates:
- `on_show_view()`:
  - Create `GameState` with starter deck, shuffle, draw `hand_size` cards
  - Create `self.hand_list = arcade.SpriteList()` with `CardSprite` per hand card
  - Space cards evenly across bottom third of screen
- `on_draw()`:
  - `self.hand_list.draw()`
  - Loop `self.hand_list`, draw each card's `token_text` and `label_text`
    at the sprite's current `center_x`, `center_y`

**Done when:** Window shows a row of colored cards at the bottom with
token symbols and labels visible.

---

## Milestone 3 — Lock Slots On Screen

**Goal:** Empty lock slots visible. No interaction yet.

**Files:**
- `grammar_mvp/views.py`
- `grammar_mvp/display.py`

**Build:**

`display.py`:
- `create_lock_slots(slot_count, screen_width, y_center) -> arcade.SpriteList`:
  Create `slot_count` `arcade.SpriteSolidColor(80, 120, color=DARK_GRAY)`
  sprites, spaced evenly, return as a `SpriteList`.

`BattleView` updates:
- `on_show_view()`: create `self.slot_list` via `create_lock_slots()`
- `on_draw()`: draw `self.slot_list`

**Done when:** Row of dark empty slots visible in the middle of the screen,
above the hand.

---

## Milestone 4 — Drag Cards

**Goal:** Player can pick up cards and move them with the mouse.

**Files:**
- `grammar_mvp/views.py`

**Build:**

Add to `BattleView`:
- `self.held_card: CardSprite | None = None`
- `self.held_offset_x`, `self.held_offset_y`

Mouse handlers:
- `on_mouse_press(x, y, button, modifiers)`:
  - `cards = arcade.get_sprites_at_point((x, y), self.hand_list)`
  - Also check `self.lock_list` (for undocking — see M5)
  - If hit: set `self.held_card`, compute offset from card center
- `on_mouse_drag(x, y, dx, dy, buttons, modifiers)`:
  - If `self.held_card`: update `center_x`, `center_y` with offset
- `on_mouse_release(x, y, button, modifiers)`:
  - If no held card: return
  - (Snap logic comes in M5 — for now, just return to home position)
  - `self.held_card.position = self.held_card.home_position`
  - `self.held_card = None`

**Done when:** Cards can be picked up, dragged around, and snap back to
their hand position on release.

---

## Milestone 5 — Dock and Undock

**Goal:** Cards snap into lock slots. Cards can be pulled back out.

**Files:**
- `grammar_mvp/views.py`

**Build:**

Update `on_mouse_release`:
- `hits = arcade.check_for_collision_with_list(self.held_card, self.slot_list)`
- If hit AND slot is empty:
  - Snap card to slot center: `held_card.position = slot.position`
  - Move sprite from `self.hand_list` to `self.lock_list`
  - Set `slot.card = held_card`, `held_card.is_locked = True`,
    `held_card.slot_index = slot.slot_index`
  - Deduct 1 mana
- Else: return card to `home_position`

Update `on_mouse_press`:
- Also check `self.lock_list` for pickup
- If picking up a locked card: clear the slot, move sprite back to
  `self.hand_list`, refund 1 mana, set `is_locked = False`

**Done when:** Cards snap into slots with a satisfying lock. Pull them
back out and they return to hand. Mana count changes.

---

## Milestone 6 — Live Parser Feedback

**Goal:** As cards dock, the composed ESENS string is parsed live.
Feedback text shows under the lock slots.

**Files:**
- `grammar_mvp/views.py`

**Build:**

Add to `BattleView`:
- `self.feedback_text = arcade.Text("", x=..., y=..., color=WHITE, font_size=14)`
- `self.mana_text = arcade.Text("MANA: 10/10", ...)`

Add method `update_parser_feedback()`:
- Read lock slots left to right → compose ESENS string from
  `slot.card.card_data["token"]` for non-None slots
- Try `parse_esens(esens_string, explain=True)`
  - Success: `self.feedback_text.text = result["explanation"]`,
    color green
  - `ESENSParseError`: `self.feedback_text.text = "Incomplete..."`,
    color gray
- Update `self.mana_text.text`

Call `update_parser_feedback()` after every dock/undock.

Draw both text objects in `on_draw()`.

**Done when:** Docking `P` `+` `H` `10` shows "Player gains health by 10"
in green. Partial sequences show gray placeholder. Mana updates.

---

## Milestone 7 — CAST Button

**Goal:** A button that fires the potion. Validates, shows result.

**Files:**
- `grammar_mvp/views.py`

**Build:**

Add to `BattleView.__init__`:
- `self.ui_manager = arcade.gui.UIManager()`
- Create `arcade.gui.UIFlatButton(text="CAST", width=120, height=50)`
- Set `button.on_click = self.on_cast_click`
- Add button to a `UIAnchorLayout`, anchor to middle-right of lock area
- `on_show_view()`: `self.ui_manager.enable()`
- `on_hide_view()`: `self.ui_manager.disable()`
- `on_draw()`: `self.ui_manager.draw()` (after sprites)

`on_cast_click(event)`:
- Compose ESENS string from lock slots
- If empty or invalid: flash red, return
- `result = parse_esens(esens_string)`
- Apply effect to `self.state` (hero or enemy) — defer full
  battle resolution to M9
- For now: just print to battle log and clear the lock slots
- Move locked cards to a discard pile (or just remove from lock_list)
- Refill hand from deck

**Done when:** Player docks cards, hits CAST, parser validates, lock
clears, hand refills from deck.

---

## Milestone 8 — Action Cards (play from hand)

**Goal:** Non-grammar cards play directly from hand on click/double-click.

**Files:**
- `grammar_mvp/cards.py` (add action dispatch)
- `grammar_mvp/views.py`

**Build:**

`cards.py` — action dispatch:
- `ACTION_REGISTRY: dict[str, Callable]` mapping action names to functions
- `redraw_hand(state, args)` — discard hand, draw hand_size from deck
- `draw_cards(state, args)` — draw `args["count"]` from deck to hand
- `modify_state(state, args)` — `setattr` on the field named in args,
  apply delta. Works for Grace (+3 mana), curses (-2 mana), Extra Slot
  (+1 slot_count), etc.
- `recycle_card(state, args)` — needs UI interaction (pick which locked
  card). For MVP: just undock the rightmost locked card.
- `dispatch_action(card_data, state)` — look up `card_data["action"]`
  in registry, call with `state` and `card_data.get("args", {})`

`views.py` — how action cards are played:
- In `on_mouse_press`: if the clicked card is `type == "action"`,
  don't start a drag. Instead mark it for play.
- In `on_mouse_release`: if the card didn't move (click, not drag),
  and it's an action card, and player has mana:
  - `dispatch_action(card.card_data, self.state)` → mutate state
  - Deduct 1 mana
  - Remove card from hand_list
  - Rebuild hand sprites to reflect new state (e.g. after Redraw)

Curse on_draw:
- In the draw-from-deck logic: when a curse is drawn, immediately
  call `dispatch_action` with `on_draw` and `on_draw_args`, then
  add the card to hand (Dead Weight) or discard it (Mana Drain,
  Heavy Hand, Shattered Slot — they fire and vanish).

**Done when:** Clicking Redraw in hand discards and redraws. Grace adds
mana. Draw 2 pulls extra cards. Curses fire on draw.

---

## Milestone 9 — Battle Engine

**Goal:** Hero and enemy fight. Turns resolve. Someone wins.

**Files:**
- `grammar_mvp/battle.py`
- `grammar_mvp/views.py`

**Build:**

`battle.py`:
- `resolve_turn(attacker: Character, defender: Character) -> str`:
  - `damage = max(1, attacker.strength - defender.defense)`
  - `defender.hp = max(0, defender.hp - damage)`
  - Return log string: `f"{attacker.name} attacks! {damage} dmg. {defender.name}: {defender.hp}/{defender.max_hp}"`
- `apply_potion(parsed_effect, state)`:
  - Read target (P→hero, E→enemy) from parsed effect dict
  - Read stat (H→hp, S→strength, D→defense)
  - Read effect type (+→add, -→subtract)
  - Read magnitude
  - Mutate the target character
  - Handle duration: add to `character.active_effects` with turn counter
- `tick_effects(character)`:
  - Decrement all active effect durations
  - Remove expired effects (reverse the stat change)
- `check_battle_end(state) -> str|None`:
  - Hero HP ≤ 0 → "lose"
  - Enemy HP ≤ 0 → "win"
  - Else → None

`BattleView` updates:
- New `phase` flow in `on_update(delta_time)`:
  - **"preview"**: auto-play turns on a timer (~1 second each).
    Call `resolve_turn` alternating. Append to battle_log.
    After 2-3 turns, switch to **"build"**.
  - **"build"**: player drags cards, docks, casts. CAST button
    calls `apply_potion`, then switches to **"resolve"**.
  - **"resolve"**: auto-play remaining turns on a timer. Tick
    effects each turn. Check for win/lose. When battle ends,
    switch to **"reward"** or **"gameover"**.
  - **"reward"**: show card choices (M10).

**Done when:** Preview turns play out, player builds and casts a potion,
battle resumes and resolves to a win or loss.

---

## Milestone 10 — Battle Display

**Goal:** Hero and enemy visible on screen with HP numbers and a
battle log.

**Files:**
- `grammar_mvp/display.py`
- `grammar_mvp/views.py`

**Build:**

`display.py`:
- `CharacterPanel` — a helper class (or just a draw function) that
  holds references to `arcade.Text` objects for one combatant:
  - Name text (e.g. "Sir Aldric"), positioned above the character area
  - HP text (e.g. "18/40"), positioned below the character area
  - A `arcade.SpriteSolidColor` placeholder rectangle for the
    character portrait
- `create_hero_panel(character, x, y) -> CharacterPanel`
- `create_enemy_panel(character, x, y) -> CharacterPanel`
- `update_panel(panel, character)` — sync HP text from Character data

Battle log:
- `self.log_texts: list[arcade.Text]` — 3-4 `arcade.Text` objects
  stacked vertically below the battle area
- On new log entry: shift texts up, newest at bottom

`BattleView` updates:
- `on_show_view()`: create panels for hero (left) and enemy (right)
  in the top third of the screen
- `on_draw()`: draw panels, draw log texts
- After each turn resolution: `update_panel()` with current Character data

**Done when:** Hero on left, enemy on right, HP numbers beneath each,
battle log scrolling between them. Numbers update as turns resolve.

---

## Milestone 11 — Win/Lose + Reward

**Goal:** Battle ends. Player sees result. On win: pick a card to add
to deck. On lose: retry.

**Files:**
- `grammar_mvp/views.py`

**Build:**

**Win state** (`phase == "reward"`):
- Generate 3 card choices from the card DB (filter by rarity
  appropriate to current battle number)
- Show 3 `CardSprite` objects in the center of the screen
- Click one → add to `state.deck` → start next battle
  (reset enemy, reshuffle deck, deal new hand)

**Lose state** (`phase == "gameover"`):
- Show "YOUR HERO HAS FALLEN" text
- Show retry button → restart same battle (reshuffle deck, deal hand)

**Battle progression:**
- List of enemy stat tuples, hardcoded for MVP:
  ```
  battles = [
      ("Wolf", 25, 7, 3),          # easy
      ("Bandit", 35, 10, 6),       # needs debuffs
      ("Duelist", 40, 12, 9),      # needs duration
      ("Troll", 50, 15, 10),       # needs big potions
      ("Dragon", 60, 18, 14),      # needs everything
  ]
  ```
- After each win: increment battle index, load next enemy

**Done when:** Full game loop — battle, win, pick card, next battle,
harder enemy, repeat until dragon or death.

---

## Milestone 12 — Intro Demo

**Goal:** The game opens with the scripted angel sequence before the
player's first real battle.

**Files:**
- `grammar_mvp/views.py`

**Build:**

New phase: `"demo"`:
- Auto-play a Knight vs Goblin fight for 2-3 turns
- Knight is losing (low HP)
- Animate: light descends, cards auto-dock into slots (`+` `H` `20`)
- Parser feedback appears: "Player gains health by 20"
- Auto-cast: Knight heals, wins the fight
- Text: "That angel is now YOU."
- Transition to first real battle

Implementation:
- Same battle engine, but input is scripted, not player-driven
- Use `on_update` with timers to pace the sequence
- Pre-build the demo hand and auto-dock one card per beat

**Done when:** Player hits start, watches the demo, then plays
their first battle.

---

## Milestone Summary

| # | Milestone | What's playable after | Key files |
|---|-----------|----------------------|-----------|
| 0 | Skeleton Window | Window opens and closes | main, views |
| 1 | GameState + Cards | Cards load from TOML | game_state, cards |
| 2 | Cards On Screen | Hand visible | cards, views |
| 3 | Lock Slots | Slots visible | views, display |
| 4 | Drag Cards | Cards move with mouse | views |
| 5 | Dock and Undock | Cards snap into slots | views |
| 6 | Parser Feedback | Live ESENS explanation | views |
| 7 | CAST Button | Potion fires | views |
| 8 | Action Cards | Non-potion cards work | cards, views |
| 9 | Battle Engine | Turns resolve, win/lose | battle, views |
| 10 | Battle Display | Hero/enemy visible | display, views |
| 11 | Win/Lose + Reward | Full game loop | views |
| 12 | Intro Demo | Scripted opening | views |

**The game is "playable" at M7** — you can dock cards and cast a potion.
**The game is "a game" at M11** — battles, progression, win/lose.
**The game is "polished" at M12** — the demo teaches without words.

---

## Build Order Rationale

Milestones 0-7 are strictly linear — each depends on the last. We go
bottom-up: data first (M1), then visuals (M2-3), then interaction
(M4-5), then validation (M6-7).

M8 (action cards) could come before or after M9 (battle). We put it
before because action cards (Redraw, Grace) make the build phase more
interesting to test even without a real battle running.

M9 and M10 are the battle — engine first (M9, logic only), then
display (M10, visuals). This way we can test battle logic with prints
before worrying about drawing.

M11 closes the loop. M12 is polish.

---

## What We're NOT Building

- Title screen / menus
- Map / run structure
- Enemy variety beyond stat scaling
- Relics / blessings (passive modifiers)
- Sound / music
- Card art (solid color rectangles only)
- Save/load
- Settings
- Deck management screen
- Animation beyond sprite movement

All of these are Tier 1+ features. The MVP proves the core: **grammar
cards dock into slots, compose potions, save heroes.**

---

## Technical Notes

### Arcade 3.x API Reference (verified against 3.3.3)

| Need | Arcade API | Notes |
|------|-----------|-------|
| Window | `arcade.Window(1280, 720, title)` | |
| Views | `arcade.View`, `window.show_view()` | Override `on_show_view`, `on_draw`, etc. |
| Card sprites | `arcade.SpriteSolidColor(80, 120, color=...)` | No image assets needed |
| Sprite groups | `arcade.SpriteList()` | `.append()`, `.remove()`, `.draw()` |
| Card text | `arcade.Text(text, x, y, color, font_size)` | Persistent object, update `.text` property |
| Hit detection | `arcade.get_sprites_at_point((x,y), sprite_list)` | Returns list, topmost = last |
| Drop detection | `arcade.check_for_collision_with_list(sprite, sprite_list)` | Returns list of colliding |
| GUI button | `arcade.gui.UIFlatButton(text, width, height)` | `.on_click` callback |
| GUI manager | `arcade.gui.UIManager()` | `.enable()`, `.disable()`, `.draw()` |
| GUI layout | `arcade.gui.UIAnchorLayout()` | `.add(widget, anchor_x, anchor_y)` |
| Drawing rects | `arcade.draw_lbwh_rectangle_filled(x, y, w, h, color)` | For debug / HP bars later |
| TOML loading | `tomllib.load()` | stdlib in Python 3.11+ |
| ESENS parsing | `parse_esens(str, explain=True)` | Returns `{object, dict, explanation}` |

### Mouse Event Signatures (Arcade 3.x)

```
on_mouse_press(x: int, y: int, button: int, modifiers: int)
on_mouse_release(x: int, y: int, button: int, modifiers: int)
on_mouse_drag(x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int)
on_mouse_motion(x: int, y: int, dx: int, dy: int)
```

### Card Sprite Text Rendering

Arcade `Text` objects are NOT sprite children. They're standalone objects
drawn at explicit coordinates. On each frame:

```python
for card in self.hand_list:
    card.token_text.x = card.center_x
    card.token_text.y = card.center_y + 10
    card.token_text.draw()
    card.label_text.x = card.center_x
    card.label_text.y = card.center_y - 30
    card.label_text.draw()
```

This means text follows the card during drag automatically — we update
positions in `on_draw`, not in `on_mouse_drag`.

### GameState → Sprite Sync Pattern

GameState changes. Sprites must reflect it. The rule: **state changes
trigger sprite rebuilds, never the reverse.**

After any state mutation (cast, action card, turn resolution):
1. Call `sync_hand()` — rebuild `hand_list` from `state.hand`
2. Call `sync_lock()` — rebuild `lock_list` from `state.lock`
3. Call `update_panels()` — update HP texts from characters
4. Call `update_parser_feedback()` — re-parse lock contents
