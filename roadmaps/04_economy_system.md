# Economy System: 3-Step Implementation

## Overview
Dynamic pricing, supply/demand mechanics, and ethical pricing choices for shop management.

**Core Validation:** Pricing formula balances fairly, supply/demand creates interesting market dynamics, ethical choices have meaningful trade-offs.

---

## Step 1: Core Logic

### 1.1 Price Calculation
```python
def calculate_potion_price(
    ingredient_cost: int,
    recipe_difficulty: int,  # 0-100
    quality: Quality,
    supply_demand_ratio: float,  # 0.5 to 2.0
    shop_reputation: int  # 0-100
) -> int:
    """
    Pure function: Calculate final price

    Returns: int gold price
    """
    # Base from ingredients and difficulty
    difficulty_multiplier = {
        0-20: 1.5,
        21-40: 2.0,
        41-60: 2.5,
        61-80: 3.0,
        81-100: 3.5
    }[recipe_difficulty // 20]

    base_price = ingredient_cost * difficulty_multiplier

    # Quality multiplier
    quality_bonus = {
        Quality.POOR: 0.75,
        Quality.STANDARD: 1.0,
        Quality.FINE: 1.25,
        Quality.EXCEPTIONAL: 1.5,
        Quality.MASTERWORK: 2.0
    }[quality]

    # Supply/demand (0.5 = oversupply, 2.0 = high demand)
    market_price = base_price * quality_bonus * supply_demand_ratio

    # Reputation bonus (0-20%)
    rep_bonus = 1.0 + (shop_reputation / 500)

    final_price = market_price * rep_bonus

    return int(final_price)
```

### 1.2 Supply & Demand
```python
@dataclass
class MarketState:
    supply: dict[str, int]  # potion_type -> quantity available
    demand: dict[str, int]  # potion_type -> demand level

def calculate_supply_demand_ratio(supply: int, demand: int) -> float:
    """
    Pure function: Convert supply/demand to price multiplier

    Low supply + high demand = high ratio (expensive)
    High supply + low demand = low ratio (cheap)
    """
    if demand == 0:
        return 0.5  # No demand = cheap

    ratio = demand / max(1, supply)

    # Clamp to reasonable range
    return max(0.5, min(2.0, ratio))

def update_market_on_sale(
    market: MarketState,
    potion_type: str,
    quantity_sold: int
) -> MarketState:
    """
    Pure function: Update market after sale

    Sale increases demand, decreases supply
    """
    new_market = MarketState(
        supply=market.supply.copy(),
        demand=market.demand.copy()
    )

    # Decrease supply
    new_market.supply[potion_type] = max(
        0,
        market.supply.get(potion_type, 0) - quantity_sold
    )

    # Increase demand (people see it's popular)
    new_market.demand[potion_type] = market.demand.get(potion_type, 10) + 1

    return new_market

def apply_market_decay(market: MarketState, days_passed: int) -> MarketState:
    """
    Pure function: Demand fades over time, supply replenishes

    Markets return to equilibrium
    """
    new_market = MarketState(supply={}, demand={})

    for potion_type in set(list(market.supply.keys()) + list(market.demand.keys())):
        # Supply slowly replenishes (competitors craft)
        old_supply = market.supply.get(potion_type, 10)
        new_market.supply[potion_type] = min(100, old_supply + days_passed)

        # Demand slowly decays to baseline (10)
        old_demand = market.demand.get(potion_type, 10)
        baseline = 10
        decay = (old_demand - baseline) * 0.1 * days_passed
        new_market.demand[potion_type] = max(1, old_demand - decay)

    return new_market
```

### 1.3 Ethical Pricing
```python
@dataclass
class Customer:
    id: str
    name: str
    budget: int  # Max they can afford
    ailment: str  # What they need
    urgency: int  # 1-10, how desperate
    wealth_level: str  # "poor", "moderate", "wealthy"

def calculate_ethical_impact(
    price_charged: int,
    fair_market_price: int,
    customer: Customer
) -> dict:
    """
    Pure function: Calculate consequences of pricing choice

    Returns: dict with reputation, affinity, and gold changes
    """
    price_ratio = price_charged / fair_market_price

    # Baseline: fair pricing
    if 0.9 <= price_ratio <= 1.1:
        return {
            "reputation_change": 0,
            "affinity_change": 0,
            "moral_alignment": "neutral"
        }

    # Overcharging
    if price_ratio > 1.1:
        severity = (price_ratio - 1.0) * 10  # 1.5 = 5, 2.0 = 10

        # Worse if customer is poor or desperate
        if customer.wealth_level == "poor":
            severity *= 2
        if customer.urgency >= 8:
            severity *= 1.5

        return {
            "reputation_change": -int(severity),
            "affinity_change": -severity / 5,
            "moral_alignment": "greedy"
        }

    # Undercharging / charity
    if price_ratio < 0.9:
        generosity = (1.0 - price_ratio) * 10

        # More impactful for poor customers
        if customer.wealth_level == "poor":
            generosity *= 1.5

        return {
            "reputation_change": int(generosity * 2),
            "affinity_change": generosity / 3,
            "moral_alignment": "charitable"
        }
```

### Tests (Step 1)
```python
def test_price_scales_with_difficulty():
    """Harder recipes should be more expensive"""
    easy_price = calculate_potion_price(
        ingredient_cost=100,
        recipe_difficulty=20,
        quality=Quality.STANDARD,
        supply_demand_ratio=1.0,
        shop_reputation=50
    )

    hard_price = calculate_potion_price(
        ingredient_cost=100,
        recipe_difficulty=80,
        quality=Quality.STANDARD,
        supply_demand_ratio=1.0,
        shop_reputation=50
    )

    assert hard_price > easy_price * 1.5

def test_supply_demand_affects_price():
    """High demand should increase price"""
    base_price = calculate_potion_price(100, 50, Quality.STANDARD, 1.0, 50)
    high_demand_price = calculate_potion_price(100, 50, Quality.STANDARD, 2.0, 50)

    assert high_demand_price > base_price * 1.8

def test_market_updates_on_sale():
    """Sale should decrease supply, increase demand"""
    market = MarketState(
        supply={"healing": 10},
        demand={"healing": 5}
    )

    new_market = update_market_on_sale(market, "healing", 1)

    assert new_market.supply["healing"] == 9
    assert new_market.demand["healing"] == 6

def test_ethical_impact_of_overcharging():
    """Overcharging poor desperate customer should be bad"""
    poor_customer = Customer(
        budget=50,
        wealth_level="poor",
        urgency=9
    )

    impact = calculate_ethical_impact(
        price_charged=150,
        fair_market_price=100,
        customer=poor_customer
    )

    assert impact["reputation_change"] < -10
    assert impact["moral_alignment"] == "greedy"
```

---

## Step 2: API + Events

### 2.1 Data Structures
```python
@dataclass
class Shop:
    id: str
    gold: int
    inventory: dict[str, list[Potion]]  # potion_type -> list of potions
    reputation: int  # 0-100

@dataclass
class SaleResult:
    potion_sold: Potion
    price_charged: int
    customer: Customer
    gold_earned: int
    reputation_change: int
    affinity_change: float
    market_updated: MarketState
```

### 2.2 Events
```python
@dataclass
class SaleMade:
    shop_id: str
    potion: Potion
    price: int
    customer: Customer
    timestamp: int

@dataclass
class MarketShifted:
    potion_type: str
    old_supply: int
    new_supply: int
    old_demand: int
    new_demand: int

@dataclass
class ReputationChanged:
    shop_id: str
    old_reputation: int
    new_reputation: int
    reason: str

@dataclass
class EthicalChoiceMade:
    shop_id: str
    customer: Customer
    fair_price: int
    charged_price: int
    moral_alignment: str  # "greedy", "neutral", "charitable"
```

### 2.3 EconomySystem Class
```python
class EconomySystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        event_bus.subscribe(PotionCreated, self.on_potion_created)
        event_bus.subscribe(DayPassed, self.on_day_passed)

    def calculate_price(
        self,
        potion: Potion,
        market: MarketState,
        shop: Shop
    ) -> int:
        """API: Get current market price for potion"""
        supply_demand = calculate_supply_demand_ratio(
            market.supply.get(potion.type, 10),
            market.demand.get(potion.type, 10)
        )

        return calculate_potion_price(
            ingredient_cost=potion.ingredient_cost,
            recipe_difficulty=potion.recipe.difficulty,
            quality=potion.quality,
            supply_demand_ratio=supply_demand,
            shop_reputation=shop.reputation
        )

    def make_sale(
        self,
        shop: Shop,
        potion: Potion,
        price: int,
        customer: Customer,
        market: MarketState
    ) -> SaleResult:
        """
        API: Execute sale transaction

        1. Calculate fair price
        2. Determine ethical impact
        3. Update shop gold
        4. Update reputation
        5. Update market
        6. Emit events
        """
        fair_price = self.calculate_price(potion, market, shop)

        ethical_impact = calculate_ethical_impact(
            price_charged=price,
            fair_market_price=fair_price,
            customer=customer
        )

        # Update shop
        old_reputation = shop.reputation
        shop.gold += price
        shop.reputation = max(0, min(100,
            shop.reputation + ethical_impact["reputation_change"]
        ))

        # Update market
        new_market = update_market_on_sale(market, potion.type, 1)

        # Emit events
        self.event_bus.emit(SaleMade(
            shop_id=shop.id,
            potion=potion,
            price=price,
            customer=customer,
            timestamp=time.time()
        ))

        self.event_bus.emit(MarketShifted(
            potion_type=potion.type,
            old_supply=market.supply.get(potion.type, 10),
            new_supply=new_market.supply.get(potion.type, 10),
            old_demand=market.demand.get(potion.type, 10),
            new_demand=new_market.demand.get(potion.type, 10)
        ))

        if ethical_impact["reputation_change"] != 0:
            self.event_bus.emit(ReputationChanged(
                shop_id=shop.id,
                old_reputation=old_reputation,
                new_reputation=shop.reputation,
                reason=f"sale_to_{customer.id}"
            ))

        self.event_bus.emit(EthicalChoiceMade(
            shop_id=shop.id,
            customer=customer,
            fair_price=fair_price,
            charged_price=price,
            moral_alignment=ethical_impact["moral_alignment"]
        ))

        return SaleResult(
            potion_sold=potion,
            price_charged=price,
            customer=customer,
            gold_earned=price,
            reputation_change=ethical_impact["reputation_change"],
            affinity_change=ethical_impact["affinity_change"],
            market_updated=new_market
        )

    def on_potion_created(self, event: PotionCreated):
        """Update supply when potions are crafted"""
        # Increase supply for this potion type
        pass

    def on_day_passed(self, event: DayPassed):
        """Apply market decay over time"""
        # Markets move toward equilibrium
        pass
```

---

## Step 3: Testbed + Integration

### 3.1 Economy Testbed
```python
class EconomyTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.economy = EconomySystem(self.event_bus)

        self.shop = Shop(
            id="player_shop",
            gold=1000,
            inventory=self._create_starter_inventory(),
            reputation=50
        )

        self.market = MarketState(
            supply={"healing": 20, "strength": 15, "speed": 10},
            demand={"healing": 25, "strength": 10, "speed": 5}
        )

        self.event_bus.subscribe(self._on_event)

    def run(self):
        """Main loop"""
        print("ECONOMY TESTBED")
        print("=" * 60)

        while True:
            self._display_status()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "price":
                self._check_price(cmd[1])
            elif cmd[0] == "sell":
                self._make_sale(cmd[1], int(cmd[2]) if len(cmd) > 2 else None)
            elif cmd[0] == "market":
                self._show_market()
            elif cmd[0] == "time":
                self._advance_time(int(cmd[1]))
            elif cmd[0] == "scenario":
                self._run_ethical_scenario(cmd[1])
            elif cmd[0] == "quit":
                break

    def _check_price(self, potion_id: str):
        """Show fair market price for potion"""
        potion = self._get_potion(potion_id)

        fair_price = self.economy.calculate_price(potion, self.market, self.shop)

        print(f"\n{potion.name} - Fair Market Price")
        print(f"  Ingredient Cost: {potion.ingredient_cost}g")
        print(f"  Difficulty: {potion.recipe.difficulty}")
        print(f"  Quality: {potion.quality.name}")
        print(f"  Supply/Demand: {self._get_supply_demand(potion.type):.2f}")
        print(f"  Shop Reputation: {self.shop.reputation}")
        print(f"  ═══════════════════════")
        print(f"  Fair Price: {fair_price}g")

    def _run_ethical_scenario(self, scenario_name: str):
        """Run predefined ethical dilemma"""
        scenarios = {
            "poor_sick": Customer(
                id="poor_sick",
                name="Poor Sick Villager",
                budget=30,
                ailment="fever",
                urgency=9,
                wealth_level="poor"
            ),
            "wealthy_vain": Customer(
                id="wealthy",
                name="Wealthy Noble",
                budget=500,
                ailment="cosmetic",
                urgency=2,
                wealth_level="wealthy"
            )
        }

        customer = scenarios.get(scenario_name)
        if not customer:
            print(f"Unknown scenario: {scenario_name}")
            return

        potion = self._get_potion("healing")  # For simplicity
        fair_price = self.economy.calculate_price(potion, self.market, self.shop)

        print(f"\n═══ ETHICAL DILEMMA ═══")
        print(f"Customer: {customer.name}")
        print(f"  Wealth: {customer.wealth_level}")
        print(f"  Budget: {customer.budget}g")
        print(f"  Urgency: {customer.urgency}/10")
        print(f"\nPotion: {potion.name}")
        print(f"  Fair Price: {fair_price}g")
        print(f"\nWhat price do you charge?")
        print(f"  [1] Full price ({fair_price}g)")
        print(f"  [2] Discount (half price)")
        print(f"  [3] Free (charitable)")
        print(f"  [4] Exploit (double price)")

        choice = input("\n> ").strip()

        price_map = {
            "1": fair_price,
            "2": fair_price // 2,
            "3": 0,
            "4": fair_price * 2
        }

        price = price_map.get(choice, fair_price)

        # Show preview of consequences
        impact = calculate_ethical_impact(price, fair_price, customer)

        print(f"\n═══ CONSEQUENCES ═══")
        print(f"  Gold Earned: +{price}g")
        print(f"  Reputation: {impact['reputation_change']:+d}")
        print(f"  Moral Alignment: {impact['moral_alignment']}")

        # Actually make the sale
        result = self.economy.make_sale(self.shop, potion, price, customer, self.market)

        print(f"\n  New Gold: {self.shop.gold}g")
        print(f"  New Reputation: {self.shop.reputation}")
```

### 3.2 Integration with Relationships
```python
class RelationshipSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        event_bus.subscribe(EthicalChoiceMade, self.on_ethical_choice)

    def on_ethical_choice(self, event: EthicalChoiceMade):
        """Adjust NPC affinity based on pricing ethics"""
        # If customer is an NPC we track
        if event.customer.id in self.npcs:
            npc = self.npcs[event.customer.id]

            if event.moral_alignment == "charitable":
                # High Agreeableness NPCs like charity
                if npc.personality.agreeableness > 0:
                    self.apply_affinity_change(npc, +1.0, reason="charitable_pricing")

            elif event.moral_alignment == "greedy":
                # High Agreeableness NPCs dislike greed
                if npc.personality.agreeableness > 0:
                    self.apply_affinity_change(npc, -1.0, reason="greedy_pricing")
```

---

## Success Criteria

This system is complete when:

✅ **Pricing formula feels fair** - Not too expensive/cheap
✅ **Supply/demand creates market dynamics** - Prices fluctuate interestingly
✅ **Ethical choices have clear trade-offs** - Gold vs. reputation vs. morality
✅ **Reputation affects future pricing** - Positive feedback loop
✅ **Market decays toward equilibrium** - Not permanent imbalances
✅ **Events integrate with other systems** - Affects NPC relationships
✅ **Testbed validates all scenarios** - Can play through dilemmas manually
