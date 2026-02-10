# MVP Game Design: Guardian Angel Card Battler

## Elevator Pitch

You are a Guardian Angel. Heroes are dying. You save them by building potions
from cards in your hand — dragging individual symbol cards into docking slots
to compose ESENS notation, then hitting CAST. The potion fires. You watch it
land. The hero lives or dies based on what you built.

Your deck is the ESENS grammar. Your hand is random. Your slots are limited.
Every battle is a puzzle: what's the best potion I can build from what I drew?

---

## The Screen

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   HERO                              ENEMY                       │
│   Sir Aldric                        Cave Troll                  │
│   HP:  ██████░░░░  18/40            HP:  ██████████  50/50      │
│   STR: 8    DEF: 6                  STR: 15   DEF: 12          │
│                                                                 │
│   DMG TAKEN/TURN: 15-6 = 9         DMG TAKEN/TURN: 8-12 = 1   │
│   TURNS TO LIVE: 2                  TURNS TO LIVE: 50           │
│                                                                 │
│ ─────────────────────────────────────────────────────────────── │
│                                                                 │
│   DOCKING SLOTS          ✦ MANA: 12 ✦                          │
│   ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                           │
│   │    │ │    │ │    │ │    │ │    │                             │
│   └────┘ └────┘ └────┘ └────┘ └────┘                            │
│                                                                 │
│                    [ ⚡ CAST ⚡ ]                                │
│                                                                 │
│   YOUR HAND                                                     │
│   ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐            │
│   │ +  │ │ H  │ │ 15 │ │ S  │ │ 3T │ │ -  │ │ 8  │            │
│   │    │ │heal│ │    │ │str │ │    │ │    │ │    │              │
│   └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Key display elements:
- **Battle state** at top — hero vs enemy with visible math
- **"Turns to live"** — the player sees exactly how desperate things are
- **Docking slots** in the middle — the workbench
- **Mana pool** — what you can spend this battle
- **CAST button** — commits the potion
- **Hand** at bottom — your drawn cards, draggable

---

## Core Loop

```
  ┌──────────────────────────────────────┐
  │  1. BATTLE OPENS                     │
  │     Hero vs Enemy stats shown.       │
  │     2-3 preview turns auto-play.     │
  │     "Turns to live" is visible.      │
  │              ↓                       │
  │  2. HAND DEALT                       │
  │     Draw cards from your deck.       │
  │     See your mana pool.              │
  │              ↓                       │
  │  3. BUILD PHASE                      │
  │     Drag cards into slots.           │
  │     Parser live-validates as you go. │
  │     Mana cost updates in real-time.  │
  │              ↓                       │
  │  4. CAST                             │
  │     Hit the button.                  │
  │     Potion effect animates.          │
  │     Stats change visibly.            │
  │              ↓                       │
  │  5. BATTLE RESOLVES                  │
  │     Remaining turns auto-play.       │
  │     Hero wins or dies.               │
  │              ↓                       │
  │  6. REWARD                           │
  │     Win → pick new cards for deck.   │
  │     Lose → try again / game over.    │
  └──────────────────────────────────────┘
```

### The Build Phase In Detail

This is where the game lives. The player is staring at their hand and the
docking slots, trying to construct the best potion they can.

- **Live validation:** As cards are placed, the game shows whether the
  current sequence is valid ESENS. Invalid = slots glow red. Valid = green.
  The parser's human-readable explanation appears below the slots in
  real-time: *"Player gains 15 health"*

- **Live cost:** The mana cost of the current construction updates as cards
  are added. Player can see if they can afford it before casting.

- **Undockable:** Cards can be pulled back out of slots freely. Experiment.
  Try things. No penalty until you hit CAST.

- **Explanation preview:** Before casting, the player sees exactly what the
  potion will do in plain English. No surprises about grammar — the surprise
  is whether the *strategy* works.

### One Cast Per Battle (MVP)

For the MVP, you get one potion per battle. One build. One cast. This keeps
it simple and makes each construction feel weighty. If it doesn't save the
hero, you lose.

Future versions could allow multiple casts per battle (spend more mana, draw
more cards mid-fight), but MVP = one shot.

---

## Card Types

### Grammar Cards (The Potion Language)

These are the ESENS tokens, one per card. They're the core of the game.

**Target Cards**

| Card | Label      | What it means                    |
|------|------------|----------------------------------|
| `P`  | Player     | Effect targets the hero          |
| `E`  | Enemy      | Effect targets the enemy         |
| `A`  | Allies     | Effect targets all allies        |
| `X`  | All Foes   | Effect targets all enemies       |
| `G`  | Global     | Effect targets everyone          |

**Effect Cards**

| Card | Label      | What it means                    |
|------|------------|----------------------------------|
| `+`  | Increase   | Add to a stat                    |
| `-`  | Decrease   | Subtract from a stat             |
| `=`  | Set        | Set stat to exact value          |
| `*`  | Multiply   | Multiply a stat                  |
| `!`  | Nullify    | Zero out a stat                  |
| `#`  | Special    | Apply a status condition         |

**Stat Cards**

| Card | Label      | What it means                    |
|------|------------|----------------------------------|
| `H`  | Health     | Hit points                       |
| `S`  | Strength   | Attack damage                    |
| `D`  | Defense    | Damage reduction                 |
| `L`  | Luck       | Crit chance, drop rates          |
| `M`  | Movement   | Speed / action range             |
| `I`  | Initiative | Turn order                       |
| `C`  | Critical   | Critical hit multiplier          |
| `R`  | Resistance | Elemental resistance             |

**Magnitude Cards**

| Card  | Label     | What it means                   |
|-------|-----------|----------------------------------|
| `5`   | Five      | Small amount                     |
| `10`  | Ten       | Medium amount                    |
| `15`  | Fifteen   | Large amount                     |
| `20`  | Twenty    | Very large amount                |
| `%`   | Percent   | Makes magnitude a percentage     |
| `F`   | Full      | Maximum / restore to full        |

**Duration Cards**

| Card  | Label        | What it means                 |
|-------|--------------|-------------------------------|
| `1T`  | 1 Turn       | Lasts 1 turn                  |
| `2T`  | 2 Turns      | Lasts 2 turns                 |
| `3T`  | 3 Turns      | Lasts 3 turns                 |
| `5T`  | 5 Turns      | Lasts 5 turns                 |
| `C`   | Combat       | Lasts the whole fight         |
| `A`   | Action       | One single action             |
| `P`   | Permanent    | Lasts forever                 |

Note: Duration `C` and `P` share letters with Critical and Player. On the
card face they'd be visually distinct (different color, different border,
maybe an hourglass icon). Context in the slot position also disambiguates.

**Trigger Cards**

| Card  | Label        | What it means                 |
|-------|--------------|-------------------------------|
| `>A`  | On Attack    | Fires when hero attacks       |
| `<D`  | On Defend    | Fires when hero is attacked   |
| `^S`  | Turn Start   | Fires at start of each turn   |
| `vE`  | Turn End     | Fires at end of each turn     |
| `K`   | On Kill      | Fires when target gets a kill |
| `?%`  | Chance       | Random % chance to fire       |

**Element Cards**

| Card  | Label        | What it means                 |
|-------|--------------|-------------------------------|
| `.F`  | Fire         | Fire element                  |
| `.W`  | Water        | Water element                 |
| `.E`  | Earth        | Earth element                 |
| `.S`  | Sky          | Sky element                   |
| `.D`  | Death        | Death element                 |

**Modifier Cards**

| Card   | Label          | What it means                |
|--------|----------------|------------------------------|
| `.ST`  | Stacking       | Effect stacks on reapply     |
| `.AR`  | Area           | Splashes to adjacent targets |
| `.DOT` | Over Time      | Ticks each turn              |
| `.RN`  | Locked         | Can't be removed/dispelled   |
| `.RE`  | Fragile        | Easily dispelled             |

**Advanced Cards (late game)**

| Card     | Label           | What it means               |
|----------|-----------------|------------------------------|
| `~P`     | Soul Link       | Dies if caster dies          |
| `~I`     | Independent     | Persists no matter what      |
| `.VH`    | Hidden          | Enemy can't see the effect   |
| `&`      | Chain           | Link two effects together    |
| `>Heal`  | Afterheal       | Heals when effect expires    |
| `>Expl`  | Afterblast      | Explodes when effect expires |
| `#Echo`  | Echo            | Repeats at intervals         |
| `#Flux`  | Flux            | Fluctuates in strength       |

---

### Non-Potion Cards

These are NOT grammar tokens. They don't go in the docking slots. They're
played directly from the hand for an immediate effect. They add variety,
recovery, and tactical options beyond potion-building.

**Utility Cards**

| Card          | Effect                                           |
|---------------|--------------------------------------------------|
| Redraw        | Discard hand, draw new cards. Costs 1 mana.      |
| Peek          | Reveal enemy's hidden resistances or next action. |
| Extra Slot    | Add a temporary 6th (or 7th) docking slot.        |
| Mana Shard    | Gain +3 mana this battle.                         |
| Quick Cast    | Cast your potion AND draw 3 more cards for a      |
|               | second cast this battle.                          |

**Blessing Cards (Angel-themed)**

| Card              | Effect                                       |
|-------------------|----------------------------------------------|
| Divine Shield     | Hero takes no damage for 1 turn. No slots.   |
| Second Chance     | If the hero dies, revive at 1 HP. One-use.   |
| Radiant Presence  | Enemy STR reduced by 3 for the battle.       |
| Guiding Light     | Show the "optimal" potion hint for 2 mana.   |
| Miracle           | Wild card — becomes any grammar card you need.|

**Curse Cards (picked up from risky choices or bad luck)**

| Card             | Effect                                        |
|------------------|-----------------------------------------------|
| Cracked Vial     | One random grammar card in hand is face-down  |
|                  | (unknown until docked).                       |
| Mana Drain       | Lose 2 mana at the start of this battle.      |
| Shattered Slot   | One docking slot is unusable this battle.      |
| Doubt            | Parser explanation is hidden — cast blind.     |
| Fallen Whisper   | One card in hand is secretly wrong (shows `+`  |
|                  | but acts as `-`).                             |

---

## Progression Roadmap

### How New Cards Reach The Player

**Battle Rewards — Pick One of Three**

After winning a battle, the player picks 1 card from a choice of 3. This is
the primary way the deck grows. Early choices are simple (stat cards, small
magnitudes). Later choices offer triggers, elements, modifiers.

```
  ✦ VICTORY! Choose a card to add to your deck: ✦

  ┌────────┐    ┌────────┐    ┌────────┐
  │   D    │    │  10    │    │   -    │
  │Defense │    │  Ten   │    │Decrease│
  │        │    │        │    │        │
  │ Common │    │ Common │    │Uncommon│
  └────────┘    └────────┘    └────────┘
```

**Rarity Tiers**

| Rarity    | When it appears          | Examples                        |
|-----------|--------------------------|---------------------------------|
| Common    | Always available         | H, S, D, +, 5, 10, 1T, 3T     |
| Uncommon  | After battle 3+          | E (target), -, 20, %, C (dur)  |
| Rare      | After battle 6+          | >A, <D, .F, .W, .ST, F (full) |
| Epic      | After battle 10+         | X, *, !, .DOT, .AR, &          |
| Legendary | After battle 15+ / boss  | #Echo, #Flux, >Expl, Miracle   |

**Starter Deck**

The player begins with a small, fixed deck. Enough to build the simplest
potions.

```
STARTER DECK (14 cards):
  P  P           ← 2x Player target
  +  +  +        ← 3x Increase
  H  H           ← 2x Health
  S              ← 1x Strength
  D              ← 1x Defense
  5  5           ← 2x magnitude 5
  10             ← 1x magnitude 10
  1T             ← 1x duration 1 turn
```

With this deck the player can build:
- `P + H 10`     (heal 10)
- `P + S 5 1T`   (strength +5 for 1 turn)
- `P + D 5`      (defense +5)
- `P + H 5`      (small heal)

They CANNOT build debuffs (no `-`), target enemies (no `E`), or use
elements, triggers, or modifiers. Those come from rewards.

**Duplicate Cards**

Getting a second copy of a card you already own is good. It means you're
more likely to draw it. Want to be a healing build? Grab more `H` and `+`
cards. Want big numbers? Stock up on `15` and `20`. Deck composition
strategy emerges naturally.

### Other Progression Mechanics

**Slot Upgrades**

The player starts with 3 docking slots. At certain milestones (every 4-5
battles), a new slot unlocks:

| Battles won | Slots available | Potion complexity possible     |
|-------------|-----------------|--------------------------------|
| 0           | 3               | P + H 10 (target+effect+stat+mag) |
| 4           | 4               | + duration OR magnitude         |
| 8           | 5               | + trigger OR element            |
| 12          | 6               | Full standard ESENS             |
| 16+         | 7               | Complex compositions            |

This is the invisible tutorial. Slot count caps what you can build. You
can't accidentally over-complicate things because you literally don't have
room.

**Hand Size**

Default hand size: 7 cards. Could be modified by blessings/curses.
Larger hand = more options per battle. Smaller hand = harder choices.

**Deck Thinning**

At rest stops (if we add a map later), the player could remove cards from
their deck. A lean deck draws more consistently. A fat deck has more
variety but less reliability. Classic deckbuilder tension.

### Release Roadmap: Content Tiers

**Tier 0 — The Demo (what we build first)**
- 1 battle that auto-plays (the angel intro)
- 5-8 real battles with escalating difficulty
- Starter deck + common/uncommon card pool
- 3 docking slots, upgrading to 5
- Win/lose states
- No map, no enemy types, no relics, no curses
- **This is the MVP.**

**Tier 1 — "The First Flight"**
- 15 battles in a single run
- Rare cards enter the pool
- Non-potion utility cards (Redraw, Mana Shard, Extra Slot)
- Blessing cards
- Elemental resistances on enemies
- Hand size variations

**Tier 2 — "The Long Watch"**
- Branching map (Slay the Spire style)
- Enemy variety (gimmick enemies that demand specific strategies)
- Curse cards (from elite encounters or risky events)
- Rest stops (heal mana, thin deck)
- Epic cards enter the pool
- Boss encounters

**Tier 3 — "Ascension"**
- Legendary cards
- Ascension difficulty levels (modifiers that make each run harder)
- Persistent meta-progression (unlock new starter decks, card backs, etc.)
- Multi-cast battles (spend mana for additional potion casts)
- Advanced chain and composition cards (&, >Heal, >Expl)
- Leaderboards (fewest cards used, lowest mana spent, fastest clear)

---

## Speculative: Card Costs and Mana Pool

### The Mana Question

Every card placed in a docking slot costs mana. The mana pool is your
budget for the battle. This prevents "just play your best cards every time"
and creates trade-offs.

### Starting Mana

The player starts each battle with a fixed mana pool. Tentatively: **10 mana**
for early battles, scaling slightly as the game progresses or modified by
blessings/curses. Unspent mana does NOT carry over (prevents hoarding /
encourages spending).

### Cost Principles

The cost of a potion is the sum of its card costs. Cards cost more when
they're more powerful or more flexible.

**Target Card Costs**

| Card | Cost | Reasoning                                  |
|------|------|--------------------------------------------|
| `P`  | 0    | Buffing your hero is baseline. Free.       |
| `E`  | 1    | Targeting enemy costs a little more.       |
| `A`  | 2    | All allies — multiplied value.             |
| `X`  | 3    | All enemies — very strong.                 |
| `G`  | 2    | Everyone — double-edged, slightly cheaper. |

**Effect Card Costs**

| Card | Cost | Reasoning                                  |
|------|------|--------------------------------------------|
| `+`  | 0    | Increase is the default. Free.             |
| `-`  | 0    | Decrease is equally basic. Free.           |
| `=`  | 1    | Set is more surgical, slight premium.      |
| `*`  | 2    | Multiply is very powerful.                 |
| `!`  | 3    | Nullify is devastating.                    |
| `#`  | 1    | Special conditions — varies.               |

**Stat Card Costs**

| Card | Cost | Reasoning                                  |
|------|------|--------------------------------------------|
| `H`  | 0    | Health is the basic survival stat. Free.   |
| `S`  | 0    | Strength is basic offense. Free.           |
| `D`  | 0    | Defense is basic defense. Free.            |
| `L`  | 1    | Luck is situational, slight premium.       |
| `M`  | 1    | Movement is tactical, slight premium.      |
| `I`  | 1    | Initiative is powerful (go first).         |
| `C`  | 1    | Critical can spike damage, premium.        |
| `R`  | 1    | Resistance is niche but strong.            |

**Magnitude Card Costs**

| Card | Cost | Reasoning                                  |
|------|------|--------------------------------------------|
| `5`  | 1    | Small effect, cheap.                       |
| `10` | 2    | Medium effect.                             |
| `15` | 3    | Large effect.                              |
| `20` | 5    | Very large. Premium.                       |
| `%`  | 1    | Percentage modifier, adds to base cost.    |
| `F`  | 6    | Full restore. The emergency button.        |

**Duration Card Costs**

| Card | Cost | Reasoning                                  |
|------|------|--------------------------------------------|
| `1T` | 0    | One turn. Barely worth it. Free.           |
| `2T` | 1    | Two turns. Slight cost.                    |
| `3T` | 2    | Three turns. Standard duration.            |
| `5T` | 3    | Five turns. Long-lasting.                  |
| `C`  | 4    | Whole combat. Very strong.                 |
| `A`  | 0    | Single action. Ultra-brief. Free.          |
| `P`  | 7    | Permanent. Extremely powerful, very rare.  |

**Trigger Card Costs**

| Card | Cost | Reasoning                                  |
|------|------|--------------------------------------------|
| `>A` | 1    | On attack — conditional, moderate.         |
| `<D` | 1    | On defend — conditional, moderate.         |
| `^S` | 2    | Turn start — reliable repeating trigger.   |
| `vE` | 1    | Turn end — slightly weaker timing.         |
| `K`  | 0    | On kill — very conditional, high risk.     |
| `?%` | 0    | Chance — gambling. Free because unreliable.|

**Element Card Costs**

| Card | Cost | Reasoning                                  |
|------|------|--------------------------------------------|
| `.F` | 1    | Fire element.                              |
| `.W` | 1    | Water element.                             |
| `.E` | 1    | Earth element.                             |
| `.S` | 1    | Sky element.                               |
| `.D` | 2    | Death. Stronger / rarer. Premium.          |

All elements cost the same (except Death) because their value is
situational — fire is amazing against earth enemies but useless against
water. The cost is for adding the modifier, not for the element's power.

**Modifier Card Costs**

| Card   | Cost | Reasoning                                |
|--------|------|------------------------------------------|
| `.ST`  | 2    | Stacking multiplies value over time.     |
| `.AR`  | 2    | Area effect multiplies targets.          |
| `.DOT` | 1    | DOT is steady, not explosive.            |
| `.RN`  | 2    | Unremovable is a strong guarantee.       |
| `.RE`  | 0    | Fragile is a DOWNSIDE. Free/discount.    |
| `.VH`  | 1    | Hidden info advantage.                   |
| `&`    | 3    | Chaining two effects is very powerful.   |

### Example Mana Calculations

| Potion              | Cards                  | Cost breakdown      | Total |
|---------------------|------------------------|---------------------|-------|
| `P+H10`            | P(0) +(0) H(0) 10(2)  | Basic heal           | 2     |
| `P+H F`            | P(0) +(0) H(0) F(6)   | Full heal            | 6     |
| `P+S5 3T`          | P(0) +(0) S(0) 5(1) 3T(2) | Timed STR buff  | 3     |
| `E-D10 C`          | E(1) -(0) D(0) 10(2) C(4) | Enemy debuff    | 7     |
| `P+S10 C>A.F`      | P(0) +(0) S(0) 10(2) C(4) >A(1) .F(1) | Complex | 8  |
| `X-H5 3T.DOT`      | X(3) -(0) H(0) 5(1) 3T(2) .DOT(1) | AOE poison | 7 |
| `P+S15 C>A.F.ST`   | P(0) +(0) S(0) 15(3) C(4) >A(1) .F(1) .ST(2) | Huge | 11 |

### Mana Balance Principles

- **Cheapest useful potion:** 2 mana (`P+H10` — a basic heal)
- **Average potion:** 4-6 mana (a solid buff or debuff with duration)
- **Expensive potion:** 7-9 mana (targeted debuff for combat, or elemental)
- **All-in potion:** 10+ mana (multi-modifier, uses almost your whole pool)
- **Starting mana (10)** means the player can always afford one decent
  potion, sometimes two if they're cheap, and occasionally one extravagant
  one that drains them

### Mana Scaling Speculation

| Approach           | How it works                              | Pros / Cons            |
|--------------------|-------------------------------------------|------------------------|
| Fixed pool         | Always 10 mana                            | Simple, predictable    |
| Scaling pool       | +1 mana every 3 battles                   | Power grows with player|
| Variable pool      | Random 8-12 mana per battle               | Adds variance/tension  |
| Enemy-based        | Harder enemies give you more mana         | Self-balancing         |
| Grace gain on win  | Win streaks increase pool, loss resets     | Momentum mechanic      |

### Multi-Cast Speculation (Post-MVP)

If we allow multiple casts per battle:
- First cast: costs listed above
- Second cast: draw 3 new cards, costs 1.5x
- Third cast: draw 2 new cards, costs 2x
- Incentivizes getting it right the first time, but gives a safety net

---

## The Demo: What The Player Sees From Moment Zero

**No menus. No title screen. Just a battle.**

```
[PRESS ANY KEY]

        ⚔️  KNIGHT vs GOBLIN  ⚔️

  Knight  ██░░░░░░░░  8/40 HP       Goblin  ████████░░  32/40 HP
  STR: 10   DEF: 6                  STR: 8    DEF: 4

  The knight falls to one knee.

        ✦ A light descends from above ✦

  An angel appears, cards swirling in its hands.
  Three cards drift down into the docking slots:

  ┌────┐ ┌────┐ ┌────┐
  │ +  │ │ H  │ │ 20 │        ← auto-placed by the angel
  └────┘ └────┘ └────┘

  The parser reads: "Player gains 20 health."

        [ ⚡ CAST ⚡ ]         ← button pulses, inviting a click

  [Player clicks CAST]

  ✦ The knight glows. HP surges to 28/40. ✦

  Knight attacks! 10 - 4 = 6 damage. Goblin HP: 26/40.
  Goblin attacks!  8 - 6 = 2 damage. Knight HP: 26/40.
  ...
  Knight wins!

  The knight kneels. "Thank you, Guardian."

  ✦ That angel is now YOU. ✦
  ✦ These cards are now YOURS. ✦

  ┌────┐ ┌────┐ ┌────┐
  │ +  │ │ H  │ │ 20 │   → ADDED TO YOUR DECK
  └────┘ └────┘ └────┘
```

Note: the demo doesn't include `P`. The `P+` is implied. The player's first
real battle uses the same 3-slot structure. `P` as a card is introduced when
`E` (enemy targeting) enters the pool, forcing the player to specify who
they're targeting. Until then, it's always the hero. Of course it is.
You're an angel.

**Battle 1 — Player's first real build:**

Hand is dealt from the starter deck. Player drags cards into 3 slots.
Parser validates. CAST. Watch it play out.

That's the game.

---

## Open Design Questions

- [ ] Can the player rearrange cards in slots, or are they left-to-right
      locked? (Rearrangeable feels better — lets them experiment.)
- [ ] Do non-potion cards (Redraw, Divine Shield) take your whole turn,
      or can they be played alongside a potion cast?
- [ ] Should the parser reject invalid sequences live (red glow) or only
      on CAST (let them try and fail)?
- [ ] Card art direction: abstract symbols? Potion ingredients? Angel
      iconography? Tarot-inspired?
- [ ] Turn timer: should the build phase be timed, or relaxed/untimed?
- [ ] Duplicate card cap: can you have 5 copies of `+` or is there a max?
- [ ] Should magnitude cards be fixed (5, 10, 15, 20) or continuous
      (any number)? Fixed is more "card-like" and constrains choices.
- [ ] What happens on a loss? Retry same battle? Lose a card? Run ends?
