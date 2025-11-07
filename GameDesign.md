# PotionWorld: Game Design Document

## Game Format: Retro Text-Only RPG

PotionWorld is designed as a **text-based, command-line style RPG** in the tradition of classic interactive fiction and early CRPGs. This design choice offers several advantages:

### Text-Based Design Benefits
- **Focus on Systems**: Deep crafting and relationship mechanics without graphics overhead
- **Imagination-Driven**: Players visualize their journey, making it more personal
- **Rapid Development**: Iterate on systems and content quickly
- **Accessibility**: Runs on any platform, minimal system requirements
- **Mod-Friendly**: Easy for community to add content via text files
- **ESENS Clarity**: Notation system displayed directly without visual translation

### Interface Style
- **Menu-Driven Navigation**: Number or letter choices for actions
- **ASCII Art** (Optional): Simple ingredient/potion representations
- **Status Displays**: Text-based character sheets, inventory lists
- **Color Coding** (Terminal Colors): Different colors for elements, effects, NPCs
- **Clear Prompts**: "What would you like to do? [1] Craft [2] Talk [3] Explore [4] Rest"

### Example Gameplay Screen
```
═══════════════════════════════════════════════════════════════
POTIONWORLD - Season 1: The Apprentice - Day 15 - Morning
Location: Academy Laboratory
═══════════════════════════════════════════════════════════════

Your Stats: Knowledge: 25/100 | Precision: 18/100 | Gold: 150
Active Quest: Master the Healing Potion for tomorrow's exam

You stand at your workbench. Instructor Thornwood watches nearby.
Your mortar and pestle are ready. The recipe book lies open.

What would you like to do?
[1] Craft a potion
[2] Talk to Instructor Thornwood (Affinity: +1)
[3] Review recipe book
[4] Check inventory
[5] Leave laboratory

> _
```

### Technical Implementation
- **Python-Based**: Leverages existing ESENS_Parser.py and ESENS_cli.py
- **Save Files**: JSON-based character/world state
- **Modular Design**: Easy to extend with new content
- **Cross-Platform**: Works on Windows, Mac, Linux terminals

## Table of Contents
1. [Core Pillars](#core-pillars)
2. [Character Systems](#character-systems)
3. [Inventory Systems](#inventory-systems)
4. [Crafting Systems](#crafting-systems)
5. [Combat & Dueling](#combat--dueling)
6. [Economy & Trading](#economy--trading)
7. [Progression Systems](#progression-systems)
8. [NPC Relationship Systems](#npc-relationship-systems)
9. [World & Environment](#world--environment)
10. [Quest & Event Systems](#quest--event-systems)

---

## Core Pillars

### 1. **Meaningful Crafting**
Every potion created has purpose and impact. The ESENS notation system provides depth while maintaining clarity. Crafting is not just about combining ingredients—it's about understanding effects, timing, and consequences.

### 2. **Reactive World**
The world responds to player choices. NPCs remember actions, relationships evolve naturally, and moral decisions create visible ripples across seasons.

### 3. **Life Journey**
The game follows a complete life arc from teenager to elder. Each season introduces age-appropriate challenges, relationships, and growth opportunities.

### 4. **Ethical Alchemy**
Potion-making involves moral dimensions: ingredient sourcing, pricing decisions, knowledge sharing, and the responsibility of wielding alchemical power.

---

## Character Systems

### Player Character (PC)

#### Core Attributes
The player character has six primary attributes that develop across seasons:

1. **Alchemical Knowledge** (0-100)
   - Unlocks recipe complexity
   - Affects success rates for difficult potions
   - Gained through lessons, experimentation, and research

2. **Precision** (0-100)
   - Reduces crafting failure chance
   - Improves potion quality
   - Gained through practice and focus training

3. **Intuition** (0-100)
   - Enables ingredient substitutions
   - Reveals hidden properties
   - Gained through experimentation and mentor teachings

4. **Reputation** (0-100)
   - Affects pricing, opportunities, and NPC reactions
   - Separate reputation tracks per region/faction
   - Gained through actions and choices

5. **Business Acumen** (0-100)
   - Improves shop profits and negotiations
   - Unlocks advanced shop features
   - Relevant primarily in Seasons 2 and 5

6. **Combat Instinct** (0-100)
   - Affects dueling performance
   - Enables tactical potion timing
   - Relevant primarily in Season 3

#### Character Progression

**Season 1 (Apprentice, Ages 14-18)**
- Focus: Alchemical Knowledge, Precision
- Stats grow through lessons and practice
- No business or combat stats yet
- Foundation for future specialization

**Season 2 (Inheritor, Ages 19-24)**
- All six stats now active
- Business Acumen becomes important
- Player can begin specializing
- Reputation splits into Village/Regional tracks

**Season 3 (Competitor, Ages 25-30)**
- Combat Instinct emphasized
- Reputation expands to include Dueling Circuit
- All stats actively used
- Specialization becomes more pronounced

**Season 4 (Investigator, Ages 31-40)**
- Intuition and Knowledge peak importance
- Political reputation track added
- Master-level stat thresholds available
- Cross-season synergies unlock

**Season 5 (Master, Ages 41+)**
- All stats can reach maximum
- Legacy system unlocks unique abilities
- Mentor stats (teaching effectiveness) introduced
- Cumulative bonuses from previous seasons

#### Skills & Specializations

Players can develop specializations that provide bonuses:

**Crafting Specializations:**
- **Perfectionist**: +20% to Precision, +10% potion quality
- **Innovator**: Can substitute similar ingredients, +15% to Intuition
- **Speed Brewer**: Craft potions 25% faster, -5% to Precision
- **Mass Producer**: Create multiple potions per craft, -10% quality

**Social Specializations:**
- **Diplomat**: +15 to all NPC affinity gains
- **Merchant**: +20% profit margins, better deals
- **Teacher**: Apprentices learn faster, +Knowledge gain when teaching
- **Competitor**: +15 Combat Instinct, intimidation options

**Research Specializations:**
- **Analyst**: Can reverse-engineer potions faster
- **Ethicist**: Moral choices provide extra reputation
- **Experimentalist**: Failures provide useful data
- **Historian**: Access to ancient recipes and lore

Players choose one specialization per season (total of 5 by endgame), creating unique builds.

#### Character Customization

**Appearance:**
- Gender, appearance, and name selection
- Character ages visually across seasons
- Optional customization of shop/workspace

**Background Choices:**
- Starting background affects initial relationships and opportunities
- Options: Urban merchant family, Rural healer lineage, Noble house, Street orphan, Traveling trader heritage

**Personality Expression:**
- Dialogue choices shape player character's voice
- Consistent choices unlock unique dialogue options
- NPCs remember and comment on personality consistency

---

## Inventory Systems

### Inventory Types

#### 1. **Ingredient Inventory**
Stores raw materials for potion crafting.

**Capacity System:**
- **Season 1**: Basic satchel (50 slots)
- **Season 2**: Expanded storage (100 slots) + shop storage (200 slots)
- **Season 3**: Traveling case (75 slots) + tournament locker (150 slots)
- **Season 4**: Royal provisions (100 slots) + research archive (300 slots)
- **Season 5**: Master vault (unlimited)

**Organization:**
- Sort by: Type, Rarity, Season Acquired, Alphabetical
- Filter by: Element affinity, Freshness, Source
- Search function
- Favorite/Pin system for frequently used ingredients

**Storage Mechanics:**
- Some ingredients degrade over time (freshness system)
- Preserved ingredients last longer but cost more
- Proper storage (containers, temperature) affects quality
- Rare ingredients can be displayed in shop for prestige

#### 2. **Potion Inventory**
Stores completed potions.

**Capacity System:**
- **Season 1**: Student locker (20 potions)
- **Season 2**: Shop shelving (50 potions) + personal case (20 potions)
- **Season 3**: Combat belt (10 quick-access) + storage (40 potions)
- **Season 4**: Investigation kit (30 potions) + court supplies (50 potions)
- **Season 5**: Master collection (100 display + unlimited storage)

**Potion Attributes:**
- Quality (Poor, Standard, Fine, Exceptional, Masterwork)
- Potency (affects magnitude of effects)
- Stability (determines shelf life)
- Batch number and creation date
- Creator signature (matters for trading)

**Organization:**
- Sort by: Effect type, Quality, Creation date, Value
- Filter by: Element, Target, Duration
- Quick-access hotbar for dueling
- Recipe linking (click potion to see recipe)

#### 3. **Equipment Inventory**
Stores tools, containers, and special items.

**Tool Types:**
- **Mortar & Pestle**: Affects grinding precision
- **Alembic**: For distillation potions
- **Cauldron**: Affects batch size and heat control
- **Vials & Bottles**: Different sizes and qualities
- **Preservation Containers**: For ingredient storage
- **Travel Equipment**: Affects gathering efficiency

**Quality Tiers:**
- Student Grade (Season 1)
- Professional Grade (Season 2+)
- Master Crafted (Season 4+)
- Legendary (Season 5 or special quests)

**Tool Degradation:**
- Tools wear with use
- Can be maintained or upgraded
- Broken tools reduce crafting effectiveness
- Special tools have unique properties

#### 4. **Recipe Book**
Not traditional inventory but crucial to gameplay.

**Recipe Organization:**
- Learned recipes (can craft)
- Discovered recipes (have seen but need practice)
- Fragment recipes (incomplete)
- Mastered recipes (higher success rate, can innovate)

**Recipe Sources:**
- Lessons and tutorials
- NPC teachings
- Experimentation discoveries
- Purchased from merchants
- Found in ancient texts
- Inherited from family
- Rewarded from quests

**Recipe Information:**
- ESENS notation
- Ingredient list with quantities
- Difficulty rating
- Success requirements (stat minimums)
- Effect description
- Historical notes and lore
- Personal notes (player can add)

---

## Crafting Systems

### ESENS-Based Crafting

#### Core Crafting Loop

1. **Recipe Selection**
   - Choose from known recipes or experiment
   - Review requirements and effects
   - Check ingredient availability

2. **Ingredient Preparation**
   - Gather required ingredients
   - Prepare ingredients (grind, distill, etc.)
   - Preparation quality affects final result

3. **Brewing Process**
   - Follow ESENS notation sequence
   - Mini-games for critical steps (timing, temperature)
   - Precision checks at key moments

4. **Result & Quality Determination**
   - Success/failure based on stats and dice roll
   - Quality tier determined by precision
   - Potency affected by ingredient quality
   - Unexpected properties from critical success

5. **Learning & Improvement**
   - Experience gained toward mastery
   - Failed attempts provide partial knowledge
   - Notes added to recipe book

#### Ingredient Properties

**17 Ingredient Types:**
1. **Roots** - Grounding, stability effects
2. **Mushrooms** - Transformation, growth effects
3. **Berries** - Energy, vitality effects
4. **Crystals** - Amplification, focus effects
5. **Tree Sap** - Binding, duration effects
6. **Seeds** - Potential, delayed effects
7. **Minerals** - Strength, defense effects
8. **Insect Parts** - Speed, precision effects
9. **Oils** - Smooth application, absorption
10. **Spores** - Spread, area effects
11. **Feathers** - Lightness, flight effects
12. **Honey** - Preservation, sweetness effects
13. **Fish Scales** - Adaptability, water effects
14. **Bones** - Structure, permanence effects
15. **Flowers** - Beauty, attraction effects
16. **Lichen** - Resilience, slow effects
17. **Exotic Fruits** - Power, rare effects

**Ingredient Rarity:**
- **Common**: Found easily, cheap
- **Uncommon**: Requires some searching, moderate price
- **Rare**: Specific locations, expensive
- **Very Rare**: Difficult to obtain, very expensive
- **Legendary**: Quest rewards, extremely valuable

**Ingredient Quality:**
- **Poor**: -10% potency
- **Standard**: Normal effects
- **Fine**: +10% potency
- **Exceptional**: +25% potency, possible bonus effect
- **Perfect**: +50% potency, guaranteed bonus effect

#### Crafting Difficulty & Success

**Difficulty Ratings:**
- **Trivial** (0-10): Auto-success for anyone
- **Easy** (11-25): Apprentice level
- **Moderate** (26-50): Journeyman level
- **Hard** (51-75): Expert level
- **Very Hard** (76-90): Master level
- **Legendary** (91-100): Requires mastery + perfect conditions

**Success Calculation:**
```
Success Chance = Base Chance (50%)
                + (Relevant Stat / 2)
                + (Tool Quality Bonus)
                + (Preparation Bonus)
                + (Specialization Bonus)
                - Difficulty
                + (d20 roll - 10)
```

**Critical Success (Natural 20 or >150% required):**
- Higher quality tier
- Bonus effect added
- No ingredient waste
- Double experience
- Chance to innovate (create variant)

**Critical Failure (Natural 1 or <25% required):**
- All ingredients lost
- Possible equipment damage
- Potential harmful vapor effect
- Negative reputation in competitive settings

#### Experimentation System

**Free Experimentation:**
- Combine any ingredients without recipe
- ESENS notation generated based on properties
- Higher failure rate but discovery potential
- Records results for future reference

**Guided Experimentation:**
- Use known recipe as base, modify one ingredient
- Lower risk than free experimentation
- Creates recipe variants
- Builds Intuition skill

**Innovation Unlocks:**
- At Knowledge 50+: Can create simple variants
- At Knowledge 75+: Can combine recipe concepts
- At Knowledge 90+: Can create entirely new potions
- Master level: Can push ESENS boundaries

#### Batch Crafting (Season 2+)

Once a recipe is mastered:
- Can craft multiple potions in one session
- Quality consistency based on Precision
- Batch size limited by cauldron and time
- Useful for shop stock or tournament prep

#### Teaching Crafting (Season 5)

- Create training potions with failsafes
- Pass knowledge to apprentices
- Apprentice success affects your reputation
- Legacy recipes passed to future generation

---

## Combat & Dueling

### Combat Philosophy
Combat in PotionWorld is strategic and turn-based, emphasizing preparation, timing, and potion synergies rather than reflexes.

### Duel Structure (Season 3 Primary)

#### Pre-Duel Phase
**Potion Selection** (2 minutes)
- Choose up to 10 potions from inventory
- Arrange in quick-access belt
- Review opponent information (if available)
- Set initial strategy

**Opponent Analysis:**
- Known fighting style
- Previous duel recordings
- Personality traits affect tactics
- Elemental preferences

#### Combat Flow

**Turn Structure:**
1. Initiative roll (modified by Combat Instinct + Initiative potions)
2. Action phase (each combatant)
3. Trigger resolution (^S start-of-turn effects)
4. Status effect updates
5. Turn end (vE end-of-turn effects)

**Action Types:**
- **Use Potion**: Drink or throw a potion
- **Observe**: Analyze opponent's status (reveals buffs/debuffs)
- **Guard**: Reduce incoming damage, +Defense this turn
- **Provoke**: Taunt opponent, affects AI behavior
- **Wait**: Delay action to later in turn (tactical timing)

**Combat Stats:**
- **Health** (100 base, modified by potions)
- **Strength** (Attack power)
- **Defense** (Damage reduction)
- **Initiative** (Turn order)
- **Resistance** (Status effect resistance)

#### ESENS in Combat

**Combat-Focused Notations:**
- `P+S30%3T>A.F` - Fire strength boost when attacking
- `E-D20%2T<D` - Weaken enemy defense when they attack you
- `P!D1T.RN` - Invulnerability that can't be removed
- `E#Stun1T` - Stun opponent for a turn
- `P+I50%C` - Initiative boost for entire combat

**Trigger Combinations:**
- Drink potion that activates `>A` (on attack)
- Attack triggers the effect
- Effect may have chaining `>Sprd` (spreads to you or others)
- Stack multiple triggers for combo chains

**Strategic Depth:**
- **Buff Stacking**: Multiple strength potions with `.ST` flag
- **Debuff Pressure**: Layer weakening effects on opponent
- **Timing Games**: Wait for opponent's buffs to expire
- **Removal Wars**: Use cleansing potions vs. non-removable effects
- **Resource Drain**: Effects with `$HP` or `$MP` resource costs

#### Duel Victory Conditions
- **Health Depletion**: Reduce opponent to 0 HP (most common)
- **Forfeit**: Opponent surrenders
- **Timeout**: Higher HP/better state at time limit wins
- **Incapacitation**: Opponent stunned/unable to act for 3 turns
- **Judge Decision**: Rare, based on style and creativity

#### Post-Duel
- Rewards based on performance
- Reputation changes
- Opponent relationship shifts
- Unlocks next tier opponents
- Spectators may offer sponsorships or challenges

### Combat AI Personality System

NPCs fight according to their Big 5 traits:

**High Openness:**
- Uses experimental/unusual potions
- Tries creative combos
- Adapts strategy mid-fight

**High Conscientiousness:**
- Follows proven strategies
- Precise timing
- Conservative, methodical

**High Extraversion:**
- Aggressive, flashy moves
- Provokes frequently
- Risk-taking behavior

**High Agreeableness:**
- Defensive, counter-focused
- Avoids excessive damage
- May show mercy/hesitate

**High Neuroticism:**
- Panic when low on health
- Overuses defensive potions
- Makes mistakes under pressure

### Combat Outside Season 3

**Season 1**: Tutorial duels only, low stakes
**Season 2**: Occasional defense scenarios (protect shop)
**Season 4**: Rare combat, more about countering effects
**Season 5**: Optional, reputation-based challenges

---

## Economy & Trading

### Currency System
- **Gold Coins**: Primary currency
- Prices scale with season and region
- Inflation system (gold becomes less valuable over time)
- Reputation affects prices (±20%)

### Pricing Philosophy

**Ingredient Costs:**
- **Common**: 5-20 gold
- **Uncommon**: 25-75 gold
- **Rare**: 100-300 gold
- **Very Rare**: 400-1000 gold
- **Legendary**: 1500+ gold or quest-only

**Potion Pricing Factors:**
- Ingredient cost (base)
- Difficulty multiplier (×1.5 to ×3)
- Quality tier bonus (+25% to +100%)
- Reputation modifier
- Supply and demand

**Dynamic Pricing (Season 2+):**
- Village needs affect demand
- Seasonal availability affects ingredient prices
- Competitor actions affect market
- Your own pricing affects reputation

### Shop Management (Season 2)

**Shop Features:**
- **Display Shelves**: Showcase potions and rare ingredients
- **Workshop Area**: Craft during shop hours
- **Storage Room**: Expanded inventory
- **Reputation Board**: Customer reviews and requests
- **Ledger**: Track income, expenses, profit

**Customer System:**
- **Walk-ins**: Random customers with random needs
- **Regulars**: Return customers with building relationships
- **Special Orders**: Custom requests with deadlines
- **Emergency Cases**: High payment, time pressure, moral choices

**Shop Upgrades:**
- Better equipment (faster crafting)
- Larger storage
- Advertising (more customers)
- Security (prevent theft)
- Aesthetics (reputation bonus)

**Ethical Pricing Dilemmas:**
- Charge poor villagers full price (profit) vs. discount (reputation + affinity)
- Exploit plague for profit vs. help community (reputation hit/gain)
- Sell dangerous potions for high price vs. refuse (moral choice)

### Trading & Merchants

**Merchant Types:**
- **General Merchants**: Common ingredients, standard prices
- **Specialty Suppliers**: Rare ingredients, high prices
- **Black Market**: Illegal/unethical ingredients, no questions
- **Guild Traders**: Members-only, better prices
- **Traveling Caravans**: Random inventory, fair prices

**Barter System:**
- Trade potions for ingredients
- Trade services for supplies
- Reputation affects barter rates
- Some NPCs prefer barter to gold

**Auction House (Season 3+):**
- Bid on rare ingredients
- Sell exceptional potions
- Competitive with other alchemists
- Market trends and speculation

### Income Sources by Season

**Season 1**: Allowance, small rewards, tournament prizes
**Season 2**: Shop profits, special orders, healing services
**Season 3**: Tournament winnings, sponsorships, dueling fees
**Season 4**: Investigation fees, royal stipend, consultation
**Season 5**: Business empire, apprentice fees, legacy sales

---

## Progression Systems

### Experience & Learning

**Knowledge Gain:**
- Completing lessons: 50-200 XP
- Crafting potions: 10-100 XP (based on difficulty)
- Failed attempts: 5 XP (consolation learning)
- Experimentation: 25-150 XP
- Teaching others: 30 XP per lesson
- Discoveries: 100-500 XP

**Skill Improvement:**
- Stats increase through use
- Precision improves by crafting (1-3 points per craft)
- Intuition improves by experimentation (2-5 points per attempt)
- Combat Instinct improves by dueling (5-10 points per duel)
- Business Acumen improves by transactions (1 point per sale)

**Mastery Levels:**
Each recipe has a mastery level (0-100):
- **0-20**: Novice (base success rate)
- **21-40**: Competent (+10% success, -10% ingredient waste)
- **41-60**: Proficient (+20% success, +10% quality)
- **61-80**: Expert (+30% success, +20% quality, can teach)
- **81-100**: Master (+40% success, +30% quality, can innovate)

### Reputation System

**Reputation Tracks:**
- **Academy Reputation** (Season 1): Affects instructor treatment, scholarships
- **Village Reputation** (Season 2): Affects prices, special orders, community help
- **Dueling Reputation** (Season 3): Affects sponsorships, opponent quality, prizes
- **Royal Reputation** (Season 4): Affects access to court, political influence
- **Master Reputation** (Season 5): Affects apprentice quality, legacy impact

**Reputation Scale (0-100 per track):**
- **0-20**: Unknown
- **21-40**: Known
- **41-60**: Respected
- **61-80**: Renowned
- **81-100**: Legendary

**Reputation Effects:**
- Unlocks quests and opportunities
- Affects NPC initial affinity
- Modifies prices and services
- Enables certain endings
- Determines legacy impact

### Achievement System

**Categories:**
- **Crafting Achievements**: Create X potions, master recipes
- **Collection Achievements**: Gather all ingredient types, rare finds
- **Social Achievements**: Max affinity with NPCs, specific relationship outcomes
- **Combat Achievements**: Win duels, perfect victories, creative combos
- **Story Achievements**: Complete seasons, moral choice paths
- **Challenge Achievements**: Speedruns, self-imposed limitations

**Rewards:**
- Titles (displayed in UI)
- Cosmetic customizations
- Bonus starting gold for New Game+
- Unlockable content (recipes, characters)

### Season Transitions

**End-of-Season Summary:**
- Stats achieved
- Relationships formed
- Major choices made
- Potions mastered
- Reputation earned

**Transition Cutscenes:**
- Time-lapse showing character aging
- Major world changes
- Letters and updates from NPCs
- Preview of next season's challenges

**Carry-Forward:**
- All stats and skills
- Inventory (with some losses/gains)
- Relationships (with some shifts)
- Reputation (with evolution)
- Major choice consequences

---

## NPC Relationship Systems

### The Big 5 Personality System

Each NPC has five personality traits rated -1, 0, or +1:

#### Openness (O)
- **+1 (High)**: Loves innovation, experimentation, new ideas
- **0 (Moderate)**: Balanced, case-by-case
- **-1 (Low)**: Prefers tradition, established methods

#### Conscientiousness (C)
- **+1 (High)**: Organized, rule-following, meticulous
- **0 (Moderate)**: Reasonably reliable
- **-1 (Low)**: Spontaneous, flexible, rule-bending

#### Extraversion (E)
- **+1 (High)**: Outgoing, energetic, social
- **0 (Moderate)**: Adaptable socially
- **-1 (Low)**: Reserved, reflective, quiet

#### Agreeableness (A)
- **+1 (High)**: Cooperative, compassionate, kind
- **0 (Moderate)**: Diplomatic
- **-1 (Low)**: Competitive, challenging, skeptical

#### Neuroticism (N)
- **+1 (High)**: Emotionally reactive, worried
- **0 (Moderate)**: Generally stable
- **-1 (Low)**: Calm, resilient

### Affinity System

**Affinity Scale (-5 to +5):**
- **+5**: Devoted - Will make sacrifices for you
- **+4**: Loyal - Actively supports you
- **+3**: Friendly - Helps willingly, offers discounts
- **+2**: Warm - Positive interactions
- **+1**: Positive - Slightly favorable
- **0**: Neutral - Professional, transactional
- **-1**: Cool - Mild dislike
- **-2**: Unfriendly - Reluctant service, price increases
- **-3**: Hostile - May refuse service
- **-4**: Antagonistic - Works against you indirectly
- **-5**: Nemesis - Active sabotage

**Affinity Mechanics:**

1. **Affinity Decay (Regression to Neutral)**
   - Every in-game week: Affinity moves 0.5 toward 0
   - Requires relationship maintenance
   - Memories can resist decay for specific events

2. **Action-Based Affinity Changes**

   Example reactions to player actions:
   ```
   InnovativePotion: O(+1.0), E(+0.5), N(-0.5)
   TraditionalPotion: O(-0.5), C(+0.5), N(+0.5)
   GiftGiving: E(+1.0), A(+0.5)
   Haggling: C(-0.5), A(-1.0), E(+0.5)
   MissedDeadline: C(-1.0), N(+0.5)
   ShareKnowledge: O(+0.5), A(+0.5), C(-0.3)
   ChargeHighPrices: A(-1.0), C(+0.3)
   ```

3. **Threshold Events**
   - Crossing certain affinity levels triggers special scenes
   - Examples:
     - 0 → +1: NPC shares personal story
     - +2 → +3: NPC offers special ingredient/recipe
     - +4 → +5: NPC becomes mentor/partner
     - 0 → -1: NPC becomes noticeably cooler
     - -2 → -3: NPC warns others about you
     - -4 → -5: NPC becomes active antagonist

4. **Memory System**
   - NPCs remember significant positive/negative events
   - Memories referenced in dialogue
   - Certain memories resist decay
   - Examples:
     - "I still remember how you helped during the plague"
     - "I haven't forgotten how you stole my research"
     - "Thanks again for that perfect healing potion"

### Key NPCs (Examples)

#### Season 1: Instructor Thornwood
```
Personality: O(-1), C(+1), E(0), A(-1), N(0)
Role: Primary academy instructor
Initial Affinity: 0

Preferences:
- Following recipes precisely: +0.5
- Experimentation: -0.5
- Late submissions: -1.0
- Helping other students: +0.3

Arc: Can become mentor figure if affinity reaches +4
```

#### Season 2: Healer Wisteria
```
Personality: O(0), C(+1), E(-1), A(+1), N(-1)
Role: Village healer and elder
Initial Affinity: +1

Preferences:
- Sharing family recipes: +1.0
- Charging high prices: -0.7
- Healing poor for free: +0.5
- Using rare ingredients: +0.2

Arc: Can pass on advanced healing techniques at +5
```

#### Season 3: Duelist Kael Emberforge
```
Personality: O(+1), C(0), E(+1), A(-1), N(0)
Role: Rival duelist and eventual ally/nemesis
Initial Affinity: -1

Preferences:
- Creative combat tactics: +1.0
- Honorable defeats: +0.5
- Dirty tactics: -1.5
- Trash talking: +0.3 (appreciates the competition)

Arc: Can become best friend (+5) or eternal rival (-5)
```

### Dialogue System Integration

**Node-Based Dialogue:**
- Dialogue nodes check affinity and personality
- Multiple response variants based on relationship state
- Personality affects NPC's phrasing and word choice

**Example Structure:**
```
[Node: Request_Help]
Check: AffinityThreshold

IF Affinity >= 3:
  "Of course! I'd be happy to help you with that."

ELIF Affinity >= 0:
  "I suppose I could help. What do you need?"

ELIF Affinity < 0:
  "Why should I help you after what you did?"

APPLY: Personality modifiers (E affects enthusiasm, A affects warmth)
```

**Personality-Based Dialogue Decorators:**
- High O: Uses creative, abstract language
- Low O: Uses traditional, concrete language
- High C: Precise, structured sentences
- Low C: Casual, loose phrasing
- High E: Enthusiastic, energetic tone
- Low E: Reserved, measured tone
- High A: Warm, supportive language
- Low A: Challenging, direct language
- High N: Worried, cautious expressions
- Low N: Confident, calm language

---

## World & Environment

### Season-Based Regions

#### Season 1: Royal Academy of Alchemical Arts
- **Setting**: Prestigious institution in capital city
- **Locations**:
  - Classrooms and laboratories
  - Library and archive
  - Student dormitories
  - Ingredient garden
  - Practice dueling grounds
  - Tournament arena
- **Atmosphere**: Structured, competitive, scholarly
- **NPCs**: 10-12 (instructors, students, staff)

#### Season 2: Grandmother's Village Shop
- **Setting**: Small rural village, close-knit community
- **Locations**:
  - Your shop and living quarters
  - Village square and market
  - Healer's hut
  - Forest gathering areas
  - Crystal caves
  - River and waterfall
- **Atmosphere**: Cozy, personal, community-focused
- **NPCs**: 8-10 (villagers, customers, competitors)

#### Season 3: Professional Dueling Circuit
- **Setting**: Various cities hosting tournaments
- **Locations**:
  - Grand arenas (3-4 major cities)
  - Training facilities
  - Sponsor lounges
  - Alchemist guild halls
  - Underground betting dens
  - Champion's quarters
- **Atmosphere**: Competitive, flashy, high-stakes
- **NPCs**: 12-15 (duelists, sponsors, fans, officials)

#### Season 4: Royal Court & Investigation Sites
- **Setting**: Capital city and surrounding regions
- **Locations**:
  - Royal palace
  - Noble estates
  - Investigation labs
  - Black market districts
  - Quarantine zones
  - Ancient ruins
- **Atmosphere**: Political, mysterious, consequential
- **NPCs**: 10-12 (nobles, officials, conspirators, victims)

#### Season 5: Your Established Enterprise
- **Setting**: Major city or returned to village (player choice)
- **Locations**:
  - Your business headquarters
  - Multiple shop locations
  - Research facilities
  - Apprentice training grounds
  - Legacy monument
  - World crisis zones
- **Atmosphere**: Reflective, legacy-focused, urgent (end crisis)
- **NPCs**: Mix of old and new (15-20 total)

### Time System

**Calendar:**
- 12 months per year
- 4 weeks per month
- 7 days per week
- Seasons advance at story milestones, not real-time

**Day Cycle:**
- Morning: Crafting, learning, social
- Afternoon: Activities, quests, travel
- Evening: Social, planning, rest
- Night: Special events, secret activities

**Time Passage:**
- In-season: Days and weeks progress
- Between seasons: Years pass in transition
- Time management becomes part of Season 2+ gameplay

**Seasonal Events:**
- Academy Tournament (Season 1 climax)
- Harvest Festival (Season 2 recurring)
- Championship Duel (Season 3 climax)
- Royal Gala (Season 4 event)
- Master's Symposium (Season 5 event)

### World State & Reactivity

**Persistent Changes:**
- Shops you affect stay affected
- NPCs remember and reference past events
- World crisis elements build across seasons
- Your choices create visible consequences

**Examples of Reactivity:**
- Save village in Season 2 → Villagers prosperous in Season 5
- Expose corruption in Season 3 → Cleaner dueling scene in Season 4
- Hoard knowledge in Season 4 → Fewer innovations appear
- Mentor well in Season 5 → Apprentices spread your techniques

---

## Quest & Event Systems

### Quest Types

#### 1. **Main Story Quests**
- Progress the narrative
- Unlock new seasons
- Major moral choices
- Cannot be failed (only delayed)
- Examples: Academy lessons, Plague response, Championship qualification

#### 2. **Character Quests**
- NPC-specific storylines
- Build relationships
- Unlock special rewards (recipes, items)
- Can be missed if affinity too low
- Examples: Help Wisteria with rare disease, Support Kael's family, Expose corrupt official

#### 3. **Reputation Quests**
- Build standing in region/faction
- Unlock tiers of access
- Often have moral dimensions
- Examples: Prove worth to guild, Impress royal court, Win over village

#### 4. **Crafting Challenges**
- Create specific potions under constraints
- Teach crafting mechanics
- Reward rare recipes or ingredients
- Examples: Create healing potion without common ingredients, Brew combat potion in limited time

#### 5. **Investigation Quests** (Season 4 primary)
- Solve mysteries through alchemy
- Analyze substances
- Create counter-potions
- Examples: Identify poison, Reverse-engineer mind control potion

#### 6. **Collection Quests**
- Gather specific ingredients
- Explore world
- Teach gathering mechanics
- Examples: Find all 17 ingredient types, Collect perfect-quality herbs

### Event System

**Random Events:**
- Ingredient gathering encounters
- Customer emergencies
- Traveling merchant visits
- NPC relationship moments
- Ethical dilemmas

**Scheduled Events:**
- Seasonal festivals
- Tournament brackets
- Royal court sessions
- Guild meetings
- Market days

**Triggered Events:**
- Affinity threshold crossings
- Reputation milestones
- Story progression points
- Moral choice consequences
- World state changes

### Moral Choice Framework

**Choice Categories:**

1. **Profit vs. Ethics**
   - Charge sick villager vs. help for free
   - Sell dangerous potions vs. refuse
   - Exploit shortage vs. fair pricing

2. **Tradition vs. Innovation**
   - Follow family recipes vs. experiment
   - Respect guild rules vs. break boundaries
   - Honor teacher's method vs. find own way

3. **Competition vs. Cooperation**
   - Hoard knowledge vs. share freely
   - Sabotage rivals vs. honorable competition
   - Protect secrets vs. advance field

4. **Caution vs. Ambition**
   - Play it safe vs. take risks
   - Obey authority vs. pursue truth
   - Accept limits vs. push boundaries

**Choice Consequences:**
- Immediate: Affinity changes, rewards/penalties
- Medium-term: Reputation shifts, opportunity unlocks
- Long-term: World state changes, ending variations
- Legacy: How you're remembered in Season 5

**Tracking:**
- "Potion Book of Life" records major choices
- NPCs reference past decisions
- World state reflects cumulative impact
- Multiple endings based on choice patterns

---

## UI/UX Design Philosophy

### Core Principles

1. **Clarity First**: ESENS notation visible but explained
2. **Contextual Help**: Tutorials available when needed
3. **Efficient Navigation**: Quick access to common functions
4. **Visual Feedback**: Clear indication of success, failure, changes
5. **Accessibility**: Colorblind modes, text scaling, remappable controls

### Key UI Screens

**Main HUD:**
- Health/status indicators (in combat)
- Current season and date
- Active quest tracker
- Quick-access inventory (hotbar)
- Affinity indicators for nearby NPCs

**Crafting Screen:**
- Recipe view (ESENS notation + description)
- Ingredient slots with drag-and-drop
- Tools and equipment status
- Success chance indicator
- Quality potential display

**Inventory Screen:**
- Tabbed organization (Ingredients, Potions, Equipment, Recipes)
- Sort and filter options
- Quick-craft from recipe book
- Item detail pop-ups with lore

**Dialogue Screen:**
- Character portrait with expression
- Affinity indicator (heart/star system)
- Personality hints (subtle icons)
- Dialogue history scroll
- Choice preview (shows potential reactions)

**Shop Management Screen (Season 2):**
- Display shelves (what customers see)
- Storage management
- Customer list with preferences
- Ledger and finances
- Shop upgrade options

---

## Accessibility & Quality of Life

### Accessibility Features
- Text size adjustment (80% to 150%)
- Colorblind modes (Deuteranopia, Protanopia, Tritanopia)
- High contrast mode
- Screen reader support for UI elements
- Remappable controls
- Auto-save and multiple save slots

### Quality of Life Features
- Fast travel (Season 2+)
- Batch crafting for mastered recipes
- Ingredient highlighting in world
- Recipe favoriting
- Quest markers and waypoints
- Skip dialogue option (for replays)
- Comprehensive glossary and help system
- Tutorial replay option
- New Game+ with bonuses

---

## Conclusion

PotionWorld combines deep systems with meaningful narrative to create a unique life-journey RPG. The ESENS notation system provides rich crafting depth, while the Big 5 personality and affinity systems create believable, reactive relationships.

**Design Priorities:**
1. Make crafting satisfying and strategic
2. Ensure every NPC feels distinct and memorable
3. Give players meaningful choices with visible consequences
4. Balance complexity with accessibility
5. Create a world that reacts to and remembers player actions

**Success Metrics:**
- Players engage with crafting experimentation
- Players form emotional connections with NPCs
- Players replay to explore different moral paths
- Players feel their choices matter
- Players complete the full life journey (all 5 seasons)

The interconnected systems create emergent gameplay where potion knowledge, social skills, and ethical choices all matter equally to success and satisfaction.
