# Medium Roadmap: Quest & Event System Text-Based Minigame

## Overview
Create a standalone text-based minigame that implements quest tracking, event systems, moral choice mechanics, and consequence tracking. This prototype will validate quest structure, branching paths, and world state changes before full Godot implementation.

## Core Features to Implement

### Phase 1: Quest Structure (Week 1-2)

#### 1.1 Quest Types
- **Six quest categories**
  1. **Main Story Quests**: Progress narrative, unlock seasons
  2. **Character Quests**: NPC-specific storylines
  3. **Reputation Quests**: Build standing in factions
  4. **Crafting Challenges**: Create specific potions
  5. **Investigation Quests**: Solve mysteries (Season 4 focus)
  6. **Collection Quests**: Gather ingredients

- **Quest properties**
  - Quest ID and name
  - Quest type
  - Description and objectives
  - Requirements (level, stats, prerequisites)
  - Rewards (gold, items, reputation, XP)
  - Time limit (optional)
  - Failure conditions (optional)

- **Quest states**
  - Locked: Prerequisites not met
  - Available: Can be started
  - Active: Currently pursuing
  - Completed: Successfully finished
  - Failed: Failed or abandoned

#### 1.2 Quest Tracking
- **Active quest log**
  - List all active quests
  - Show progress per objective
  - Display time remaining (if timed)
  - Highlight urgent quests

- **Objective tracking**
  - Multiple objectives per quest
  - Sequential (A then B then C) or parallel (A, B, C in any order)
  - Progress indicators (3/5 items collected)
  - Completion checkmarks

- **Quest notifications**
  - New quest available
  - Objective completed
  - Quest completed
  - Quest failed
  - Time warnings

#### 1.3 Basic Quest Examples
- **Main Story Quest (Season 1)**
  - Name: "First Brew"
  - Type: Main Story
  - Objectives:
    1. Gather 3 Roots
    2. Gather 2 Berries
    3. Craft Simple Healing Potion
  - Reward: 100 XP, unlock next lesson

- **Character Quest**
  - Name: "Healer's Request"
  - Type: Character (Healer Wisteria)
  - Requirements: Village Reputation 20+, Affinity with Wisteria 2+
  - Objectives:
    1. Craft 5 Healing Potions
    2. Deliver to Wisteria
  - Reward: 50 gold, +1 affinity, rare ingredient

- **Crafting Challenge**
  - Name: "No Shortcuts"
  - Type: Crafting Challenge
  - Objectives:
    1. Craft Strength Potion without using Common Roots
  - Reward: Innovation XP, unlock substitution tutorial

### Phase 2: Moral Choices (Week 3)

#### 2.1 Choice Framework
- **Choice categories**
  1. **Profit vs. Ethics**: Money or morality
  2. **Tradition vs. Innovation**: Old ways or new methods
  3. **Competition vs. Cooperation**: Hoard or share knowledge
  4. **Caution vs. Ambition**: Safety or risk

- **Choice properties**
  - Choice prompt (situation description)
  - 2-4 options
  - Immediate consequences
  - Medium-term effects
  - Long-term impacts

- **Choice presentation**
  - Clear description of situation
  - Preview potential outcomes (optional hint system)
  - Cannot undo once chosen
  - Track choice history

#### 2.2 Moral Dilemma Examples
- **Dilemma: Sick Villager**
  - **Situation**: Poor villager needs expensive healing potion
  - **Options**:
    - A) Charge full price (100 gold, -1 Wisteria affinity, -5 Village reputation)
    - B) Give discount (50 gold, +0.5 Wisteria affinity)
    - C) Give free (+2 Wisteria affinity, +10 Village reputation, -ingredient cost)
  - **Long-term**: Choice affects epidemic quest availability

- **Dilemma: Dangerous Knowledge**
  - **Situation**: Found recipe for mind control potion
  - **Options**:
    - A) Learn recipe (unlock powerful but unethical potion)
    - B) Destroy recipe (+ethics reputation, lose knowledge)
    - C) Report to authorities (+legal reputation, investigator path)
  - **Long-term**: Affects Season 4 conspiracy questline

- **Dilemma: Rival's Sabotage**
  - **Situation**: Opportunity to sabotage competitor's shop
  - **Options**:
    - A) Sabotage (eliminate competitor, -ethics, risk of discovery)
    - B) Ignore (fair competition continues)
    - C) Warn competitor (+affinity with rival, potential alliance)
  - **Long-term**: Affects market share and Season 3 dueling circuit

#### 2.3 Consequence Tracking
- **Choice tracking system**
  - "Potion Book of Life" records major choices
  - Categories: Ethical, Innovative, Competitive, Ambitious
  - Track overall moral pattern

- **Consequence types**
  - **Immediate**: Gold, items, affinity changes
  - **Medium-term**: Quest unlocks, reputation shifts
  - **Long-term**: World state changes, ending variations
  - **Legacy**: How remembered in Season 5

- **World state changes**
  - Persistent changes to game world
  - NPCs remember and reference choices
  - Unlocked/locked content based on choices
  - Multiple ending paths

### Phase 3: Event System (Week 4)

#### 3.1 Event Types
- **Random Events**
  - Ingredient gathering encounters
  - Customer emergencies
  - Traveling merchant visits
  - NPC relationship moments
  - Ethical dilemmas

- **Scheduled Events**
  - Seasonal festivals
  - Tournament brackets
  - Royal court sessions
  - Guild meetings
  - Market days

- **Triggered Events**
  - Affinity threshold crossings
  - Reputation milestones
  - Story progression points
  - Moral choice consequences
  - World state changes

#### 3.2 Event Properties
- **Event structure**
  - Event ID and name
  - Trigger condition
  - Description
  - Player choices (if interactive)
  - Outcomes and consequences
  - Cooldown (if repeatable)

- **Event timing**
  - One-time events
  - Repeatable events
  - Seasonal events (annually)
  - Random chance events

- **Event consequences**
  - Affect world state
  - Trigger other events
  - Modify NPC behavior
  - Create quests

#### 3.3 Event Examples
- **Random Event: Rare Ingredient**
  - **Trigger**: Random during gathering (5% chance)
  - **Description**: You spot a rare Crystal growing in unusual location
  - **Choices**:
    - A) Take it (gain Crystal, mark location)
    - B) Leave it (ethical, location remains for future)
  - **Consequence**: Choice affects ecology questline

- **Scheduled Event: Harvest Festival**
  - **Trigger**: First week of Fall each year
  - **Description**: Village celebrates harvest with festival
  - **Activities**:
    - Potion brewing contest (test skills)
    - Socialize with NPCs (build affinity)
    - Special merchant with rare goods
  - **Rewards**: Gold, reputation, unique items

- **Triggered Event: Rival Confrontation**
  - **Trigger**: Village Reputation reaches 60, rival at 40
  - **Description**: Rival alchemist confronts you about competition
  - **Choices**:
    - A) Aggressive (potential duel, -affinity)
    - B) Diplomatic (negotiate territory, +affinity)
    - C) Cooperative (propose partnership, alliance)
  - **Consequence**: Affects Season 3 dueling availability

### Phase 4: Quest Chains & Integration (Week 5)

#### 4.1 Quest Chains
- **Multi-stage questlines**
  - Series of connected quests
  - Each stage unlocks next
  - Overall story arc

- **Example: Plague Questline (Season 2)**
  - **Stage 1**: "Strange Symptoms"
    - Investigate sick villagers
    - Identify unknown ailment
    - Reward: 50 gold, unlock Stage 2
  - **Stage 2**: "Source of Illness"
    - Trace contamination to water source
    - Choice: Warn village immediately (panic) or investigate quietly
    - Reward: Clues, unlock Stage 3
  - **Stage 3**: "The Cure"
    - Craft antidote (challenging recipe)
    - Choice: Charge for cure (profit) or distribute free (reputation)
    - Reward: Major reputation change, Season 2 climax
  - **Stage 4**: "Prevention"
    - Implement long-term solution
    - Choice: Expensive perfect fix or cheaper compromise
    - Reward: Determine village's future health

- **Branching paths**
  - Choices affect available stages
  - Different routes through questline
  - Multiple possible endings

#### 4.2 Consequence Integration
- **Cross-system effects**
  - Quest choices affect NPC affinity
  - Moral choices affect reputation
  - Reputation unlocks new quests
  - Completed quests affect world state

- **World state tracking**
  - Track major world changes
  - NPCs reference past events
  - Environment reflects consequences
  - News system spreads information

- **Long-term consequences**
  - Season 1 choices affect Season 5
  - Butterfly effect (small choices compound)
  - Multiple ending determination
  - Legacy calculation

#### 4.3 Quest Journal & UI
- **Quest journal interface**
  - Active quests tab
  - Completed quests tab
  - Failed/abandoned quests tab
  - "Potion Book of Life" (moral choices)

- **Quest details view**
  - Full description
  - Objective list with progress
  - Recommended level/stats
  - Rewards preview
  - Related NPCs/locations
  - Notes section

- **Quest sorting/filtering**
  - Sort by: Type, Urgency, Reward, Location
  - Filter by: Season, Category, NPC
  - Search by name

## Technical Implementation

### Technology Stack
- **Language**: Python 3.x
- **Data**: JSON for quests, events, choices
- **State**: World state tracking
- **Interface**: Command-line with clear quest display

### File Structure
```
quest_event_minigame/
├── main.py                        # Game loop and UI
├── quest_manager.py               # Quest tracking and logic
├── event_system.py                # Event generation and handling
├── choice_manager.py              # Moral choice tracking
├── consequence_tracker.py         # Track world state changes
├── world_state.py                 # Persistent world state
├── quest_journal.py               # Quest log UI
├── data/
│   ├── quests.json               # Quest definitions
│   ├── events.json               # Event definitions
│   ├── choices.json              # Moral choice scenarios
│   ├── quest_chains.json         # Quest chain definitions
│   └── world_state.json          # Initial world state
├── saves/
│   └── quest_save.json           # Quest progress and world state
└── tests/
    └── test_quests.py            # Unit tests
```

### Key Classes

```python
class Quest:
    id: str
    name: str
    quest_type: QuestType
    description: str
    objectives: List[Objective]
    requirements: Dict[str, any]
    rewards: Rewards
    state: QuestState
    time_limit: Optional[int]  # days
    failure_conditions: List[str]

    def can_start(player: Player, world_state: WorldState) -> bool
    def check_objectives() -> bool
    def complete() -> Rewards
    def fail() -> None

class Objective:
    description: str
    target: any  # depends on objective type
    current: any  # current progress
    completed: bool

    def check_completion() -> bool
    def update_progress(value: any)

class MoralChoice:
    id: str
    prompt: str
    category: ChoiceCategory
    options: List[ChoiceOption]
    chosen_option: Optional[str]

    def present_choice() -> str
    def record_choice(option_id: str)
    def apply_consequences(world_state: WorldState)

class ChoiceOption:
    id: str
    text: str
    immediate_consequences: Dict[str, any]
    medium_consequences: List[str]
    long_term_effects: List[str]

class Event:
    id: str
    name: str
    event_type: EventType
    trigger: Trigger
    description: str
    choices: Optional[List[ChoiceOption]]
    outcomes: List[Outcome]
    cooldown: Optional[int]  # days
    last_triggered: Optional[int]

    def can_trigger(world_state: WorldState, player: Player) -> bool
    def trigger_event()
    def resolve_outcome(choice: Optional[str])

class WorldState:
    quest_states: Dict[str, QuestState]
    npc_states: Dict[str, NPCState]
    world_flags: Dict[str, bool]
    reputation_values: Dict[str, int]
    moral_choices: List[MoralChoice]
    current_season: int
    current_day: int

    def set_flag(flag: str, value: bool)
    def get_flag(flag: str) -> bool
    def apply_consequence(consequence: Consequence)

class QuestManager:
    def get_available_quests(player: Player, world_state: WorldState) -> List[Quest]
    def start_quest(quest_id: str)
    def update_quest(quest_id: str, progress: any)
    def complete_quest(quest_id: str) -> Rewards
    def fail_quest(quest_id: str)
    def check_quest_chains() -> List[Quest]  # unlocked by completion

class EventSystem:
    def check_random_events() -> Optional[Event]
    def check_scheduled_events(day: int) -> List[Event]
    def check_triggered_events(world_state: WorldState) -> List[Event]
    def trigger_event(event: Event)
```

## Testing Goals

### Success Metrics
- [ ] Quests feel purposeful and rewarding
- [ ] Objectives are clear and trackable
- [ ] Moral choices feel meaningful
- [ ] Consequences are noticeable and impactful
- [ ] Events feel natural and timely
- [ ] Quest chains create compelling narratives
- [ ] World state reflects player actions
- [ ] Journal is easy to navigate
- [ ] Branching paths are discoverable
- [ ] Long-term consequences matter

### Data Collection
- Track quest completion rates
- Note which moral choices are most popular
- Measure consequence noticeability
- Identify confusing objectives
- Record player feedback on impact

## Integration Path to Godot

### Phase 1 Output
- Validated quest structure
- Balanced reward systems
- Tested consequence chains
- Event timing algorithms

### Phase 2 Requirements
- Quest data format for Godot
- World state save format
- Event trigger systems
- Journal UI patterns

### Phase 3 Godot Implementation
- Port quest system to GDScript
- Create visual quest journal
- Implement event popups
- Add quest markers/waypoints
- Connect to save system

## Known Challenges

### Challenge 1: Choice Consequence Balance
- **Problem**: Too subtle = unnoticeable, too extreme = punishing
- **Mitigation**: Clear feedback, fair trade-offs
- **Test in minigame**: Do players notice consequences?

### Challenge 2: Quest Complexity
- **Problem**: Too many objectives = overwhelming
- **Mitigation**: Clear UI, 3-5 objectives max
- **Test in minigame**: Can players track multiple quests?

### Challenge 3: Event Timing
- **Problem**: Too frequent = spam, too rare = missed content
- **Mitigation**: Tune probabilities, test extensively
- **Test in minigame**: Do events feel natural?

### Challenge 4: World State Complexity
- **Problem**: Too many flags = bugs, too few = shallow
- **Mitigation**: Careful design, testing
- **Test in minigame**: Track all state changes

## Next Steps After Completion

1. **Document quest patterns** - What structures work best
2. **Export quest data** - Prepare for Godot import
3. **Create quest design guide** - How to write compelling quests
4. **Write integration guide** - Port to Godot
5. **Design UI mockups** - Visual quest journal
6. **Begin Godot prototype** - Implement validated system

## Timeline Summary

- **Week 1-2**: Quest structure and tracking
- **Week 3**: Moral choice system
- **Week 4**: Event system and triggers
- **Week 5**: Quest chains and integration
- **Week 6**: Integration prep and documentation

## Success Definition

This minigame is successful if:
1. Quests provide clear goals and satisfying rewards
2. Moral choices feel meaningful with noticeable consequences
3. Events enhance the world without overwhelming
4. Quest chains create compelling narratives
5. World state meaningfully reflects player actions
6. Journal helps players track progress effectively
7. All mechanics are validated and ready for Godot implementation
