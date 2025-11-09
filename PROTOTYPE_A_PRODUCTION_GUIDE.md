# Prototype A: Production Guide
## "The Cozy Welcome" - 60% Cozy, 40% RPG

**Tone Balance:**
- 60% Cozy: Gentle pacing, satisfying loops, warm relationships, beautiful moments
- 40% RPG: Meaningful choices, stat progression, build diversity, visible consequences

**Reference Games:**
- Persona 5 (daily life structure + stats + relationships)
- Fire Emblem: Three Houses (academy setting + character bonding + choices matter)
- Stardew Valley (gathering, crafting loops, NPC schedules)
- Potion Craft (ingredient discovery, visual crafting)

---

## Core Design Pillars for Prototype A

### 1. **Cozy Elements (60%)**
✅ Gentle, non-punishing tutorials
✅ Beautiful garden gathering with satisfying feedback
✅ NPCs feel like friends (warm, memorable, supportive)
✅ Crafting has tactile, meditative minigame
✅ No time pressure or stress in first hour
✅ Optional exploration (never forced)

### 2. **RPG Elements (40%)**
✅ Stats matter (Precision affects crafting success)
✅ Choices have visible consequences (Ezekiel affinity changes)
✅ Build planning (background choice affects playstyle)
✅ Progression tracking (XP, mastery levels)
✅ Multiple valid paths (supporting vs. not supporting Ezekiel both work)
✅ Foreshadowing of deeper systems (Rachel's nightmare, mysterious note)

---

## Minute-by-Minute Breakdown (Refined)

### **Minutes 0-5: Arrival (60% Cozy, 40% RPG)**

#### Scene: Cart Ride to Academy
**Visuals:**
- Golden hour sunset lighting (warm, inviting)
- Rolling hills, academy spires in distance
- Gentle ambient music (strings, soft piano)

**Narration (Grandmother's Letter - voiceover):**
> "Dearest child,
>
> You have the gift—I've seen it in the way you handle ingredients, the care you take with every step. The academy will teach you technique and notation, but never forget: potions are made for people, not perfection.
>
> Trust your heart as much as your head. And remember, every choice you make as an alchemist matters—not just to your potions, but to the world around you.
>
> With all my love,
> Grandmother"

**Cozy Element:** Warm letter, beautiful scenery, no pressure
**RPG Element:** Letter foreshadows choice/consequence theme

#### Interactive Character Creation
**Cart Driver (friendly NPC):** "First time at the academy? You must be excited!"

**Name Entry:**
- Text input with warm UI (parchment texture, quill cursor)
- Optional: Suggested names if player wants

**Appearance:**
- 4 options (2 masc-coded, 2 femme-coded)
- Warm art style (think Spiritfarer, Persona 5)
- Optional: Age slider (14-18, affects starting dialogue slightly)

**Driver:** "So what brings you to alchemy? Everyone's got their reason..."

**Background Choice (Reframed for 60/40 tone):**

```
[Rural Healer's Apprentice]
"My grandmother taught me. Healing is in my blood."
→ Cozy: Know herb gathering already, villagers trust you
→ RPG: Start with +5 Intuition, +3 Precision
→ Unlocks: Special grandmother recipes later

[City Merchant's Child]
"My family's apothecary needs a certified alchemist."
→ Cozy: Good at pricing, know how to talk to customers
→ RPG: Start with +5 Business, +3 Precision
→ Unlocks: Shop expansion options in Season 2

[Noble House Tradition]
"Every generation of my family attends the academy."
→ Cozy: Professors know your family, instant respect
→ RPG: Start with +5 Reputation, +3 Knowledge
→ Unlocks: Royal court connections in Season 4

[Scholarship Winner]
"I competed against hundreds for this spot."
→ Cozy: Underdog story, earn respect through skill
→ RPG: Start with +5 Knowledge, +3 Combat Instinct
→ Unlocks: Rival-to-friend arc with competitive NPCs

[Wanderer's Intuition]
"I've traveled everywhere. Ingredients speak to me."
→ Cozy: Know rare ingredients, natural forager
→ RPG: Start with +5 Intuition, +3 Business
→ Unlocks: Exotic ingredient sources early
```

**Cozy Element:** Each background feels personal, warm
**RPG Element:** Clear stat impacts, visible consequences

**Driver drops you off:**
- "Good luck, kid. You're gonna do great."
- Warm goodbye, you wave

---

### **Minutes 5-12: The Dorm Room (70% Cozy, 30% RPG)**

#### Meeting Rachel (Your Roommate)

**Scene:**
- Cozy dorm room (two beds, desks, window overlooking garden)
- Warm evening light through window
- Rachel's side already decorated (plants, books, colorful blanket)

**Rachel Introduction:**
```
[KIRA enters, arms full of books, nearly drops them]

KIRA: "Oh! You're here! Hi! I'm Rachel!"
[Sets books down messily]
"I got here yesterday and I've already explored EVERYTHING. The garden is amazing, the library has this restricted section that's totally mysterious, and—oh, sorry, I'm talking too much, aren't I?"

[Nervous laugh]

"I do that when I'm excited. I'm Rachel. Did I say that already?"
```

**Cozy Element:** Endearing introduction, immediate warmth
**RPG Element:** Rachel's personality visible (High E, High A)

**First Choice (Low Stakes, But Revealing):**
```
KIRA: "Want to explore the garden together? Or do you need time to unpack? I totally get it if you want space!"

→ [Let's explore together!]
   Cozy: Immediate friendship, she shows you around
   RPG: Rachel +0.5, High E NPCs like enthusiasm

→ [I'll unpack first, thanks]
   Cozy: Take your time, no pressure, she understands
   RPG: Rachel +0.0 (neutral), sets "thoughtful" personality flag

→ [Can you help me unpack?]
   Cozy: She helps enthusiastically, bonding moment
   RPG: Rachel +0.7, unlocks "study buddy" option later
```

**Cozy Element:** All choices are valid, no wrong answer
**RPG Element:** Choice affects relationship trajectory

#### If Player Chooses to Unpack

**Exploration Tutorial (Gentle):**
- Click on items to examine
- Each has a warm description:

```
[Desk] - "Carved wood desk with drawer. Smells like cedar."
→ Click drawer: Find blank journal
   "Your grandmother slipped this in your bag. The first page reads: 'Document your journey.'"

[Window] - "View of the ingredient garden. Purple flowers glow faintly in the twilight."
→ RPG Element: Foreshadows Midnight Bloom

[Recipe Book on Shelf] - "Academy-issued recipe compendium. Mostly empty."
→ First page has welcome note from Headmaster
   Cozy: Warm welcome message
   RPG: Explains mastery system briefly

[Equipment on Workbench] - "Basic mortar & pestle, some glass vials."
→ "Standard student-grade equipment. It'll do for now."
   RPG Element: Hints at upgrades later
```

**Cozy Element:** No pressure, optional exploration, warm descriptions
**RPG Element:** Environmental storytelling, system hints

---

### **Minutes 12-20: The Garden (65% Cozy, 35% RPG)**

#### Setting the Tone

**If with Rachel:**
- She chatters enthusiastically about plants
- Points out interesting things
- "Oh! Moonbell flowers! They only bloom at night. Aren't they pretty?"

**If alone:**
- Peaceful ambient sounds (birds, wind, rustling leaves)
- Other students gathering in background (living world)
- Calm, meditative music

**Visual Design (Cozy Focus):**
- Warm evening light (golden hour)
- Glowing particles around special ingredients
- Gentle animations (flowers swaying, butterflies)
- Color-coded glow by ingredient type (green=roots, red=berries, etc.)

#### Gathering Tutorial

**UI Design (Cozy-RPG Hybrid):**
```
[Approach glowing mushroom patch]

UI Tooltip: "Common Mushrooms - Press [E] to gather"

[Gathering Animation]
- Character kneels down
- Hand reaches out gently
- Mushrooms sparkle and lift into hand
- Satisfying "pling!" sound
- Particle effects (gentle, not overwhelming)

Notification (Warm Design):
┌──────────────────────────┐
│ ✨ Gathered!             │
│                          │
│ Common Mushrooms x3      │
│ [Small rotating 3D icon] │
│                          │
│ "Fresh and earthy"       │
└──────────────────────────┘
```

**Cozy Elements:**
- Beautiful visuals and sounds
- Gentle animations
- Warm, encouraging notifications
- Optional flavor text ("Fresh and earthy")

**RPG Elements:**
- Ingredient added to inventory
- Stack counter (x3)
- Sets up resource management

#### Gathering Sequence

**Available Ingredients:**
1. **Common Mushrooms** (glowing blue) - Easy to spot
2. **Common Berries** (glowing red) - On bushes
3. **Common Roots** (glowing green) - In soil patches
4. **Tree Sap** (glowing amber) - On tree trunk
5. **Moonbell Flowers** (glowing purple-white) - Optional, rare

**Tutorial Flow:**
- Game guides you to mushrooms first (closest)
- Berries and roots are visible nearby
- Tree sap requires slight exploration (teaches exploration)
- Moonbell flowers are hidden (rewards curiosity)

**If player finds Moonbell:**
```
[Gather Moonbell Flowers]

Special Notification:
┌──────────────────────────┐
│ 🌙 Rare Discovery!       │
│                          │
│ Moonbell Flowers x2      │
│                          │
│ "Blooms only at night.   │
│  Professors love these." │
│                          │
│ Intuition +5 XP          │
└──────────────────────────┘
```

**Cozy Element:** Rewards exploration without requiring it
**RPG Element:** XP gain, foreshadows gift-giving system

#### Meeting Thornwood (Inciting Incident)

**Triggered when player has gathered 3+ ingredient types:**

```
[THORNWOOD approaches from behind]

THORNWOOD: "Ahem."

[Player character startles, turns around]

THORNWOOD: "First-day students shouldn't be in the ingredient garden unsupervised. Academy policy, page fourteen."

[He looks stern but not angry]

THORNWOOD: "However... I see you're gathering with care. Not trampling the beds like last year's cohort."
```

**Choice (Tone-Setting for Player Character):**
```
→ [I'm so sorry! I didn't know]
   Cozy: Polite, apologetic
   RPG: Thornwood +0.5 (appreciates respect), sets "cautious" flag

→ [I couldn't wait to see the ingredients!]
   Cozy: Enthusiastic, genuine
   RPG: Thornwood +0.3 (respects passion), sets "curious" flag

→ [I was being careful, I promise]
   Cozy: Practical, reassuring
   RPG: Thornwood +0.5 (values precision), sets "responsible" flag

→ [My grandmother taught me proper gathering]
   Cozy: Personal, shows background
   RPG: Thornwood +0.7 (respects tradition), sets "traditional" flag
   Unlock: Only available with Rural Healer background
```

**Cozy Element:** Thornwood is stern but fair, not mean
**RPG Element:** Choice shapes PC personality, different options based on background

**Thornwood's Response:**
```
THORNWOOD: "Hmph. Well, since you're already here..."

[Walks to tree, collects sap into vial]

THORNWOOD: "Tree sap. Essential binding agent. You'll need this for tomorrow's lesson."

[Hands player 2x Tree Sap]

THORNWOOD: "Welcome to the Royal Academy. I'm Instructor Thornwood. I expect precision, dedication, and respect for the craft."

[Softens slightly]

"Your grandmother sent word of your enrollment. She speaks highly of you. Let's see if she's right."

[Walks away]
```

**Cozy Element:** Gruff-but-kind archetype, grandmother connection
**RPG Element:** Establishes Thornwood as authority figure, hints at high standards

**Rachel's Reaction (if she's with you):**
```
KIRA: [Whispers] "That's Thornwood. He's REALLY strict but everyone says he's the best teacher here."

[Normal voice]

"He didn't yell at you! That's a good sign. Last year he made someone cry on day one."

[Nervous laugh]

"Okay that sounded bad. He's not mean! Just... particular."
```

**Cozy Element:** Rachel as friendly guide, relatable nervousness
**RPG Element:** Establishes academy hierarchy and reputation systems

---

### **Minutes 20-30: First Crafting Lesson (50% Cozy, 50% RPG)**

#### Transition: Next Morning

**Fade to black with warm text:**
```
~ The Next Morning ~

[Sunrise over academy]
[Gentle morning music - soft strings, woodwinds]
```

**Brief Cutscene (Optional Skip):**
- Morning routine montage: Getting dressed, Rachel rushing, walking to class together
- Other students gathering in hallway
- Warm chatter in background
- Shows living academy world

**Cozy Element:** Lived-in world, daily routine comfort
**RPG Element:** Establishes time passage, day structure

#### Classroom Scene

**Setting:**
- 8 student desks arranged in U-shape
- Instructor's demonstration table at front
- Shelves with ingredient jars (glowing softly)
- Large windows with morning light

**NPCs Present:**
- Rachel (sits next to you, waves)
- Ezekiel (messy hair, curious eyes, sketching in notebook)
- Miriam (nervous, organized desk, reviewing notes)
- 5 other students (background, less defined)

**Thornwood Enters:**
```
THORNWOOD: "Good morning. Today you will craft your first potion."

[Walks to demonstration table]

"Before we discuss notation and theory, you will learn by doing. This is how the craft has been taught for three centuries."

[Holds up vial of green liquid]

"Simple Healing Tonic. Four ingredients. Basic binding. No room for creativity."

[Looks at class]

"Not yet."
```

**Cozy Element:** Traditional teaching, no judgment, clear expectations
**RPG Element:** Foreshadows experimentation unlocking later

#### The Recipe

**UI: Recipe Card Appears (Beautiful Design)**
```
╔════════════════════════════════════════╗
║     SIMPLE HEALING TONIC               ║
╟────────────────────────────────────────╢
║ Restores 30 HP over 10 seconds         ║
║ Difficulty: Trivial (5/100)            ║
║ Tradition: First potion for all        ║
║ academy students since 1642            ║
╟────────────────────────────────────────╢
║ INGREDIENTS:                           ║
║  🍄 Common Mushrooms x2 [Healing base] ║
║  🍯 Tree Sap x1 [Binding agent]        ║
║  🫐 Common Berries x1 [Potency boost]  ║
╟────────────────────────────────────────╢
║ NOTATION: P+H30%10s.ST                 ║
║ (Don't worry about this yet)           ║
╟────────────────────────────────────────╢
║ Success Rate: 95% (Student-grade)      ║
║ Quality Potential: Standard            ║
╚════════════════════════════════════════╝
```

**Cozy Elements:**
- Beautiful, readable design
- Historical flavor text (tradition)
- "Don't worry about this yet" (reassuring)
- High success rate (not punishing)

**RPG Elements:**
- Clear stats (30 HP, 10 seconds)
- Success rate visible
- ESENS notation shown (but not required yet)
- Difficulty rating

#### Crafting Minigame (Tactile, Satisfying)

**Step 1: Grind Mushrooms**

**UI:**
```
[Mortar & Pestle appear on screen]
[2 whole mushrooms in mortar]

Instruction: "Grind the mushrooms into powder"
[Circular motion indicator appears]

Player Input: Click and drag in circular motions
```

**Feedback (60% Cozy, 40% RPG):**
- **Visual:** Mushrooms gradually break down (3 stages: chunks → bits → powder)
- **Sound:** Satisfying grinding sound (ASMR-quality)
- **Particles:** Gentle dust particles rise
- **Haptic:** Controller vibration on each grind (if applicable)
- **Progress Bar:** Shows grinding completion (0% → 100%)

**Quality System (RPG Element):**
```
If player grinds smoothly (3-5 circles): "Perfect powder - Precision +1 XP"
If player grinds too fast (jerky): "Acceptable powder - No bonus"
If player barely grinds: "Coarse powder - May reduce quality"
```

**Cozy Element:** Can't fail, only affect quality
**RPG Element:** Skill affects outcome slightly

**Step 2: Add Tree Sap**

**UI:**
```
[Ground mushrooms in mortar]
[Tree sap vial appears]

Instruction: "Add tree sap to bind the mixture"
```

**Interaction:**
- Drag vial to mortar
- Pouring animation (liquid flows smoothly)
- Mixture glows faintly and binds together
- Satisfying "whoosh" sound

**Visual Feedback:**
- Powder + sap = sticky paste (texture changes)
- Color shifts from brown-gray to brown-green
- Gentle glow effect

**Cozy Element:** Beautiful visual transformation, automatic success
**RPG Element:** Learn about binding agents (teaches crafting theory)

**Step 3: Add Berries**

**UI:**
```
[Paste in mortar]
[3 berries appear]

Instruction: "Add berries for potency"
```

**Interaction:**
- Drag berries one by one
- Each berry squishes satisfyingly
- Paste turns green with each berry
- Sweet scent particle effect (visual sparkles)

**Visual Magic Moment:**
- Final berry added → paste glows bright green
- Swirl effect as it homogenizes
- Transforms into liquid potion

**Cozy Element:** Magical transformation, beautiful and safe
**RPG Element:** See ingredient properties combine

**Step 4: Decant into Vial**

**UI:**
```
[Glowing green liquid in mortar]
[Empty vial appears]

Instruction: "Pour carefully into the vial"
```

**Interaction:**
- Tilt mortar by dragging
- Liquid flows into vial
- If steady: Perfect fill
- If jerky: Spills slightly (cosmetic only, doesn't fail)

**Final Moment:**
```
[Vial fills with glowing green potion]
[Cork stopper appears, seals with satisfying *pop*]
[Potion rotates slowly, showing it off]

Success!
┌──────────────────────────────────────┐
│ ⚗️ SIMPLE HEALING TONIC CREATED      │
│                                      │
│ Quality: Standard                    │
│ Potency: 30 HP / 10s                 │
│                                      │
│ "Your first potion. Keep it safe."  │
│                                      │
│ Precision +10 XP                     │
│ Knowledge +25 XP                     │
│                                      │
│ Recipe added to Compendium           │
└──────────────────────────────────────┘
```

**Cozy Elements:**
- Beautiful success animation
- Sentimental message
- Can't fail (first potion always succeeds)
- Warm congratulatory tone

**RPG Elements:**
- Clear XP gains
- Quality rating (sets up system)
- Recipe learning tracked

**Thornwood's Reaction:**
```
THORNWOOD: [Nods] "Acceptable. You followed instructions precisely."

[To whole class]

"Each of you has now created your first potion. This is the foundation. Master the basics before attempting complexity."

[Looks at your character]

"Keep that vial. First potions are... significant."
```

**Cozy Element:** Gruff approval, sentimental moment
**RPG Element:** Sets expectation for progression

---

### **Minutes 30-40: Free Time & Social Exploration (70% Cozy, 30% RPG)**

#### Transition: Class Ends

**Thornwood:** "Afternoon is yours. Use it wisely."

**Tutorial Prompt:**
```
╔════════════════════════════════════╗
║  Afternoon Free Time               ║
╟────────────────────────────────────╢
║ You have time to explore or        ║
║ socialize before dinner.           ║
║                                    ║
║ Where would you like to go?        ║
╚════════════════════════════════════╝

[Map Menu Opens - Illustrated, Cozy Style]
```

**Available Locations:**
1. 🌿 **Garden** - Gather more ingredients
2. 📚 **Library** - Read about potion history
3. 🛏️ **Dormitory** - Talk to Rachel
4. ⛲ **Courtyard** - Meet other students
5. 🏛️ **Main Hall** - Explore academy

**Cozy Element:** Player choice, no pressure, illustrated map
**RPG Element:** Time management (gentle), location-based events

#### Designed Path: Courtyard (Social Focus)

**If player chooses Courtyard:**

**Setting:**
- Beautiful stone courtyard with fountain
- Trees providing shade
- 3 students practicing at stone tables
- Warm afternoon light, birds chirping

**Meet Ezekiel (Important NPC)**

**Visual:**
- Messy dark hair, intense eyes
- Sitting alone at table with ingredients spread out
- Sketching something in notebook
- Looks up as you approach

```
MARCUS: "Hey. You're the new student, right?"

[Doesn't wait for answer]

"I'm Ezekiel. Watch this."

[Takes ingredients: 2 mushrooms, 1 sap, 1 berry, + crystal dust]

"Thornwood says 'follow the recipe exactly.' But what if we add crystal dust to amplify the effect?"
```

**Choice (Sets PC's Approach to Alchemy):**
```
→ [That sounds cool!]
   Cozy: Enthusiastic support
   RPG: Ezekiel +1.0, Openness +1, sets "innovative" path

→ [What if it goes wrong?]
   Cozy: Cautious but curious
   RPG: Ezekiel +0.3, Neuroticism +0.5, sets "careful" path

→ [Thornwood said no experimenting]
   Cozy: Rule-following, responsible
   RPG: Ezekiel +0.0, Conscientiousness +1, sets "traditional" path

→ [Let me try it with you]
   Cozy: Collaborative, supportive
   RPG: Ezekiel +1.5, Agreeableness +0.5, unlock joint experiment
```

**Cozy Element:** All responses feel natural, in-character
**RPG Element:** Each shapes both relationship and PC personality

**If player chooses "Let me try it with you":**

**Mini-Scene:**
```
MARCUS: [Surprised] "Really? Okay, yeah!"

[You both craft at the table]
[Same minigame, but crystal dust adds sparkle effect]

Result: Potion turns brighter green, almost glowing

MARCUS: "Whoa. It worked!"

[Tests it - drinks half]

MARCUS: "I can FEEL it. Stronger than the standard version."

[Offers you the other half]

"Partners?"
```

**Bonding Moment (Cozy Core):**
- Share potion (symbol of trust)
- Ezekiel smiles genuinely
- Warm music swell
- **Ezekiel Affinity → +2.0** (significant)

**RPG Element:**
- Learn about ingredient substitution
- Unlock Ezekiel as study partner
- Sets up Season 1 friendship arc

#### Meet Miriam (Supporting NPC)

**After Ezekiel interaction, notice Miriam:**

**Visual:**
- Sitting at far table, alone
- Ingredients laid out precisely, but she looks stressed
- Her potion is brown instead of green

```
SENA: [Muttering to herself] "No, no, no... what did I do wrong?"

[Looks up, sees you approaching]

[Nervous] "Oh! Um... I... my potion turned brown."

[Near tears]

"I followed the recipe exactly. I thought I did. But it's ruined and I don't know why and Thornwood is going to think I'm incompetent and—"

[Takes breath]

"Sorry. I'm panicking."
```

**Choice (Tests Player's Compassion):**
```
→ [Help her figure it out]
   Cozy: Kind, helpful, investigative
   RPG: Miriam +2.0, Agreeableness +1, mini-puzzle gameplay

→ [Reassure her gently]
   Cozy: Emotional support, no pressure
   RPG: Miriam +1.0, reduces her Neuroticism slightly

→ [Suggest asking Thornwood]
   Cozy: Practical advice
   RPG: Miriam +0.5, Conscientiousness +0.5

→ [Say nothing, walk away]
   Cozy: Respects her space
   RPG: Miriam +0.0, no relationship development
```

**If player helps:**

**Mini-Puzzle (Cozy Detective Moment):**
```
[Examine Miriam's table]

Ingredients used:
- Common Mushrooms x4 (should be x2!)
- Tree Sap x1
- Common Berries x1

[Click on mushrooms]
"She used twice as many mushrooms. That's why it's dark and thick."

→ Explain to Miriam
```

**Miriam's Reaction:**
```
SENA: [Realization] "Oh! I counted wrong. I was so nervous I miscounted."

[Relieved laugh]

"Thank you. I was about to cry in front of everyone."

[Genuine smile]

"I'm Miriam. Sorry for the... mess. I get anxious about grades."

[Shyly] "Want to study together sometime? I'm good at memorization, just bad at... not panicking."
```

**Cozy Payoff:**
- Helped someone feel better
- Made a friend through kindness
- Miriam will return favor later (plants seed)

**RPG Payoff:**
- Miriam +2.0 affinity (big gain)
- Learn about ingredient ratios
- Unlock Miriam study sessions (memory/knowledge bonuses)

---

### **Minutes 40-50: The Ezekiel Dilemma (50% Cozy, 50% RPG)**

#### Transition: Dinner Bell

**Bell chimes across courtyard**

**Rachel appears:** "Dinner time! Come on!"

**Walking to Dining Hall:**
- Warm chatter of students
- Smell of food (described)
- Cozy evening setting

**Incident: Ezekiel in Trouble**

**Scene:**
```
[Passing hallway]
[Hear raised voice]

INSTRUCTOR REVAL: "Experimentation is for THIRD-YEARS, Mr. Caldwell!"

[See Ezekiel standing outside classroom, head down]

REVAL: "I will be reporting this to Headmaster Sinclair. One more incident and you'll be scrubbing cauldrons for a month!"

[Reval storms off]

[Ezekiel slumps against wall]
```

**Cozy Element:** Witnessing injustice creates empathy
**RPG Element:** Sets up moral choice

**Choice: Approach or Ignore**
```
→ [Go to Ezekiel]
   Continue to scene

→ [Give him space]
   Skip scene, neutral outcome
```

**If approach:**

**Finding Ezekiel in Garden (Private Moment)**

**Setting:**
- Garden at twilight
- Purple Moonbell flowers glowing
- Ezekiel sitting on bench, frustrated

```
MARCUS: [Doesn't look up] "Reval caught me experimenting. Again."

[Bitter laugh]

"I just wanted to test if moonbell petals work in healing tonics. They do, by the way. Makes them 30% stronger."

[Looks at you]

"But that doesn't matter. Reval's reporting me to Sinclair. If I get one more violation, I could be expelled."

[Voice cracks slightly]

"My family isn't rich. They saved for years to send me here. If I get kicked out..."

[Stands up, pacing]

"I don't get it. Isn't alchemy about discovery? Why do they punish curiosity?"
```

**THE BIG CHOICE (Moral Core of Prototype)**

**UI: Choice Screen with Time Pressure (60 seconds)**
```
╔═══════════════════════════════════════════════════╗
║  Ezekiel could be expelled for experimenting.      ║
║  What do you believe?                             ║
╟───────────────────────────────────────────────────╢
║  💚 [Support Ezekiel]                              ║
║  "You were just being creative. Reval's wrong."   ║
║                                                   ║
║  ⚖️ [Gentle Critique]                             ║
║  "Maybe save experiments for when you're ready?"  ║
║                                                   ║
║  🤐 [Stay Neutral]                                ║
║  "I don't want to get involved, sorry."           ║
║                                                   ║
║  💡 [Offer Solution]                              ║
║  "What if I ask Thornwood about experiment days?" ║
║  (Requires Openness or previous curious choices)  ║
╚═══════════════════════════════════════════════════╝

[Timer: 60s]
```

**Consequences (Visible Immediately + Long-Term):**

**Option 1: Support Ezekiel**
```
MARCUS: [Eyes light up] "Thank you. Everyone else just tells me to follow the rules."

[Stands straighter]

"You get it. Alchemy isn't about memorizing recipes—it's about pushing boundaries."

[Determined]

"I'm not going to stop. But it means a lot that you believe in me."

Immediate:
- Ezekiel Affinity +2.5
- Thornwood Affinity -0.5 (he hears about it)
- PC Trait: "Innovator" unlocked

Long-term (Shown in journal):
- Ezekiel will share experimental recipes
- Unlock: Ezekiel rebellion arc
- Philosophy: Innovation over tradition
```

**Option 2: Gentle Critique**
```
MARCUS: [Disappointed but understanding] "Yeah... maybe you're right."

[Sighs]

"I just hate waiting. But I don't want to get expelled either."

[Looks at you]

"Thanks for being honest, I guess."

Immediate:
- Ezekiel Affinity +0.5
- Thornwood Affinity +0.3
- PC Trait: "Balanced" unlocked

Long-term:
- Ezekiel will be more cautious
- Unlock: Ezekiel redemption arc
- Philosophy: Caution and growth
```

**Option 3: Stay Neutral**
```
MARCUS: [Hurt] "Right. Okay."

[Turns away]

"Forget I said anything."

[Walks off alone]

Immediate:
- Ezekiel Affinity -0.5
- No other changes
- PC Trait: "Self-Preserving" unlocked

Long-term:
- Ezekiel distances himself
- Miss his friendship arc
- Philosophy: Self over community
```

**Option 4: Offer Solution** (Unlockable)
```
MARCUS: [Surprised] "You'd do that? Talk to Thornwood?"

[Hopeful]

"If there were official experiment days, I wouldn't have to sneak around."

[Genuine smile]

"That's... actually really smart. Thanks."

Immediate:
- Ezekiel Affinity +2.0
- Thornwood Affinity +0.5 (respects initiative)
- PC Trait: "Diplomat" unlocked
- Unlock: Special conversation with Thornwood

Long-term:
- Ezekiel trusts you deeply
- Thornwood sees your leadership
- Unlock: Best of both worlds arc
- Philosophy: Find middle ground
```

**Cozy Elements:**
- Ezekiel is vulnerable, not aggressive
- All choices feel valid emotionally
- Game respects player values
- No "right" answer, just different paths

**RPG Elements:**
- Clear mechanical consequences
- Long-term arc changes
- Stat changes visible
- Unlockable options based on previous choices

**Journal Entry Auto-Writes:**
```
╔════════════════════════════════════════╗
║  Day 1 Reflection                      ║
╟────────────────────────────────────────╢
║ Ezekiel got in trouble for experimenting║
║ with moonbell petals. He could be      ║
║ expelled.                              ║
║                                        ║
║ I [supported him / advised caution /   ║
║  stayed neutral / offered to help].    ║
║                                        ║
║ Grandmother always said potions are    ║
║ about people. But are they also about  ║
║ rules? Or discovery?                   ║
║                                        ║
║ I'm not sure yet. But I think this     ║
║ choice will matter.                    ║
╚════════════════════════════════════════╝
```

---

### **Minutes 50-58: Evening Reflection (65% Cozy, 35% RPG)**

#### Back to Dorm Room

**Setting:**
- Nighttime, stars visible through window
- Rachel already in bed, reading
- Soft lamp light, cozy atmosphere

**Rachel's Check-In:**
```
KIRA: [Looks up from book] "Hey! How was your first day?"

[Warm smile]

"I heard you helped Miriam with her potion. That was really nice."

[If you interacted with Ezekiel:]
"Also heard Ezekiel got in trouble again. That's... complicated."

[Yawns]

"Sorry, I'm exhausted. First days are a lot."

[Turns off lamp]

"Goodnight! Tomorrow's gonna be great."
```

**Cozy Element:** Roommate check-in, warm domestic moment
**RPG Element:** NPCs talk to each other (living world)

**Brief Cutscene: Rachel's Nightmare**

**After Rachel falls asleep:**
```
[Screen darkens]
[Rachel tosses and turns]

KIRA: [Sleep-talking] "No... I didn't mean to... it wasn't my fault..."

[Whimpers]

"Don't tell them... please don't..."

[Breathing heavily, then settles]

[Camera close-up on her worried face]
```

**Cozy Element:** Humanizes Rachel, creates mystery gently
**RPG Element:** Foreshadows Rachel's secret quest arc

#### Journal & Stats Screen

**UI: Journal Opens (Warm Parchment Design)**
```
╔════════════════════════════════════════════════╗
║       🌙 End of Day 1 🌙                       ║
╟────────────────────────────────────────────────╢
║ RELATIONSHIPS:                                 ║
║                                                ║
║ Rachel         [♥♥♥♡♡] +1.5 Friendly            ║
║ Ezekiel       [♥♥♥♥♡] +2.5 Warm                ║
║ Miriam         [♥♥♥♡♡] +2.0 Grateful            ║
║ Thornwood    [♥♡♡♡♡] +0.3 Neutral             ║
║                                                ║
╟────────────────────────────────────────────────╢
║ STATS:                                         ║
║                                                ║
║ Precision    [███░░░░░░░] 11/100               ║
║ Knowledge    [█████░░░░░] 25/100               ║
║ Intuition    [██░░░░░░░░] 10/100               ║
║                                                ║
║ Next threshold: Precision 25 (unlock bonuses) ║
╟────────────────────────────────────────────────╢
║ RECIPES LEARNED:                               ║
║                                                ║
║ Simple Healing Tonic [Novice 25/100]           ║
║                                                ║
╟────────────────────────────────────────────────╢
║ MAJOR CHOICES:                                 ║
║                                                ║
║ • Supported Ezekiel's experimentation           ║
║   → Innovation Path                            ║
║                                                ║
╟────────────────────────────────────────────────╢
║ TRAITS UNLOCKED:                               ║
║                                                ║
║ Innovator - Encourages creative thinking       ║
╚════════════════════════════════════════════════╝
```

**Cozy Elements:**
- Beautiful, readable design
- Hearts for affinity (warm visual)
- Encouraging messages ("You're learning!")
- Progress feels meaningful

**RPG Elements:**
- Clear numerical tracking
- Threshold system visible
- Recipe mastery progress
- Choice consequences tracked

---

### **Minutes 58-60: Hook for Hour Two (60% Cozy, 40% RPG)**

#### Morning of Day 2

**Transition:**
```
~ Day 2 - Morning ~

[Sunrise through window]
[Rachel already awake, getting ready]
```

**Rachel:** "Morning! Thornwood posted the lesson plan—we're making Stamina Boost today!"

**Breakfast Scene (Quick)**
- Walk to dining hall together
- Background students chatting (living world)
- Warm morning atmosphere

**Ezekiel Approaches:**
```
[If you supported Ezekiel:]
MARCUS: [Sits with you] "Hey. Thanks again for yesterday."

[Lowers voice]

"Want to study together later? I know some... unofficial techniques."

[Grins]

Unlock: Ezekiel Study Sessions (Precision +5/session)

[If you didn't support:]
MARCUS: [Sits far away, doesn't make eye contact]
```

**Cozy Element:** Immediate payoff for choices
**RPG Element:** Mechanical rewards for relationship building

**The Mysterious Note:**

**Scene:**
```
[Back at dorm, getting recipe book]

[As you open it, a folded note falls out]

[Pick it up]

Note reads:
"Meet me in the library. Tonight. Midnight.
 Come alone.
 I have something you need to see.
 -A Friend"

[Rachel peeks over shoulder]

KIRA: [Worried] "That's... creepy. You're not actually going, right?"

Choice:
→ [I'm curious]
→ [Probably not]
→ [Will you come with me?]
```

**Hook Elements:**
- Mystery (who sent it?)
- Intrigue (what do they have?)
- Choice (go or not?)
- Rachel's reaction (adds stakes)

**Final Scene: Thornwood's Class**

```
THORNWOOD: "Today, Stamina Boost. Four ingredients. More complex timing."

[Looks at class]

"Yesterday was foundation. Today, we see who paid attention."

[Camera pans across nervous students]

THORNWOOD: "Begin."

[Screen fades to black]

═══════════════════════════════════════
         END OF HOUR ONE

    Continue to discover:
    • The midnight meeting
    • Advanced crafting challenges
    • Miriam's secret
    • Ezekiel's rebellion
    • And the mystery of the Moonbell...
═══════════════════════════════════════
```

---

## Production Assets Needed

### Art Assets (Cozy 60%, RPG 40%)

**Characters (Portraits + Sprites):**
1. **Player Character** - 4 appearance variants
   - Portraits: Neutral, Happy, Surprised, Determined
   - Sprite: Walking, Gathering, Crafting poses

2. **Rachel** - Energetic roommate
   - Portraits: Happy, Excited, Worried, Sleeping
   - Sprite: Various poses

3. **Ezekiel** - Curious experimenter
   - Portraits: Curious, Frustrated, Hopeful, Determined
   - Sprite: Sitting, Standing

4. **Miriam** - Anxious student
   - Portraits: Nervous, Relieved, Shy smile
   - Sprite: Sitting

5. **Thornwood** - Strict instructor
   - Portraits: Stern, Slightly softened, Thoughtful
   - Sprite: Standing, Walking

**Environments:**
1. **Cart Scene** - Sunset approach to academy (single illustration)
2. **Dorm Room** - Cozy interior with clickable objects
3. **Garden** - Beautiful twilight scene with glowing ingredients
4. **Classroom** - U-shaped desks, ingredient shelves
5. **Courtyard** - Fountain, stone tables, trees

**UI Elements:**
- Recipe cards (parchment texture)
- Journal pages (warm, readable)
- Relationship hearts
- Stat bars (progress bars with warm colors)
- Ingredient icons (17 types eventually, 5 for prototype)
- Notifications (achievement-style popups)

**Crafting Minigame:**
- Mortar & pestle (3D or high-quality 2D)
- Ingredient visuals (whole → ground → mixed)
- Vials, bottles, stoppers
- Particle effects (grinding dust, glowing liquid, sparkles)

### Audio Assets

**Music (Cozy Focus):**
1. Main Theme - Warm, nostalgic (piano, strings)
2. Garden Theme - Peaceful, ambient (woodwinds, harp)
3. Crafting Theme - Gentle, focused (soft percussion, celesta)
4. Evening Theme - Reflective, soft (acoustic guitar, ambient)
5. Choice Theme - Thoughtful, slightly tense (strings)

**Sound Effects:**
- Gathering: Gentle "plings," rustling
- Crafting: Grinding, pouring, bubbling, cork pop
- UI: Page turns, gentle clicks, notification chimes
- Ambient: Birds, wind, fountain, student chatter

**Voice (Optional):**
- Character barks (laughs, sighs, gasps)
- OR full voice acting for key scenes

### Technical Systems

**Core Gameplay:**
1. Inventory system (ingredients, potions)
2. Crafting minigame engine
3. Recipe database
4. Stat tracking
5. Affinity system
6. Choice consequence tracking

**UI Systems:**
1. Dialogue system with choices
2. Journal/stats screen
3. Map/location navigation
4. Notification system
5. Save/load

**For Prototype Only:**
- 1 recipe (Simple Healing Tonic)
- 5 ingredient types
- 4 NPCs with full implementation
- 2 locations (garden, classroom)
- 1 major choice
- 60 minutes of content

---

## Success Criteria

### Cozy Metrics (60%)
- 80%+ players say "I felt relaxed while playing"
- 75%+ players say "I care about Rachel/Ezekiel/Miriam"
- 70%+ players say "Crafting was satisfying"
- 80%+ players say "The world felt warm and inviting"

### RPG Metrics (40%)
- 75%+ players say "My choices felt meaningful"
- 70%+ players say "I understood the stats"
- 65%+ players say "I want to optimize my build"
- 80%+ players say "I want to see the consequences of my choice"

### Overall Success:
- 85%+ want to continue playing after 60 minutes
- 70%+ understand all core systems
- 60%+ can explain Ezekiel's dilemma to someone else

---

## Development Timeline Estimate

**Week 1-2: Core Systems**
- Inventory + stat tracking
- Basic UI framework
- Save/load system

**Week 3-4: Crafting Minigame**
- Mortar & pestle interaction
- Visual feedback (grinding, mixing)
- Success/quality system

**Week 5-6: Dialogue & Choices**
- Dialogue system
- Affinity tracking
- Choice consequence implementation

**Week 7-8: Art & Polish**
- Character portraits
- Environment art
- UI beautification

**Week 9-10: Sound & Playtesting**
- Music implementation
- Sound effects
- Internal playtesting & iteration

**Week 11-12: External Playtesting & Polish**
- External playtest (10-15 players)
- Iterate based on feedback
- Final polish

**Total: 12 weeks for polished 60-minute prototype**

---

## Next Steps

1. **Validate Tone** - Does 60% cozy, 40% RPG feel right in practice?
2. **Test Crafting Minigame** - Is grinding/mixing fun or tedious?
3. **Test Ezekiel Choice** - Do players care enough to feel invested?
4. **Art Style Test** - Create one character + one environment to validate visual direction
5. **Music Test** - Compose 1-2 tracks to validate audio direction

**After prototype succeeds:** Expand to full Season 1 (20+ hours)
