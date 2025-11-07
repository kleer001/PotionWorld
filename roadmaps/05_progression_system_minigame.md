# Medium Roadmap: Progression System Text-Based Minigame

## Overview
Create a standalone text-based minigame that implements player stats, experience gain, mastery levels, reputation tracking, and specialization choices. This prototype will validate progression pacing, stat scaling, and character development across seasons before full Godot implementation.

## Core Features to Implement

### Phase 1: Core Stats & XP (Week 1-2)

#### 1.1 Player Stats System
- **Six primary attributes (0-100)**
  1. **Alchemical Knowledge**
     - Unlocks recipe complexity
     - Affects success rates
     - Gained through lessons, crafting, research

  2. **Precision**
     - Reduces failure chance
     - Improves quality
     - Gained through practice

  3. **Intuition**
     - Enables substitutions
     - Reveals hidden properties
     - Gained through experimentation

  4. **Reputation**
     - Affects opportunities
     - Separate tracks per region
     - Gained through actions

  5. **Business Acumen**
     - Improves profits
     - Unlocks shop features
     - Gained through transactions

  6. **Combat Instinct**
     - Affects dueling
     - Enables tactical timing
     - Gained through combat

- **Stat display**
  - Clear visualization (bars, numbers)
  - Show progress to next milestone
  - Indicate stat effects on gameplay

- **Stat growth tracking**
  - Track total XP per stat
  - Show recent gains
  - Display growth history

#### 1.2 Experience System
- **XP sources and amounts**
  - Crafting potions: 10-100 XP (based on difficulty)
  - Failed crafts: 5 XP (consolation)
  - Experimentation: 25-150 XP
  - Combat victories: 50-200 XP
  - Completing quests: 100-500 XP
  - Learning lessons: 50-200 XP
  - Sales transactions: 5-20 XP (Business Acumen)
  - Discoveries: 200-500 XP

- **XP distribution**
  - Activities award XP to relevant stats
  - Some activities award multiple stats
  - Bonus XP for challenging content

- **XP scaling**
  - Early levels: Fast progression
  - Mid levels: Moderate pace
  - Late levels: Slower, but still achievable
  - Soft cap at 100 per stat

#### 1.3 Stat Milestones
- **Milestone thresholds**
  - 0-20: Novice
  - 21-40: Competent
  - 41-60: Proficient
  - 61-80: Expert
  - 81-100: Master

- **Milestone rewards**
  - Unlock new abilities
  - Improve existing mechanics
  - Unlock new content
  - Visual indicators (titles, badges)

- **Milestone notifications**
  - Celebrate reaching milestones
  - Explain new unlocks
  - Show stat comparison to previous level

### Phase 2: Reputation & Mastery (Week 3)

#### 2.1 Reputation System
- **Multiple reputation tracks**
  - **Academy Reputation** (Season 1)
  - **Village Reputation** (Season 2)
  - **Dueling Circuit Reputation** (Season 3)
  - **Royal Court Reputation** (Season 4)
  - **Master Reputation** (Season 5)

- **Reputation scale (0-100)**
  - 0-20: Unknown
  - 21-40: Known
  - 41-60: Respected
  - 61-80: Renowned
  - 81-100: Legendary

- **Reputation effects**
  - Unlock quests and opportunities
  - Affect NPC initial affinity
  - Modify prices (±20%)
  - Enable certain endings
  - Determine legacy impact

- **Reputation gain/loss**
  - Completing quests: +5 to +20
  - Helping community: +3 to +10
  - Moral choices: -10 to +15
  - Failed obligations: -5 to -15
  - Major achievements: +20 to +50

#### 2.2 Recipe Mastery
- **Per-recipe mastery (0-100)**
  - Track individually per recipe
  - Grows with successful crafts
  - Faster growth for challenging recipes

- **Mastery levels**
  - **Novice (0-20)**: Base success rate
  - **Competent (21-40)**: +10% success, -10% waste
  - **Proficient (41-60)**: +20% success, +10% quality
  - **Expert (61-80)**: +30% success, +20% quality, can teach
  - **Master (81-100)**: +40% success, +30% quality, can innovate

- **Mastery benefits**
  - Improved success rates
  - Better quality output
  - Ingredient savings
  - Batch crafting unlock (60+)
  - Innovation unlock (80+)

- **Mastery progression**
  - Each successful craft: +5 to +10 mastery
  - Critical success: +15 mastery
  - Failure: +1 mastery (small consolation)
  - Teaching: +2 mastery per lesson

#### 2.3 Achievement System
- **Achievement categories**
  - **Crafting**: Create X potions, master recipes
  - **Collection**: Gather all ingredient types
  - **Social**: Max affinity with NPCs
  - **Combat**: Win duels, perfect victories
  - **Story**: Complete seasons, moral paths
  - **Challenge**: Speedruns, limitations

- **Achievement rewards**
  - Titles (displayed in UI)
  - Cosmetic customizations
  - Bonus gold for New Game+
  - Unlockable content

- **Achievement tracking**
  - Progress bars for incremental achievements
  - Hidden achievements (discovered when earned)
  - Completion percentage

### Phase 3: Specializations (Week 4)

#### 3.1 Specialization System
- **Specialization categories**
  - **Crafting Specializations**: Improve crafting
  - **Social Specializations**: Improve relationships
  - **Research Specializations**: Improve knowledge

- **Crafting Specializations**
  - **Perfectionist**: +20% Precision, +10% quality
  - **Innovator**: Substitute ingredients, +15% Intuition
  - **Speed Brewer**: Craft 25% faster, -5% Precision
  - **Mass Producer**: Multiple potions/craft, -10% quality

- **Social Specializations**
  - **Diplomat**: +15 to all affinity gains
  - **Merchant**: +20% profit margins
  - **Teacher**: Apprentices learn faster
  - **Competitor**: +15 Combat Instinct

- **Research Specializations**
  - **Analyst**: Reverse-engineer faster
  - **Ethicist**: Moral choices give extra reputation
  - **Experimentalist**: Failures provide useful data
  - **Historian**: Access ancient recipes

- **Specialization selection**
  - Choose one per season (5 total by endgame)
  - Cannot change once chosen
  - Preview benefits before choosing
  - Some require stat prerequisites

#### 3.2 Skill Trees (Optional)
- **Tree structure**
  - Branch paths for different playstyles
  - Prerequisites for advanced skills
  - Limited points force choices

- **Skill categories**
  - Passive bonuses (always active)
  - Active abilities (triggered)
  - Unlocks (new features)

- **Skill examples**
  - **Efficient Gathering**: +20% ingredient yield
  - **Quality Focus**: +15% potion quality
  - **Speed Reading**: Learn recipes 50% faster
  - **Bulk Discount**: -10% merchant prices

#### 3.3 Season Progression
- **Season-based stat growth**
  - **Season 1 (Apprentice)**: Focus Knowledge, Precision
  - **Season 2 (Inheritor)**: All stats active, Business grows
  - **Season 3 (Competitor)**: Combat Instinct emphasized
  - **Season 4 (Investigator)**: Intuition, Knowledge peak
  - **Season 5 (Master)**: All stats reach maximum

- **Season transitions**
  - End-of-season summary
  - Stats achieved display
  - Relationships summary
  - Major choices recap
  - Preview next season

- **Carryover mechanics**
  - All stats carry forward
  - Reputation evolves
  - Mastery maintained
  - Some inventory changes

### Phase 4: Balance & Pacing (Week 5)

#### 4.1 Progression Pacing
- **Target milestones by season**
  - **Season 1 end**: Knowledge 40-50, Precision 30-40
  - **Season 2 end**: Primary stats 50-60, Business 30-40
  - **Season 3 end**: Combat 60-70, others 60-70
  - **Season 4 end**: Most stats 70-80
  - **Season 5 end**: Multiple stats at 90-100

- **XP rate tuning**
  - Early game: Fast progression (feel powerful)
  - Mid game: Steady pace (maintain engagement)
  - Late game: Slower but satisfying (achievements matter)

- **Diminishing returns**
  - Higher stats require more XP
  - Prevents trivializing content
  - Maintains challenge

#### 4.2 Balance Testing
- **Stat effectiveness testing**
  - Do all stats feel impactful?
  - Are any stats too strong/weak?
  - Do stats scale appropriately?

- **Reputation balance**
  - Is reputation gain too fast/slow?
  - Do reputation levels feel significant?
  - Are there enough ways to earn reputation?

- **Mastery progression**
  - Time to master recipes reasonable?
  - Benefits feel rewarding?
  - Motivation to master multiple recipes?

- **Specialization balance**
  - Are all specializations viable?
  - Do players feel locked into choices?
  - Trade-offs clear and interesting?

#### 4.3 Player Feedback Systems
- **Progress visibility**
  - Always show current stats
  - Highlight recent gains
  - Show progress to goals

- **Goal setting**
  - Suggest next milestones
  - Track player-set goals
  - Celebrate achievements

- **Comparison systems**
  - Compare to previous seasons
  - Compare to average/expected
  - Show growth trajectory

## Technical Implementation

### Technology Stack
- **Language**: Python 3.x
- **Data**: JSON for player state, achievements, specializations
- **Interface**: Command-line with progress visualization
- **Math**: Stat formulas, XP curves

### File Structure
```
progression_minigame/
├── main.py                       # Game loop and UI
├── player_stats.py               # Stat management
├── experience_system.py          # XP and leveling
├── reputation_manager.py         # Reputation tracking
├── mastery_system.py             # Recipe mastery
├── achievement_tracker.py        # Achievement system
├── specialization_manager.py     # Specialization choices
├── season_manager.py             # Season progression
├── data/
│   ├── stat_config.json         # Stat definitions
│   ├── achievements.json        # Achievement definitions
│   ├── specializations.json     # Specialization options
│   └── xp_curves.json           # XP progression curves
├── saves/
│   └── progression_save.json    # Player progress
└── tests/
    └── test_progression.py      # Unit tests
```

### Key Classes

```python
class Player:
    name: str
    current_season: int
    stats: Dict[str, int]  # stat_name -> value (0-100)
    xp: Dict[str, int]  # stat_name -> total XP
    reputation: Dict[str, int]  # region -> reputation (0-100)
    recipe_mastery: Dict[str, int]  # recipe_id -> mastery (0-100)
    achievements: List[Achievement]
    specializations: List[Specialization]
    season_history: List[SeasonSummary]

class StatManager:
    def add_xp(stat: str, amount: int) -> int  # returns new stat value
    def calculate_stat_from_xp(xp: int) -> int
    def get_milestone_level(stat_value: int) -> str
    def check_milestone_crossed(old_value: int, new_value: int) -> bool

class ReputationManager:
    def gain_reputation(region: str, amount: int)
    def lose_reputation(region: str, amount: int)
    def get_reputation_level(region: str) -> str
    def get_reputation_modifiers(region: str) -> Dict[str, float]

class MasterySystem:
    def add_mastery(recipe_id: str, amount: int)
    def get_mastery_level(recipe_id: str) -> str
    def get_mastery_bonuses(recipe_id: str) -> Dict[str, float]
    def check_batch_crafting_unlocked(recipe_id: str) -> bool

class AchievementTracker:
    def check_achievements(player: Player, action: str)
    def unlock_achievement(achievement_id: str)
    def get_completion_percentage() -> float
    def get_achievement_rewards(achievement_id: str) -> List[Reward]

class SpecializationManager:
    def choose_specialization(specialization_id: str, season: int)
    def get_active_specializations() -> List[Specialization]
    def get_available_specializations(player: Player) -> List[Specialization]
    def apply_specialization_bonuses() -> Dict[str, float]

class SeasonManager:
    def advance_season()
    def generate_season_summary(player: Player) -> SeasonSummary
    def apply_season_carryover(player: Player)
    def check_season_completion(player: Player) -> bool
```

## Testing Goals

### Success Metrics
- [ ] Progression feels rewarding at all stages
- [ ] Stats feel impactful on gameplay
- [ ] XP gains feel fair and consistent
- [ ] Reputation system creates meaningful opportunities
- [ ] Recipe mastery provides satisfying growth
- [ ] Achievements encourage diverse play
- [ ] Specializations create distinct builds
- [ ] Season progression feels natural
- [ ] Balance between stats is appropriate
- [ ] Pacing maintains engagement across 5 seasons

### Data Collection
- Track XP gain rates per activity
- Measure time to reach stat milestones
- Note which specializations are most popular
- Identify stat imbalances
- Record player feedback on pacing

## Integration Path to Godot

### Phase 1 Output
- Validated XP formulas and curves
- Balanced stat effects
- Tested progression pacing
- Achievement system design

### Phase 2 Requirements
- Player data format for save system
- Stat progression formulas
- Achievement definitions
- Specialization mechanics

### Phase 3 Godot Implementation
- Port progression systems to GDScript
- Create stat display UI
- Implement achievement notifications
- Add specialization selection UI
- Connect to save system

## Known Challenges

### Challenge 1: Progression Pacing
- **Problem**: Too fast = trivialize content, too slow = frustration
- **Mitigation**: Iterative testing, adjustable XP curves
- **Test in minigame**: Simulate full 5-season progression

### Challenge 2: Stat Balance
- **Problem**: Some stats may be more valuable than others
- **Mitigation**: Ensure all stats have clear, useful effects
- **Test in minigame**: Track which stats players prioritize

### Challenge 3: Specialization Lock-in
- **Problem**: Wrong choice may feel bad long-term
- **Mitigation**: All choices viable, clear previews
- **Test in minigame**: Can all specialization combos succeed?

### Challenge 4: Achievement Fatigue
- **Problem**: Too many achievements = overwhelming
- **Mitigation**: Focus on meaningful achievements
- **Test in minigame**: Do achievements enhance or distract?

## Next Steps After Completion

1. **Document progression curves** - XP rates, stat scaling
2. **Export progression data** - Prepare for Godot import
3. **Create balance guide** - How to tune progression
4. **Write integration guide** - Port to Godot
5. **Design UI mockups** - Stat screens, achievement notifications
6. **Begin Godot prototype** - Implement validated progression

## Timeline Summary

- **Week 1-2**: Core stats and XP system
- **Week 3**: Reputation and mastery systems
- **Week 4**: Specializations and season progression
- **Week 5**: Balance testing and pacing tuning
- **Week 6**: Integration prep and documentation

## Success Definition

This minigame is successful if:
1. Progression feels rewarding throughout all seasons
2. All stats feel impactful and balanced
3. XP gains feel fair and consistent
4. Reputation provides meaningful opportunities
5. Recipe mastery creates satisfying growth
6. Specializations enable distinct playstyles
7. All mechanics are validated and ready for Godot implementation
