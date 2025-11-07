# Medium Roadmap: Crafting System Text-Based Minigame

## Overview
Create a standalone text-based minigame that implements the ESENS-based potion crafting system. This prototype will validate the crafting mechanics, success/failure calculations, and quality determination before full Godot implementation.

## Core Features to Implement

### Phase 1: Basic Crafting Loop (Week 1-2)

#### 1.1 Recipe System
- **Text-based recipe display**
  - Show ESENS notation clearly
  - Display ingredient requirements
  - Show difficulty rating (0-100)
  - Display effect descriptions

- **Recipe database**
  - Implement JSON storage for recipes
  - Start with 10-15 simple recipes (3-4 ingredients)
  - Include recipes of varying difficulty (Trivial to Hard)

- **Recipe learning progression**
  - Locked vs. unlocked recipes
  - Discovery system (mark as "discovered" after first attempt)
  - Mastery tracking (0-100 per recipe)

#### 1.2 Ingredient System
- **Ingredient database**
  - All 17 ingredient types with properties
  - Rarity system (Common to Legendary)
  - Quality tiers (Poor, Standard, Fine, Exceptional, Perfect)

- **Player ingredient inventory**
  - Simple list-based inventory
  - Track quantity and quality per ingredient
  - Starting inventory with common ingredients

- **Ingredient properties**
  - Element associations
  - Base effects (matching ESENS notation)
  - Quality modifiers to potency

#### 1.3 Core Crafting Mechanics
- **Recipe selection interface**
  - List available recipes
  - Filter by difficulty, learned status
  - Show requirements vs. current inventory

- **Ingredient selection**
  - Choose ingredients from inventory
  - Validate against recipe requirements
  - Option to substitute (if high Intuition)

- **Success calculation**
  ```
  Success = Base(50%) + (Stat/2) + ToolBonus + PrepBonus - Difficulty + d20
  ```
  - Implement dice rolling for randomness
  - Show success probability before crafting
  - Clear feedback on success/failure

- **Quality determination**
  - Quality tiers based on success margin
  - Critical success (Natural 20 or >150%)
  - Critical failure (Natural 1 or <25%)
  - Ingredient quality affects final potion quality

### Phase 2: Player Stats & Progression (Week 3)

#### 2.1 Crafting Stats
- **Alchemical Knowledge (0-100)**
  - Unlocks recipe complexity
  - Affects success rate
  - Gains XP from crafting and study

- **Precision (0-100)**
  - Reduces failure chance
  - Improves quality consistency
  - Gains XP from successful crafts

- **Intuition (0-100)**
  - Enables ingredient substitution
  - Reveals hidden properties
  - Gains XP from experimentation

#### 2.2 Tool System
- **Tool types**
  - Mortar & Pestle
  - Alembic
  - Cauldron

- **Tool quality tiers**
  - Student Grade (Season 1)
  - Professional Grade
  - Master Crafted

- **Tool effects**
  - Bonus to success chance
  - Quality improvements
  - Tool degradation over use

#### 2.3 Experience & Mastery
- **XP system**
  - Award XP per craft (10-100 based on difficulty)
  - Award XP for failures (5 XP consolation)
  - XP increases stats gradually

- **Recipe mastery**
  - Track per-recipe mastery (0-100)
  - Mastery levels unlock bonuses:
    - Novice (0-20): Base success
    - Competent (21-40): +10% success
    - Proficient (41-60): +20% success
    - Expert (61-80): +30% success
    - Master (81-100): +40% success

### Phase 3: Advanced Mechanics (Week 4)

#### 3.1 Experimentation System
- **Free experimentation**
  - Combine any ingredients without recipe
  - ESENS parser generates notation
  - Higher failure rate
  - Possible new recipe discovery

- **Guided experimentation**
  - Modify one ingredient in known recipe
  - Lower risk than free mode
  - Creates recipe variants

- **Innovation unlocks**
  - Knowledge 50+: Simple variants
  - Knowledge 75+: Combine concepts
  - Knowledge 90+: Entirely new potions

#### 3.2 Batch Crafting
- **Batch mode unlocks**
  - Available once recipe mastery reaches 60+
  - Craft multiple potions in one session

- **Batch mechanics**
  - Quality consistency based on Precision
  - Batch size limited by cauldron quality
  - Slight time efficiency bonus

- **Bulk operations**
  - Auto-consume correct ingredients
  - Summary of results (successes/failures)
  - Experience still awarded per potion

#### 3.3 Preparation Mini-games
- **Ingredient preparation**
  - Simple text-based timing challenges
  - Grinding: Hit optimal pressure (1-10 scale)
  - Distilling: Hit optimal temperature
  - Mixing: Hit optimal timing

- **Preparation bonuses**
  - Perfect preparation: +10% success
  - Good preparation: +5% success
  - Poor preparation: -5% success

- **Skip option**
  - Auto-prepare with average results
  - Useful for batch crafting

### Phase 4: Polish & Integration (Week 5)

#### 4.1 UI/UX Improvements
- **Clear visual hierarchy**
  - Color-coding for rarity
  - Symbols for quality tiers
  - Icons for ingredient types

- **Helpful feedback**
  - Explain success/failure reasons
  - Show stat gains clearly
  - Highlight newly unlocked recipes

- **Streamlined navigation**
  - Quick commands (shortcuts)
  - Clear menu structure
  - Help/tutorial system

#### 4.2 Balancing
- **Success rate tuning**
  - Ensure early recipes feel achievable
  - Test difficulty curve
  - Adjust stat scaling if needed

- **XP and progression pacing**
  - Should reach Proficient in Season 1
  - Expert by Season 3
  - Master by Season 5

- **Recipe distribution**
  - Balance between easy starter recipes
  - Gradual difficulty increase
  - Legendary recipes feel special

#### 4.3 Testing & Validation
- **Test scenarios**
  - New player experience (low stats)
  - Mid-game progression
  - End-game mastery

- **Edge cases**
  - All failures in a row (bad luck)
  - All critical successes (extreme luck)
  - Missing ingredients
  - Invalid substitutions

- **Data export**
  - Export recipe database format for Godot
  - Export ingredient database format
  - Document stat formulas clearly

## Technical Implementation

### Technology Stack
- **Language**: Python 3.x
- **Parser**: Existing ESENS_Parser.py
- **Data**: JSON for recipes, ingredients, save data
- **Interface**: Command-line with rich text formatting (colorama/rich library)

### File Structure
```
crafting_minigame/
├── main.py                 # Game loop and UI
├── crafting_engine.py      # Core crafting logic
├── recipe_manager.py       # Recipe handling
├── inventory_manager.py    # Ingredient inventory
├── player_stats.py         # Stats and progression
├── data/
│   ├── recipes.json       # Recipe database
│   ├── ingredients.json   # Ingredient database
│   └── tools.json         # Tool definitions
├── saves/
│   └── player_save.json   # Player progress
└── tests/
    └── test_crafting.py   # Unit tests
```

### Key Classes

```python
class Recipe:
    id: str
    name: str
    esens_notation: str
    ingredients: List[IngredientRequirement]
    difficulty: int
    effects: List[str]
    unlocked: bool
    mastery: int

class Ingredient:
    id: str
    name: str
    type: IngredientType (enum of 17 types)
    rarity: Rarity (Common to Legendary)
    quality: Quality (Poor to Perfect)
    properties: Dict[str, any]

class Player:
    knowledge: int (0-100)
    precision: int (0-100)
    intuition: int (0-100)
    inventory: Dict[str, Ingredient]
    tools: List[Tool]
    known_recipes: List[Recipe]
    xp: int

class CraftingEngine:
    def calculate_success(player, recipe, tools, prep_bonus) -> tuple[bool, int]
    def determine_quality(success_margin, ingredient_quality) -> Quality
    def apply_experience(player, recipe, success) -> None
    def check_discovery(ingredients) -> Optional[Recipe]
```

## Testing Goals

### Success Metrics
- [ ] Can craft simple potion within 5 minutes of starting
- [ ] Success/failure feels fair (not too easy, not frustrating)
- [ ] Progression feels rewarding (stats increase noticeably)
- [ ] Experimentation is risky but exciting
- [ ] Recipe mastery creates satisfying power growth
- [ ] Critical successes feel special and rewarding
- [ ] Failures provide useful feedback and partial progress

### Data Collection
- Track average success rates by difficulty tier
- Track time to reach mastery levels
- Identify recipes that are too hard/easy
- Note confusing UI elements
- Record player feedback on "feel"

## Integration Path to Godot

### Phase 1 Output
- Validated stat formulas
- Balanced recipe difficulty curve
- Tested success/failure rates
- Player progression pacing data

### Phase 2 Requirements
- Recipe JSON format for import
- Ingredient JSON format for import
- Tool system specifications
- UI/UX patterns that work well

### Phase 3 Godot Implementation
- Port Python crafting engine to GDScript
- Create visual crafting UI in Godot
- Integrate with ESENS parser
- Add crafting animations and effects
- Connect to save system

## Known Challenges

### Challenge 1: ESENS Complexity
- **Problem**: ESENS notation may be overwhelming for new players
- **Mitigation**: Progressive tutorial, hide complexity early
- **Test in minigame**: Start with simple potions (E+H, P+S)

### Challenge 2: Success Rate Balance
- **Problem**: Too much randomness feels unfair, too little is boring
- **Mitigation**: Clear stat thresholds, mastery reduces randomness
- **Test in minigame**: Try different d20 weights (d12, d10)

### Challenge 3: Ingredient Substitution
- **Problem**: How to determine valid substitutions?
- **Mitigation**: Similar ingredient types, require Intuition stat
- **Test in minigame**: Define substitution rules clearly

### Challenge 4: Progression Pacing
- **Problem**: Stats need to grow at right pace across 5 seasons
- **Mitigation**: Track XP rates, adjust scaling
- **Test in minigame**: Simulate crafting over time

## Next Steps After Completion

1. **Document learnings** - What worked, what didn't
2. **Export data formats** - Prepare for Godot import
3. **Create video demo** - Show crafting loop to team/testers
4. **Write integration guide** - How to port to Godot
5. **Begin Godot prototype** - Start with validated mechanics
6. **Iterate based on feedback** - Refine based on playtesting

## Timeline Summary

- **Week 1-2**: Basic crafting loop functional
- **Week 3**: Stats and progression working
- **Week 4**: Advanced mechanics (experimentation, batching)
- **Week 5**: Polish, testing, documentation
- **Week 6**: Integration prep and handoff to Godot phase

## Success Definition

This minigame is successful if:
1. Crafting loop feels satisfying and skill-based
2. Progression creates sense of growth and mastery
3. ESENS notation enhances rather than confuses
4. Experimentation is fun and rewarding
5. All mechanics are validated and balanced
6. Ready for confident Godot implementation
