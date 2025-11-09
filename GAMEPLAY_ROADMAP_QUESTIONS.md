# PotionWorld: Gameplay Roadmap Questions & Modern Player Expectations

## Executive Summary

PotionWorld sits at the intersection of **crafting simulation**, **life simulation**, and **narrative RPG** genres. This document identifies critical design questions that need resolution and outlines what modern players expect from this genre blend.

---

## Part 1: Critical Questions to Iron Out

### 🎮 Core Gameplay Loop Questions

#### 1. What is the minute-to-minute gameplay feel?
**Current State:** Systems exist (crafting, relationships, quests) but the core loop isn't defined.

**Questions to Answer:**
- What does a typical 15-minute play session look like?
- Is this turn-based (like Persona's daily system) or real-time (like Stardew Valley)?
- How much time does a player spend in each activity (crafting 40%, socializing 30%, exploring 20%, managing 10%)?
- Can players "fail" a day/week, or is time more forgiving?

**Modern Player Expectation:** Clear daily/weekly routines with satisfying micro-loops (craft → sell → upgrade → craft better)

**Recommendation:**
```
Morning: Social/Learning/Quest Phase (30 min)
Afternoon: Crafting/Experimentation Phase (30 min)
Evening: Shop Management/Results Phase (15 min)
Night: Story/Relationship Events (Optional, 15 min)

Week ends with: Festival/Tournament/Major Event
Season ends with: Climactic story moment
```

---

#### 2. How complex should ESENS notation be for players?
**Current State:** ESENS parser exists, full notation is powerful but potentially overwhelming.

**Questions to Answer:**
- Do players manually write ESENS notation, or select from pre-built recipes?
- At what point do players see the raw notation vs. simplified descriptions?
- Is understanding ESENS required for casual players, or only for optimization?
- How do we tutorial 17 ingredient types + notation without overwhelming?

**Modern Player Expectation:**
- **Casual players:** Want simple drag-and-drop with visual feedback
- **Hardcore players:** Want to understand and manipulate the notation system
- **Reference:** Opus Magnum (visual programming), Potion Craft (ingredient discovery)

**Recommendation:**
```
Season 1: Visual recipe following (ingredients highlighted, no notation visible)
Season 2: Notation becomes visible but not required to understand
Season 3: Players can modify recipes if they understand notation
Season 4: Reverse-engineering requires notation understanding
Season 5: Create new potions by writing/modifying ESENS
```

---

#### 3. How punishing should failures be?
**Current State:** Crafting has success/failure rates, but consequences aren't defined.

**Questions to Answer:**
- Failed potions: Lost ingredients completely, or partial recovery?
- Failed relationships: Can you recover from -5 affinity, or is that a "dead end"?
- Failed quests: Can they be retried, or are they permanent story branches?
- Failed business: Can your shop go bankrupt, forcing a different path?
- Death: Is there permadeath, or just setbacks?

**Modern Player Expectation:** Meaningful consequences without frustration
- **Soulslike fans:** Expect harsh punishment, resources matter
- **Cozy game fans:** Want low-stakes, forgiving systems
- **Roguelike fans:** Expect failure to teach and enable progress

**Recommendation:**
```
Failed Crafting: 50% ingredient recovery, gain knowledge even on failure
Failed Relationships: Can always recover to 0, but getting to +5 requires specific quests
Failed Quests: Main quests can be retried, side quests may have alternatives
Failed Business: Can go into debt, forcing side jobs, but never permanent game over
Death: No permadeath, but Season 3 combat losses have reputation penalties
```

---

### 🎭 Narrative & Choice Questions

#### 4. How much do choices actually matter?
**Current State:** Moral choice framework exists, but impact scope is unclear.

**Questions to Answer:**
- Can choices lock you out of entire seasons? (e.g., expelled from academy)
- Do choices affect only NPCs, or world state, available quests, and endings?
- Should the game warn players before major choices ("This will have consequences")?
- Can you replay seasons to see different outcomes, or is this one playthrough = one life?
- How many distinct endings exist (3? 10? 50?)?

**Modern Player Expectation:**
- **Narrative game fans:** Expect visible, meaningful consequences (like Disco Elysium, Witcher 3)
- **CRPG fans:** Want branching paths and multiple solutions
- **Life sim fans:** Want to see relationships evolve organically

**Recommendation:**
```
Major Choices: 4-5 per season that affect:
  - Which NPCs become allies/enemies
  - Available quests and opportunities
  - Regional reputation
  - Ending variations (8 main endings, with 3 variations each = 24 total)

Hidden Stats Tracking:
  - Innovation vs. Tradition score
  - Profit vs. Altruism score
  - Community vs. Individual score
  → These determine finale options

No "game over" choices, but some paths are incompatible
  (Can't be both guild master AND rogue alchemist)
```

---

#### 5. How linear vs. open-ended is each season?
**Current State:** 5 seasons defined with themes, but structure isn't specified.

**Questions to Answer:**
- Must players complete Season 1 before Season 2, or can they skip ahead?
- Within a season, how much freedom? (Open world vs. quest chain)
- Can players extend a season indefinitely, or is there a time limit?
- Can you return to previous season locations? (Visit the academy as a master)
- Is New Game+ just harder, or does it unlock new content?

**Modern Player Expectation:**
- **Roguelike fans:** Want replayability with different builds
- **Life sim fans:** Want open-ended time management
- **Story fans:** Want structured narrative with milestones

**Recommendation:**
```
Season Structure: Linear (must complete seasons in order)
  → Each season has 3 Acts with mandatory story beats
  → Between acts, open exploration and side content
  → Season ends when "final quest" is triggered (player choice when)

Time Limit: Soft limit (reputation/opportunities decay if you delay too long)
  → Can spend 50-200 in-game days per season
  → Optimal path is ~100 days, but no hard game over

New Game+:
  → Carry over recipe knowledge (but not items)
  → Unlock "Master Mode" recipes
  → Access hidden NPCs and quests
  → Speedrun-friendly options (skip tutorials, fast-forward)
```

---

### ⚔️ Combat & Challenge Questions

#### 6. How deep should the combat system be?
**Current State:** Turn-based potion combat framework exists, Season 3 is combat-focused.

**Questions to Answer:**
- Is combat avoidable, or mandatory for progression?
- How many combat encounters per season? (Season 3: many, other seasons: few?)
- Should there be difficulty settings (story mode vs. strategic mode)?
- What's the "skill floor" vs. "skill ceiling"? (easy to grasp, hard to master)
- Are there non-combat alternatives (bribe, convince, flee)?

**Modern Player Expectation:**
- **Tactics fans:** Want deep, chess-like combat (Divinity: Original Sin, Into the Breach)
- **Casual fans:** Want combat to be optional or simple
- **Deckbuilder fans:** Want interesting combinations and synergies (Slay the Spire)

**Recommendation:**
```
Season 1: Tutorial duels only (2-3 total)
Season 2: Rare defense scenarios (protect shop from bandits: 1-2 encounters)
Season 3: Main combat season (15-20 duels required, 30+ optional)
  → Tournament bracket system
  → Rising difficulty with personality-based AI
Season 4: Occasional combat (5-7 encounters, mostly solving puzzles vs. fighting)
Season 5: Optional endgame challenges (3 legendary duelists)

Difficulty Options:
  - Story Mode: Auto-win combat, skip if desired
  - Standard: Balanced challenge, requires some strategy
  - Alchemist Mode: Complex AI, limited potions, permadeath consequences
```

---

### 💰 Economy & Progression Questions

#### 7. What is the resource economy balance?
**Current State:** Economy system exists, but scarcity isn't defined.

**Questions to Answer:**
- Should money be tight (struggle to buy ingredients) or abundant (optimize for profit)?
- Can players get "soft-locked" by selling critical ingredients?
- Should rare ingredients be farmable, or one-time finds?
- Is there endgame money sink? (Why keep earning gold in Season 5?)
- Can you "break" the economy (infinite money exploits)?

**Modern Player Expectation:**
- **Survival fans:** Expect scarcity and tough choices
- **Tycoon fans:** Want to optimize and get rich
- **RPG fans:** Expect gradual power curve

**Recommendation:**
```
Season 1: Money is tight (student allowance + small rewards)
  → Forces ingredient gathering and prioritization
  → Can't buy everything, must choose

Season 2: Money becomes comfortable (if you run shop well)
  → Can afford common/uncommon ingredients freely
  → Rare ingredients still require saving or quests

Season 3: Money flows (sponsorships, prize money)
  → Can buy most things
  → Legendary ingredients still quest-locked

Season 4: Money is abundant BUT...
  → Best ingredients aren't for sale (political access required)
  → Money becomes tool for influence, not limitation

Season 5: Money is irrelevant
  → Focus on legacy, not profit
  → Endgame sink: Building research center, funding apprentices

Critical Ingredients: Never sellable if quest-critical (UI warns)
Exploit Prevention: Price scaling (buying 100 of same thing increases cost)
```

---

#### 8. How do stats and skills progress?
**Current State:** Progression system exists with 6 attributes, but XP flow is unclear.

**Questions to Answer:**
- Do stats grow automatically (use-based) or manual (level-up points)?
- Can you max all stats, or must you specialize?
- What unlocks at each stat threshold? (50, 75, 90, 100)
- Are there skill trees, or freeform progression?
- Can you respec, or are choices permanent?

**Modern Player Expectation:**
- **RPG fans:** Want meaningful build diversity (don't want to max everything)
- **Action fans:** Want skill-based progression (player skill > character stats)
- **Life sim fans:** Expect gradual, satisfying growth

**Recommendation:**
```
Hybrid System:
  → Stats grow through USE (craft potions → Precision grows)
  → Each season, choose 1 Specialization (permanent)
  → Stats CAN theoretically max, but it requires 100% optimization

Stat Soft Caps:
  → Season 1 cap: 40 per stat (can't exceed until Season 2)
  → Season 2 cap: 60
  → Season 3 cap: 80
  → Season 4 cap: 95
  → Season 5 cap: 100 (only achievable if focused)

Specializations (choose 1 per season, total 5):
  → Each gives passive bonuses
  → Some combinations unlock unique recipes
  → Example: Perfectionist + Analyst = Reverse-Engineering Master

No Respec: Choices are permanent (fits life journey theme)
  → BUT: New Game+ lets you try different builds
```

---

### 🌍 World & Exploration Questions

#### 9. How big is the world, and how do players navigate it?
**Current State:** Season-based regions described, but map/travel unclear.

**Questions to Answer:**
- Is each season a single hub area, or multiple locations?
- How does travel work? (Fast travel, real-time movement, menu-based?)
- Are there random encounters while gathering ingredients?
- Can you revisit previous season locations? (Go back to academy as master)
- Is there a world map, or just scene transitions?

**Modern Player Expectation:**
- **Open world fans:** Want exploration and discovery
- **Visual novel fans:** Want focused, story-driven scenes
- **Efficiency fans:** Want fast travel and minimal walking

**Recommendation:**
```
Season 1: Single location (Academy) with 8-10 distinct areas
  → Classrooms, Library, Garden, Dorms, Arena, etc.
  → All accessible via hub menu (no walking sim)

Season 2: Village hub + 5 gathering zones
  → Village: Shop, Square, Healer's Hut, etc.
  → Gathering zones: Forest, Caves, River, Waterfall, Mountain
  → Fast travel unlocked after visiting once

Season 3: 4 Cities (Tournament Circuit)
  → Travel between cities (map menu)
  → Each city has 3-4 locations

Season 4: Capital City + Investigation Sites
  → Large capital with 10+ locations
  → Investigation sites are temporary (quest-specific)

Season 5: Return to any previous location
  → Unlock: "Master's Privilege" fast travel
  → See how world changed based on your choices

Gathering: Mini-game or click-to-collect (not tedious walking)
Random Encounters: Optional (can toggle for extra content)
```

---

#### 10. How much voice/personality does the player character have?
**Current State:** Dialogue system framework exists, PC personality is undefined.

**Questions to Answer:**
- Is the PC a blank slate (player insert) or defined character (like Geralt)?
- Do dialogue choices shape PC personality, or just outcomes?
- Does the PC have a voice (text only, or voiced)?
- Can players choose gender, appearance, background?
- Does the PC's personality affect gameplay (not just story)?

**Modern Player Expectation:**
- **RPG fans:** Want player agency and customization
- **Narrative fans:** Want a defined character with arc
- **Life sim fans:** Want self-insert and projection

**Recommendation:**
```
Hybrid Approach: "Voiced Protagonist with Player Direction"
  → PC has personality, but player shapes its expression
  → Like Mass Effect (Shepard has character, but you choose tone)

Character Creation:
  → Name, gender, appearance (3-4 preset options per category)
  → Background choice (affects starting stats and NPC reactions)
    - Urban Merchant (Business +5, Precision +3)
    - Rural Healer (Intuition +5, Reputation +3)
    - Noble House (Reputation +5, Knowledge +3)
    - Street Orphan (Combat +5, Business +3)
    - Traveling Trader (Intuition +3, Business +5)

Dialogue Personality Traits:
  → Choices tagged with: [Pragmatic], [Idealistic], [Humorous], [Serious]
  → Consistent choices unlock unique dialogue
  → NPCs comment on your consistency ("You always see the bright side")

Voice: Text-only (budget-friendly, more dialogue depth)
  → Optional: Voice barks for emotions (laugh, sigh, etc.)
```

---

## Part 2: What Modern Players Expect From This Genre

### 📊 Genre Expectations Matrix

PotionWorld is a hybrid of multiple genres. Here's what fans of each genre will expect:

#### **Crafting Simulation Players** (Potion Craft, Alchemy Garden)

**Expect:**
✅ Satisfying ingredient combination discovery
✅ Visual feedback for crafting process (particles, sounds)
✅ Gradual recipe unlock progression
✅ Ability to experiment and discover new recipes
✅ Quality variance based on skill/tools
✅ Recipe book/collection tracking

**Will Complain If:**
❌ Crafting is just "click button, get potion" (too simple)
❌ No experimentation (must follow exact recipes only)
❌ Ingredients are too easy to find (no gathering challenge)
❌ Crafting UI is clunky or has too many clicks

**PotionWorld Status:** ✅ Strong (ESENS system provides depth, experimentation supported)

---

#### **Life Simulation Players** (Stardew Valley, Rune Factory, Story of Seasons)

**Expect:**
✅ Daily routine with satisfying loops
✅ Relationship building with NPCs (gifts, dialogue, events)
✅ Seasonal festivals and special events
✅ Home/shop customization
✅ Long-term goals (marriage, business expansion)
✅ "Cozy" atmosphere with low pressure
✅ Optional optimization (can play casually or min-max)

**Will Complain If:**
❌ Time pressure is stressful (strict deadlines, permafail)
❌ NPCs feel robotic (repetitive dialogue)
❌ Can't pursue relationships/friendships deeply
❌ No "chill" mode (everything is combat/challenge)
❌ World feels static (no seasonal changes, NPC routines)

**PotionWorld Status:** ⚠️ Needs Work
- ✅ Strong: Big 5 personality system, affinity tracking
- ❌ Missing: Daily routines, seasonal festivals, cozy atmosphere definition
- ❌ Missing: Marriage/romance system? (not mentioned in docs)

---

#### **Narrative RPG Players** (Disco Elysium, Dragon Age, Witcher 3)

**Expect:**
✅ Meaningful choices with visible consequences
✅ Complex characters with depth and growth
✅ World reactivity (NPCs remember your actions)
✅ Multiple endings based on choices
✅ Moral ambiguity (not clear good/evil)
✅ Rich lore and world-building
✅ Character-driven quests (not just fetch quests)

**Will Complain If:**
❌ Choices don't matter (illusion of choice)
❌ NPCs are one-dimensional
❌ World doesn't react to player actions
❌ Single linear story with no branching
❌ Moral choices are black-and-white

**PotionWorld Status:** ✅ Strong (moral choice framework, Big 5 NPCs, multi-season arc)

---

#### **Turn-Based Tactics Players** (Divinity: Original Sin, Slay the Spire, Into the Breach)

**Expect:**
✅ Strategic depth (build crafting, synergies)
✅ Challenging AI with variety
✅ Multiple viable strategies (not one "best" build)
✅ Clear combat feedback (what killed me, how to improve)
✅ Preparation matters (pre-combat loadout)
✅ Skill ceiling (easy to learn, hard to master)

**Will Complain If:**
❌ Combat is trivial (no strategy needed)
❌ AI is predictable or dumb
❌ Only one viable strategy
❌ RNG feels unfair (can't mitigate randomness)
❌ Combat is repetitive (same enemies, same tactics)

**PotionWorld Status:** ⚠️ Unclear
- ✅ Strong: ESENS combat notation, personality-based AI
- ❌ Unknown: Balance, difficulty curve, strategic variety
- ❌ Unknown: Is combat fun enough to carry Season 3?

---

### 🎯 Critical Modern Player Expectations (Industry-Wide)

#### 1. **Accessibility**
Modern players expect:
- Colorblind modes
- Remappable controls
- Adjustable text size
- Difficulty options
- Skip/fast-forward for replays
- Comprehensive tutorials (that can be skipped)

**PotionWorld Status:** Mentioned in design doc ✅

---

#### 2. **Respect for Player Time**
Modern players expect:
- Multiple save slots
- Save anywhere (or at least frequent autosave)
- Fast travel (after initial discovery)
- Skip cutscenes/dialogue (on replay)
- No unskippable animations for common actions
- Clear quest markers/guidance

**PotionWorld Status:** ⚠️ Needs definition
- Save system mentioned, but details unclear
- No info on cutscene length, skip options
- Quest markers/guidance system not specified

---

#### 3. **Quality of Life Features**
Modern players expect (based on genre):
- Batch crafting for known recipes ✅ (mentioned in design)
- Ingredient auto-sorting and filtering ✅ (mentioned)
- Recipe favoriting ✅ (mentioned)
- "Craft All" button for shop stock
- "Take All" for gathering
- Undo button for mistakes (selling wrong item)
- Clear UI for complex systems

**PotionWorld Status:** ✅ Mostly covered

---

#### 4. **Post-Launch Content & Community**
Modern players expect:
- Regular bug fixes
- Balance patches
- QOL updates based on feedback
- Optional DLC/expansions
- Modding support (if PC)
- Community features (sharing recipes, builds)
- Achievements/trophies with meaningful challenges

**PotionWorld Status:** ✅ Post-launch plan exists (Phase 5)

---

### 🔥 Genre-Specific Hot Topics (2024-2025)

#### **Cozy Game Boom** (Stardew Valley, Animal Crossing, Unpacking)
**Trend:** Players want low-stress, meditative games
**Expectation:** "I can play this game to relax after work"

**PotionWorld Opportunity:**
- Season 2 (Village Shop) is perfectly positioned for this
- Emphasize gathering, crafting, building relationships
- Add "Cozy Mode" difficulty: no combat, generous timers, forgiving failures

---

#### **Roguelike/Roguelite Influence** (Hades, Slay the Spire, Balatro)
**Trend:** Players want replayability and build variety
**Expectation:** "Each run/playthrough feels different"

**PotionWorld Opportunity:**
- 5 specializations across 5 seasons = 3,125 possible builds (5^5)
- New Game+ with different choices and recipes
- Randomized ingredient locations and NPC personalities
- Challenge modes (speedrun, pacifist, solo recipes only)

---

#### **Deckbuilder/Combo Mechanics** (Slay the Spire, Balatro, Marvel Snap)
**Trend:** Players love discovering synergies
**Expectation:** "Finding the perfect combo is so satisfying"

**PotionWorld Opportunity:**
- ESENS notation enables emergent combos
- Potions that interact with each other
- Build crafting: "Speedrun build" vs. "Quality build" vs. "Combat build"
- Community sharing best combos

---

#### **Meaningful Choice Fatigue** (Baldur's Gate 3, Disco Elysium)
**Trend:** Players want choices to matter, but not be overwhelming
**Expectation:** "Don't give me 50 meaningless choices, give me 5 that actually change things"

**PotionWorld Opportunity:**
- Limit to 4-5 MAJOR choices per season (20-25 total)
- Make them obvious ("This is a big moment")
- Show consequences within 1-2 hours of gameplay
- Track cumulative impact (not just isolated choices)

---

#### **Relationship Sim Depth** (Fire Emblem, Persona, Hades)
**Trend:** Players want deep, memorable NPC relationships
**Expectation:** "I feel like I know these characters"

**PotionWorld Opportunity:**
- Big 5 personality system creates unique NPCs
- Memory system makes NPCs feel alive
- Multi-season arcs (see characters grow old)
- Romance options? (Not mentioned in docs—consider adding)

---

### ⚠️ Common Pitfalls to Avoid

Based on modern game analysis, here are mistakes that kill player engagement:

#### 1. **Tutorial Overload**
❌ Don't: 2-hour tutorial explaining every system
✅ Do: Progressive tutorials (introduce mechanics as needed)
✅ Do: Let players experiment and fail safely

#### 2. **Meaningless Grind**
❌ Don't: Require 100 repetitive crafts to progress
✅ Do: Batch crafting, meaningful practice (mastery system)
✅ Do: Progression feels earned, not tedious

#### 3. **Unclear Objectives**
❌ Don't: "Figure out what to do"
✅ Do: Clear quest log with hints
✅ Do: Optional markers for those who want them

#### 4. **Punishing Experimentation**
❌ Don't: Experimenting wastes rare resources with no benefit
✅ Do: Failed experiments provide knowledge/partial resources
✅ Do: Reward curiosity (special recipes for trying weird combos)

#### 5. **Static World**
❌ Don't: NPCs repeat same 3 lines forever
✅ Do: Dialogue changes based on relationship and world state
✅ Do: World reacts to player actions (shops close if you ruin them)

#### 6. **False Choices**
❌ Don't: "Choose A or B" → both lead to same outcome
✅ Do: Choices create visible differences
✅ Do: Track choices and pay them off later

#### 7. **Complexity Without Clarity**
❌ Don't: ESENS notation is required but never explained well
✅ Do: Multiple learning styles (visual, text, experimentation)
✅ Do: Comprehensive glossary and reference

---

## Part 3: Priority Questions for Immediate Resolution

### 🎯 Must Answer Before Vertical Slice

To create a playable vertical slice (first 30-60 minutes), you need to answer:

1. **What is the core gameplay loop?** (Minute-to-minute, hour-to-hour)
2. **How complex is ESENS for new players?** (Visual vs. notation-heavy)
3. **What does Season 1 feel like?** (Cozy school life or competitive pressure?)
4. **How punishing are failures?** (Harsh or forgiving)
5. **Does the PC have a defined personality?** (Blank slate or voiced protagonist)

### 🎯 Must Answer Before Full Production

Before building all 5 seasons, you need to answer:

6. **How linear are seasons?** (Can you skip? Replay? Fast-forward?)
7. **How deep is combat?** (Main feature or side content?)
8. **What's the money curve?** (Tight throughout, or abundant later?)
9. **How big is the world?** (Hub-based or open exploration?)
10. **Do choices lock content?** (Or do all paths lead to similar content?)

### 🎯 Can Answer During Development

These can be iterated on:

- Exact stat balance and progression curves
- Number of NPCs and quests per season
- Visual style and art direction
- Sound design and music
- Post-launch content and modding

---

## Part 4: Recommendations Summary

### For a Successful Gameplay Roadmap:

#### **Define Your Core Pillars (Choose 3-4 Max)**

Example:
1. **Meaningful Crafting** - ESENS system, experimentation, mastery
2. **Living Relationships** - Big 5 NPCs, memories, long-term arcs
3. **Life Journey** - 5 seasons, aging, cumulative choices
4. **Cozy Strategy** - Tactical depth without stress (difficulty options)

#### **Identify Your Primary Audience**

**Option A: Cozy Crafters** (Stardew Valley fans)
- Emphasize: Gathering, relationships, daily routines
- De-emphasize: Combat difficulty, time pressure

**Option B: Strategy Optimizers** (Slay the Spire fans)
- Emphasize: Build variety, combat depth, challenge modes
- De-emphasize: Cozy atmosphere, relationship depth

**Option C: Narrative Explorers** (Disco Elysium fans)
- Emphasize: Choice consequences, NPC depth, world reactivity
- De-emphasize: Mechanical complexity, combat

**Recommendation:** Option A + C Hybrid
- Core audience: Cozy narrative fans who like crafting
- Secondary audience: Strategy fans (via combat depth in Season 3)
- Tertiary audience: Speedrunners and optimizers (New Game+, challenges)

#### **Create a Vertical Slice Document**

Define the first 60 minutes of gameplay:
```
Minutes 0-10: Character creation, intro cutscene, arrive at academy
Minutes 10-20: First lesson (ESENS tutorial), craft first potion
Minutes 20-30: Meet 2 NPCs, first dialogue choice
Minutes 30-40: Gather ingredients in garden, second potion
Minutes 40-50: First moral choice (help classmate vs. outperform)
Minutes 50-60: End of first day, journal entry, tease next day
```

This vertical slice will answer most of your critical questions through prototyping.

---

## Conclusion

**Bottom Line:** PotionWorld has strong foundations (ESENS system, Big 5 personalities, 5-season arc), but needs to answer critical questions about:

1. **Moment-to-moment gameplay** (What does playing feel like?)
2. **Complexity vs. accessibility** (Who is this for?)
3. **Punishment vs. forgiveness** (What happens when players fail?)
4. **Linearity vs. openness** (How much freedom?)

**Next Steps:**
1. Answer the "Must Answer Before Vertical Slice" questions
2. Create a 60-minute vertical slice prototype
3. Playtest with target audience (cozy crafters, narrative fans)
4. Iterate based on feedback
5. Finalize Season 1 before building Season 2

Modern players expect:
- **Depth with accessibility** (easy to start, hard to master)
- **Meaningful choices** (not just cosmetic)
- **Respect for time** (saves, fast travel, skip options)
- **Memorable characters** (not generic NPCs)
- **Replayability** (builds, choices, New Game+)

PotionWorld can deliver all of this—it just needs clear answers to these design questions first.
