# Medium Roadmap: Inventory System Text-Based Minigame

## Overview
Create a standalone text-based minigame that implements inventory management, storage systems, item organization, and degradation mechanics. This prototype will validate inventory capacity, sorting/filtering, and item lifecycle before full Godot implementation.

## Core Features to Implement

### Phase 1: Basic Inventory (Week 1-2)

#### 1.1 Inventory Types
- **Four separate inventories**
  1. **Ingredient Inventory**: Raw materials
  2. **Potion Inventory**: Completed potions
  3. **Equipment Inventory**: Tools, containers
  4. **Recipe Book**: Known recipes (special inventory)

- **Capacity system**
  - Each inventory has slot limit
  - Different limits per season
  - Upgradeable capacity
  - Visual capacity indicator (e.g., "45/50")

- **Item stacking**
  - Identical items stack
  - Stack limits per item type
  - Clear stack count display

#### 1.2 Ingredient Inventory
- **Ingredient properties**
  - Name and ID
  - Type (17 ingredient types)
  - Rarity (Common to Legendary)
  - Quality (Poor to Perfect)
  - Quantity owned
  - Freshness (time-sensitive)

- **Season-based capacity**
  - Season 1: Basic satchel (50 slots)
  - Season 2: Shop storage (200 slots) + personal (100 slots)
  - Season 3: Travel case (75 slots) + locker (150 slots)
  - Season 4: Royal provisions (100 slots) + archive (300 slots)
  - Season 5: Master vault (unlimited)

- **Organization features**
  - Sort by: Type, Rarity, Quantity, Freshness, Alphabetical
  - Filter by: Element, Season acquired, Quality
  - Search by name
  - Favorite/pin system

#### 1.3 Potion Inventory
- **Potion properties**
  - Name and ID
  - ESENS notation
  - Quality tier (Poor to Masterwork)
  - Potency percentage
  - Stability (shelf life)
  - Creation date
  - Creator signature

- **Season-based capacity**
  - Season 1: Student locker (20 potions)
  - Season 2: Shop shelves (50) + personal case (20)
  - Season 3: Combat belt (10 quick-access) + storage (40)
  - Season 4: Investigation kit (30) + court supplies (50)
  - Season 5: Master collection (100 display + unlimited storage)

- **Organization features**
  - Sort by: Effect type, Quality, Creation date, Value
  - Filter by: Element, Target, Duration, Combat-ready
  - Search by name or effect
  - Quick-access hotbar (for combat)

### Phase 2: Equipment & Recipe Book (Week 3)

#### 2.1 Equipment Inventory
- **Tool types**
  - **Mortar & Pestle**: Grinding precision
  - **Alembic**: Distillation quality
  - **Cauldron**: Batch size, heat control
  - **Vials & Bottles**: Storage containers
  - **Preservation Containers**: Ingredient freshness
  - **Travel Equipment**: Gathering efficiency

- **Tool properties**
  - Quality tier (Student to Legendary)
  - Durability (current/max)
  - Bonuses provided
  - Special properties
  - Equipped status

- **Quality tiers**
  - Student Grade (Season 1): Basic bonuses
  - Professional Grade (Season 2+): Better bonuses
  - Master Crafted (Season 4+): Significant bonuses
  - Legendary (Season 5 or quests): Unique abilities

- **Tool degradation**
  - Durability decreases with use
  - Broken tools = reduced effectiveness
  - Repair mechanic (costs gold/materials)
  - Maintenance extends life

#### 2.2 Recipe Book
- **Recipe organization**
  - **Learned**: Can craft, have recipe
  - **Discovered**: Seen but need practice
  - **Fragment**: Incomplete knowledge
  - **Mastered**: High success rate, can innovate

- **Recipe properties**
  - ESENS notation
  - Ingredient list with quantities
  - Difficulty rating
  - Success requirements (stat minimums)
  - Effect description
  - Historical notes/lore
  - Personal notes (player-added)
  - Mastery level (0-100)

- **Recipe sources**
  - Lessons and tutorials
  - NPC teachings
  - Experimentation discoveries
  - Purchased from merchants
  - Found in ancient texts
  - Inherited from family
  - Quest rewards

- **Recipe book features**
  - Sort by: Difficulty, Mastery, Season learned
  - Filter by: Ingredient type, Effect, Element
  - Search by name or effect
  - Bookmark favorites
  - Quick-craft from recipe (if ingredients available)

### Phase 3: Advanced Features (Week 4)

#### 3.1 Storage Systems
- **Multiple storage locations**
  - Personal inventory (on-hand)
  - Shop storage (Season 2)
  - Bank/vault (secure storage)
  - Tournament locker (Season 3)
  - Royal archive (Season 4)

- **Transfer mechanics**
  - Move items between locations
  - Bulk transfer options
  - Transfer costs (time or gold)
  - Access restrictions (location-based)

- **Storage upgrades**
  - Increase capacity
  - Add organization features
  - Improve preservation
  - Unlock new storage types

#### 3.2 Item Degradation & Freshness
- **Freshness system**
  - Ingredients degrade over time
  - Fresh (100%) → Aging (75%) → Stale (50%) → Spoiled (25%) → Ruined (0%)
  - Freshness affects potion quality
  - Some ingredients immune (minerals, crystals)

- **Freshness tracking**
  - Days since acquisition
  - Display freshness percentage
  - Visual indicators (colors, icons)
  - Warnings for spoiling soon

- **Preservation mechanics**
  - Preservation containers slow decay
  - Some storage types preserve better
  - Preservation potions extend life
  - Proper storage matters (temperature)

- **Potion stability**
  - Potions also degrade (slower than ingredients)
  - Stability based on crafting quality
  - Poor quality: Degrades quickly
  - Masterwork: Nearly permanent

#### 3.3 Item Display & Value
- **Display mechanics (Season 2+)**
  - Display rare ingredients in shop
  - Show off rare potions
  - Prestige bonus to reputation
  - Attracts customers

- **Item valuation**
  - Auto-calculate item worth
  - Factors: Rarity, quality, freshness, demand
  - Compare to market prices
  - Track inventory total value

- **Bulk operations**
  - Sell multiple items at once
  - Discard spoiled ingredients
  - Mark items for display
  - Quick-sort inventory

### Phase 4: Integration & Polish (Week 5)

#### 4.1 Inventory UI/UX
- **Clear visualization**
  - Grid or list view
  - Item icons/symbols
  - Color coding for rarity
  - Status indicators (fresh, equipped, favorited)

- **Quick actions**
  - Use/consume item
  - Equip tool
  - Transfer to storage
  - Sell/discard
  - View details

- **Detail views**
  - Full item information
  - Usage history (potions)
  - Lore and notes (recipes)
  - Related items (ingredients in recipe)

#### 4.2 Inventory Management Challenges
- **Capacity constraints**
  - Must make choices about what to carry
  - Encourages planning
  - Storage management strategy

- **Freshness pressure**
  - Use ingredients before spoiling
  - Trade-off between variety and waste
  - Preservation costs vs. buying fresh

- **Tool maintenance**
  - Balance use with durability
  - Repair costs vs. replacement
  - Upgrade decisions

#### 4.3 Testing & Balance
- **Capacity balance**
  - Is inventory too large/small?
  - Do upgrades feel worthwhile?
  - Frustration vs. strategic depth

- **Degradation rates**
  - Too fast = frustrating waste
  - Too slow = no pressure
  - Test different rates

- **Organization effectiveness**
  - Can players find items quickly?
  - Are sort/filter options useful?
  - Search function adequate?

## Technical Implementation

### Technology Stack
- **Language**: Python 3.x
- **Data**: JSON for items, recipes, tools
- **Interface**: Command-line with clear item lists
- **Time**: Day tracking for freshness

### File Structure
```
inventory_minigame/
├── main.py                        # Game loop and UI
├── inventory_manager.py           # Core inventory logic
├── ingredient_inventory.py        # Ingredient-specific
├── potion_inventory.py            # Potion-specific
├── equipment_inventory.py         # Equipment-specific
├── recipe_book.py                 # Recipe management
├── freshness_system.py            # Degradation mechanics
├── storage_manager.py             # Multiple storage locations
├── data/
│   ├── ingredients.json          # Ingredient definitions
│   ├── potions.json              # Potion definitions
│   ├── tools.json                # Tool definitions
│   ├── recipes.json              # Recipe definitions
│   └── storage_config.json       # Storage options
├── saves/
│   └── inventory_save.json       # Player inventory state
└── tests/
    └── test_inventory.py         # Unit tests
```

### Key Classes

```python
class Inventory:
    inventory_type: str
    capacity: int
    items: List[Item]

    def add_item(item: Item, quantity: int) -> bool
    def remove_item(item_id: str, quantity: int) -> bool
    def get_item(item_id: str) -> Optional[Item]
    def is_full() -> bool
    def sort(criteria: str)
    def filter(criteria: Dict) -> List[Item]
    def search(query: str) -> List[Item]

class Ingredient(Item):
    id: str
    name: str
    type: IngredientType (enum of 17 types)
    rarity: Rarity
    quality: Quality
    quantity: int
    freshness: float (0.0 to 1.0)
    acquisition_date: int (day number)

    def calculate_value() -> int
    def degrade(days_passed: int, storage_quality: float)

class Potion(Item):
    id: str
    name: str
    esens_notation: str
    quality: Quality
    potency: float
    stability: float (0.0 to 1.0)
    creation_date: int
    creator: str

    def calculate_value() -> int
    def degrade(days_passed: int)

class Tool(Item):
    id: str
    name: str
    tool_type: ToolType
    quality_tier: QualityTier
    durability: int
    max_durability: int
    bonuses: Dict[str, float]
    equipped: bool

    def repair(amount: int) -> int  # returns cost
    def use() -> None  # decreases durability
    def is_broken() -> bool

class Recipe:
    id: str
    name: str
    esens_notation: str
    ingredients: List[IngredientRequirement]
    difficulty: int
    effects: List[str]
    unlocked: bool
    mastery: int
    notes: str  # player-added

    def can_craft(inventory: Inventory) -> bool
    def get_missing_ingredients(inventory: Inventory) -> List[str]

class FreshnessSystem:
    def calculate_freshness(ingredient: Ingredient, days_passed: int, storage_quality: float) -> float
    def apply_degradation(ingredient: Ingredient, days: int)
    def check_spoilage(ingredient: Ingredient) -> bool

class StorageManager:
    storages: Dict[str, Inventory]

    def transfer_item(item_id: str, from_storage: str, to_storage: str, quantity: int)
    def access_storage(storage_id: str, location: str) -> bool
    def upgrade_storage(storage_id: str, upgrade_type: str) -> int  # returns cost
```

## Testing Goals

### Success Metrics
- [ ] Inventory management feels strategic, not tedious
- [ ] Capacity constraints create interesting decisions
- [ ] Sorting/filtering helps find items quickly
- [ ] Freshness system adds pressure without frustration
- [ ] Tool degradation balances use with maintenance
- [ ] Recipe book is easy to navigate
- [ ] Storage systems feel worthwhile
- [ ] Bulk operations save time
- [ ] Item display adds meaningful prestige
- [ ] Visual organization is clear and helpful

### Data Collection
- Track inventory fullness over time
- Measure item spoilage rates
- Note which organization features are used most
- Identify confusing UI elements
- Record player feedback on capacity balance

## Integration Path to Godot

### Phase 1 Output
- Validated inventory formulas
- Balanced capacity constraints
- Tested degradation rates
- Organization patterns that work

### Phase 2 Requirements
- Item data formats for Godot
- Inventory save format
- Storage configuration
- Recipe book structure

### Phase 3 Godot Implementation
- Port inventory systems to GDScript
- Create visual inventory UI
- Implement drag-and-drop
- Add item tooltips and details
- Connect to save system

## Known Challenges

### Challenge 1: Capacity Balance
- **Problem**: Too small = frustrating, too large = meaningless
- **Mitigation**: Test with various capacities, gradual upgrades
- **Test in minigame**: Track when players hit capacity

### Challenge 2: Freshness Frustration
- **Problem**: Ingredients spoiling feels like punishment
- **Mitigation**: Clear warnings, preservation options, reasonable rates
- **Test in minigame**: Do players feel pressured or punished?

### Challenge 3: Organization Complexity
- **Problem**: Too many options = overwhelming
- **Mitigation**: Good defaults, intuitive categories
- **Test in minigame**: Can players find items in <5 seconds?

### Challenge 4: Tool Maintenance Tedium
- **Problem**: Constant repairs become chore
- **Mitigation**: Durability lasts reasonable time, batch repairs
- **Test in minigame**: How often do tools break?

## Next Steps After Completion

1. **Document inventory patterns** - Best practices for organization
2. **Export inventory data** - Prepare for Godot import
3. **Create UI mockups** - Visual inventory screens
4. **Write integration guide** - Port to Godot
5. **Design drag-and-drop** - Interaction patterns
6. **Begin Godot prototype** - Implement validated inventory

## Timeline Summary

- **Week 1-2**: Basic inventory types and organization
- **Week 3**: Equipment and recipe book systems
- **Week 4**: Advanced features (storage, degradation)
- **Week 5**: Polish, testing, UI/UX refinement
- **Week 6**: Integration prep and documentation

## Success Definition

This minigame is successful if:
1. Inventory management is engaging without being tedious
2. Capacity constraints create strategic decisions
3. Organization tools help players find items quickly
4. Freshness system adds pressure without frustration
5. Tool maintenance is meaningful but not annoying
6. Recipe book is intuitive and helpful
7. All mechanics are validated and ready for Godot implementation
