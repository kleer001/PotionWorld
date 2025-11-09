# First Hour Gameplay Prototypes

Three distinct approaches to the opening 60 minutes of PotionWorld, each testing different design priorities.

---

## Prototype A: "The Cozy Welcome"
**Philosophy:** Gentle onboarding, relationship-first, low-stakes exploration
**Target Player:** Stardew Valley fans, cozy game enthusiasts, narrative explorers
**Core Question:** Can we make crafting + relationships engaging without pressure?

### Minute-by-Minute Breakdown

#### **Minutes 0-5: Arrival (Playable Cutscene)**
- **Scene:** Horse-drawn cart approaching the Royal Academy at sunset
- **Narration:** Your grandmother's voice-over letter reading
  - "You have the gift, child. The academy will teach you technique, but never forget—potions are about people, not just ingredients."
- **Player Input:**
  - Choose your name (text input)
  - Choose appearance (4 presets: 2 masc, 2 femme)
  - Choose background from dialogue with cart driver:
    - "So, what brings you to the academy?"
    - → [Rural Healer] "My grandmother taught me the basics"
    - → [Urban Merchant] "My family's business needs an alchemist"
    - → [Noble House] "It's tradition for my family"
    - → [Street Orphan] "I won a scholarship competition"

**Gameplay Test:** Does character creation feel meaningful or like a delay?

---

#### **Minutes 5-12: The Dorm Room (Exploration Tutorial)**
- **Scene:** Arrive at dorm room, roommate already unpacked
- **Meet:** Rachel (High E, High A) - enthusiastic, friendly roommate
  - AUTO-DIALOGUE: "Oh! You're finally here! I'm Rachel! I got here yesterday—have you seen the ingredient garden? It's HUGE!"
  - First affinity moment:
    - Rachel: "Want to explore together, or do you need time to unpack?"
    - → [Explore together] Rachel +0.5, immediately go to garden
    - → [Unpack first] Rachel +0.0, solo time to examine room

**If player chooses unpack:**
- **Tutorial:** Click on desk → Recipe book (empty)
- **Tutorial:** Click on shelf → Equipment (basic mortar & pestle)
- **Tutorial:** Click on chest → Inventory screen opens
  - Empty except for "Grandmother's Letter" (readable lore)
  - UI tooltip: "This is your ingredient inventory. You'll fill it soon!"
- **Tutorial:** Click on door → Exit to hallway

**Gameplay Test:** Do players naturally click on objects, or do they need more guidance?

---

#### **Minutes 12-20: The Garden (Gathering Tutorial)**
- **Scene:** Beautiful ingredient garden with 5-6 marked gathering spots
- **Meet:** If with Rachel, she points things out. If alone, find Instructor Thornwood pruning.

**Tutorial Flow:**
1. **Approach glowing mushroom patch**
   - UI: "Press [E] to gather"
   - Gather 3x Common Mushrooms (visual particles, satisfying sound)
   - Ingredient added to inventory (notification with icon)

2. **Approach berry bush**
   - Gather 3x Common Berries

3. **Approach root patch**
   - Gather 3x Common Roots

**NPC Encounter:**
- **Thornwood:** (Low O, High C) notices you gathering
  - "First day students shouldn't be in the garden unsupervised."
  - Response choices:
    - → [Apologize] "Sorry, I didn't know!" (C +0.5, shows respect for rules)
    - → [Enthusiastic] "I couldn't wait to see the ingredients!" (O +0.3, shows curiosity)
    - → [Practical] "I wanted to be prepared for lessons" (C +0.5, N -0.3)
  - Thornwood: "Hmph. Well, since you're here, take some tree sap too. You'll need it tomorrow."
  - Gain 2x Tree Sap

**Gameplay Test:** Is gathering satisfying or tedious? Do personality responses feel meaningful?

---

#### **Minutes 20-30: First Crafting Lesson (Core Mechanic Introduction)**
- **Scene:** Transition to "Next Morning" (fade to black, morning music)
- **Setting:** Classroom with 6 student NPCs + Instructor Thornwood

**Lesson Structure:**
1. **Thornwood Lecture (can skip after first playthrough):**
   - "Today, you'll brew your first potion: Simple Healing Tonic."
   - "Potions are described using ESENS notation—but don't worry about that yet."
   - "Just follow the recipe exactly. Precision is everything."

2. **Recipe Display:**
   ```
   SIMPLE HEALING TONIC

   Ingredients:
   - 2x Common Mushrooms
   - 1x Tree Sap (binder)
   - 1x Common Berries (flavor)

   [Visual Recipe Card - ingredients light up in order]
   ```

3. **Crafting Minigame (Simplified for first potion):**
   - **Step 1:** "Grind mushrooms"
     - Click and drag mortar in circles (3 circles = success)
     - Visual: Mushrooms turn to powder

   - **Step 2:** "Add tree sap"
     - Drag sap vial to cauldron
     - Visual: Mixture binds together

   - **Step 3:** "Add berries"
     - Drag berries to cauldron
     - Visual: Potion turns soft green

   - **Step 4:** "Stir gently"
     - Click and drag spoon slowly (not too fast!)
     - If too fast: "Too aggressive!" (visual shake)
     - If right: Success sparkles

4. **Result:**
   - SUCCESS: "Simple Healing Tonic (Standard Quality)" added to inventory
   - Thornwood: "Acceptable. You followed instructions. That's the foundation."
   - +10 Precision XP, +25 Knowledge XP
   - Recipe added to recipe book

**Gameplay Test:** Is crafting engaging with this level of interactivity? Too simple or just right?

---

#### **Minutes 30-40: Free Time (Social Introduction)**
- **Scene:** Class ends, afternoon free time
- **Tutorial Prompt:** "You have free time until dinner. What will you do?"

**Available Locations (Hub Menu):**
- **Garden** (gather more ingredients)
- **Library** (meet studious NPC, read lore)
- **Dormitory** (talk to Rachel)
- **Courtyard** (meet other students)

**Designed Path (but player can choose):**

**Option 1: Courtyard (Social Focus)**
- Find 3 students practicing potion-making
- **Meet:**
  - **Ezekiel** (High O, Low C) - experimenting with recipe
    - "Thornwood says follow the recipe, but what if we add crystal dust?"
    - → [Encourage] "Try it!" (O +1.0, Ezekiel likes you)
    - → [Warn] "Better not get in trouble" (C +0.5, O -0.5)

  - **Miriam** (Low E, High N) - looks stressed
    - "I... I think I messed up my potion. It turned brown."
    - → [Help] "Let me see if I can help" (A +1.0, unlock mini-quest)
    - → [Reassure] "First day! Everyone messes up" (N -0.5, gentle comfort)
    - → [Leave] "You'll figure it out" (A -0.3, N +0.3)

**If player helps Miriam:**
- Mini-quest: "Identify what went wrong"
- Look at her ingredients: She used twice as many mushrooms
- → Explain the ratio concept
- Miriam: "Thank you... I was too nervous to ask Thornwood"
- Miriam Affinity → +1.5 (big boost)
- Unlock: Miriam will help you later (plants this seed)

**Gameplay Test:** Do players naturally explore socially, or do they need direction?

---

#### **Minutes 40-48: First Moral Choice (Stakes Introduction)**
- **Scene:** Bell rings for dinner, walking to dining hall
- **Event:** Overhear Ezekiel arguing with **Instructor Reval** (Strict disciplinarian)
  - Reval: "Experimentation is for third-years! You'll be scrubbing cauldrons for a week!"
  - Ezekiel storms off, clearly upset

**Player finds Ezekiel in garden (alone)**
- Ezekiel: "Reval's going to report me. I could get expelled if I mess up again."
- Ezekiel: "My family saved for years to send me here. If I get kicked out..."
- Ezekiel: "I just wanted to try something new. Is that so wrong?"

**MORAL CHOICE (Timed: 30 seconds to decide):**

**Option A: [Support Ezekiel]** "You were just being creative"
- Ezekiel Affinity +2.0
- Unlock Ezekiel friendship path
- Thornwood Affinity -0.5 (he hears you defended rule-breaking)
- Sets tone: You value innovation over tradition

**Option B: [Gentle Critique]** "Maybe wait until you're more experienced?"
- Ezekiel Affinity +0.5 (appreciates honesty, but disappointed)
- Thornwood Affinity +0.3 (respects rule-following)
- Balanced path

**Option C: [Stay Neutral]** "I'm not getting involved"
- Ezekiel Affinity -0.5 (hurt)
- No other affinity changes
- Ezekiel won't trust you with secrets later

**Option D: [Offer Solution]** "What if I ask Thornwood about experiment days?"
- Requires: High O background choice or previous O dialogue
- Ezekiel Affinity +1.5
- Thornwood Affinity +0.0 (respects initiative)
- Unlock special scene: Approach Thornwood later

**Post-Choice:**
- Journal Entry Auto-Writes:
  - "First day thoughts: Ezekiel got in trouble for experimenting. Made me think about Grandmother's letter—technique vs. heart. Who's right?"

**Gameplay Test:** Does the choice feel weighty? Do players understand consequences?

---

#### **Minutes 48-55: Evening Reflection (System Introduction)**
- **Scene:** Back in dorm room, Rachel already asleep
- **Tutorial:** Journal System
  - Opens automatically (first time only)
  - Shows:
    - **Relationships:** Rachel (+0.5), Thornwood (+0.3), Ezekiel (+2.0), Miriam (+1.5)
    - **Stats:** Precision (8/100), Knowledge (25/100)
    - **Recipes Learned:** Simple Healing Tonic (Novice 10/100)
    - **Choices Made:** Supported Ezekiel (Innovation path)

**Foreshadowing:**
- Brief cutscene: Rachel mumbles in sleep
  - "No... don't tell them... it wasn't my fault..."
  - Camera close on her worried face
  - Fade to black

**Gameplay Test:** Is journal overwhelming or satisfying? Do players understand tracking?

---

#### **Minutes 55-60: Day 2 Morning (Choice Payoff)**
- **Scene:** Breakfast in dining hall
- **Event:** Consequence of Ezekiel choice

**If you supported Ezekiel:**
- Ezekiel sits with you at breakfast
- "Thanks for having my back. Most people just follow Thornwood blindly."
- Ezekiel: "Want to study together? I can show you some tricks I learned."
- **Unlock:** Ezekiel Study Sessions (optional activity for bonus Precision)

**If you stayed neutral:**
- Ezekiel sits alone, doesn't make eye contact
- Rachel: "Heard about Ezekiel. Rough stuff. You staying out of it?"
- No study session unlock

**Final Tutorial:**
- Thornwood announces: "Today, you'll craft your second potion—a Stamina Boost."
- "This one requires four components and better timing. Let's see who paid attention."

**Hook for Next Hour:**
- New ingredient types introduced
- Harder crafting challenge
- Miriam asks for help again (building relationship)
- Mysterious note falls out of your recipe book: "Meet me in the library at midnight. -A Friend"

**END OF HOUR ONE**

---

### Prototype A: Metrics to Test

1. **Engagement:** Do players want to keep playing after 60 minutes?
2. **Clarity:** Do players understand crafting, gathering, and affinity systems?
3. **Connection:** Do players care about NPCs (Rachel, Ezekiel, Miriam, Thornwood)?
4. **Agency:** Does the Ezekiel choice feel meaningful?
5. **Pacing:** Does this feel too slow? Too fast? Just right?

**Success Criteria:**
- 80%+ playtesters say "I want to know what happens next"
- 70%+ understand crafting without getting frustrated
- 60%+ remember at least 2 NPC names and personalities

---

## Prototype B: "The Cold Open"
**Philosophy:** Start with high stakes, then flashback to explain
**Target Player:** Narrative RPG fans, mystery lovers, players who want immediate tension
**Core Question:** Can we hook players emotionally before teaching systems?

### Minute-by-Minute Breakdown

#### **Minutes 0-8: Cold Open (Playable Crisis)**
- **Scene:** You're 17 years old (end of Season 1), in the Academy Tournament Finals
- **Setting:** Massive arena, cheering crowd, spotlights
- **Context (minimal):** "Finals Match: You vs. Corwin Ashford"

**Tutorial: Combat Introduction (Simplified)**
- You have 5 pre-selected potions in your quick-access belt
- Each potion has a simple icon and name:
  - Strength Boost (red, muscle icon)
  - Defense Shell (blue, shield icon)
  - Speed Surge (yellow, lightning icon)
  - Healing Tonic (green, heart icon)
  - Mystery Potion (purple, ??? icon)

**Turn 1:**
- Opponent drinks Strength Boost
- Tutorial: "Your turn! Select a potion to drink"
- Players experiment with UI (no real wrong choice, just learning)

**Turn 2-3:**
- Simplified combat plays out
- Opponent is winning (scripted)
- Your health drops to 30%

**Turn 4: The Choice**
- Internal monologue: "The mystery potion... Grandmother's recipe. I've never tested it."
- Rachel's voice from crowd: "Don't do it! It's not worth it!"
- Ezekiel's voice: "Trust your instinct!"

**CHOICE (Timed: 15 seconds):**
- → [Use Mystery Potion] Risk it
- → [Play It Safe] Use Healing Tonic

**If Use Mystery Potion:**
- Visual: Dramatic swirling effect
- Potion explodes in your hands
- Purple smoke fills arena
- Screen flashes white
- Crowd gasps
- Fade to black
- Text: "Three Years Earlier..."

**If Play It Safe:**
- You lose the tournament
- Corwin shakes your hand: "Good match"
- You see Thornwood in crowd, disappointed
- Close-up on your face: Determination
- Text: "This is where it started to go wrong... Three Years Earlier..."

**Gameplay Test:** Does cold open create urgency? Or does it confuse players?

---

#### **Minutes 8-15: Flashback - Character Creation**
- **Scene:** Cart arriving at academy (same as Prototype A)
- **Difference:** Player already knows this matters
  - They've seen the tournament
  - They know stakes exist
  - They want to understand the mystery potion

**Streamlined Character Creation:**
- Name, appearance (faster, 2 minutes max)
- Background choice, but now framed as:
  - "How did you learn to make potions?"
  - Choice affects which potions you start knowing

**Gameplay Test:** Does flashback structure maintain momentum?

---

#### **Minutes 15-25: Flashback - First Day, Accelerated**
- **Scene:** Garden gathering (same as Prototype A, but faster)
- **Meet Rachel:** She's the one who warned you in the arena
  - Players now care: "Why did she warn me?"
- **Meet Thornwood:** He's the one who looked disappointed
  - Players now care: "What does he want from me?"

**Gathering Tutorial:** Same mechanics, but with context
- Narrator: "Back then, I didn't know which ingredients would matter..."

**Gameplay Test:** Does added context make mundane tasks more engaging?

---

#### **Minutes 25-35: First Crafting (With Foreshadowing)**
- **Scene:** Crafting Simple Healing Tonic (same as Prototype A)
- **Addition:** After crafting, you notice a purple flower outside window
  - Rachel: "Don't touch Midnight Bloom. It's banned for first-years."
  - Close-up on purple flower (same color as mystery potion)

**Players connect:** "THAT'S the ingredient in the mystery potion!"

**Gameplay Test:** Does mystery hook increase engagement with tutorial?

---

#### **Minutes 35-48: Ezekiel Choice (Now With Weight)**
- **Same scenario as Prototype A**
- **Addition:** Ezekiel whispers: "I've been growing Midnight Bloom in secret"
- **Players realize:** Ezekiel is connected to the mystery potion

**Enhanced Choice:**
- Supporting Ezekiel = Accessing forbidden knowledge
- Not supporting = Playing it safe (like the arena choice)
- Parallel choice structure reinforces theme

**Gameplay Test:** Does mystery layer make choice more compelling?

---

#### **Minutes 48-55: The Secret Meeting**
- **Scene:** You receive note: "Midnight. Library. Come alone."
- **Rachel warns:** "Whatever this is, be careful."
- **You go to library**

**Meet:** Mysterious figure in shadows (face not revealed)
- "You have potential. But Thornwood will never teach you what you need."
- "Some knowledge is forbidden for a reason. Some... is forbidden to control you."
- Offers: Ancient recipe book with Midnight Bloom recipes
- "Take it. Or spend three years learning to lose."

**CHOICE:**
- → [Take the book] Path of forbidden knowledge
- → [Refuse] Path of traditional learning
- → [Report to Thornwood] Path of authority

**Each choice leads to different tournament outcome in flash-forward**

**Gameplay Test:** Does mystery payoff feel earned?

---

#### **Minutes 55-60: Flash-Forward Reveal**
- **Return to tournament (3 years later)**
- **Context provided based on choice:**
  - Took book = Mystery potion came from it
  - Refused = Mystery potion is grandmother's (different backstory)
  - Reported = No mystery potion, but you have Thornwood's secret technique

**Cliffhanger Ending:**
- Purple smoke clears
- You're standing, but something's wrong
- Your hands are glowing with strange energy
- Thornwood shouts: "Everyone out! NOW!"
- Rachel runs toward you: "Your eyes... they're not—"
- Screen cuts to black

**END OF HOUR ONE**

**Hook for Hour Two:**
- What happened with the potion?
- What's wrong with your character?
- Flash forward to Season 2, dealing with consequences?
- Or continue Season 1 with new context?

---

### Prototype B: Metrics to Test

1. **Hook Strength:** Do players care about the mystery immediately?
2. **Confusion:** Is flashback structure too confusing?
3. **Investment:** Do players care MORE about NPCs knowing future context?
4. **Pacing:** Does cold open justify itself, or feel gimmicky?
5. **Replayability:** Do players want to retry with different choices?

**Success Criteria:**
- 90%+ playtesters want to know what happens next (higher than Prototype A)
- 60%+ aren't confused by flashback structure
- 70%+ say cold open made them "care immediately"

---

## Prototype C: "The Systems Showcase"
**Philosophy:** Teach all core systems quickly, trust player intelligence
**Target Player:** Strategy gamers, optimizers, system-mastery fans
**Core Question:** Can we compress tutorials and let players experiment freely?

### Minute-by-Minute Breakdown

#### **Minutes 0-3: Rapid Character Creation**
- **Screen:** Character creation interface (game-y, not narrative)
- **Options displayed simultaneously:**
  - Name, appearance (sliders)
  - Background (shows starting stats clearly)
    - Rural Healer: Intuition +5, Precision +3
    - Urban Merchant: Business +5, Precision +3
    - Etc.
  - Starting specialization preview (locked, but shown for planning)

**Philosophy:** "Let me make my build and start playing"

**Gameplay Test:** Do optimizer players appreciate speed?

---

#### **Minutes 3-10: Interactive Tutorial (All Systems at Once)**
- **Scene:** Academy classroom, but UI-focused
- **Thornwood:** "Let's see what you know. Craft a healing potion."

**Tutorial Phase (Player-Driven):**
- Recipe book opens (shows 3 starter recipes)
- Inventory opens (shows gathered ingredients)
- Crafting station opens (shows tools)
- All UI visible simultaneously

**Interactive Tooltips:**
- Hover over anything → Tooltip explains
- Click on ESENS notation → Glossary opens
- Right-click ingredient → See all recipes using it
- Everything is explorable

**Guided Task:**
- "Craft Simple Healing Tonic (2 mushrooms, 1 sap, 1 berry)"
- Players figure out the UI themselves
- Undo button available if mistakes made

**Simplified Crafting:**
- No minigame (just click "Craft")
- Success/failure based on stats + dice roll
- Result shows:
  - Success chance: 85%
  - Quality potential: Standard-Fine
  - XP gain: +10 Precision
- Player clicks "Confirm" → Result shown instantly

**Gameplay Test:** Is removing minigame more satisfying for this audience?

---

#### **Minutes 10-20: Sandbox Experimentation**
- **Thornwood:** "Free crafting time. Experiment."
- **Tutorial:** "Try crafting the other two recipes, or experiment with your own combinations"

**Available Recipes:**
1. Simple Healing Tonic
2. Stamina Boost (3 ingredients)
3. Focus Elixir (4 ingredients)

**Experimentation Mode:**
- Click "Experiment" button
- Drag any ingredients to crafting window
- Game shows:
  - "Unknown Result - 45% Success Chance"
  - "Predicted Effect: Minor strength boost OR Minor poison"
  - "Crafting anyway will cost ingredients but grant knowledge"
- Players can try or cancel

**Reward Experimentation:**
- Failed experiments grant +5 Intuition XP
- Successful experiments discover new recipe variants
- Discovered recipes added to book with player's name

**Gameplay Test:** Do players engage with experimentation when given freedom?

---

#### **Minutes 20-28: Relationship System Tutorial (Efficient)**
- **Scene:** Class ends, 4 NPCs approach you
- **UI:** Relationship sidebar appears (always visible)

**Each NPC introduces themselves with personality shown:**
```
[Portrait] Rachel
O:0 C:0 E:+1 A:+1 N:0
Affinity: 0 (Neutral)
"Hey! Want to study together?"
```

**Tutorial:**
- "NPCs have personality traits (hover to see what they mean)"
- Hover over E:+1 → "High Extraversion: Outgoing, energetic, seeks interaction"
- "Dialogue choices affect affinity based on personality match"

**Speed Dating Dialogue:**
- Each NPC asks one question
- Player chooses response
- Affinity changes show immediately
- Personality explanation shows why

**Example:**
- **Ezekiel:** "Thornwood's so strict. You think we should always follow rules?"
- → [Yes, rules are important] C NPCs like this (+0.5), O NPCs dislike (-0.3)
- → [No, creativity matters more] O NPCs like this (+0.5), C NPCs dislike (-0.3)
- **UI shows:** "Ezekiel (High O): +0.5. Appreciates creative thinking."

**Gameplay Test:** Is explicit personality system MORE engaging for system-focused players?

---

#### **Minutes 28-38: Economy & Progression Tutorial**
- **Scene:** Visit academy shop
- **Tutorial:** "Manage your resources"

**Shop UI:**
```
Academy Merchant
(Your reputation: Neutral - Standard prices)

Common Mushrooms: 5g each (You have: 3)
Common Berries: 5g each (You have: 3)
Uncommon Crystals: 25g each (You have: 0)
Rare Phoenix Feather: 500g (You have: 0)

Your gold: 100g
```

**Tutorial Tasks:**
1. Buy 5x Uncommon Crystals (125g) → Learn about rarity tiers
2. Try to buy Phoenix Feather → "Insufficient funds" → Learn about economy
3. Sell 3 Simple Healing Tonics → Earn 45g → Learn about profit margins

**Progression UI Opens:**
```
Character Stats:
Precision: 15/100 [████░░░░░░] → Next bonus at 25
Knowledge: 30/100 [█████░░░░░] → Next bonus at 50
Intuition: 10/100 [███░░░░░░░] → Next bonus at 25

Current Bonuses:
- None yet (reach threshold to unlock)

XP needed to next threshold: 15 Precision, 20 Knowledge
```

**Gameplay Test:** Do explicit numbers satisfy optimizer players?

---

#### **Minutes 38-48: Combat Tutorial (Efficient)**
- **Scene:** "First-year practice duel (optional)"
- **Thornwood:** "Dueling is part of academy training. Try if you wish."

**Combat UI (Minimalist):**
```
YOUR STATS:              OPPONENT STATS:
HP: 100/100              HP: 100/100
Strength: 10             Strength: 10
Defense: 10              Defense: 10
Initiative: 12           Initiative: 8
```

**Potion Belt (Pre-Loaded for Tutorial):**
1. Strength Boost (+20% Strength, 3 turns)
2. Defense Shell (+30% Defense, 2 turns)
3. Healing Tonic (Restore 30 HP)

**Turn 1:**
- Initiative: You go first (higher initiative)
- **Actions:** Use Potion, Observe (see enemy buffs), Guard (+20% Defense this turn), Wait (delay action)
- Tutorial: "Try using Strength Boost"
- You drink → Strength: 10 → 12 (displayed clearly)

**Turns 2-4:**
- Opponent drinks Defense Shell
- Combat plays out with clear stat changes shown
- You win (tutorial designed for success)

**Tutorial Message:** "Combat in Season 3 is deeper. This was just basics."

**Gameplay Test:** Do players understand combat with minimal explanation?

---

#### **Minutes 48-55: Choice Efficiency Test**
- **Scene:** Ezekiel approaches with dilemma (same as other prototypes)
- **UI Difference:** Shows explicit consequences

**Choice Interface:**
```
Ezekiel is in trouble for experimenting.

[Support Ezekiel]
Predicted: Ezekiel +2.0, Thornwood -0.5
Unlocks: Ezekiel friendship path
Philosophy: Innovation over rules

[Stay Neutral]
Predicted: Ezekiel -0.5
Unlocks: Nothing
Philosophy: Self-preservation

[Report to Thornwood]
Predicted: Thornwood +1.0, Ezekiel -3.0
Unlocks: Thornwood's favor
Philosophy: Authority and tradition
```

**Warning:** "Major choice - affects available quests"

**Gameplay Test:** Does showing consequences reduce tension or increase strategic satisfaction?

---

#### **Minutes 55-60: Build Planning Reveal**
- **Scene:** Evening journal
- **UI:** Full character sheet with build planning

**Shows:**
```
Season 1 Progress (Day 1/100):
- Precision: 15/40 (Season cap)
- Knowledge: 30/40 (Season cap)
- Intuition: 10/40 (Season cap)

Season 1 Specialization Choice (Choose at Day 50):
→ Perfectionist (+20% Precision, +10% quality)
→ Innovator (Substitute ingredients, +15% Intuition)
→ Speed Brewer (25% faster crafting, -5% Precision)
→ Diplomat (+15 affinity gains)

Current Build Path: Innovation-focused
- High Ezekiel affinity = Ezekiel study bonus
- Experimentation XP = Intuition focus
→ Recommended Specialization: Innovator
```

**Hook for Hour Two:**
- "You have 49 days to build your character before specialization choice"
- "How will you balance crafting, socializing, and questing?"
- "Multiple paths are viable—find yours"

**END OF HOUR ONE**

---

### Prototype C: Metrics to Test

1. **Clarity:** Do explicit systems reduce or increase overwhelm?
2. **Engagement:** Do optimizer players prefer this approach?
3. **Retention:** Do players care about NPCs with less narrative focus?
4. **Satisfaction:** Is removing minigames better for this audience?
5. **Planning:** Do players appreciate build-planning information?

**Success Criteria:**
- 85%+ strategy players say "I understand all systems"
- 70%+ strategy players prefer this to narrative approach
- 60%+ still care about story/NPCs despite system focus

---

## Comparison Matrix

| Element | Prototype A (Cozy) | Prototype B (Mystery) | Prototype C (Systems) |
|---------|-------------------|----------------------|----------------------|
| **Pacing** | Slow, relaxed | Fast, then flashback | Medium, efficient |
| **Tutorial Style** | Guided, gentle | Context-driven | Self-directed |
| **Emotional Hook** | Friendship | Mystery/stakes | Mastery/optimization |
| **Crafting Complexity** | Minigame (circles, timing) | Same, but with context | Click-to-craft (stats only) |
| **NPC Introduction** | Gradual, personal | Fast, with future context | Rapid, system-focused |
| **Choice Presentation** | Timed, emotional | Timed, mysterious | Explained, strategic |
| **UI Visibility** | Hidden until needed | Hidden until needed | Everything visible |
| **Target Completion** | "I love these characters" | "I need to know what happens" | "I understand my build" |

---

## Recommendations

### **Test All Three**
Each prototype tests different hypotheses:

**Prototype A:** Best for primary audience (cozy crafters, narrative fans)
- **Strengths:** Character connection, gentle learning, satisfying loops
- **Risks:** May feel slow for some players

**Prototype B:** Best for narrative RPG fans, mystery lovers
- **Strengths:** Immediate engagement, mystery hook, replayability
- **Risks:** Flashback may confuse, cold open may be too intense

**Prototype C:** Best for strategy/optimization fans
- **Strengths:** Respects player intelligence, efficient, build-focused
- **Risks:** May lack emotional connection, feel sterile

### **Hybrid Approach (Recommended)**
Combine strengths of all three:

**Solution:** Offer choice at start
```
Welcome to PotionWorld!

How would you like to begin?

[Cozy Start] - Gentle tutorial, meet characters slowly
[Mystery Start] - Cold open with flashback structure
[Systems Start] - Efficient tutorial, focus on mechanics

(You can change this in settings anytime)
```

This respects different player types and increases accessibility.

---

## Next Steps

1. **Build One Prototype First**
   - Recommend: Prototype A (targets primary audience)
   - Timeline: 2-4 weeks for playable 60 minutes
   - Assets needed: 1 location (academy), 4 NPCs, 3 ingredients, 1 recipe

2. **Playtest With 10-15 Players**
   - Mix of target audiences
   - Record: Completion time, confusion points, engagement moments
   - Survey: "Did you want to keep playing?"

3. **Iterate Based on Feedback**
   - If pacing too slow → Add more Prototype B elements
   - If systems confusing → Add more Prototype C clarity
   - If characters boring → Deepen Prototype A moments

4. **Build Other Prototypes If Needed**
   - Only if first prototype doesn't hit targets
   - Or if different publishers want to see different approaches

**Goal:** Have one polished 60-minute experience that proves the concept before building 20+ hours of content.
