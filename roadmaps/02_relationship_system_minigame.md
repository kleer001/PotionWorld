# Medium Roadmap: Character/NPC Relationship System Text-Based Minigame

## Overview
Create a standalone text-based minigame that implements the Big 5 personality system, affinity tracking, and memory-based NPC interactions. This prototype will validate relationship mechanics, affinity decay, and personality-driven responses before full Godot implementation.

## Core Features to Implement

### Phase 1: Basic Personality & Affinity (Week 1-2)

#### 1.1 Big 5 Personality System
- **NPC personality profiles**
  - Five traits: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
  - Each trait: -1 (Low), 0 (Moderate), +1 (High)
  - JSON storage for NPC definitions

- **Personality display**
  - Clear visualization of NPC traits
  - Personality descriptions (e.g., "Traditional, Meticulous, Reserved")
  - Icons or symbols for quick recognition

- **Starter NPCs (5-8 characters)**
  - Instructor Thornwood (O:-1, C:+1, E:0, A:-1, N:0)
  - Healer Wisteria (O:0, C:+1, E:-1, A:+1, N:-1)
  - Student Mira (O:+1, C:0, E:+1, A:+1, N:0)
  - Rival Kael (O:+1, C:0, E:+1, A:-1, N:0)
  - Merchant Aldric (O:0, C:-1, E:+1, A:0, N:0)

#### 1.2 Affinity System
- **Affinity tracking (-5 to +5)**
  - Current affinity value per NPC
  - Visual representation (hearts, bars, text)
  - Affinity level labels (Devoted, Friendly, Neutral, Hostile, etc.)

- **Initial affinity**
  - Different starting values per NPC
  - Based on background or intro circumstances
  - Most NPCs start at 0 (Neutral)

- **Affinity change mechanics**
  - Actions trigger personality-based reactions
  - Calculate affinity delta based on Big 5 profile
  - Clear feedback showing affinity change (+0.5, -1.0, etc.)

#### 1.3 Basic Interaction System
- **Action menu**
  - List of possible actions with NPCs
  - Actions have personality impact profiles
  - Examples:
    - Show innovative potion
    - Follow traditional method
    - Give gift
    - Haggle on price
    - Share knowledge
    - Ask for help

- **Action-to-personality mapping**
  ```python
  actions = {
      "InnovativePotion": {"O": +1.0, "E": +0.5, "N": -0.5},
      "TraditionalPotion": {"O": -0.5, "C": +0.5, "N": +0.5},
      "GiftGiving": {"E": +1.0, "A": +0.5},
      "Haggling": {"C": -0.5, "A": -1.0, "E": +0.5},
      "MissDeadline": {"C": -1.0, "N": +0.5},
      "ShareKnowledge": {"O": +0.5, "A": +0.5, "C": -0.3},
  }
  ```

- **Response generation**
  - NPCs respond based on current affinity level
  - Personality affects tone and word choice
  - Clear indication of how NPC feels about action

### Phase 2: Affinity Decay & Memory (Week 3)

#### 2.1 Time System
- **In-game calendar**
  - Track days and weeks
  - Simple time advance mechanic
  - Display current date

- **Time progression**
  - Manual time advance ("Pass time" command)
  - Or automatic with each action batch
  - Week boundaries trigger decay

#### 2.2 Affinity Decay (Regression to Neutrality)
- **Decay mechanics**
  - Every week: affinity moves 0.5 toward 0
  - Example: +3 → +2.5 → +2.0 → +1.5...
  - Requires relationship maintenance

- **Decay visualization**
  - Show decay warnings ("Relationship fading")
  - Display time since last interaction
  - Suggest maintenance actions

- **Relationship maintenance**
  - Regular interactions prevent decay
  - Memories can slow/prevent decay
  - High-affinity relationships decay slower

#### 2.3 Memory System
- **Memory creation**
  - Significant events create memories
  - Threshold: Affinity change >= 1.0 (positive or negative)
  - Maximum memories per NPC (5-10)

- **Memory types**
  - Positive memories (resist positive decay)
  - Negative memories (resist negative decay)
  - Landmark memories (resist decay completely)

- **Memory in dialogue**
  - NPCs reference memories in responses
  - "I still remember when you..."
  - Memories affect future interactions

- **Memory decay**
  - Memories fade over long periods (optional)
  - Old memories have less impact
  - New memories can overwrite old ones

### Phase 3: Advanced Interactions (Week 4)

#### 3.1 Threshold Events
- **Affinity thresholds**
  - Crossing thresholds triggers special events
  - Different events for positive/negative crossings

- **Positive threshold events**
  - 0 → +1: NPC shares personal story
  - +1 → +2: NPC offers small favor
  - +2 → +3: NPC offers special ingredient/recipe
  - +3 → +4: NPC becomes active ally
  - +4 → +5: NPC becomes devoted mentor/partner

- **Negative threshold events**
  - 0 → -1: NPC becomes noticeably cooler
  - -1 → -2: NPC increases prices/reluctant service
  - -2 → -3: NPC warns others about you
  - -3 → -4: NPC refuses non-essential requests
  - -4 → -5: NPC actively works against you

- **Event consequences**
  - Unlock new dialogue options
  - Change NPC behavior patterns
  - Create new memories
  - Affect other NPCs (gossip system)

#### 3.2 Dialogue System
- **Dynamic dialogue**
  - Dialogue changes based on affinity level
  - Personality affects phrasing
  - Multiple response variants per interaction

- **Personality-based phrasing**
  - High O: Creative, abstract language
  - Low O: Traditional, concrete language
  - High C: Precise, structured sentences
  - Low C: Casual, loose phrasing
  - High E: Enthusiastic, energetic tone
  - Low E: Reserved, measured tone
  - High A: Warm, supportive language
  - Low A: Challenging, direct language
  - High N: Worried, cautious expressions
  - Low N: Confident, calm language

- **Dialogue options**
  - Player choices affect affinity
  - Preview personality impact (optional hint system)
  - Consistent personality creates unique player voice

- **Contextual responses**
  - NPCs remember recent actions
  - Reference ongoing situations
  - React to player reputation

#### 3.3 Multi-NPC Interactions
- **Gossip system**
  - NPCs talk to each other
  - Information spreads based on personality
  - High E NPCs gossip more frequently
  - High C NPCs verify before believing

- **Reputation effects**
  - Actions with one NPC affect others
  - High-affinity NPCs defend you
  - Low-affinity NPCs spread negative gossip
  - Some NPCs are opinion leaders (more influence)

- **Network visualization**
  - Show which NPCs know each other
  - Display information flow
  - Track reputation by social group

### Phase 4: Complex Scenarios (Week 5)

#### 4.1 Moral Dilemma System
- **Dilemma scenarios**
  - Situations that please some NPCs, alienate others
  - No perfect solution
  - Test player priorities

- **Example dilemmas**
  - **Profit vs. Ethics**: Charge sick villager vs. help free
    - Affects: High A NPCs (negative if charge), Business-minded NPCs (positive if charge)
  - **Tradition vs. Innovation**: Follow family recipe vs. experiment
    - Affects: High O NPCs (positive if innovate), Low O NPCs (negative if innovate)
  - **Competition vs. Cooperation**: Share knowledge vs. keep secrets
    - Affects: High A NPCs (positive if share), Low A NPCs (negative if share)

- **Consequence tracking**
  - Track player's moral patterns
  - Create player reputation profile
  - Unlock endings based on patterns

#### 4.2 Relationship Arcs
- **Character-specific storylines**
  - Multi-stage arcs for key NPCs
  - Require specific affinity levels to progress
  - Choices affect arc outcomes

- **Arc structure**
  - Introduction (affinity 0-1)
  - Trust building (affinity 2-3)
  - Challenge/conflict (affinity tested)
  - Resolution (affinity 4-5 or -3 to -5)

- **Example arc: Instructor Thornwood**
  - Stage 1: Strict teacher, hard to please
  - Stage 2: Recognizes your talent (affinity +3)
  - Stage 3: Offers advanced training (affinity +4)
  - Stage 4: Becomes mentor figure (affinity +5)
  - Alternative: Rebel against methods (affinity -3 to -5)

#### 4.3 Testing & Balancing
- **Affinity progression pacing**
  - How many interactions to reach +5?
  - How quickly does decay threaten relationships?
  - Balance maintenance burden

- **Personality reaction balance**
  - Are any traits too easy/hard to please?
  - Do all five traits feel impactful?
  - Test with diverse NPC profiles

- **Memory system testing**
  - Do memories prevent excessive decay?
  - Are significant events memorable enough?
  - Memory cap working well?

## Technical Implementation

### Technology Stack
- **Language**: Python 3.x
- **Data**: JSON for NPCs, actions, dialogues
- **Interface**: Command-line with rich text formatting
- **Time**: Simple turn/day counter

### File Structure
```
relationship_minigame/
├── main.py                    # Game loop and UI
├── npc_manager.py             # NPC handling
├── affinity_engine.py         # Affinity calculations
├── dialogue_system.py         # Dialogue generation
├── time_manager.py            # Calendar and decay
├── memory_system.py           # Memory tracking
├── data/
│   ├── npcs.json             # NPC definitions
│   ├── actions.json          # Action definitions
│   ├── dialogues.json        # Dialogue templates
│   └── dilemmas.json         # Moral dilemmas
├── saves/
│   └── relationship_save.json # Progress save
└── tests/
    └── test_relationships.py  # Unit tests
```

### Key Classes

```python
class NPC:
    id: str
    name: str
    personality: Personality (O, C, E, A, N values)
    affinity: float (-5 to +5)
    memories: List[Memory]
    last_interaction: int (day number)
    gossip_network: List[str] (other NPC IDs)

class Personality:
    openness: int (-1, 0, +1)
    conscientiousness: int
    extraversion: int
    agreeableness: int
    neuroticism: int

    def calculate_reaction(action: Action) -> float

class Memory:
    event: str
    affinity_change: float
    day_created: int
    decay_resistance: float

class Action:
    id: str
    name: str
    description: str
    personality_impacts: Dict[str, float]
    creates_memory: bool

class AffinityEngine:
    def apply_action(npc: NPC, action: Action) -> float
    def apply_decay(npc: NPC, days_passed: int) -> float
    def check_threshold_crossed(old_affinity, new_affinity) -> Optional[Event]
    def spread_gossip(npc: NPC, action: Action, other_npcs: List[NPC])

class DialogueSystem:
    def generate_response(npc: NPC, context: str) -> str
    def apply_personality_tone(text: str, personality: Personality) -> str
    def apply_affinity_filter(text: str, affinity: float) -> str
```

## Testing Goals

### Success Metrics
- [ ] Personality traits feel distinct and impactful
- [ ] Affinity progression feels natural and earned
- [ ] Decay creates maintenance gameplay without frustration
- [ ] Memories make relationships feel meaningful
- [ ] Dialogue feels personality-appropriate
- [ ] Threshold events feel rewarding/consequential
- [ ] Moral dilemmas create interesting tension
- [ ] Gossip system makes social network feel alive

### Data Collection
- Track average affinity progression rate
- Measure decay impact over time
- Note which personalities are easiest/hardest to befriend
- Identify confusing or frustrating interactions
- Record player feedback on NPC distinctiveness

## Integration Path to Godot

### Phase 1 Output
- Validated affinity formulas
- Balanced personality reaction values
- Tested decay rates
- Memory system specifications

### Phase 2 Requirements
- NPC JSON format for import
- Action definitions format
- Dialogue template structure
- Personality tone algorithms

### Phase 3 Godot Implementation
- Port relationship engine to GDScript
- Create NPC portrait and affinity UI
- Implement dialogue system with portraits
- Add visual memory indicators
- Connect to save system

## Known Challenges

### Challenge 1: Decay Rate Balance
- **Problem**: Too fast = frustrating, too slow = no maintenance needed
- **Mitigation**: Test with various rates (0.25, 0.5, 0.75 per week)
- **Test in minigame**: Simulate weeks passing, gather feedback

### Challenge 2: Personality Complexity
- **Problem**: Five traits may be too subtle for players to notice
- **Mitigation**: Clear personality descriptions, consistent behaviors
- **Test in minigame**: Can players predict NPC reactions?

### Challenge 3: Memory Overload
- **Problem**: Too many memories = clutter, too few = shallow
- **Mitigation**: Cap at 5-10 per NPC, prioritize recent/significant
- **Test in minigame**: Track memory usefulness

### Challenge 4: Dialogue Generation
- **Problem**: Personality-based generation may feel repetitive
- **Mitigation**: Multiple templates, mix personality traits
- **Test in minigame**: Vary dialogue enough?

## Next Steps After Completion

1. **Document personality patterns** - Which traits work best
2. **Export NPC data formats** - Prepare for Godot import
3. **Create NPC design guide** - How to create compelling NPCs
4. **Write integration guide** - Port relationship system to Godot
5. **Design UI mockups** - Visual affinity indicators
6. **Begin Godot prototype** - Implement validated system

## Timeline Summary

- **Week 1-2**: Personality and affinity basics
- **Week 3**: Decay and memory system
- **Week 4**: Advanced interactions and dialogue
- **Week 5**: Complex scenarios and testing
- **Week 6**: Integration prep and documentation

## Success Definition

This minigame is successful if:
1. NPCs feel like distinct individuals with recognizable personalities
2. Relationship progression feels earned and meaningful
3. Affinity decay creates interesting maintenance gameplay
4. Memories make relationships feel personal and consequential
5. Moral dilemmas create genuine tension and trade-offs
6. All mechanics are validated and ready for Godot implementation
