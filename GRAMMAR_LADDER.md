# ESENS Grammar Ladder — Full Concept Breakdown

## Token Census (from ESENS_Parser.py)

| Category            | Tokens                                           | Count |
|---------------------|--------------------------------------------------|-------|
| Targets             | P, E, A, X, G                                    | 5     |
| Effects             | +, -, =, *, !, #                                 | 6     |
| Stats               | H, S, D, L, G, M, I, C, R, E                    | 10    |
| Magnitude forms     | flat (10), percent (10%), full (F)                | 3     |
| Duration types      | nT, C, P, A, n-mT (range)                        | 5     |
| Triggers            | >A, <D, ^S, vE, K, ?n%, ?condition               | 7     |
| Elements            | .F, .W, .E, .S, .D                               | 5     |
| Special flags       | .ST, .AR, .DOT                                   | 3     |
| Removability        | .RN, .RE, .RD, .RC                               | 4     |
| Chain effects       | >Heal, >Expl, >Sprd, >Trig                       | 4     |
| Source dependency    | ~P, ~E, ~I                                        | 3     |
| Stacking behavior   | Sn, S+, S*, SU                                   | 4     |
| Visibility          | .VH, .VV, .VP                                    | 3     |
| Resource connection  | $MP, $HP, $G                                      | 3     |
| Interaction tags    | .IX, .IA, .IM                                    | 3     |
| Meta effects        | #Gobstop, #Phase, #Echo, #Flux                   | 4     |
| Structural          | . (delimiter), & (chain), , (multi), ?cond        | 4     |
| **TOTAL**           |                                                  | **76** |

76 tokens. But tokens ≠ concepts. Many tokens are "same idea, different
letter" (5 elements all work the same way). The real ladder is about
**new relationships** — new ways symbols connect.

---

## The Ladder: 30 Rungs

Each rung introduces ONE new concept. The player types what's in the
"Player types" column. Everything else is implied or auto-completed by the
game engine until that concept is formally introduced.

### PHASE 1 — "Baby's First Miracle" (Rungs 1-5)
*P+ is implied. You're an angel. Of course you're helping.*

| #  | Concept               | Player types    | Full ESENS     | What's new                          |
|----|-----------------------|-----------------|----------------|-------------------------------------|
| 1  | Health exists         | `H10`           | `P+H10`        | H = health, numbers = amount        |
| 2  | Strength exists       | `S5`            | `P+S5`         | S = strength (a second stat!)       |
| 3  | Defense exists        | `D8`            | `P+D8`         | D = defense (stats are a family)    |
| 4  | Size matters          | `H5` vs `H25`  | `P+H5`/`P+H25` | Magnitude — bigger number = stronger |
| 5  | Percentages           | `S20%`          | `P+S20%`       | % = relative boost, not flat        |

*After Phase 1 the player can buff any of 3 stats with flat or % values.*

---

### PHASE 2 — "Not Everything Lasts" (Rungs 6-10)
*Introducing duration. Potions stop being permanent freebies.*

| #  | Concept               | Player types    | Full ESENS     | What's new                          |
|----|-----------------------|-----------------|----------------|-------------------------------------|
| 6  | Turns exist           | `S5 3T`         | `P+S5 3T`      | 3T = lasts 3 turns, then gone       |
| 7  | Combat duration       | `D10 C`         | `P+D10C`       | C = whole combat (longer than nT)   |
| 8  | Single action         | `S15 A`         | `P+S15A`       | A = one action only (burst)         |
| 9  | Permanent             | `H20 P`         | `P+H20P`       | P = permanent (rare, powerful)      |
| 10 | Duration range        | `S8 2-4T`       | `P+S8 2-4T`    | Uncertain duration (2 to 4 turns)   |

*After Phase 2 the player understands that power has a time cost.*

---

### PHASE 3 — "The Other Side" (Rungs 11-15)
*The training wheels come off. P+ is no longer implied.*

| #  | Concept               | Player types    | Full ESENS     | What's new                          |
|----|-----------------------|-----------------|----------------|-------------------------------------|
| 11 | Reveal: P+            | `P+H10`         | `P+H10`        | Now you type the FULL thing         |
| 12 | Decrease (-)          | `P+D10 C`...but enemy is the problem | — | Setup: buff alone can't win  |
| 13 | Target enemy          | `E-S5 C`        | `E-S5C`        | E = enemy, - = decrease. DEBUFF.    |
| 14 | Enemy defense strip   | `E-D8 3T`       | `E-D8 3T`      | Same grammar, different target      |
| 15 | Full (F) magnitude    | `P+HF`          | `P+HF`         | F = restore to FULL. Max heal.      |

*After Phase 3 the player can buff OR debuff, self OR enemy. The core
sentence structure is complete: WHO + WHAT + WHICH + HOWMUCH + HOWLONG.*

---

### PHASE 4 — "When, Not Just What" (Rungs 16-21)
*Triggers. Potions that react to events instead of firing immediately.*

| #  | Concept               | Player types       | Full ESENS         | What's new                       |
|----|-----------------------|--------------------|--------------------|----------------------------------|
| 16 | On attack trigger     | `P+S8 C>A`         | `P+S8C>A`          | >A = activates when attacking    |
| 17 | On defend trigger     | `P+D10 C<D`        | `P+D10C<D`         | <D = activates when defending    |
| 18 | Turn start trigger    | `P+H3 C^S`         | `P+H3C^S`          | ^S = fires at start of each turn |
| 19 | Turn end trigger      | `E-H2 CvE`         | `E-H2CvE`          | vE = fires at end of turn (DOT-like) |
| 20 | On kill trigger       | `P+S5 CK`          | `P+S5CK`           | K = activates on killing blow    |
| 21 | Chance trigger        | `P+C20 C?50%`      | `P+C20C?50%`       | ?50% = 50% chance each turn      |

*After Phase 4 potions are no longer "fire and forget." They're conditional,
reactive, situational. The player is thinking tactically.*

---

### PHASE 5 — "The World Has Colors" (Rungs 22-26)
*Elements. Rock-paper-scissors layer on top of everything.*

| #  | Concept               | Player types       | Full ESENS         | What's new                       |
|----|-----------------------|--------------------|--------------------|----------------------------------|
| 22 | Fire element          | `P+S10 C.F`        | `P+S10C.F`         | .F = fire-typed. Beats earth.    |
| 23 | Water element         | `P+S10 C.W`        | `P+S10C.W`         | .W = water. Beats fire.          |
| 24 | Earth element         | `P+D8 C.E`         | `P+D8C.E`          | .E = earth. Beats sky.           |
| 25 | Sky element           | `P+S12 C.S`        | `P+S12C.S`         | .S = sky. Beats water.           |
| 26 | Death element         | `E-H10 3T.D`       | `E-H10 3T.D`       | .D = death. The wildcard.        |

*After Phase 5 every potion has an optional elemental flavor. Enemies now
have resistances. The right element doubles damage; the wrong one halves it.*

---

### PHASE 6 — "More Stats" (Rungs 27-33)
*The remaining 7 stats, introduced one at a time as battles demand them.*

| #  | Concept               | Player types       | Full ESENS         | What's new                       |
|----|-----------------------|--------------------|--------------------|----------------------------------|
| 27 | Luck                  | `P+L15 C`          | `P+L15C`           | L = luck (crit chance, drops)    |
| 28 | Movement              | `P+M5 3T`          | `P+M5 3T`          | M = movement (speed/range)       |
| 29 | Initiative            | `P+I10 C`          | `P+I10C`           | I = initiative (who goes first)  |
| 30 | Critical              | `P+C25% C`         | `P+C25%C`          | C = crit chance                  |
| 31 | Resistance            | `P+R20 C.F`        | `P+R20C.F`         | R = resistance (fire resist etc) |
| 32 | Gold                  | `P+G50`            | `P+G50`            | G = gold (economy potion)        |
| 33 | Element stat          | `E-E0 3T`          | `E-E0 3T`          | E stat = strip elemental affinity|

*After Phase 6 the player has access to all 10 stats. Most battles from
here on can be solved many different ways.*

---

### PHASE 7 — "More Effects" (Rungs 34-37)
*Beyond + and -. New ways to change numbers.*

| #  | Concept               | Player types       | Full ESENS         | What's new                       |
|----|-----------------------|--------------------|--------------------|----------------------------------|
| 34 | Set (=)               | `P=H30`            | `P=H30`            | = SET to exact value, not add    |
| 35 | Multiply (*)          | `P*S2 3T`          | `P*S2 3T`          | * = DOUBLE (multiply by 2)       |
| 36 | Nullify (!)           | `E!S3T`            | `E!S3T`            | ! = completely NULLIFY stat       |
| 37 | Special (#)           | `P#Stun1T`         | `P#Stun1T`         | # = special condition (stun etc) |

*After Phase 7 the player has all 6 effect types. = and * are surgical
tools. ! is a hammer. # opens up status conditions.*

---

### PHASE 8 — "More Targets" (Rungs 38-40)
*Beyond P and E. Group targeting.*

| #  | Concept               | Player types       | Full ESENS         | What's new                       |
|----|-----------------------|--------------------|--------------------|----------------------------------|
| 38 | All allies (A)        | `A+H10 C^S`        | `A+H10C^S`         | A = heal ALL allies each turn    |
| 39 | All enemies (X)       | `X-S5 C`           | `X-S5C`            | X = debuff ALL enemies           |
| 40 | Global (G)            | `G-D5 3T`          | `G-D5 3T`          | G = affects EVERYONE (both sides)|

*After Phase 8 all 5 targets are available. Multi-target battles become
possible (multiple allies, multiple enemies).*

---

### PHASE 9 — "Combat Modifiers" (Rungs 41-43)
*How effects behave in battle.*

| #  | Concept               | Player types       | Full ESENS         | What's new                       |
|----|-----------------------|--------------------|--------------------|----------------------------------|
| 41 | Stacking (ST)         | `P+S5 C>A.ST`      | `P+S5C>A.ST`       | .ST = effect stacks each trigger |
| 42 | Area effect (AR)      | `E-H8 3T.AR`       | `E-H8 3T.AR`       | .AR = splash to adjacent targets |
| 43 | Damage over time      | `E-H4 5T.DOT`      | `E-H4 5T.DOT`      | .DOT = ticks each turn           |

---

### PHASE 10 — "Advanced Modifiers" (Rungs 44-55)
*The deep end. Each of these is a modifier that dots onto existing potions.*

| #  | Concept               | Example             | Token(s)    | What's new                           |
|----|-----------------------|---------------------|-------------|--------------------------------------|
| 44 | Removability: locked  | `P+S10 C.RN`        | .RN         | Can't be dispelled                   |
| 45 | Removability: easy    | `E-S8 3T.RE`        | .RE         | Easy to cleanse                      |
| 46 | Removability: hard    | `E-D10 C.RD`        | .RD         | Hard to cleanse                      |
| 47 | Removability: specific| `P#Poison5T.RC`     | .RC         | Needs specific cleanse               |
| 48 | Source: player-linked | `P+S10 C.~P`        | ~P          | Effect dies if caster dies           |
| 49 | Source: enemy-linked  | `E-S8 C.~E`         | ~E          | Effect dies if target dies           |
| 50 | Source: independent   | `P+D5 C.~I`         | ~I          | Persists no matter what              |
| 51 | Visibility: hidden    | `E-S5 C.VH`         | .VH         | Enemy can't see the debuff           |
| 52 | Visibility: all       | `P+S10 C.VV`        | .VV         | Everyone sees it (intimidation)      |
| 53 | Visibility: player    | `P+D8 C.VP`         | .VP         | Only you see it (secret defense)     |
| 54 | Interaction: exclusive| `P+S10 C.IX`        | .IX         | Cancels other STR buffs              |
| 55 | Interaction: additive | `P+S5 C.IA`         | .IA         | Adds with other STR buffs            |
| 56 | Interaction: multiply | `P+S5 C.IM`         | .IM         | Multiplies with other STR buffs      |

---

### PHASE 11 — "Stacking Mastery" (Rungs 57-60)

| #  | Concept               | Example             | Token(s)    | What's new                           |
|----|-----------------------|---------------------|-------------|--------------------------------------|
| 57 | Max stacks            | `P+S5 C>A.ST.S3`    | .S3         | Caps at 3 stacks                     |
| 58 | Add duration on stack | `P+S5 3T>A.ST.S+`   | .S+         | Reapplying extends time              |
| 59 | Multiply on stack     | `P+S5 C>A.ST.S*`    | .S*         | Each stack multiplies effect         |
| 60 | Unique stacking       | `P+S5 C.ST.SU`      | .SU         | Different sources stack separately   |

---

### PHASE 12 — "Chain Reactions" (Rungs 61-64)

| #  | Concept               | Example             | Token(s)    | What's new                           |
|----|-----------------------|---------------------|-------------|--------------------------------------|
| 61 | Chain: heal on expire | `P+S10 3T.>Heal`    | >Heal       | When buff ends, heal                 |
| 62 | Chain: explode        | `E-H0 3T.>Expl`     | >Expl       | When effect ends, AOE damage         |
| 63 | Chain: spread         | `E-S5 3T.>Sprd`     | >Sprd       | When effect ends, jumps to neighbors |
| 64 | Chain: trigger        | `P+D10 3T.>Trig`    | >Trig       | When effect ends, triggers next      |

---

### PHASE 13 — "Economy & Resources" (Rungs 65-67)

| #  | Concept               | Example             | Token(s)    | What's new                           |
|----|-----------------------|---------------------|-------------|--------------------------------------|
| 65 | Costs mana            | `P+S15 C.$MP5`      | $MP         | Drains 5 mana/turn to maintain       |
| 66 | Costs health          | `P+S20 C.$HP3`      | $HP         | Drains 3 HP/turn — power at a price  |
| 67 | Costs gold            | `P+L10 C.$G1`       | $G          | Drains gold/turn — luck costs money  |

---

### PHASE 14 — "Meta Effects" (Rungs 68-71)

| #  | Concept               | Example             | Token(s)    | What's new                           |
|----|-----------------------|---------------------|-------------|--------------------------------------|
| 68 | Gobstopper            | `P+S5 C.#Gobstop`   | #Gobstop    | Transforms into new effects over time|
| 69 | Phase                 | `P+S10 C.#Phase`    | #Phase      | Changes with combat phase            |
| 70 | Echo                  | `P+H5 C.#Echo`      | #Echo       | Repeats at intervals                 |
| 71 | Flux                  | `P+S8 C.#Flux`      | #Flux       | Fluctuates in strength               |

---

### PHASE 15 — "Composition" (Rungs 72-74)
*Combining everything. The final tools.*

| #  | Concept               | Example                     | Token(s)  | What's new                       |
|----|-----------------------|-----------------------------|-----------|----------------------------------|
| 72 | Chaining (&)          | `P+S10 C&E-D5 C`            | &         | Two effects in one potion        |
| 73 | Conditions            | `P+S15 C>A.?HP<30%`         | ?HP<30%   | Only activates under conditions  |
| 74 | Multi-element         | `P+S10 C.F,W`               | ,         | Dual-element potion              |

---

## Summary

| Phase | Name                | Rungs  | New concepts | Running total |
|-------|---------------------|--------|--------------|---------------|
| 1     | Baby's First Miracle| 1-5    | 5            | 5             |
| 2     | Not Everything Lasts| 6-10   | 5            | 10            |
| 3     | The Other Side      | 11-15  | 5            | 15            |
| 4     | When, Not Just What | 16-21  | 6            | 21            |
| 5     | The World Has Colors| 22-26  | 5            | 26            |
| 6     | More Stats          | 27-33  | 7            | 33            |
| 7     | More Effects        | 34-37  | 4            | 37            |
| 8     | More Targets        | 38-40  | 3            | 40            |
| 9     | Combat Modifiers    | 41-43  | 3            | 43            |
| 10    | Advanced Modifiers  | 44-56  | 13           | 56            |
| 11    | Stacking Mastery    | 57-60  | 4            | 60            |
| 12    | Chain Reactions     | 61-64  | 4            | 64            |
| 13    | Economy & Resources | 65-67  | 3            | 67            |
| 14    | Meta Effects        | 68-71  | 4            | 71            |
| 15    | Composition         | 72-74  | 3            | 74            |

**74 rungs. 74 battles. 15 phases.**

That's a FULL game if every rung is a battle. But the MVP doesn't need all
74 — Phases 1-5 (26 rungs) cover the core grammar and make a tight, complete
experience. Phases 6-15 are expansion content.

---

## MVP Cut Line

```
┌─────────────────────────────────────────────────────────┐
│  PHASE 1-5: THE MVP  (26 battles)                       │
│  ─────────────────────────────────────────               │
│  Covers: all targets, +/-, 3 stats, magnitudes,         │
│  durations, triggers, elements                           │
│  Playtime: ~30-45 minutes                                │
│  This IS the game. Ship this.                            │
├─────────────────────────────────────────────────────────┤
│  PHASE 6-9: EXPANSION PACK 1  (17 battles)              │
│  ─────────────────────────────────────────               │
│  Remaining stats, effect types, group targets,           │
│  combat modifiers (ST/AR/DOT)                            │
├─────────────────────────────────────────────────────────┤
│  PHASE 10-15: EXPANSION PACK 2  (31 battles)            │
│  ─────────────────────────────────────────               │
│  Deep modifiers, chains, resources, meta effects,        │
│  composition. The endgame. The grad school.              │
└─────────────────────────────────────────────────────────┘
```
