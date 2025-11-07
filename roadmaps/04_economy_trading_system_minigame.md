# Medium Roadmap: Economy/Trading System Text-Based Minigame

## Overview
Create a standalone text-based minigame that implements shop management, dynamic pricing, customer interactions, and trading mechanics. This prototype will validate economic balance, supply/demand systems, and ethical pricing dilemmas before full Godot implementation.

## Core Features to Implement

### Phase 1: Basic Shop Operations (Week 1-2)

#### 1.1 Shop Setup
- **Shop properties**
  - Shop name and location
  - Display shelves (visible inventory)
  - Storage room (back stock)
  - Workshop area (crafting space)
  - Reputation board (reviews, requests)
  - Ledger (financial tracking)

- **Starting conditions**
  - Initial gold (1000-2000)
  - Basic inventory (common ingredients, simple potions)
  - Basic tools (student-grade equipment)
  - Clean reputation (neutral start)

- **Shop display**
  - Show shelves with stocked potions
  - Display prices clearly
  - Show available storage space
  - Track gold balance

#### 1.2 Customer System
- **Customer types**
  - **Walk-ins**: Random needs, random budgets
  - **Regulars**: Returning customers, building relationships
  - **Special orders**: Custom requests with deadlines
  - **Emergency cases**: Time pressure, moral choices

- **Customer attributes**
  - Budget (poor, moderate, wealthy)
  - Ailment/need (healing, buff, specific effect)
  - Urgency (casual, hurried, desperate)
  - Haggling willingness
  - Affinity toward player (if regular)

- **Customer generation**
  - Random arrival system
  - Frequency based on reputation
  - More regulars as reputation grows
  - Special events trigger emergency customers

#### 1.3 Basic Transactions
- **Selling potions**
  - Customer requests type/effect
  - Player offers matching potion
  - Price negotiation (optional haggling)
  - Transaction completes, gold added

- **Buying ingredients**
  - Visit merchant menu
  - Browse available ingredients
  - Purchase with gold
  - Add to inventory

- **Simple pricing**
  - Fixed base prices initially
  - No dynamic pricing yet
  - Profit margin calculation shown

### Phase 2: Dynamic Economy (Week 3)

#### 2.1 Pricing System
- **Price calculation formula**
  ```
  Price = (IngredientCost * DifficultyMultiplier * QualityBonus)
          * ReputationModifier * SupplyDemandModifier
  ```

- **Ingredient costs**
  - Common: 5-20 gold
  - Uncommon: 25-75 gold
  - Rare: 100-300 gold
  - Very Rare: 400-1000 gold
  - Legendary: 1500+ gold

- **Difficulty multiplier**
  - Trivial: ×1.5
  - Easy: ×2.0
  - Moderate: ×2.5
  - Hard: ×3.0
  - Very Hard: ×3.5
  - Legendary: ×5.0

- **Quality bonus**
  - Poor: -25%
  - Standard: 0%
  - Fine: +25%
  - Exceptional: +50%
  - Masterwork: +100%

- **Reputation modifier**
  - Unknown: -10%
  - Known: 0%
  - Respected: +5%
  - Renowned: +10%
  - Legendary: +20%

#### 2.2 Supply & Demand
- **Demand tracking**
  - Track customer requests by potion type
  - High demand = price increase
  - Low demand = price decrease

- **Supply tracking**
  - Track your inventory by potion type
  - Abundant stock = price decrease
  - Scarce stock = price increase

- **Seasonal effects**
  - Winter = more healing potions needed
  - Spring = more growth/farming potions
  - Summer = more energy/stamina potions
  - Fall = more preservation potions

- **Dynamic ingredient pricing**
  - Merchants adjust prices based on season
  - Rare ingredients fluctuate more
  - Player can speculate (buy low, sell high)

#### 2.3 Competitor System
- **Rival shops**
  - 2-3 other alchemists in region
  - Compete for customers
  - Affect market prices

- **Competitor actions**
  - Undercut prices (temporary)
  - Special promotions
  - Exclusive ingredients
  - Reputation campaigns

- **Market share**
  - Track percentage of customers you attract
  - Affected by price, reputation, availability
  - Higher market share = more customers

### Phase 3: Advanced Shop Management (Week 4)

#### 3.1 Shop Upgrades
- **Upgrade types**
  - **Better Shelves**: Display more potions
  - **Larger Storage**: Store more inventory
  - **Workshop Tools**: Craft faster/better
  - **Advertising**: Attract more customers
  - **Security**: Prevent theft
  - **Aesthetics**: Reputation bonus

- **Upgrade costs**
  - Tier 1: 500-1000 gold
  - Tier 2: 1500-2500 gold
  - Tier 3: 3000-5000 gold

- **Upgrade effects**
  - Measurable benefits (more capacity, faster craft)
  - Long-term investment
  - Some upgrades unlock new features

#### 3.2 Special Orders & Contracts
- **Special order system**
  - NPCs request specific potions
  - Deadline for completion
  - Bonus payment for on-time delivery
  - Reputation penalty for failure

- **Contract types**
  - **Bulk orders**: Multiple potions, same type
  - **Custom recipes**: Specific effects required
  - **Rare ingredients**: Source hard-to-find materials
  - **Exclusive supply**: Ongoing relationship

- **Order management**
  - Track active orders
  - Show deadlines clearly
  - Prioritize based on urgency/reward

#### 3.3 Ledger & Finances
- **Income tracking**
  - Daily revenue
  - Weekly summary
  - Best-selling products
  - Most profitable customers

- **Expense tracking**
  - Ingredient purchases
  - Tool maintenance
  - Shop upgrades
  - Miscellaneous costs

- **Financial reports**
  - Profit/loss statement
  - Cash flow analysis
  - Break-even point
  - Growth trends

- **Financial goals**
  - Reach 10,000 gold
  - Maintain positive cash flow for month
  - Achieve 60% profit margin

### Phase 4: Ethical & Social Dimensions (Week 5)

#### 4.1 Ethical Pricing Dilemmas
- **Scenario: Poor Sick Villager**
  - Customer can't afford healing potion
  - Options:
    - Charge full price (max profit, -affinity)
    - Discount (less profit, +affinity)
    - Give free (no profit, ++affinity, +reputation)
  - Consequences affect reputation and relationships

- **Scenario: Plague Outbreak**
  - High demand for healing potions
  - Options:
    - Exploit shortage (high profit, reputation hit)
    - Fair pricing (moderate profit, reputation bonus)
    - Below cost (loss, major reputation gain)
  - Long-term community effects

- **Scenario: Dangerous Potion Request**
  - Customer wants harmful/illegal potion
  - Options:
    - Refuse (no profit, +ethics reputation)
    - Sell at high price (profit, -ethics, legal risk)
    - Report to authorities (+legal reputation)
  - May affect future customer types

- **Scenario: Competitor Sabotage**
  - Opportunity to sabotage rival shop
  - Options:
    - Sabotage (eliminate competitor, -ethics)
    - Compete fairly (harder but ethical)
    - Help competitor (ally potential, market share loss)
  - Affects reputation and relationships

#### 4.2 Customer Relationships
- **Regular customer system**
  - Customers become regulars after 3+ purchases
  - Build affinity through fair treatment
  - Regulars provide:
    - Steady income
    - Word-of-mouth advertising
    - Tips about market/ingredients
    - Defend your reputation

- **Customer preferences**
  - Remember favorite potions
  - Loyalty discounts for regulars
  - Refer friends if happy
  - Leave if consistently dissatisfied

- **Reviews & reputation**
  - Customers leave reviews after purchase
  - Good reviews: +reputation, more customers
  - Bad reviews: -reputation, fewer customers
  - Can respond to reviews (damage control)

#### 4.3 Merchant Relationships
- **Merchant types**
  - **General Merchants**: Common ingredients, fair prices
  - **Specialty Suppliers**: Rare ingredients, premium prices
  - **Black Market**: Illegal/unethical, no questions, expensive
  - **Guild Traders**: Members-only, better prices, ethical
  - **Traveling Caravans**: Random inventory, bargains

- **Negotiation system**
  - Haggle for better prices
  - Bulk discounts
  - Loyalty discounts (regular purchases)
  - Trade potions for ingredients

- **Merchant affinity**
  - Build relationships for better deals
  - Exclusive access to rare ingredients
  - Early notification of shipments
  - Credit lines (buy now, pay later)

## Technical Implementation

### Technology Stack
- **Language**: Python 3.x
- **Data**: JSON for items, customers, shop state
- **Interface**: Command-line with clear menus
- **Time**: Day/week progression system

### File Structure
```
economy_minigame/
├── main.py                      # Game loop and UI
├── shop_manager.py              # Shop operations
├── customer_system.py           # Customer generation and interaction
├── pricing_engine.py            # Dynamic pricing calculations
├── inventory_manager.py         # Inventory tracking
├── ledger_system.py             # Financial tracking
├── merchant_system.py           # Buying from merchants
├── data/
│   ├── shop_config.json        # Shop properties
│   ├── customers.json          # Customer templates
│   ├── merchants.json          # Merchant definitions
│   ├── market_data.json        # Supply/demand state
│   └── upgrades.json           # Shop upgrade options
├── saves/
│   └── shop_save.json          # Progress save
└── tests/
    └── test_economy.py         # Unit tests
```

### Key Classes

```python
class Shop:
    name: str
    gold: int
    display_inventory: List[Potion]  # visible to customers
    storage_inventory: List[Potion]  # back stock
    ingredient_inventory: Dict[str, int]
    tools: List[Tool]
    reputation: int
    upgrades: List[Upgrade]
    market_share: float

class Customer:
    id: str
    name: str
    customer_type: CustomerType (WalkIn, Regular, Emergency)
    budget: int
    ailment: str
    urgency: int (1-10)
    affinity: float (if regular)
    haggle_willingness: float

class PricingEngine:
    def calculate_price(potion: Potion, shop: Shop, market: MarketData) -> int
    def apply_reputation_modifier(price: int, reputation: int) -> int
    def apply_supply_demand(price: int, demand: float, supply: float) -> int
    def negotiate_price(base_price: int, customer: Customer, player_skill: int) -> int

class MarketData:
    supply: Dict[str, float]  # by potion type
    demand: Dict[str, float]  # by potion type
    season: Season
    competitor_prices: Dict[str, int]

    def update_supply(potion_type: str, quantity_change: int)
    def update_demand(potion_type: str, purchases: int)
    def advance_season()

class Ledger:
    daily_revenue: List[int]
    daily_expenses: List[int]
    transactions: List[Transaction]

    def record_sale(potion: Potion, price: int)
    def record_expense(item: str, cost: int)
    def generate_report(period: str) -> Report

class Merchant:
    id: str
    name: str
    merchant_type: MerchantType
    inventory: Dict[str, Ingredient]
    base_prices: Dict[str, int]
    affinity: float

    def get_price(ingredient: Ingredient) -> int  # with modifiers
    def negotiate(player_skill: int, affinity: float) -> float  # discount percentage
```

## Testing Goals

### Success Metrics
- [ ] Shop management feels engaging, not tedious
- [ ] Pricing feels fair and understandable
- [ ] Supply/demand system creates interesting decisions
- [ ] Ethical dilemmas feel meaningful
- [ ] Profit margins are achievable but challenging
- [ ] Upgrades feel worthwhile
- [ ] Customer relationships develop naturally
- [ ] Financial tracking is clear and useful
- [ ] Balance between profit and ethics is challenging

### Data Collection
- Track average daily profit
- Measure time to afford each upgrade tier
- Note which ethical choices are most popular
- Identify overpowered/underpowered strategies
- Record player feedback on economic balance

## Integration Path to Godot

### Phase 1 Output
- Validated pricing formulas
- Balanced supply/demand system
- Tested ethical dilemma consequences
- Customer generation algorithms

### Phase 2 Requirements
- Shop data format for Godot
- Customer templates
- Market state tracking
- Ledger UI patterns

### Phase 3 Godot Implementation
- Port shop management to GDScript
- Create visual shop UI
- Implement customer animations/portraits
- Add visual ledger/reports
- Connect to save system and other gameplay systems

## Known Challenges

### Challenge 1: Economic Balance
- **Problem**: Too easy to make money = no challenge, too hard = frustrating
- **Mitigation**: Tune ingredient costs, pricing formulas, demand rates
- **Test in minigame**: Track profit over time, adjust as needed

### Challenge 2: Supply/Demand Complexity
- **Problem**: Players may not understand dynamic pricing
- **Mitigation**: Clear explanations, visual indicators (arrows, colors)
- **Test in minigame**: Can players predict price changes?

### Challenge 3: Ethical Dilemma Impact
- **Problem**: Consequences may feel insignificant or too punishing
- **Mitigation**: Balance reputation/gold trade-offs carefully
- **Test in minigame**: Do players feel tension in decisions?

### Challenge 4: Shop Management Tedium
- **Problem**: Too much micromanagement becomes boring
- **Mitigation**: Automate repetitive tasks, focus on decisions
- **Test in minigame**: Is restocking fun or chore?

## Next Steps After Completion

1. **Document economic patterns** - What strategies work best
2. **Export shop data formats** - Prepare for Godot import
3. **Create shop design guide** - How to balance economy
4. **Write integration guide** - Port economy to Godot
5. **Design UI mockups** - Visual shop interface
6. **Begin Godot prototype** - Implement validated economy

## Timeline Summary

- **Week 1-2**: Basic shop operations and transactions
- **Week 3**: Dynamic pricing and supply/demand
- **Week 4**: Advanced management and upgrades
- **Week 5**: Ethical dilemmas and relationships
- **Week 6**: Integration prep and documentation

## Success Definition

This minigame is successful if:
1. Shop management is engaging with meaningful decisions
2. Economic systems feel fair and understandable
3. Supply/demand creates interesting opportunities
4. Ethical dilemmas provide genuine tension
5. Customer relationships develop naturally
6. Profit/ethics balance is challenging but achievable
7. All mechanics are validated and ready for Godot implementation
