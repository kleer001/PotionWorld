# PotionWorld — Project Guide

See [CLAUDE_GENERIC.md](CLAUDE_GENERIC.md) for general coding standards.

## What This Is

A card-based Guardian Angel potion battler. The player is an angel who saves
dying heroes by composing ESENS potion notation from cards dragged into lock
slots. Grammar IS the game mechanic.

## Key Design Docs

- `MVP_GAME_DOC.md` — Game design: cards, battles, progression, mana
- `GRAMMAR_MVP_DESIGN.md` — Guardian Angel framing, battle flow
- `GRAMMAR_LADDER.md` — Full 74-rung ESENS teaching sequence
- `ESENS_README.md` — ESENS notation spec

## Architecture

### Tech Stack
- **Python 3.10+**
- **Arcade 3.x** — game engine (Window, View, Sprite, SpriteList, gui.UIManager)
- **ESENS_Parser.py** — existing parser. `parse_esens()`, `validate_esens()`

### Project Layout
```
grammar_mvp/           ← the MVP game (what we're building)
  data/
    cards.toml         ← all card definitions (grammar + action + curse)
  battle.py            ← combat engine (Character, turn resolution)
  cards.py             ← card loading, CardSprite, action dispatch
  game_state.py        ← GameState dataclass (single source of truth)
  views.py             ← BattleView (the main Arcade View)
  display.py           ← drawing helpers (character panels, lock slots)
  main.py              ← entry point

ESENS_Parser.py        ← DO NOT MODIFY — the existing parser
```

### Archived (not deleted)
```
archive/monte_carlo/   ← balance sim, mothballed until playtesting
  monte_carlo.py         combat MC simulator (party RPG, LD50, adaptive difficulty)
  FINDINGS.md            preliminary balance analysis
  MANUAL.md              CLI + runtime API reference
  README.md              revival instructions
```

### Core Data Flow
```
cards.toml → Card objects → Deck → Hand (SpriteList)
                                      ↓ drag
                                   Lock Slots
                                      ↓ CAST
                                   ESENS string → Parser → GameState mutation
                                      ↓
                                   Battle resolves → Reward
```

### GameState (single source of truth)
All game logic reads/writes GameState. The View reads GameState to draw.
One-way: GameState → Sprites. Never the reverse.

Key fields: `hero`, `enemy` (Character dataclasses), `mana`, `deck`,
`hand`, `lock` (list of card slots), `slot_count`, `phase`.

### Card Types
- **grammar** — ESENS tokens. Dock in lock slots. Compose potions.
- **action** — Play from hand instantly. Mutate GameState directly.
- **curse** — Trigger on draw. Cannot be played. `on_draw` field in TOML.

### Card Data
All cards defined in `grammar_mvp/data/cards.toml`. Each card has:
`token`, `type`, `category`, `label`, `description`, `mana_cost`, `rarity`, `color`.
Action cards add `action` (function name) and optional `args` table.
Curse cards add `on_draw` and `on_draw_args`.

**Ref files:** Any card can use `ref = "filename.toml"` to load its full
definition from a separate file in `grammar_mvp/data/`. The ref file has a
single `[card]` table. Fields in `cards.toml` override the ref file (local
wins). Use refs for complex cards with multi-step effects or long configs.
See `example_complex_card.toml` for the pattern.

## ESENS Parser

The parser at `ESENS_Parser.py` is complete and working. Do not modify it.
- `parse_esens(notation, explain=True)` → `{object, dict, explanation}`
- `validate_esens(notation)` → `True` or raises `ESENSParseError`
- The `explanation` string is the live feedback shown under lock slots.

## Conventions

- Arcade 3.x API: use `arcade.View`, `arcade.SpriteList`, `arcade.Sprite`,
  `arcade.SpriteSolidColor`, `arcade.Text`, `arcade.gui.UIManager`,
  `arcade.gui.UIFlatButton`, `arcade.get_sprites_at_point()`,
  `arcade.check_for_collision_with_list()`
- Draggable cards: `on_mouse_press` → pickup, `on_mouse_drag` → move,
  `on_mouse_release` → snap to slot or return to hand
- All cards cost 1 mana. No exceptions for now.
- HP only for MVP display. STR/DEF exist in data but aren't shown as stats —
  they appear in the battle log math.
- No health bars. Just `18/40` text under each character.
