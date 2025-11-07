# Medium Roadmap: Combat/Dueling System Text-Based Minigame

## Overview
Create a standalone text-based minigame that implements turn-based potion combat with ESENS-driven effects, status management, and AI personality-based tactics. This prototype will validate combat mechanics, trigger systems, and strategic depth before full Godot implementation.

## Core Features to Implement

### Phase 1: Basic Combat Structure (Week 1-2)

#### 1.1 Combat Stats & State
- **Combatant stats**
  - Health (100 base)
  - Strength (attack power)
  - Defense (damage reduction)
  - Initiative (turn order)
  - Resistance (status effect resistance)

- **Status effect tracking**
  - Active buffs/debuffs per combatant
  - Duration tracking (turns remaining)
  - Stacking rules (can stack vs. replace)
  - Removability flags (.RN = not removable)

- **Combat state manager**
  - Current turn number
  - Turn order queue
  - Active status effects
  - Combat log history

#### 1.2 Turn Structure
- **Initiative system**
  - Roll for initiative at combat start
  - Modified by Initiative stat + potions
  - Re-roll each turn or static (configurable)

- **Turn phases**
  1. **Start of turn** (^S triggers activate)
  2. **Action phase** (combatant chooses action)
  3. **Effect resolution** (apply damage, status)
  4. **Trigger resolution** (conditional effects)
  5. **Status update** (durations decrement)
  6. **End of turn** (vE triggers activate)

- **Turn display**
  - Clear indication of whose turn
  - Show active status effects
  - Display available actions
  - Combat log with recent events

#### 1.3 Action Types
- **Use Potion**
  - Select from combat belt (10 slots)
  - Apply potion effects via ESENS
  - Target self or opponent
  - Consume potion from inventory

- **Observe**
  - Reveal opponent's status effects
  - Show buff/debuff details
  - Costs one turn
  - Useful for strategic planning

- **Guard**
  - Increase Defense this turn (+50%)
  - Reduce incoming damage
  - Defensive tactical option

- **Provoke**
  - Taunt opponent
  - Affects AI behavior (more aggressive)
  - May reduce opponent accuracy

- **Wait**
  - Delay action to later in turn
  - Tactical timing for triggers
  - Can react to opponent's action

### Phase 2: ESENS Integration (Week 3)

#### 2.1 ESENS Parser Integration
- **Effect parsing**
  - Use existing ESENS_Parser.py
  - Parse potion notation to effects
  - Create StatusEffect objects
  - Handle complex notations

- **Effect application**
  - Apply stat modifications (P+S30%)
  - Apply enemy debuffs (E-D20%)
  - Handle instant effects (#Damage, #Heal)
  - Manage durations (3T, 5T, C)

- **Element system**
  - Element types: .F (Fire), .W (Water), .E (Earth), .A (Air)
  - Element interactions (bonuses/penalties)
  - Display element clearly in UI

#### 2.2 Trigger System
- **Trigger types**
  - `^S`: Start of turn
  - `vE`: End of turn
  - `>A`: On attack (when you attack)
  - `<D`: On being attacked
  - `>Sprd`: Spread to others
  - Custom triggers (damage thresholds, etc.)

- **Trigger evaluation**
  - Check conditions each phase
  - Execute triggered effects
  - Chain triggers (trigger → new trigger)
  - Prevent infinite loops

- **Trigger visualization**
  - Show when triggers activate
  - Explain cause and effect
  - Highlight in combat log

#### 2.3 Status Effect Management
- **Effect categories**
  - Buffs (positive effects on self)
  - Debuffs (negative effects on self)
  - Enemy debuffs (negative effects on opponent)
  - Persistent effects (duration = C)

- **Stacking rules**
  - `.ST` flag = can stack
  - Default = replace existing
  - Track stack count
  - Max stacks limit

- **Removal mechanics**
  - `.RN` flag = not removable
  - Cleansing potions remove debuffs
  - Death/combat end clears all
  - Show removability status

### Phase 3: AI & Strategy (Week 4)

#### 3.1 Opponent AI System
- **AI decision-making**
  - Evaluate available potions
  - Assess current situation (HP, buffs, debuffs)
  - Choose optimal action
  - Personality affects decisions

- **AI difficulty levels**
  - **Easy**: Random choices, poor timing
  - **Medium**: Basic strategy, some mistakes
  - **Hard**: Good strategy, optimal timing
  - **Expert**: Near-perfect play, advanced combos

- **AI personality integration**
  - High Openness: Uses unusual potions, adapts
  - High Conscientiousness: Methodical, proven tactics
  - High Extraversion: Aggressive, flashy, risky
  - High Agreeableness: Defensive, avoids overkill
  - High Neuroticism: Panics when low HP

#### 3.2 Strategic Depth
- **Combo systems**
  - Buff stacking (multiple strength potions)
  - Trigger chaining (attack triggers spread)
  - Setup + payoff (debuff then exploit)

- **Counter-play**
  - Cleansing potions remove debuffs
  - Defensive potions counter aggression
  - Timing Wait action to react
  - Observe to plan counter

- **Resource management**
  - Limited potion inventory (10 slots)
  - Expensive potions vs. efficient ones
  - Save powerful potions for critical moments

- **Risk/reward decisions**
  - High damage but self-harm
  - Strong buff but long cooldown
  - Gamble on critical effects

#### 3.3 Pre-Duel Phase
- **Potion selection**
  - Choose 10 potions from full inventory
  - Arrange in combat belt
  - Strategic loadout building
  - Save/load loadout presets

- **Opponent analysis**
  - View opponent stats (if known)
  - Review fighting style info
  - Check elemental preferences
  - Read personality traits

- **Strategy planning**
  - Set initial game plan
  - Identify win conditions
  - Plan for contingencies

### Phase 4: Victory Conditions & Outcomes (Week 5)

#### 4.1 Victory Conditions
- **Health Depletion** (most common)
  - Reduce opponent to 0 HP
  - Player wins or loses

- **Forfeit**
  - Opponent surrenders
  - Based on morale or situation
  - AI may forfeit if hopeless

- **Timeout**
  - Turn limit reached (optional)
  - Higher HP wins
  - Tie-breaker: better status effects

- **Incapacitation**
  - Stunned for 3+ turns
  - Unable to act = loss

- **Judge Decision** (rare)
  - Based on style and creativity
  - For exhibition matches

#### 4.2 Post-Duel Results
- **Performance metrics**
  - Turns taken
  - Damage dealt/received
  - Potions used
  - Creative combo bonus

- **Rewards**
  - Gold earned
  - Reputation change
  - Potion/ingredient rewards
  - Unlock next tier opponents

- **Relationship changes**
  - Affinity with opponent shifts
  - Honorable victory = +affinity
  - Dirty tactics = -affinity
  - Spectators react

#### 4.3 Opponent Variety
- **Opponent archetypes**
  - **Aggressive Bruiser**: High damage, low defense
  - **Defensive Tank**: High HP/defense, slow
  - **Status Master**: Debuff/control focus
  - **Balanced Duelist**: Well-rounded
  - **Trickster**: Unusual tactics, unpredictable

- **Opponent progression**
  - Early opponents: Simple strategies
  - Mid-tier: More potions, better tactics
  - High-tier: Advanced combos, counters
  - Champion: All of the above + personality

- **Named opponents (5-10)**
  - Kael Emberforge (O:+1, C:0, E:+1, A:-1, N:0)
    - Style: Aggressive fire potions, high risk
  - Lyra Frostwhisper (O:0, C:+1, E:-1, A:0, N:-1)
    - Style: Defensive ice potions, patient
  - Zephyr Quickbrew (O:+1, C:-1, E:+1, A:0, N:+1)
    - Style: Speed and chaos, unpredictable
  - Thorne Ironroot (O:-1, C:+1, E:0, A:-1, N:0)
    - Style: Traditional earth potions, methodical
  - Seren Voidcaller (O:+1, C:0, E:0, A:0, N:0)
    - Style: Exotic status effects, mysterious

## Technical Implementation

### Technology Stack
- **Language**: Python 3.x
- **Parser**: ESENS_Parser.py for effect parsing
- **Data**: JSON for potions, opponents, combat stats
- **Interface**: Command-line with clear combat visualization

### File Structure
```
combat_minigame/
├── main.py                   # Game loop and UI
├── combat_engine.py          # Core combat logic
├── combatant.py              # Combatant class (player/AI)
├── status_effect.py          # Status effect management
├── trigger_system.py         # Trigger evaluation
├── ai_controller.py          # AI decision-making
├── combat_log.py             # Combat history tracking
├── data/
│   ├── combat_potions.json  # Combat-focused potions
│   ├── opponents.json       # Opponent definitions
│   └── loadouts.json        # Pre-made loadouts
├── saves/
│   └── combat_save.json     # Progress save
└── tests/
    └── test_combat.py       # Unit tests
```

### Key Classes

```python
class Combatant:
    name: str
    health: int
    max_health: int
    strength: int
    defense: int
    initiative: int
    resistance: int
    active_effects: List[StatusEffect]
    combat_belt: List[Potion] (max 10)
    personality: Optional[Personality]  # For AI

class StatusEffect:
    name: str
    source: str (potion name)
    stat_affected: str
    modifier: float
    duration: int (turns, or -1 for permanent/C)
    element: Optional[str]
    triggers: List[Trigger]
    removable: bool
    stackable: bool

class Trigger:
    trigger_type: str (^S, vE, >A, <D, etc.)
    effect: str (ESENS notation)
    condition: Optional[callable]

class CombatEngine:
    def resolve_turn(combatant: Combatant, action: Action)
    def apply_potion(combatant: Combatant, potion: Potion, target: Combatant)
    def evaluate_triggers(phase: str, combatant: Combatant)
    def update_status_effects(combatant: Combatant)
    def check_victory_condition() -> Optional[str]
    def calculate_damage(attacker: Combatant, defender: Combatant, base_damage: int) -> int

class AIController:
    def choose_action(combatant: Combatant, opponent: Combatant) -> Action
    def evaluate_potion(potion: Potion, situation: CombatState) -> float
    def apply_personality_bias(choices: List[Action], personality: Personality) -> Action
    def check_forfeit_condition(combatant: Combatant) -> bool

class CombatLog:
    def add_event(event: str, turn: int)
    def display_recent(count: int)
    def export_log() -> str
```

## Testing Goals

### Success Metrics
- [ ] Combat feels strategic, not random
- [ ] ESENS effects apply correctly
- [ ] Triggers work as expected (no bugs)
- [ ] Status effect management is clear
- [ ] AI provides challenge at appropriate difficulty
- [ ] Personality affects AI behavior noticeably
- [ ] Victory feels earned, not lucky
- [ ] Loadout building is engaging
- [ ] Combat log helps understand what happened
- [ ] Turn structure flows smoothly

### Data Collection
- Track average combat duration (turns)
- Note which potions are overpowered/underpowered
- Identify confusing status interactions
- Measure AI difficulty accuracy
- Record player feedback on fun factor

## Integration Path to Godot

### Phase 1 Output
- Validated combat formulas
- Balanced potion effects
- Tested trigger system
- AI behavior patterns

### Phase 2 Requirements
- Combat potion JSON format
- Opponent JSON format
- Status effect specifications
- Combat UI/UX patterns

### Phase 3 Godot Implementation
- Port combat engine to GDScript
- Create visual combat UI
- Add animations for attacks/effects
- Implement particle effects for elements
- Connect to ESENS parser and save system

## Known Challenges

### Challenge 1: Trigger Complexity
- **Problem**: Complex triggers may be buggy or confusing
- **Mitigation**: Start simple (^S, vE), add gradually
- **Test in minigame**: Validate trigger order and chains

### Challenge 2: Status Effect Stacking
- **Problem**: Unclear how stacking works (additive? multiplicative?)
- **Mitigation**: Define clear rules, test edge cases
- **Test in minigame**: Stack 5+ buffs, verify math

### Challenge 3: AI Balance
- **Problem**: Too easy = boring, too hard = frustrating
- **Mitigation**: Multiple difficulty levels, test extensively
- **Test in minigame**: Gather win/loss rates at each level

### Challenge 4: Combat Pacing
- **Problem**: Battles too fast (luck) or too slow (grindy)
- **Mitigation**: Tune damage values, HP totals
- **Test in minigame**: Track average battle duration

### Challenge 5: ESENS Combat Notation
- **Problem**: Some ESENS patterns may not translate to combat well
- **Mitigation**: Create combat-specific potion library
- **Test in minigame**: Ensure all ESENS features work

## Example Combat Potions

```json
[
  {
    "name": "Flame Strike Potion",
    "esens": "P+S30%3T>A.F",
    "description": "Boost strength by 30% for 3 turns, triggers when you attack, fire element"
  },
  {
    "name": "Weakness Curse",
    "esens": "E-D20%2T<D",
    "description": "Weaken enemy defense by 20% for 2 turns when they attack you"
  },
  {
    "name": "Iron Skin Potion",
    "esens": "P+D50%C.RN",
    "description": "Increase defense by 50% for entire combat, cannot be removed"
  },
  {
    "name": "Stun Bomb",
    "esens": "E#Stun1T",
    "description": "Stun opponent for 1 turn, prevents their action"
  },
  {
    "name": "Regeneration Elixir",
    "esens": "P+H10^S5T.ST",
    "description": "Heal 10 HP at start of turn for 5 turns, stackable"
  },
  {
    "name": "Speed Serum",
    "esens": "P+I50%C",
    "description": "Increase initiative by 50% for entire combat"
  },
  {
    "name": "Cleansing Tonic",
    "esens": "P!Clear1T",
    "description": "Remove all removable debuffs"
  }
]
```

## Next Steps After Completion

1. **Document combat patterns** - What strategies work best
2. **Export combat data** - Prepare for Godot import
3. **Create AI design guide** - How to design challenging opponents
4. **Write integration guide** - Port combat system to Godot
5. **Design UI mockups** - Visual combat interface
6. **Begin Godot prototype** - Implement validated combat

## Timeline Summary

- **Week 1-2**: Basic combat structure and turn system
- **Week 3**: ESENS integration and status effects
- **Week 4**: AI system and strategic depth
- **Week 5**: Victory conditions, opponent variety, polish
- **Week 6**: Integration prep and documentation

## Success Definition

This minigame is successful if:
1. Combat feels strategic with meaningful decision-making
2. ESENS effects work correctly and create interesting gameplay
3. Trigger system adds depth without confusion
4. AI provides appropriate challenge at each difficulty
5. Personality-based AI feels distinct and noticeable
6. Loadout building is engaging and impactful
7. All mechanics are validated and ready for Godot implementation
