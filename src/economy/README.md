# Economy System

Phase 4 implementation of PotionWorld's economy and trading system following the Hybrid API + Event Architecture.

## Features

- **Dynamic Pricing**: Quality, reputation, affinity, and market conditions affect prices
- **Market Dynamics**: Supply and demand fluctuate based on player and NPC actions
- **Transaction System**: Secure gold transfers with full event tracking
- **Combat Rewards**: Victory rewards scaled by difficulty and performance
- **Wallet Management**: Per-entity gold tracking with transaction history
- **Event-Driven**: Emits events for cross-system integration (quests, progression, relationships)

## Architecture

### Core Components

1. **Formulas** (`formulas.py`): Pure functions for economic mechanics
   - Ingredient and potion base pricing
   - Quality, reputation, and affinity modifiers
   - Market supply/demand calculations
   - Bulk discount calculations
   - Combat reward formulas
   - Profit margin analysis

2. **System** (`system.py`): EconomySystem API with event emission
   - `add_gold()` / `deduct_gold()` - Wallet operations
   - `calculate_potion_price()` - Dynamic potion pricing
   - `calculate_ingredient_price()` - Dynamic ingredient pricing
   - `execute_transaction()` - Secure transaction processing
   - `award_combat_reward()` - Victory gold distribution
   - `update_market()` - Market condition updates
   - Event emission for all economic actions

3. **Tests** (`tests/`): Comprehensive test coverage
   - Formula validation
   - System integration tests
   - Event emission verification
   - Edge case handling

4. **Testbed** (`testbed.py`): Interactive CLI for testing
   - Pricing simulations
   - Transaction testing
   - Market dynamics visualization
   - Combat reward testing
   - Built-in test runner

## Quick Start

### Run the Testbed

```bash
python systest.py --economy
```

Or directly:
```bash
python -m src.economy.testbed
```

### Run Tests

```bash
python -m src.economy.tests.test_formulas
python -m src.economy.tests.test_system
```

### Basic Usage

```python
from src.core.event_bus import EventBus
from src.core.data_structures import Quality, Potion, PriceModifiers
from src.economy.system import EconomySystem

bus = EventBus()
economy = EconomySystem(bus)

economy.add_gold("player", 1000, "starting_funds")

potion = Potion(
    id="healing_1",
    recipe_id="healing_potion",
    esens_notation="P+H20",
    quality=Quality.FINE,
    potency=1.1,
    created_by="player",
    created_at=time.time()
)

price, modifiers = economy.calculate_potion_price(
    potion=potion,
    ingredient_cost=50,
    difficulty=30,
    buyer_reputation=60,
    seller_affinity=2.0,
    demand=1.2,
    supply=0.8
)

transaction = economy.execute_transaction(
    buyer_id="customer",
    seller_id="player",
    item_id=potion.id,
    item_type="potion",
    quantity=1,
    unit_price=price,
    modifiers=modifiers
)

print(f"Sold for {price} gold!")
```

## Events

The economy system emits the following events:

- `TransactionCompleted`: Every successful transaction
- `GoldChanged`: When any wallet balance changes
- `PriceCalculated`: When prices are calculated (for analytics)
- `MarketShifted`: When market conditions change
- `ReputationEarned`: When economic actions affect reputation

## Pricing Mechanics

### Base Prices

**Ingredients by Rarity:**
- Common: 10 gold
- Uncommon: 50 gold
- Rare: 200 gold
- Very Rare: 700 gold
- Legendary: 2000 gold

**Potions:**
```
base_price = ingredient_cost × (1.5 + difficulty / 100)
```

Example:
```python
# Ingredients cost 50g, recipe difficulty 30
# Base: 50 × 1.8 = 90 gold
```

### Quality Modifiers

Quality affects final price:

- **Poor**: ×0.75 (75% of base)
- **Standard**: ×1.0 (100% of base)
- **Fine**: ×1.25 (125% of base)
- **Exceptional**: ×1.5 (150% of base)
- **Masterwork**: ×2.0 (200% of base)

### Reputation Modifier

Reputation (0-100) affects pricing:

```
modifier = (reputation - 50) / 250
```

Examples:
- Reputation 0: -20% (prices higher when buying, lower when selling)
- Reputation 50: 0% (neutral)
- Reputation 100: +20% (better prices)

### Affinity Modifier

NPC affinity (-5 to +5) affects their prices:

```
modifier = -affinity / 25
```

Examples:
- Affinity -5 (Nemesis): +20% markup
- Affinity 0 (Neutral): No change
- Affinity +5 (Devoted): -20% discount

### Market Dynamics

Supply and demand create dynamic pricing:

```
multiplier = demand / supply
clamped to 0.5x - 2.0x range
```

Examples:
- High demand (2.0), Low supply (0.5): ×2.0 (maximum)
- Equal: ×1.0 (neutral)
- Low demand (0.5), High supply (2.0): ×0.5 (minimum)

#### Demand Updates

Demand increases with transactions, decays over time:

```python
demand_increase = transactions_today × 0.05
new_demand = current × 0.9 + base_demand × 0.1
```

#### Supply Updates

Supply adjusts based on inventory changes:

```python
net_change = items_added - items_sold
new_supply = current + (net_change × 0.1)
```

### Final Price Calculation

All modifiers combine multiplicatively:

```
final = base × quality × demand × rarity × (1 + reputation) × (1 + affinity)
minimum = 1 gold
```

Example:
```python
# Base: 100g
# Quality: Fine (×1.25)
# Reputation: 60 (+0.04)
# Affinity: +3 (-0.12)
# Demand/Supply: ×1.2
# Rarity: ×1.5

# Final: 100 × 1.25 × 1.2 × 1.5 × 1.04 × 0.88 = 194 gold
```

### Bulk Discounts

Quantity purchases receive discounts:

- 3-4 items: 5% discount
- 5-9 items: 10% discount
- 10+ items: 15% discount

Applied to unit price before total calculation.

## Combat Rewards

Victory in combat earns gold:

```
base_reward = 100 gold
speed_bonus = max(0, (20 - turn_count) × 5)
difficulty_bonus = difficulty × 2
margin_bonus = victory_margin × 50

total = base + speed + difficulty + margin
```

Example:
```python
# 8 turns, difficulty 60, margin 0.7
# Base: 100
# Speed: (20-8)×5 = 60
# Difficulty: 60×2 = 120
# Margin: 0.7×50 = 35
# Total: 315 gold
```

## Wallet System

Each entity has a wallet tracking:
- Current gold balance
- Transaction history (IDs)
- Automatic creation on first access

### Operations

**Add Gold:**
```python
new_balance = economy.add_gold(
    owner_id="player",
    amount=100,
    reason="quest_reward"
)
```

**Deduct Gold:**
```python
success = economy.deduct_gold(
    owner_id="player",
    amount=50,
    reason="purchase_ingredients"
)
```

**Check Balance:**
```python
wallet = economy.get_wallet("player")
print(f"Balance: {wallet.gold}")
```

## Transaction System

Secure two-party gold transfers:

```python
transaction = economy.execute_transaction(
    buyer_id="player",
    seller_id="merchant",
    item_id="potion_123",
    item_type="potion",
    quantity=1,
    unit_price=100,
    modifiers=price_modifiers
)
```

**Guarantees:**
- Atomic: Either fully succeeds or fully fails
- Balance check: Buyer must have sufficient gold
- History tracking: Both parties record transaction
- Event emission: All observers notified

Returns `None` if insufficient funds, otherwise `Transaction` object.

## Market Condition Tracking

Track supply/demand per item:

```python
condition = economy.get_market_condition("healing_potion")
print(f"Demand: {condition.demand_level}")
print(f"Supply: {condition.supply_level}")
print(f"Price Multiplier: {condition.current_multiplier}")

economy.update_market(
    item_id="healing_potion",
    transactions_today=15,
    items_added=10,
    items_sold=20,
    reason="market_activity"
)
```

## Integration Examples

### Crafting System

```python
class CraftingIntegration:
    def __init__(self, event_bus):
        event_bus.subscribe(PotionCreated, self.on_potion_created)

    def on_potion_created(self, event):
        ingredient_cost = self.calculate_ingredient_cost(event.potion)
        price, _ = economy.calculate_potion_price(
            event.potion,
            ingredient_cost,
            difficulty=50
        )
        self.update_shop_inventory(event.potion, price)
```

### Combat System

```python
class CombatIntegration:
    def __init__(self, event_bus):
        event_bus.subscribe(CombatEnded, self.on_combat_ended)

    def on_combat_ended(self, event):
        if event.winner_id == "player":
            difficulty = self.get_opponent_difficulty()
            margin = self.calculate_victory_margin(event)
            reward = economy.award_combat_reward(
                event.winner_id,
                event.turn_count,
                difficulty,
                margin
            )
            print(f"Victory! Earned {reward} gold!")
```

### Relationship System

```python
class RelationshipIntegration:
    def __init__(self, event_bus):
        event_bus.subscribe(TransactionCompleted, self.on_transaction)

    def on_transaction(self, event):
        if self.was_fair_price(event):
            self.relationship_system.apply_action(
                npc_id=event.seller_id,
                action=fair_trade_action,
                current_day=today
            )
```

### Quest System

```python
class QuestIntegration:
    def __init__(self, event_bus):
        event_bus.subscribe(GoldChanged, self.on_gold_changed)

    def on_gold_changed(self, event):
        if event.owner_id == "player":
            self.check_wealth_objectives(event.new_balance)

        if event.reason == "donation":
            self.update_generosity_quest(event.delta)
```

## Testbed Commands

```
wallets       - Show all wallet balances
market        - Show market conditions
events [n]    - Show recent n events
price         - Test potion pricing scenarios
transaction   - Test transaction flow
combat        - Test combat rewards
test          - Run all automated tests
help          - Show help
quit          - Exit
```

## Example Testbed Session

```
ECONOMY TESTBED
==============================================================

Testing Potion Pricing:
==============================================================
POOR              67 gold  (quality: 0.75x)
STANDARD          90 gold  (quality: 1.00x)
FINE             112 gold  (quality: 1.25x)
EXCEPTIONAL      135 gold  (quality: 1.50x)
MASTERWORK       180 gold  (quality: 2.00x)

Testing Affinity-Based Pricing:
==============================================================
Nemesis          108 gold  (modifier: +0.20)
Neutral           90 gold  (modifier: +0.00)
Devoted           72 gold  (modifier: -0.20)

Testing Market Dynamics:
==============================================================
Initial state:
Demand: 1.00  Supply: 1.00

After high transaction volume:
Demand: 1.81  Supply: 1.00

After selling more than adding:
Demand: 1.72  Supply: 0.50

Wallet Balances:
==============================================================
player            935 gold  (6 transactions)
merchant         5315 gold  (6 transactions)
rival             500 gold  (0 transactions)
```

## Design Principles

Following SOLID, DRY, and KISS principles:

- **Single Responsibility**: Each function does one thing
- **Pure Functions**: No side effects in formulas
- **Event-Driven**: Loose coupling through events
- **Testable**: All logic has comprehensive tests
- **Clean Code**: Self-documenting, no unnecessary comments

## Success Criteria

✅ **Pricing reflects quality** - Better potions cost more
✅ **Relationships affect prices** - Affinity provides discounts
✅ **Markets feel dynamic** - Supply/demand creates variation
✅ **Transactions are secure** - No gold duplication or loss
✅ **Combat feels rewarding** - Victory provides appropriate gold
✅ **Events integrate seamlessly** - Other systems can react
✅ **Wallet operations are safe** - Balance checks prevent overdraft
✅ **Testbed validates all mechanics** - Interactive testing works

## Future Enhancements

- Shop inventory management
- Special orders and contracts
- Black market pricing
- Auction house mechanics
- Seasonal price fluctuations
- Economic reputation tracking
- Trade routes and merchants
- Investment and interest systems
