# The Potion Primer — Grammar MVP Design

## Elevator Pitch

You are a **Guardian Angel**. Your heroes are dying. The only way to save them
is to write the right potion — in a language you're learning as you go.

Hit start. A hero is already getting beaten down by a goblin. An angel descends,
hands the hero a potion — you see the grammar flash on screen: `P+H10`. The
hero rises. The goblin falls. The hero kneels and prays to the angel. That
angel is about to be **you**.

No backstory. No timeline. No village. Just battles, potions, and grammar —
learned by doing.

**Scope:** ~500-800 lines of new Python on top of the existing ESENS parser.
Terminal-based or minimal Arcade UI. No Godot, no economy, no gathering, no
relationships. Just combat and grammar.

---

## The Fantasy

You are a Guardian Angel. Mortals fight. Mortals lose. You intervene with
potions — divine formulae written in ESENS notation. Each battle you win
**rewards you with new symbols**, expanding what you can write. Your power
grows as your vocabulary grows.

The grammar IS the progression system. New tokens are your XP.

---

## The Opening (No Menus, No Exposition)

```
[PRESS START]

        ⚔️  HERO vs GOBLIN  ⚔️

  Hero    ██░░░░░░░░  12/40 HP       Goblin  ████████░░  35/40 HP

  Goblin attacks! 8 damage!
  Hero HP: 4/40...

  The hero falls to one knee.

        ✦ A light descends from above ✦

  An angel appears. A vial materializes in the hero's hand.

        ╔═══════════════════════╗
        ║      P + H 1 0       ║
        ╚═══════════════════════╝

  The hero drinks. HP restored!

  Hero    ██████░░░░  24/40 HP       Goblin  ████████░░  35/40 HP

  Hero attacks! The goblin falls!

  The hero kneels. "Thank you, Guardian."

        That angel is now YOU.

  ✦ SYMBOLS UNLOCKED: P  +  H  [number] ✦
```

The player just watched the whole loop — crisis, potion, payoff, reward —
before they've touched a single key. Now they know what the game is.

---

## The Loop

```
┌─────────────────────────────────────────────────────┐
│  1. BATTLE STARTS  (hero vs enemy, hero is losing)  │
│         ↓                                           │
│  2. CRISIS MOMENT  (hero about to die)              │
│         ↓                                           │
│  3. ANGEL PROMPT   (you must write a potion)        │
│         ↓                                           │
│  4. WRITE POTION   (player types ESENS notation)    │
│         ↓                                           │
│  5. POTION LANDS   (watch the effect play out)      │
│         ↓                                           │
│  6. HERO WINS      (battle resolves)                │
│         ↓                                           │
│  7. PRAYER + REWARD (new symbols unlocked)          │
└─────────────────────────────────────────────────────┘
```

No narrator. No cutscenes. The battle IS the story. The grammar IS the reward.

---

## Progression: Symbols as Power

The player starts with NOTHING. The intro demo gives them their first symbols.
Each battle won unlocks more. Your **symbol inventory** is always visible.

```
YOUR SYMBOLS:  P  +  H  [number]
```

After each battle, new symbols appear with a flash:

```
✦ NEW SYMBOL UNLOCKED ✦

    3T  —  "for 3 turns"

  Potions can now have DURATION.
  Your power is not permanent. Use it wisely.

YOUR SYMBOLS:  P  E  +  -  H  S  D  [number]  [n]T  C
```

This is the entire progression system. No XP bars, no skill trees, no level-ups.
You literally gain **letters and symbols** — the building blocks of the language.

---

## Battle System (Minimal Viable Combat)

### Two NPCs, Three Stats Each

```
HERO                          ENEMY
┌──────────────────┐          ┌──────────────────┐
│ HP:  ████████░░  │          │ HP:  ██████████  │
│ STR: 8           │          │ STR: 12          │
│ DEF: 6           │          │ DEF: 10          │
└──────────────────┘          └──────────────────┘
```

- **HP** — health points (0 = dead)
- **STR** — damage dealt per attack (attack = STR - opponent DEF, min 1)
- **DEF** — damage reduced

That's it. Three numbers per side. The complexity comes from the POTIONS,
not the combat.

### Battle Flow

1. Show hero and enemy with stats
2. Auto-play 2-3 turns — hero is losing, player watches
3. **CRISIS** — hero is low HP, about to die
4. **ANGEL PROMPT** — "Your hero needs you. Write a potion."
   - Show available symbols
   - Show what the hero needs (in plain English): "The hero needs healing"
5. Player types ESENS notation
6. Parser validates → effect applied to battle
7. Battle resumes — hero wins with the potion's help
8. Hero prays → new symbols unlocked

### Why Battles Are Rigged (By Design)

Every battle is **unwinnable without the specific grammar concept it teaches**.
The enemy is always tuned so that:
- Raw stats alone = hero dies
- Correct potion = hero wins convincingly

This isn't difficulty — it's pedagogy. The player can't brute-force old
symbols. They MUST use the new one.

---

## The Battles (7 Encounters)

### Battle 0 — THE DEMO (Player watches, doesn't play)

**Enemy:** Goblin (STR 8, DEF 4, HP 35)
**Hero:** Wounded Knight (STR 10, DEF 6, HP 12/40)

The angel (AI) descends and gives `P+H10`. Hero heals to 22, wins the fight.
Player sees the full loop demonstrated before they touch anything.

**Unlocks:** `P` `+` `H` `[number]`

---

### Battle 1 — "HEAL" (Player's first potion)

**Enemy:** Wolf (STR 7, DEF 3, HP 25)
**Hero:** Farmer (STR 6, DEF 4, HP 8/30)

The farmer is almost dead. Simple healing is all that's needed. The player
writes their first potion with the symbols they just saw demonstrated.

**Prompt hint:** "The farmer is bleeding out. He needs health."
**Solution:** `P+H15` or any `P+H[enough]`
**Grammar taught:** Target + Effect + Stat + Magnitude (the basics)

**Unlocks:** `E` `-` `S` `D` (enemy targeting, decrease, strength, defense)

---

### Battle 2 — "WEAKEN" (Target the enemy)

**Enemy:** Bandit Captain (STR 14, DEF 10, HP 35)
**Hero:** Town Guard (STR 9, DEF 7, HP 30)

The guard can't scratch the bandit — DEF too high. Healing won't help because
the guard can't deal enough damage to win. The player must target the ENEMY
for the first time.

**Prompt hint:** "The guard's blade bounces off. The bandit is too strong."
**Solution:** `E-D8` or `E-S6` (reduce enemy defense or strength)
**Grammar taught:** Enemy targeting, debuffs

**Unlocks:** `[n]T` `C` (duration — turns and combat)

---

### Battle 3 — "TIMING" (Duration matters)

**Enemy:** Dueling Champion (STR 12, DEF 9, HP 40)
**Hero:** Young Challenger (STR 10, DEF 6, HP 35)

Close fight, but the hero loses in a war of attrition. A permanent buff would
be overpowered (and the player doesn't have `P` for permanent yet). They need
a timed boost — just long enough to win.

**Prompt hint:** "She needs an edge — but only for a few strikes."
**Solution:** `P+S8 3T` (strength boost for 3 turns)
**Grammar taught:** Duration — temporary effects, turns vs. combat

**Unlocks:** `>A` `<D` `^S` (triggers — on attack, on defend, start of turn)

---

### Battle 4 — "REACT" (Trigger-based potions)

**Enemy:** Assassin (STR 18, DEF 4, HP 25)
**Hero:** Knight (STR 10, DEF 12, HP 40)

The assassin hits insanely hard but is fragile. Static buffs aren't enough —
the assassin will kill the knight in 3 hits. The knight needs a potion that
activates WHEN she's attacked, turning the assassin's aggression against him.

**Prompt hint:** "The assassin strikes too fast. The knight needs to react."
**Solution:** `P+D8 C<D` (defense boost on defend) or `E-S10 C>A` (enemy
loses strength whenever they attack)
**Grammar taught:** Triggers — potions that respond to events

**Unlocks:** `.F` `.W` `.E` `.S` `.D` (elements)

---

### Battle 5 — "ELEMENTS" (Elemental advantage)

**Enemy:** Flame Wyrm (STR 16, DEF 14, HP 45, Fire element — resists non-water)
**Hero:** Ranger (STR 12, DEF 8, HP 35)

Normal attacks are halved against the wyrm's fire armor. The ranger needs a
water-element potion to break through. Old notation won't cut it.

**Prompt hint:** "Fire armor. Normal steel is useless. Think about what
beats fire."
**Solution:** `P+S12 C.W` (water-element strength boost for combat)
**Grammar taught:** Elements — adding elemental properties to effects

**Unlocks:** `.ST` `.AR` `.DOT` (stacking, area, damage-over-time)

---

### Battle 6 — "OVERWHELM" (Multi-target / stacking)

**Enemy:** 3x Shadow Thieves (STR 9, DEF 5, HP 18 each)
**Hero:** Paladin (STR 14, DEF 12, HP 50)

The paladin can beat any one thief easily. But three at once deal 3x damage per
round — she drops fast. The player needs area effect or DOT to handle the group.

**Prompt hint:** "Three against one. She can't fight them all alone."
**Solution:** `X-H5 3T.DOT` (all enemies lose 5 HP/turn for 3 turns) or
`X-S5 C.AR` (reduce all enemies' strength for combat, area)
**Grammar taught:** Extended modifiers — AOE, DOT, stacking

**Unlocks:** `.?HP<` `&` (conditionals, chaining)

---

### Battle 7 — "ASCENSION" (Full grammar, the final test)

**Enemy:** The Fallen Angel (STR 20, DEF 18, HP 80, Death element)
**Hero:** The Chosen (STR 12, DEF 10, HP 45)

An angel that fell. Your opposite. The stats are impossible. The player must
compose a complex, multi-layered potion using everything they've learned.
Multiple valid solutions — this is the creative capstone.

**Prompt hint:** "Everything you've learned. One formula. Make it count."
**Solution:** Any valid complex notation, e.g.:
- `P+S15 C>A.S.ST.?HP<50%` (sky-element strength, stacking, triggers on
  attack, activates when low HP)
- `E-D12 C.S&P+S10 C>A` (debuff enemy defense + self-buff on attack)
**Grammar taught:** Full ESENS — conditionals, chaining, the whole language

**Reward:** No new symbols. Instead:

```
The Fallen Angel dissolves into light.
The Chosen looks up.

"I don't need you anymore."

They smile.

        ✦ YOUR HERO HAS ASCENDED ✦

  You taught them everything.
  The grammar of miracles.

                        FIN
```

---

## Symbol Unlock Progression

| Battle | New Symbols Unlocked                    | Cumulative Vocabulary       |
|--------|-----------------------------------------|-----------------------------|
| Demo   | `P` `+` `H` `[number]`                 | 4 tokens                    |
| 1      | `E` `-` `S` `D`                        | 8 tokens                    |
| 2      | `[n]T` `C`                              | 10 tokens                   |
| 3      | `>A` `<D` `^S`                          | 13 tokens                   |
| 4      | `.F` `.W` `.E` `.S` `.D`               | 18 tokens                   |
| 5      | `.ST` `.AR` `.DOT`                      | 21 tokens                   |
| 6      | `.?HP<` `&`                             | 23 tokens                   |
| 7      | —                                       | COMPLETE                    |

---

## What the Player NEVER Sees

- A menu screen (start drops straight into the demo)
- A tutorial popup
- The word "tutorial"
- A narrator explaining things
- Any backstory or lore dump
- An inventory, a shop, a map, a dialogue tree

---

## Technical Architecture

### What We Reuse

- **`ESENS_Parser.py`** — the entire existing parser. `parse_esens()` returns
  structured effect data. `validate_esens()` confirms syntax. The `explain`
  flag generates human-readable descriptions.

### What We Build

```
grammar_mvp/
├── battle.py          # Minimal combat engine (~150 lines)
│   ├── Character      # dataclass: name, hp, max_hp, str, def, element
│   ├── apply_potion() # bridges parser output → stat changes
│   ├── resolve_turn() # one attack round
│   └── run_battle()   # full battle with potion intervention
│
├── puzzle.py          # Angel prompt + validation (~80 lines)
│   ├── prompt_angel() # gets player input, shows available symbols
│   ├── validate()     # calls ESENS parser
│   ├── hint()         # progressive hints on failure
│   └── check_win()    # simulates: does this potion save the hero?
│
├── game.py            # Main loop — iterate battles (~60 lines)
│   ├── intro_demo()   # the scripted demo battle
│   └── play()         # loop through battles 1-7
│
├── display.py         # Terminal formatting (~80 lines)
│   ├── hp_bar()       # ASCII health bars
│   ├── battle_card()  # side-by-side stat display
│   ├── flash()        # symbol unlock animation
│   └── typewriter()   # slow text for dramatic moments
│
└── data/
    └── battles.json   # All 8 battle definitions (demo + 7 player battles)
```

**Estimated total: ~400-500 lines of new code + ~150 lines of JSON data.**

### Battle Data Format

```json
{
  "id": 1,
  "title": "HEAL",
  "hero": {
    "name": "Farmer",
    "hp": 8, "max_hp": 30,
    "str": 6, "def": 4
  },
  "enemy": {
    "name": "Wolf",
    "hp": 25, "max_hp": 25,
    "str": 7, "def": 3
  },
  "preview_turns": 3,
  "prompt_hint": "The farmer is bleeding out. He needs health.",
  "valid_pattern": "P\\+H\\d+",
  "min_heal": 10,
  "symbols_unlocked": ["E", "-", "S", "D"],
  "unlock_flavor": "You can now target enemies. And take things away."
}
```

---

## Open Questions

- [ ] Terminal-only or minimal Arcade/Pygame GUI?
- [ ] Freeform typing from Battle 1, or drag-drop/fill-blank early on?
- [ ] Allow creative solutions or require specific notation?
- [ ] Sound? Even terminal beeps for hits add juice.
- [ ] One sitting (~15-20 min) or save between battles?
- [ ] After beating all 7 — endless mode with random battles + full grammar?
