# Streamlined Minigame Roadmaps - What to Cut

## Purpose
Each minigame should **validate core mechanics only**, not be a complete game. This document identifies elements that can be cut or simplified from each roadmap.

---

## 1. Crafting System - KEEP MOSTLY AS IS ✓
**Core to test:** Success calculation, stat effects, quality determination, mastery progression

**CUT/SIMPLIFY:**
- ~~Phase 4 "Integration prep"~~ (Week 6) - Not needed for prototype
- **Reduce recipes from 10-15 to 5-8** - Enough to test difficulty curve
- **Simplify tool system** - Just 1 tool type with 2-3 quality tiers (not all 3 tool types)
- ~~Preparation mini-games (3.3)~~ - Nice-to-have, not core to crafting validation
- **Batch crafting** - Keep, tests mastery benefits

**New timeline:** 3-4 weeks instead of 5

---

## 2. Relationship System - NEEDS STREAMLINING
**Core to test:** Big 5 personality reactions, affinity calculation, decay mechanics, memory system

**CUT/SIMPLIFY:**
- **Reduce NPCs from 5-8 to 3-4** - Enough to show personality diversity
- ~~Multi-NPC Interactions (3.3)~~ - Gossip system and network visualization beyond core
- ~~Relationship Arcs (4.2)~~ - Multi-stage arcs are quest-like, not core relationship mechanic
- ~~Moral Dilemma System (4.1)~~ - Tested in quest system, redundant here
- **Simplify dialogue system** - Just show personality affects response, don't need full generation
- ~~Week 5 "Complex Scenarios"~~ - Focus on Weeks 1-4 only

**What to keep:**
- Basic personality & affinity (Phase 1) ✓
- Decay & memory (Phase 2) ✓
- Threshold events (Phase 3) ✓
- Personality-based dialogue variance (simplified)

**New timeline:** 3 weeks instead of 5

---

## 3. Combat System - NEEDS STREAMLINING
**Core to test:** Turn structure, ESENS effect application, triggers, status management, AI personality

**CUT/SIMPLIFY:**
- **Reduce opponents from 5-10 to 2-3 archetypes** - Just need to test AI variety
- ~~Multiple victory conditions~~ - Just HP depletion needed for prototype
- ~~Post-duel results/rewards~~ - Tested in progression/economy systems
- ~~Relationship changes from combat~~ - Tested in relationship system
- **Simplify pre-duel** - Just pick 5 potions, skip loadout presets/analysis
- **Reduce action types** - Keep Use Potion, Guard, observe. Cut Provoke, Wait (can add later)

**What to keep:**
- Combat stats & turn structure ✓
- ESENS integration with triggers ✓
- Status effect management ✓
- AI with personality ✓
- Strategic depth (combos, counter-play) ✓

**New timeline:** 3-4 weeks instead of 5

---

## 4. Economy System - NEEDS SIGNIFICANT STREAMLINING
**Core to test:** Pricing formula, supply/demand, ethical pricing choices

**CUT/SIMPLIFY:**
- ~~Competitor system (2.3)~~ - Not core to pricing mechanics
- ~~Ledger & financial reports (3.3)~~ - Nice-to-have, just show gold balance
- ~~Shop upgrades~~ - Tested in progression system, not core to economy
- ~~Special orders & contracts (3.2)~~ - Quest-like, beyond core
- **Simplify customer types** - Just walk-ins with varying budgets. Cut regulars, special orders, emergency
- **Reduce merchant types** - Just 1 general merchant is enough
- ~~Market share tracking~~ - Beyond core

**What to keep:**
- Basic shop operations (buy/sell) ✓
- Dynamic pricing formula ✓
- Supply & demand mechanics ✓
- Ethical pricing dilemmas (2-3 scenarios) ✓
- Simple reputation effect on prices ✓

**New timeline:** 2-3 weeks instead of 5

---

## 5. Progression System - NEEDS STREAMLINING
**Core to test:** XP gain, stat scaling, mastery progression, specialization choices

**CUT/SIMPLIFY:**
- ~~Achievement system (2.3)~~ - Orthogonal to core progression, separate concern
- ~~Multiple reputation tracks (5 tracks)~~ - Just 1-2 to demonstrate concept
- ~~Season transitions (3.3)~~ - Tested in full game, not needed for stat progression
- ~~Skill trees (3.2)~~ - Already marked optional, cut entirely
- **Reduce specializations** - 2-3 per category instead of 4, choose 2-3 total instead of 5

**What to keep:**
- Core stats & XP system ✓
- Stat milestones ✓
- Recipe mastery ✓
- Reputation (1-2 tracks only) ✓
- Specializations (simplified) ✓

**New timeline:** 3 weeks instead of 5

---

## 6. Inventory System - NEEDS STREAMLINING
**Core to test:** Capacity constraints, organization (sort/filter), freshness/degradation

**CUT/SIMPLIFY:**
- ~~Multiple storage locations (3.1)~~ - Just test one inventory with capacity
- ~~Item display for prestige (3.3)~~ - Tested in economy system
- **Reduce inventory types from 4 to 2** - Just ingredients + potions (skip equipment, recipe book tested elsewhere)
- **Simplify equipment system** - Don't need full tool degradation in inventory test
- ~~Transfer mechanics between storages~~ - Not core
- ~~Bulk operations~~ - Nice-to-have, not core

**What to keep:**
- Basic inventory capacity ✓
- Organization (sort, filter, search) ✓
- Freshness/degradation system ✓
- Quality/rarity properties ✓

**New timeline:** 2-3 weeks instead of 5

---

## 7. Quest System - NEEDS SIGNIFICANT STREAMLINING
**Core to test:** Quest structure, objective tracking, moral choices with consequences

**CUT/SIMPLIFY:**
- **Reduce quest types from 6 to 3** - Main Story, Character, Crafting Challenge
- ~~Event system (Phase 3)~~ - Should be separate prototype or cut entirely
- **Simplify world state** - Just track 5-10 key flags, not full world simulation
- ~~Quest chains (4.1)~~ - Single quests demonstrate mechanics, chains are extra
- **Reduce moral dilemmas** - 3-5 scenarios instead of full system
- ~~Relationship arcs~~ - Tested in relationship system

**What to keep:**
- Quest structure & tracking ✓
- Objective progress (sequential & parallel) ✓
- Moral choice framework ✓
- Consequence tracking (simplified) ✓
- Quest states (locked, available, active, completed) ✓

**New timeline:** 3 weeks instead of 5

---

## Summary: Streamlined Timelines

| Minigame | Original | Streamlined | Savings |
|----------|----------|-------------|---------|
| Crafting | 5 weeks | **3-4 weeks** | 1-2 weeks |
| Relationship | 5 weeks | **3 weeks** | 2 weeks |
| Combat | 5 weeks | **3-4 weeks** | 1-2 weeks |
| Economy | 5 weeks | **2-3 weeks** | 2-3 weeks |
| Progression | 5 weeks | **3 weeks** | 2 weeks |
| Inventory | 5 weeks | **2-3 weeks** | 2-3 weeks |
| Quest | 5 weeks | **3 weeks** | 2 weeks |
| **TOTAL** | **35 weeks** | **20-23 weeks** | **12-15 weeks** |

---

## Key Principles for Streamlining

1. **Single responsibility**: Each minigame tests ONE core system
2. **No overlap**: Don't test relationships in combat, economy in progression, etc.
3. **Minimum viable data**: 3-5 examples demonstrate a pattern, not 10+
4. **Skip integration**: No "Week 6 integration prep" - that happens in Godot
5. **Cut nice-to-haves**: If it's not essential to validate the formula/mechanic, cut it
6. **Reduce scope, not depth**: Test fewer examples thoroughly, not many examples shallowly

---

## Next Steps

Would you like me to:
1. **Update all roadmaps** with these streamlined versions?
2. **Pick a specific roadmap** to streamline first as an example?
3. **Adjust the cuts** based on your priorities?
