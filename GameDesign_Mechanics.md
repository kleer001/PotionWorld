# PotionWorld: Game Mechanics

*See also: [Overview](GameDesign_Overview.md) | [Narrative](GameDesign_Narrative.md) | [Technical](GameDesign_Technical.md)*

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

**Combat Specializations:**
- **Tactical Duelist**: +20% Combat Instinct, better potion timing in duels
- **Defensive Specialist**: +15% to defensive potion effects, resistance bonuses
- **Aggressive Brewer**: Offensive potions deal +25% damage, -10% to defensive potions
- **Counter-Alchemist**: Can identify and counter opponent's potions mid-duel

**Investigation Specializations:**
- **Forensic Analyst**: Can detect potion traces and residues, faster analysis
- **Pattern Seeker**: +15% Intuition, connects clues more easily
- **Poison Expert**: Specializes in toxins and antidotes, +20% to counter-brewing
- **Mystery Solver**: Unlocks special investigation dialogue options, reputation bonus

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
