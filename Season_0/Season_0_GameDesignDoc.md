# Season 0: Game Design Document
## "The Demo" - First Hour Playable Experience

**Version:** 1.0
**Last Updated:** 2025-11-09
**Target Duration:** 60 minutes
**Tone:** 60% Cozy, 40% RPG

---

## Executive Summary

**Season 0** is the playable demo for PotionWorld - a complete 60-minute vertical slice that introduces players to the core gameplay loop, establishes the cozy-RPG tone, and validates all critical systems before full production.

**Purpose:**
- Prove the concept works (fun + engaging)
- Test whether 60/40 cozy-RPG balance resonates
- Validate crafting minigame satisfaction
- Confirm players care about NPCs and choices
- Identify production pipeline needs
- Use for pitching, crowdfunding, or playtesting

**Success Criteria:**
- 85%+ playtesters want to continue playing
- 80%+ feel the game is "cozy and relaxing"
- 75%+ say "I care about the characters"
- 75%+ say "My choice with Marcus felt meaningful"

---

## Core Pillars (60/40 Balance)

### Cozy Elements (60%)
1. **Gentle, Non-Punishing Gameplay**
   - First potion always succeeds
   - No game-overs or harsh failures
   - Tutorials are optional after first playthrough
   - All choices are emotionally valid

2. **Satisfying Tactile Loops**
   - Gathering has beautiful visuals and sounds
   - Crafting minigame is meditative and rewarding
   - Progress is visible and encouraging

3. **Warm, Memorable Characters**
   - Kira: Enthusiastic, supportive roommate
   - Marcus: Vulnerable innovator, not aggressive rebel
   - Sena: Relatable anxiety, rewarding to help
   - Thornwood: Strict but fair, gruff-but-kind

4. **Beautiful, Inviting World**
   - Warm color palette (golden hour, soft lamplight)
   - Cozy spaces (dorm room, twilight garden)
   - Living world (other students, ambient life)

### RPG Elements (40%)
1. **Meaningful Choices**
   - Marcus dilemma has 4 distinct outcomes
   - Choices affect relationships and unlocks
   - Background selection impacts dialogue and stats
   - Long-term consequences visible

2. **Visible Progression**
   - Stats track clearly (Precision, Knowledge, Intuition)
   - Recipe mastery levels (0-100)
   - Affinity system with numerical feedback
   - XP gains shown immediately

3. **Build Diversity**
   - 5 backgrounds with different stat starts
   - Personality traits unlock based on choices
   - Multiple valid paths (innovator, traditionalist, diplomat)

4. **System Depth**
   - ESENS notation present but not required yet
   - Ingredient properties hint at deeper systems
   - Foreshadowing of combat, economy, quests

---

## Story Synopsis

### The Hook
You arrive at the Royal Academy of Alchemical Arts with your grandmother's letter and a dream to become a master potion-maker. This is **Day 1** of your journey.

### The Journey (60 Minutes)
**Minutes 0-20: Welcome & Wonder**
- Arrive at academy with grandmother's blessing
- Meet Kira, your warm and energetic roommate
- Gather ingredients in the beautiful twilight garden
- Learn the academy's expectations from Instructor Thornwood

**Minutes 20-40: Learning & Connection**
- Craft your first potion with satisfying tactile gameplay
- Explore the academy during free time
- Meet Marcus (curious experimenter) and Sena (anxious perfectionist)
- Help Sena solve a crafting problem, making a friend

**Minutes 40-60: Choice & Consequence**
- Marcus gets in trouble for experimenting with forbidden ingredients
- Face a meaningful moral choice: support innovation or follow tradition?
- See immediate consequences (affinity changes, unlock paths)
- Receive a mysterious note for a midnight meeting
- End on a cliffhanger that makes players want Season 1

### The Themes
- **Tradition vs Innovation:** Is alchemy about following recipes or pushing boundaries?
- **Community vs Ambition:** Do you help others or focus on your own success?
- **Heart vs Head:** Grandmother's wisdom (compassion) vs Academy's rules (precision)

---

## Core Gameplay Loop

### Macro Loop (60-Minute Arc)
```
Arrive → Gather → Learn → Craft → Socialize → Choose → Reflect → Hook
```

### Micro Loop (Repeatable Core)
```
Gather Ingredients → Craft Potions → Gain XP → Build Relationships → Make Choices
         ↑                                                                ↓
         ←─────────────── Unlock New Opportunities ←─────────────────────┘
```

### Daily Structure (Introduced, Not Fully Implemented Yet)
```
Morning:   Learning & Crafting (Thornwood's class)
Afternoon: Free Time (Socialize, Gather, Explore)
Evening:   Reflection & Planning (Journal, relationships)
Night:     Story Events (Kira's nightmare, mysterious note)
```

---

## Characters

### Player Character
**Customization:**
- Name (text input)
- Appearance (4 presets)
- Background (5 options, affects stats and dialogue)

**Personality Development:**
- Shaped by choices throughout demo
- Traits unlock: Innovator, Traditionalist, Diplomat, Helper, etc.

**Starting Stats (Based on Background):**
| Background | Precision | Knowledge | Intuition | Business | Reputation |
|------------|-----------|-----------|-----------|----------|------------|
| Rural Healer | 3 | 0 | 5 | 0 | 0 |
| City Merchant | 3 | 0 | 0 | 5 | 0 |
| Noble House | 3 | 3 | 0 | 0 | 5 |
| Scholarship | 3 | 5 | 0 | 0 | 0 |
| Wanderer | 0 | 0 | 5 | 3 | 0 |

### Kira - The Roommate
**Role:** Warm welcome, emotional support, living-world guide

**Personality (Big 5):**
- Openness: 0 (Balanced)
- Conscientiousness: 0 (Balanced)
- Extraversion: +1 (High - outgoing, enthusiastic)
- Agreeableness: +1 (High - supportive, kind)
- Neuroticism: 0 (Balanced, but hides anxiety)

**Arc in Season 0:**
- Greets player warmly, offers to explore
- Shows enthusiasm for academy
- Checks in after first day
- Nightmare scene hints at hidden past (Season 1 hook)
- Reacts to mysterious note with worry

**Key Scenes:**
1. First meeting (Minutes 5-12)
2. Garden exploration (optional, Minutes 12-20)
3. Evening check-in (Minutes 50-55)
4. Nightmare foreshadowing (Minutes 55-58)

### Marcus - The Innovator
**Role:** Moral choice catalyst, innovation path representative

**Personality (Big 5):**
- Openness: +1 (High - curious, experimental)
- Conscientiousness: 0 (Balanced)
- Extraversion: 0 (Balanced)
- Agreeableness: 0 (Balanced)
- Neuroticism: 0 (Calm under normal circumstances)

**Arc in Season 0:**
- Introduced experimenting in courtyard
- Gets caught by Instructor Reval
- Vulnerable confession about family sacrifice
- Player makes moral choice
- Outcome determines Season 1 relationship

**Key Scenes:**
1. Courtyard experimentation (Minutes 30-35)
2. Gets in trouble (Minutes 40-42)
3. Garden confession (Minutes 42-50)
4. Day 2 approach (Minutes 58-60, outcome varies)

**Dilemma:** "Is curiosity worth risking expulsion?"

### Sena - The Perfectionist
**Role:** Help-opportunity, empathy check, alternative path

**Personality (Big 5):**
- Openness: 0 (Balanced)
- Conscientiousness: +1 (High - organized, careful)
- Extraversion: -1 (Low - reserved, shy)
- Agreeableness: +1 (High - cooperative, grateful)
- Neuroticism: +1 (High - anxious, worried about grades)

**Arc in Season 0:**
- Struggling with failed potion
- Player can choose to help or ignore
- If helped, becomes study partner
- Represents "high-achieving but anxious" archetype

**Key Scenes:**
1. Failed potion crisis (Minutes 35-40)
2. Grateful response if helped (immediate)
3. Study offer (unlocks for Season 1)

**Challenge:** "Can you help someone struggling?"

### Thornwood - The Instructor
**Role:** Authority figure, tradition representative, mentor potential

**Personality (Big 5):**
- Openness: -1 (Low - traditional, established methods)
- Conscientiousness: +1 (High - precise, rule-following)
- Extraversion: 0 (Balanced - professional)
- Agreeableness: -1 (Low - demanding, challenging)
- Neuroticism: 0 (Calm, controlled)

**Arc in Season 0:**
- Establishes academy rules and expectations
- Catches player in garden (not angry, teaching moment)
- Teaches first crafting lesson
- Reacts to player's Marcus choice (indirectly)
- Softens slightly if player shows respect

**Key Scenes:**
1. Garden encounter (Minutes 18-20)
2. First crafting lesson (Minutes 20-30)
3. Day 2 announcement (Minutes 58-60)

**Character Note:** Gruff-but-kind, never cruel. Represents high standards, not tyranny.

---

## Locations

### 1. Cart Approach (Minutes 0-5)
**Type:** Playable cutscene / Character creation
**Visuals:** Golden hour sunset, rolling hills, academy in distance
**Mood:** Nostalgic, hopeful, warm
**Interactivity:** Name entry, appearance selection, background choice via dialogue

### 2. Dorm Room (Minutes 5-12, 50-58)
**Type:** Hub, exploration space
**Visuals:** Cozy interior, two beds, window overlooking garden, warm lamplight
**Mood:** Safe, comfortable, personal space
**Interactivity:**
- Click on objects (desk, recipe book, window, equipment)
- Talk to Kira
- Receive mysterious note

**Clickable Objects:**
- Desk drawer → Journal (empty, grandmother's note)
- Window → See garden and Moonbell flowers (foreshadowing)
- Recipe book → Empty except for welcome message
- Equipment shelf → Basic mortar & pestle

### 3. Ingredient Garden (Minutes 12-20)
**Type:** Gathering location, tutorial space
**Visuals:** Twilight garden, glowing ingredients, beautiful ambient lighting
**Mood:** Peaceful, meditative, magical
**Interactivity:**
- Gather 5 ingredient types (mushrooms, berries, roots, sap, moonbell)
- Encounter Thornwood
- Explore with or without Kira

**Gathering Spots:**
1. Mushroom patch (glowing blue)
2. Berry bushes (glowing red)
3. Root patches (glowing green)
4. Tree with sap (glowing amber)
5. Moonbell flowers (glowing purple-white, hidden)

**Ambient Life:**
- Other students gathering in background
- Birds, butterflies, gentle wind
- Rustling leaves

### 4. Classroom (Minutes 20-30, 58-60)
**Type:** Crafting tutorial space
**Visuals:** U-shaped student desks, instructor's demonstration table, ingredient shelves
**Mood:** Academic, focused, traditional
**Interactivity:**
- Crafting minigame (first potion)
- Watch Thornwood demonstrate
- See other students crafting

**NPCs Present:**
- Thornwood (instructor)
- Kira (classmate)
- Marcus (classmate)
- Sena (classmate)
- 5 background students

### 5. Courtyard (Minutes 30-40)
**Type:** Social hub, exploration space
**Visuals:** Stone courtyard, fountain, practice tables, trees
**Mood:** Open, social, warm afternoon
**Interactivity:**
- Meet Marcus (experimenting)
- Find Sena (struggling with potion)
- Optional: Explore other areas

**Social Encounters:**
- Marcus at practice table
- Sena at far table
- Background students chatting

---

## Core Systems

### 1. Inventory System

**Ingredient Inventory:**
```
Common Mushrooms x3
Common Berries x3
Common Roots x3
Tree Sap x2
Moonbell Flowers x2 (if found)
```

**Potion Inventory:**
```
Simple Healing Tonic (Standard Quality) x1
[More if player experiments with Marcus]
```

**UI Features:**
- Grid or list view
- Stack counters (x3, x2, etc.)
- Icons for each ingredient
- Hover for description
- Sort/filter (for future expansion)

### 2. Crafting System

**Recipe: Simple Healing Tonic**
```
Ingredients:
- Common Mushrooms x2
- Tree Sap x1
- Common Berries x1

Effect: Restores 30 HP over 10 seconds
ESENS: P+H30%10s.ST
Difficulty: 5/100 (Trivial)
Success Rate: 95% (for beginners)
```

**Minigame Steps:**
1. **Grind Mushrooms** - Circular dragging motion
2. **Add Tree Sap** - Drag vial to mortar, pour
3. **Add Berries** - Drag berries one by one
4. **Decant** - Tilt mortar to pour into vial

**Quality Factors:**
- Grinding precision (smooth circles = better)
- Timing (not relevant for first potion, tutorial only)
- Ingredient quality (all "standard" in demo)

**Outcome:**
- Always succeeds (tutorial safety)
- Quality can be Standard or Fine
- XP gained: Precision +10, Knowledge +25

### 3. Relationship System

**Affinity Scale:** -5 to +5
- +5: Devoted
- +3: Friendly
- 0: Neutral
- -3: Hostile
- -5: Nemesis

**NPCs Tracked:**
| NPC | Starting Affinity | Possible Range in Demo |
|-----|-------------------|------------------------|
| Kira | 0 | 0 to +2.0 |
| Marcus | 0 | -0.5 to +2.5 |
| Sena | 0 | 0 to +2.0 |
| Thornwood | 0 | -0.5 to +0.7 |

**Affinity Changes:**
- Dialogue choices: ±0.3 to ±1.0
- Help actions: +1.5 to +2.0
- Major choices: ±2.5
- Decay: Not active in demo (too short)

**UI Display:**
- Hearts (filled/empty) in journal
- Numerical value (optional, can hide)
- Status word (Neutral, Friendly, Warm, etc.)

### 4. Stats & Progression

**Core Stats:**
| Stat | Starting | Demo Cap | Purpose |
|------|----------|----------|---------|
| Precision | 0-5 | 15 | Crafting quality |
| Knowledge | 0-5 | 30 | Recipe unlocks |
| Intuition | 0-5 | 10 | Experimentation |
| Business | 0-5 | 5 | Not used in demo |
| Reputation | 0-5 | 5 | Social interactions |

**XP Sources in Demo:**
- Craft Simple Healing Tonic: +10 Precision, +25 Knowledge
- Help Sena: +5 Intuition
- Find Moonbell: +5 Intuition
- Experiment with Marcus (optional): +10 Intuition

**Progression Display:**
- Progress bars with clear numbers
- "Next threshold at 25" indicators
- XP gain notifications

### 5. Choice & Consequence System

**Major Choice: Marcus Dilemma**

**Options:**
1. **Support Marcus** → Marcus +2.5, Thornwood -0.5, Unlock "Innovator" trait
2. **Gentle Critique** → Marcus +0.5, Thornwood +0.3, Unlock "Balanced" trait
3. **Stay Neutral** → Marcus -0.5, Unlock "Self-Preserving" trait
4. **Offer Solution** → Marcus +2.0, Thornwood +0.5, Unlock "Diplomat" trait (requires Openness background or previous O choices)

**Consequence Tracking:**
- Stored in player profile
- Affects Day 2 Marcus interaction (immediate)
- Sets up Season 1 arc (long-term)
- Journal records choice and reasoning

**Minor Choices:**
- Explore with Kira vs alone: Kira ±0.5
- Response to Thornwood: ±0.5, sets personality flag
- Help Sena or not: Sena ±2.0
- Approach Marcus experiment: Marcus ±1.5

### 6. Journal System

**Tabs:**
1. **Relationships** - Shows all NPCs with affinity levels
2. **Stats** - Progress bars for all 5 core stats
3. **Recipes** - Simple Healing Tonic (Novice 25/100 mastery)
4. **Choices** - Major choice recorded with reflection
5. **Traits** - Unlocked personality traits

**UI Design:**
- Warm parchment aesthetic
- Hand-drawn flourishes
- Readable font (fantasy but clear)
- Auto-updates, but player can open anytime

---

## Gameplay Flow (Detailed)

### Scene 1: Cart Ride & Character Creation (0-5 min)

**Flow:**
1. Opening: Cart approaching academy at sunset
2. Grandmother's letter (voiceover): Warm welcome, themes introduction
3. Cart driver dialogue: "What brings you to the academy?"
4. **Player Input:** Name entry
5. **Player Input:** Appearance selection (4 presets)
6. **Player Input:** Background choice (5 options)
7. Arrival: Cart stops, player steps out
8. **Transition:** Fade to dorm room

**Teaching:**
- Game tone (cozy, warm)
- Story setup (grandmother's blessing, academy life)
- Character ownership (your journey)

### Scene 2: Dorm Room Exploration (5-12 min)

**Flow:**
1. Meet Kira (enthusiastic greeting)
2. **Choice:** Explore together or unpack first?
3. **If unpack:** Click on objects (desk, window, shelf)
4. **If explore:** Skip to garden with Kira
5. Read grandmother's note in journal
6. See moonbell flowers through window (foreshadowing)
7. **Transition:** Exit to garden

**Teaching:**
- Click to interact
- Dialogue choices
- Relationship system basics (Kira affinity)

### Scene 3: Garden Gathering (12-20 min)

**Flow:**
1. Enter beautiful twilight garden
2. **Tutorial:** Gather mushrooms (press E, satisfying animation)
3. Gather berries and roots (player-directed)
4. Encounter Thornwood (triggered when 3+ ingredients gathered)
5. **Choice:** How to respond to Thornwood
6. Thornwood gives tree sap, introduces himself
7. **Optional:** Find moonbell flowers (hidden, rewards exploration)
8. **Transition:** Fade to "Next Morning"

**Teaching:**
- Gathering mechanics
- Ingredient types (visual identity)
- Authority figure (Thornwood)
- Exploration rewards (moonbell)

### Scene 4: First Crafting Lesson (20-30 min)

**Flow:**
1. Classroom scene, students at desks
2. Thornwood lecture (brief, skippable after first playthrough)
3. Recipe card displays (Simple Healing Tonic)
4. **Crafting Minigame:**
   - Step 1: Grind mushrooms
   - Step 2: Add tree sap
   - Step 3: Add berries
   - Step 4: Decant into vial
5. Success animation (always succeeds)
6. XP gain notification (+10 Precision, +25 Knowledge)
7. Recipe added to journal
8. Thornwood approval ("Acceptable")
9. **Transition:** "Afternoon free time"

**Teaching:**
- Core crafting loop
- Recipe system
- XP and progression
- Quality feedback

### Scene 5: Courtyard Socializing (30-40 min)

**Flow:**
1. **Hub menu:** Choose location (Garden, Library, Dorm, Courtyard)
2. **Designed path:** Courtyard
3. Meet Marcus experimenting with crystal dust
4. **Choice:** How to respond to experimentation
5. **Optional:** Experiment together (if supportive)
6. Notice Sena struggling at far table
7. **Choice:** Help Sena or not
8. **If help:** Mini-puzzle (identify extra mushrooms)
9. Sena grateful response, offers to study together
10. **Transition:** Dinner bell rings

**Teaching:**
- Free exploration
- Social interactions build relationships
- Helping NPCs rewards friendship
- Multiple simultaneous opportunities

### Scene 6: Marcus Dilemma (40-50 min)

**Flow:**
1. Walking to dinner, overhear argument
2. See Marcus being scolded by Instructor Reval
3. **Choice:** Approach Marcus or give him space
4. **If approach:** Find Marcus in garden (twilight again)
5. Marcus confession (family sacrifice, fear of expulsion)
6. **MAJOR CHOICE:** 4 options with visible consequences
7. Marcus responds based on choice
8. Journal entry auto-writes reflection
9. **Transition:** Return to dorm

**Teaching:**
- Choices have weight
- Moral ambiguity (no clear "right" answer)
- Immediate feedback (affinity changes)
- Long-term implications (trait unlocks)

### Scene 7: Evening Reflection (50-58 min)

**Flow:**
1. Dorm room at night
2. Kira bedtime chat (asks about your day)
3. Kira falls asleep
4. **Cutscene:** Kira's nightmare (foreshadowing)
5. **Journal opens automatically:**
   - Relationships tab (show affinity levels)
   - Stats tab (show progress bars)
   - Recipes tab (show mastery)
   - Choices tab (show Marcus reflection)
6. Player can explore journal freely
7. **Transition:** Fade to "Next Morning"

**Teaching:**
- Tracking systems (affinity, stats, mastery)
- Choices are recorded
- NPCs have hidden depths (Kira's nightmare)

### Scene 8: Day 2 Hook (58-60 min)

**Flow:**
1. Morning, getting ready for class
2. Find mysterious note in recipe book
3. **Choice:** Tell Kira about note or keep secret
4. Kira's worried reaction (if told)
5. Walk to breakfast
6. **Marcus encounter (outcome varies):**
   - If supported: Sits with you, offers study sessions
   - If neutral: Sits alone, avoids eye contact
   - If diplomat: Sits with you, discusses Thornwood meeting
7. Thornwood announces Day 2 lesson (Stamina Boost, harder)
8. **Final line:** "Let's see who paid attention."
9. **TITLE CARD:** "To Be Continued in Season 1..."
10. **Credits roll** with demo statistics:
    - Relationships formed
    - Choices made
    - Path unlocked

**Teaching:**
- Your choices had immediate impact
- Mystery hooks for future content
- Anticipation for full game

---

## Technical Specifications

### Engine
**Target:** Godot 4.x
- GDScript for game logic
- Scene-based architecture
- Resource-based data (JSON for NPCs, recipes, etc.)

### Platform Targets
**Primary:** PC (Windows, Mac, Linux)
**Secondary:** Web (for easy demo distribution)
**Future:** Console, Mobile

### Controls
**Mouse/Keyboard:**
- Click to interact
- Drag for minigames
- WASD or point-click for movement (TBD)
- ESC for menu/journal

**Controller (Optional for Demo):**
- A/X to interact
- Left stick to move
- B/Circle for back/cancel

### Save System
**Demo:**
- Auto-save at scene transitions
- One save slot
- Settings saved separately

**Data Saved:**
- Player name, appearance, background
- All affinity levels
- All stats and XP
- Recipe mastery
- Choices made
- Inventory
- Traits unlocked

### Performance Targets
- 60 FPS on mid-range PC (2019+)
- 30 FPS on web builds
- Load times under 3 seconds between scenes
- Memory under 500MB

---

## Art Direction

### Visual Style
**Recommended:** Pixel art or hand-drawn 2D
- Warm color palette (oranges, greens, purples, soft blues)
- Spiritfarer / Persona 5 inspired aesthetics
- Readable UI with cozy textures

### Color Palette
**Environment:**
- Golden hour: Warm oranges, yellows
- Twilight: Soft purples, blues
- Night: Deep blues, glowing elements
- Interior: Warm browns, soft lamplight

**Ingredient Coding:**
- Mushrooms: Blue glow
- Berries: Red glow
- Roots: Green glow
- Sap: Amber glow
- Moonbell: Purple-white glow

### Character Design
**Style Considerations:**
- Expressive faces (portraits)
- Simple but distinct silhouettes (sprites)
- Age-appropriate (14-18 year olds)
- Diverse appearances

### UI Design
**Aesthetic:**
- Parchment textures
- Hand-drawn flourishes
- Fantasy-themed but readable
- Warm color accents
- Clear iconography

---

## Audio Direction

### Music Style
**Genre:** Orchestral + Acoustic + Ambient
**Mood:** Cozy, nostalgic, hopeful, gentle

**Required Tracks:**
1. **Main Theme** (Character creation) - Piano, strings, warm and welcoming
2. **Garden Theme** (Gathering) - Woodwinds, harp, peaceful and meditative
3. **Crafting Theme** (Minigame) - Soft percussion, celesta, focused but gentle
4. **Courtyard Theme** (Social) - Acoustic guitar, light strings, friendly and open
5. **Evening Theme** (Reflection) - Solo piano, ambient, reflective and soft
6. **Choice Theme** (Marcus dilemma) - Strings, thoughtful and slightly tense
7. **Hook Theme** (Mysterious note) - Ambient, mysterious, anticipatory

### Sound Effects

**Gathering:**
- Mushroom pluck (soft "plink")
- Berry pick (light pop)
- Root dig (earthy scrape)
- Sap collect (drip and pour)
- Success chime (gentle and magical)

**Crafting:**
- Grinding (ASMR stone-on-stone)
- Pouring liquid (smooth flow)
- Berry squish (satisfying pop)
- Bubbling (gentle simmer)
- Cork stopper (satisfying "pop")
- Success sparkles (magical chime)

**UI:**
- Page turn (parchment rustle)
- Menu open/close (soft whoosh)
- Button click (gentle tap)
- Notification (pleasant chime)
- Affinity gain (warm "ding")

**Ambient:**
- Garden: Birds, wind, rustling leaves
- Classroom: Student murmurs, quill scratches
- Dorm: Clock ticking, distant academy bells
- Courtyard: Fountain, distant conversations

---

## Success Metrics & Testing

### Playtesting Goals

**Phase 1: Internal (Week 11)**
- Test all systems function
- Identify bugs and crashes
- Validate 60-minute runtime
- Check tutorial clarity

**Phase 2: Friends & Family (Week 12)**
- Test emotional engagement
- Validate cozy-RPG balance
- Check if Marcus choice feels meaningful
- Gather general feedback

**Phase 3: External (Post Week 12)**
- 10-15 target audience playtesters
- Formal survey and metrics
- Video recordings (with permission)
- Iterate based on feedback

### Key Metrics

**Engagement:**
- % who complete full 60 minutes: Target 90%+
- % who want to continue: Target 85%+
- Average play time: Target 55-65 minutes

**Emotional Response:**
- % who say "cozy and relaxing": Target 80%+
- % who care about NPCs: Target 75%+
- % who remember 2+ NPC names: Target 70%+

**Mechanical Understanding:**
- % who understand crafting: Target 90%+
- % who understand affinity: Target 70%+
- % who understand stats: Target 65%+

**Choice Impact:**
- % who say Marcus choice felt meaningful: Target 75%+
- % who would replay with different choice: Target 60%+

### Exit Survey Questions

**Engagement:**
1. On a scale of 1-10, how much do you want to keep playing?
2. Would you buy the full game based on this demo?

**Tone:**
3. Did the game feel cozy and relaxing? (Yes/No)
4. Did the game feel like an RPG with meaningful choices? (Yes/No)
5. Was the balance between cozy and RPG appropriate? (Too cozy / Just right / Too RPG-focused)

**Characters:**
6. Which characters do you remember? (List names)
7. Which character is your favorite and why?
8. Did you care about Marcus's situation? (Yes/No/Unsure)

**Mechanics:**
9. Was the crafting minigame fun? (Too simple / Just right / Too complex)
10. Did you understand the relationship system? (Yes/No/Somewhat)
11. Did you understand what stats do? (Yes/No/Somewhat)

**Choice:**
12. What did you choose regarding Marcus? Why?
13. Did your choice feel meaningful? (Yes/No/Unsure)
14. Would you replay to see different outcomes? (Yes/No/Maybe)

**General:**
15. What was your favorite moment?
16. What confused you or felt unclear?
17. Any bugs or technical issues?
18. Additional comments?

---

## Scope & Boundaries

### In Scope for Season 0
✅ Character creation (name, appearance, background)
✅ 5 locations (cart, dorm, garden, classroom, courtyard)
✅ 5 NPCs (Player, Kira, Marcus, Sena, Thornwood)
✅ 1 complete crafting minigame
✅ 5 ingredient types
✅ 1 craftable recipe (Simple Healing Tonic)
✅ Gathering tutorial
✅ Relationship system (affinity tracking)
✅ Stat progression (Precision, Knowledge, Intuition)
✅ 1 major choice (Marcus dilemma) with 4 outcomes
✅ Multiple minor choices
✅ Journal system (relationships, stats, recipes, choices)
✅ Day/night transitions
✅ Mystery hook (midnight note)

### Out of Scope for Season 0
❌ Combat/dueling (Season 3 feature)
❌ Shop management (Season 2 feature)
❌ Economy/money system (mentioned but not used)
❌ Quest log (too complex for 60 minutes)
❌ Multiple recipes to craft
❌ Batch crafting
❌ Ingredient quality variance
❌ Tool upgrades
❌ Time management pressure
❌ Romance options (friendship only)
❌ Voice acting (text only with possible barks)
❌ Full ESENS notation teaching (shown but not required)
❌ Experimentation system (hinted but not playable except with Marcus)

### Maybe in Scope (If Time Permits)
🤔 Second recipe (Stamina Boost) for Day 2 teaser
🤔 Library location (brief visit)
🤔 Additional background students (populated world)
🤔 Controller support
🤔 Basic settings menu (volume, text speed)

---

## Risks & Mitigation

### Risk 1: Crafting Minigame Not Fun
**Impact:** High - Core loop fails
**Likelihood:** Medium
**Mitigation:**
- Prototype minigame first (Week 3-4)
- Internal playtest early
- Iterate based on feedback
- Have backup simplified version ready

### Risk 2: Players Don't Care About Marcus Choice
**Impact:** High - Emotional core fails
**Likelihood:** Low
**Mitigation:**
- Strong character writing
- Build empathy before choice (show family sacrifice)
- Make all options feel valid
- Show immediate consequences

### Risk 3: 60 Minutes Feels Too Short/Long
**Impact:** Medium - Pacing issues
**Likelihood:** Medium
**Mitigation:**
- Time gameplay during development
- Cut scenes if too long
- Add optional content if too short
- Playtesting will reveal

### Risk 4: Art Production Takes Too Long
**Impact:** Medium - Timeline slip
**Likelihood:** Medium
**Mitigation:**
- Start with simple placeholder art
- Hire artist early (Week 1-2)
- Use asset store for some elements
- Prioritize character portraits over environments

### Risk 5: Scope Creep
**Impact:** High - Never finish demo
**Likelihood:** High
**Mitigation:**
- Strict scope document (this GDD)
- Weekly check-ins on progress
- "Maybe" features only if ahead of schedule
- Ruthlessly cut features that don't serve core goals

---

## Post-Demo Strategy

### If Demo Succeeds (85%+ want to continue)
**Path:** Full production of Season 1

**Next Steps:**
1. Expand to full Season 1 (20 hours)
2. Add 15+ more recipes
3. Introduce 8+ more NPCs
4. Build Academy Tournament climax
5. Complete seasonal arc

### If Demo Partially Succeeds (65-85%)
**Path:** Iterate on demo based on feedback

**Next Steps:**
1. Identify specific pain points from playtesting
2. Rebuild weak systems (e.g., crafting, choice presentation)
3. Re-test with new playtesters
4. Proceed to Season 1 once metrics hit targets

### If Demo Fails (<65% want to continue)
**Path:** Major pivot or cancellation

**Next Steps:**
1. Deep analysis of why it failed
2. Consider fundamental changes (genre, tone, systems)
3. Prototype alternative approaches
4. Or: Gracefully cancel and move to different project

---

## Appendix A: Dialogue Samples

### Grandmother's Letter (Opening)
> "Dearest child,
>
> You have the gift—I've seen it in the way you handle ingredients, the care you take with every step. The academy will teach you technique and notation, but never forget: potions are made for people, not perfection.
>
> Trust your heart as much as your head. And remember, every choice you make as an alchemist matters—not just to your potions, but to the world around you.
>
> With all my love,
> Grandmother"

### Kira's First Line
> "Oh! You're here! Hi! I'm Kira!
>
> [Sets books down messily]
>
> I got here yesterday and I've already explored EVERYTHING. The garden is amazing, the library has this restricted section that's totally mysterious, and—oh, sorry, I'm talking too much, aren't I?
>
> [Nervous laugh]
>
> I do that when I'm excited. I'm Kira. Did I say that already?"

### Marcus's Confession
> "My family isn't rich. They saved for years to send me here. If I get kicked out...
>
> [Voice cracks slightly]
>
> I don't get it. Isn't alchemy about discovery? Why do they punish curiosity?"

### Thornwood's Introduction
> "Hmph. Well, since you're already here...
>
> [Walks to tree, collects sap]
>
> Tree sap. Essential binding agent. You'll need this for tomorrow's lesson.
>
> [Hands player 2x Tree Sap]
>
> Welcome to the Royal Academy. I'm Instructor Thornwood. I expect precision, dedication, and respect for the craft.
>
> [Softens slightly]
>
> Your grandmother sent word of your enrollment. She speaks highly of you. Let's see if she's right."

---

## Appendix B: Technical Asset List

### Characters (Art)
- Player (4 variants x 4 expressions = 16 portraits)
- Kira (4 expressions)
- Marcus (4 expressions)
- Sena (3 expressions)
- Thornwood (3 expressions)
- Cart Driver (1 portrait, optional)

**Total: ~27 character portraits**

### Sprites
- Player (walking, gathering, crafting)
- Kira (standing, walking)
- Marcus (sitting, standing)
- Sena (sitting, standing)
- Thornwood (standing, walking)
- Background students (5x simple sprites)

**Total: ~20 sprite variations**

### Environments
1. Cart scene (single illustration)
2. Dorm room (clickable interior)
3. Garden (twilight, with gathering spots)
4. Classroom (desks, shelves)
5. Courtyard (fountain, tables)

**Total: 5 environment illustrations**

### UI Elements
- Recipe card template
- Journal pages (5 tab designs)
- Notification popup
- Choice selection screen
- Dialogue box
- Inventory grid
- Stat progress bars
- Relationship hearts
- Main menu
- Settings menu

**Total: ~15 UI screens/elements**

### Icons
- 5 ingredient icons (mushroom, berry, root, sap, moonbell)
- 1 potion icon (healing tonic vial)
- Various UI icons (stats, close, back, etc.)

**Total: ~15 icons**

### Minigame Assets
- Mortar & pestle (3D or high-quality 2D)
- Ingredient states (whole, ground, mixed)
- Vials and bottles
- Particle effects (dust, sparkles, glow)
- Liquid effects

**Total: ~10 minigame assets + particles**

---

## Version History

**v1.0 (2025-11-09)**
- Initial Game Design Document
- Complete 60-minute demo specification
- All systems, characters, and scenes defined
- Success metrics established
- 12-week production timeline

---

## Credits & References

**Inspired By:**
- Persona 5 (daily structure, social links)
- Fire Emblem: Three Houses (academy setting, character relationships)
- Stardew Valley (cozy gathering and crafting loops)
- Potion Craft (visual potion crafting)
- Spiritfarer (warm art style and character focus)

**Developed For:**
- PotionWorld: A Life's Journey (Full Game)
- Season 0 Demo / Vertical Slice
