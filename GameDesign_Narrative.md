# PotionWorld: Narrative Design

*See also: [Overview](GameDesign_Overview.md) | [Mechanics](GameDesign_Mechanics.md) | [Technical](GameDesign_Technical.md)*

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
