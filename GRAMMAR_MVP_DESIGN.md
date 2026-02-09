# The Potion Primer — Grammar MVP Design

## Elevator Pitch

A tiny coming-of-age story told in 7 vignettes. Each vignette teaches one layer
of ESENS potion notation. Each lesson ends with a **battle** — two NPCs clashing
in a simple turn-based duel where the hero is doomed to lose... unless the player
writes the right potion. You learn grammar by saving someone's life.

**Scope:** ~500-800 lines of new Python on top of the existing ESENS parser.
Terminal-based or minimal Arcade UI. No Godot, no economy, no gathering, no
Big 5 personalities. Just story, grammar, and consequence.

---

## The Loop

```
┌─────────────────────────────────────────────┐
│  1. STORY BEAT  (3-5 lines of narrative)    │
│         ↓                                   │
│  2. GRAMMAR LESSON  (new notation concept)  │
│         ↓                                   │
│  3. THE CRISIS  (NPC battle begins,         │
│                   hero is losing)            │
│         ↓                                   │
│  4. WRITE THE POTION  (player input)        │
│         ↓                                   │
│  5. WATCH IT WORK  (battle resolves with    │
│                      the potion applied)     │
│         ↓                                   │
│  6. THE ECHO  (one-line emotional coda)     │
└─────────────────────────────────────────────┘
```

The battle is the payoff. You don't just validate notation — you watch it
**land**. The hero was about to die, and the potion you wrote turned the tide.

---

## Battle System (Minimal Viable Combat)

### Two NPCs, Three Stats Each

```
HERO                          VILLAIN
┌──────────────────┐          ┌──────────────────┐
│ HP:  ████████░░  │          │ HP:  ██████████  │
│ STR: 8           │          │ STR: 12          │
│ DEF: 6           │          │ DEF: 10          │
└──────────────────┘          └──────────────────┘
```

- **HP** — health points (0 = lose)
- **STR** — damage dealt per attack (attack = STR - opponent DEF, min 1)
- **DEF** — damage reduced

That's it. No mana, no items, no positioning. Three numbers.

### Battle Flow

1. Show the hero and villain with their stats
2. Run 2-3 "preview turns" so the player can see the hero is losing
   - Display turn-by-turn: `"Villain attacks! 12 STR - 6 DEF = 6 damage. Hero HP: 34/40"`
   - Make it clear: at this rate, the hero loses in N turns
3. **PAUSE** — "The hero reaches for a potion. What does it do?"
4. Player writes ESENS notation
5. Parser validates → potion effect is applied to the battle state
6. Battle resumes with the potion active — hero wins (or at least survives)
7. Display the result with flair

### Why This Works

- The parser already outputs structured effect data (target, stat, magnitude, duration)
- Applying an effect to 3 stats is trivial: `hero.strength += effect.magnitude`
- Duration tracking is just a counter: decrement each turn, remove at 0
- Each skip's battle is **designed to be unwinnable without the right grammar concept**
  - Skip 1: hero needs healing → must learn `P+H`
  - Skip 4: hero needs reactive defense → must learn triggers
  - Skip 6: hero needs stacking/AOE → must learn extended modifiers

---

## The Seven Skips

### Skip 1 — "The Gift" (Age 8)

**Story:** Your grandmother is making dinner. She nicks her finger with a knife
and winces. She looks at you and smiles. "Why don't you make me something for
this?" She slides her old potion notebook across the table, open to the first
page. Three symbols. That's all it takes.

**Grammar:** Target + Effect + Stat + Magnitude
- New tokens: `P` (player), `+` (increase), `H` (health), numbers

**Battle:** Grandmother vs. Kitchen (not a real fight — she keeps pricking
herself on rose thorns in the garden, losing 2 HP/turn). She's at 8/20 HP.
Write a healing potion to get her back up.

**Solution:** `P+H15` (heal player 15 HP)

**The Echo:** "She kissed your forehead. The cut was already gone."

---

### Skip 2 — "The Lesson" (Age 14)

**Story:** First day at the academy. Instructor Thornwood chalks a formula on
the board. "Potions are not permanent," he says, not looking at anyone.
"Neither are your mistakes. But you must learn how long things last."

**Grammar:** Duration
- New tokens: `3T` (3 turns), `C` (combat duration), `P` (permanent)

**Battle:** Academy sparring match. Senior student (STR 10, DEF 8, HP 30) vs.
your friend Rachel (STR 7, DEF 5, HP 25). Rachel is outmatched. She needs a
strength boost, but only for the remaining turns of the match.

**Solution:** `P+S5 3T` (boost strength by 5 for 3 turns) — enough to close
the gap and let Rachel win before it wears off.

**The Echo:** "Thornwood didn't smile. But he didn't not smile either."

---

### Skip 3 — "The Dare" (Age 17)

**Story:** Night in the dormitory. Ezekiel grins at you across a candle.
"They say you can only brew for yourself. But what about... for someone else?
Or *to* someone else?" He slides a vial across the table. "Prove it."

**Grammar:** Multiple targets
- New tokens: `E` (enemy), `A` (all allies), `X` (all enemies)

**Battle:** Ezekiel has gotten himself into trouble — challenged a bully in the
courtyard. The bully (STR 14, DEF 10, HP 40) is destroying Ezekiel (STR 8,
DEF 6, HP 35). You can't boost Ezekiel — you need to *debuff the bully*.

**Solution:** `E-S6 C` (reduce enemy strength by 6 for combat) or
`E-D8 C` (reduce enemy defense by 8 for combat)

**The Echo:** "Ezekiel never told anyone what you did. That was the point."

---

### Skip 4 — "The Competition" (Age 22)

**Story:** The regional potion duel. Your first real competition. The crowd is
loud. Your opponent is fast — she strikes before you can think. You realize:
the best potions don't wait to be used. They *react*.

**Grammar:** Triggers
- New tokens: `>A` (on attack), `<D` (on defend), `^S` (start of turn)

**Battle:** Your champion (STR 10, DEF 7, HP 35) vs. a speed duelist (STR 15,
DEF 5, HP 30). The duelist hits first and hits hard. Raw stats won't save you —
you need a potion that triggers *when the duelist attacks*, punishing her
aggression.

**Solution:** `P+D10 C<D` (boost defense by 10 for combat, triggers on defend)
or `P+S8 C>A` (boost strength by 8 for combat, triggers on attack)

**The Echo:** "She bowed to you after. You hadn't expected that."

---

### Skip 5 — "The Elements" (Age 28)

**Story:** The desert border. You've traveled further than anyone in your
family ever has. The sand burns. The creatures here are different — armored in
fire, weak to water. Your old potions slide off them like rain off stone.
Everything needs an element now.

**Grammar:** Elemental tags
- New tokens: `.F` (fire), `.W` (water), `.E` (earth), `.S` (sky), `.D` (death)

**Battle:** A fire-armored sand drake (STR 16, DEF 14, HP 45, Fire-resistant)
vs. a local ranger (STR 12, DEF 8, HP 35). Normal damage is halved by fire
resistance. The ranger needs a water-element attack boost to break through.

**Solution:** `P+S12 C.W` (boost strength by 12, water element, for combat) —
water element bypasses fire resistance and deals bonus damage.

**The Echo:** "The desert taught you that the world is bigger than your village.
So are its problems."

---

### Skip 6 — "The Masterwork" (Age 35)

**Story:** The royal court. The queen's champion faces three assassins at once.
One potion. One chance. It needs to do more than one thing. It needs to *stack*.
It needs to hit *everyone*.

**Grammar:** Extended modifiers
- New tokens: `.ST` (stacking), `.AR` (area effect), `.DOT` (damage over time)

**Battle:** The champion (STR 14, DEF 12, HP 50) vs. three assassins (STR 10,
DEF 6, HP 20 each). One-on-one the champion wins, but three-on-one is death.
The potion must affect all enemies or stack damage over time.

**Solution:** `X-H5 3T.DOT` (all enemies lose 5 HP per turn for 3 turns, DOT)
or `X-S6 C.AR` (reduce all enemies' strength by 6 for combat, area effect)

**The Echo:** "The queen never learned your name. The champion never forgot it."

---

### Skip 7 — "The Letter" (Age 60)

**Story:** Your study. Late evening. A letter from your grandchild — they're
starting at the academy next year. They ask: "What's the most important potion
you ever made?" You dip your pen. You write one formula. Everything you know,
in a single line.

**Grammar:** Full ESENS — conditionals, chaining, the complete language

**Battle:** The "final exam" — a vision/memory of a legendary battle. An ancient
golem (STR 20, DEF 18, HP 80, Earth-element) vs. a young hero (STR 10, DEF 8,
HP 40). Unwinnable by every measure. The player must write a complex,
multi-layered potion using everything they've learned.

**Solution:** `P+S15 C>A.F.ST.?HP<50%` (boost strength by 15 for combat, on
attack, fire element, stacking, only when HP below 50%) — or any valid complex
notation that turns the tide. Multiple correct answers accepted.

**The Echo:** "You sealed the letter. Some lessons take a lifetime to teach,
and a single line to write."

---

## Technical Architecture

### What We Reuse

- **`ESENS_Parser.py`** — the entire existing parser. `parse_esens()` returns
  structured effect data. `validate_esens()` confirms syntax. The `explain`
  flag generates human-readable descriptions.

### What We Build

```
grammar_mvp/
├── battle.py          # Minimal combat engine (~100-150 lines)
│   ├── Character      # dataclass: name, hp, max_hp, strength, defense, element
│   ├── PotionEffect   # bridges parser output → stat modifications
│   ├── Battle         # runs turn loop, applies effects, tracks duration
│   └── BattleDisplay  # formats combat for terminal output
│
├── story.py           # Story engine (~50-80 lines)
│   ├── load_skip()    # loads a skip from data
│   └── display_skip() # renders narrative text with pacing
│
├── puzzle.py          # Input/validation loop (~60-100 lines)
│   ├── prompt_potion() # gets player input
│   ├── validate()      # calls ESENS parser
│   ├── hint()          # progressive hints on failure
│   └── grade()         # checks if potion actually solves the battle
│
├── game.py            # Main game loop (~50-80 lines)
│   └── play()         # iterates through 7 skips
│
├── data/
│   └── skips.json     # All 7 skip definitions (story, battle setup,
│                      #   valid solutions, hints, grammar concepts)
│
└── display.py         # Terminal formatting (~50-80 lines)
    ├── hp_bar()       # ASCII health bars
    ├── battle_card()  # character stat display
    ├── typewriter()   # slow text reveal for story beats
    └── color()        # ANSI color helpers
```

**Estimated total: ~400-600 lines of new code + ~200 lines of JSON data.**

### Battle Engine Pseudocode

```python
@dataclass
class Character:
    name: str
    hp: int
    max_hp: int
    strength: int
    defense: int
    element: str = None
    active_effects: list = field(default_factory=list)

def resolve_turn(attacker: Character, defender: Character) -> str:
    """One attack. Returns narrative string."""
    damage = max(1, attacker.strength - defender.defense)
    # Element bonus/resistance
    if attacker.element and defender.element:
        damage = apply_element_modifier(damage, attacker.element, defender.element)
    defender.hp = max(0, defender.hp - damage)
    return f"{attacker.name} attacks! {damage} damage. {defender.name} HP: {defender.hp}/{defender.max_hp}"

def apply_potion(effect, battle):
    """Bridge from ESENS parser output to battle state."""
    target = battle.hero if effect.target == "P" else battle.villain
    if effect.stat == "H":
        target.hp = min(target.max_hp, target.hp + effect.magnitude)
    elif effect.stat == "S":
        target.strength += effect.magnitude  # (or -= for debuffs)
    elif effect.stat == "D":
        target.defense += effect.magnitude
    # Track duration for removal
    target.active_effects.append(ActiveEffect(effect, remaining=effect.duration))
```

### Data Format (One Skip)

```json
{
  "skip": 1,
  "title": "The Gift",
  "age": 8,
  "narrative": [
    "Your grandmother is making dinner.",
    "She nicks her finger and winces.",
    "She slides her notebook across the table.",
    "\"Why don't you make me something for this?\""
  ],
  "grammar_intro": {
    "concept": "Target + Effect + Stat + Magnitude",
    "new_tokens": ["P", "+", "H", "<number>"],
    "example": "P+H5",
    "explanation": "Player gains 5 health"
  },
  "battle": {
    "hero": { "name": "Grandmother", "hp": 8, "max_hp": 20, "str": 3, "def": 2 },
    "villain": { "name": "Rose Thorns", "hp": 999, "max_hp": 999, "str": 4, "def": 99 },
    "preview_turns": 2,
    "win_condition": "hero_survives_3_turns"
  },
  "valid_solutions": ["P+H*"],
  "hints": [
    "Who needs help? (P for player)",
    "What direction? (+ to increase)",
    "What stat? (H for health)",
    "How much? (pick a number)"
  ],
  "echo": "She kissed your forehead. The cut was already gone."
}
```

---

## What This Proves

1. **ESENS is learnable** — players can write notation, not just read it
2. **Grammar has stakes** — wrong notation = hero dies, right notation = hero lives
3. **Story carries mechanics** — each grammar concept arrives at an emotionally
   resonant moment, not as a tutorial popup
4. **The parser already works** — we're building a game *around* existing tech
5. **Scope is contained** — 7 screens, 3 stats, no inventory, no economy,
   no open world. Done in days, not months.

---

## Open Questions

- [ ] Terminal-only or minimal GUI (Arcade)?
- [ ] Allow freeform input from Skip 1, or scaffold with blanks early on?
- [ ] Multiple valid solutions per skip, or one canonical answer?
- [ ] Sound? Even terminal beeps for hits would add juice.
- [ ] Save progress between skips, or play all 7 in one sitting (~20 min)?
