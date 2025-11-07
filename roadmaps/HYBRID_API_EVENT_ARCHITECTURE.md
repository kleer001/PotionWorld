# PotionWorld: Hybrid API + Event Architecture

## Vision

Build **7 system libraries** with:
- **Clean APIs** - Clear input/output contracts
- **Pure logic** - Testable formulas and state machines
- **Event emission** - Side effects and cross-system communication
- **Comprehensive tests** - Unit + integration coverage
- **CLI testbeds** - Developer tools for validation

**Implementation:** Progressive, starting with core systems

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  Event Bus                          │
│  (Pub/Sub for cross-system communication)          │
└─────────────────────────────────────────────────────┘
           ↑                    ↑                ↑
           │ emits              │ emits          │ emits
           │                    │                │
    ┌──────────┐         ┌──────────┐      ┌──────────┐
    │ System A │←─calls──│ System B │      │ System C │
    │   API    │         │   API    │      │   API    │
    └──────────┘         └──────────┘      └──────────┘
         ↓                     ↓                  ↓
    [Pure Logic]         [Pure Logic]       [Pure Logic]
```

### Key Principles

1. **Systems expose APIs** - Clear function signatures
2. **APIs return results** - Immediate, synchronous output
3. **APIs emit events** - Asynchronous side effects
4. **Other systems listen** - Loosely coupled reactions
5. **Everything is testable** - Pure functions where possible

---

## The 7 Systems

### 1. Crafting System
**API:** `craft_potion(recipe, ingredients, stats, tools) -> CraftResult`
**Events:** `CraftCompleted`, `CraftFailed`, `RecipeMasteryGained`, `PotionCreated`

### 2. Relationship System
**API:** `apply_action(npc, action, current_affinity) -> AffinityChange`
**Events:** `AffinityChanged`, `ThresholdCrossed`, `MemoryCreated`

### 3. Combat System
**API:** `execute_turn(combatant, action, opponent, combat_state) -> TurnResult`
**Events:** `DamageDealt`, `StatusApplied`, `TriggerActivated`, `CombatEnded`

### 4. Economy System
**API:** `calculate_price(potion, market_state, shop_state) -> Price`
**Events:** `SaleMade`, `MarketShifted`, `ReputationChanged`

### 5. Progression System
**API:** `add_xp(stat, amount, current_value) -> StatChange`
**Events:** `StatIncreased`, `MilestoneReached`, `SpecializationUnlocked`

### 6. Inventory System
**API:** `add_item(item, inventory, timestamp) -> InventoryChange`
**Events:** `ItemAdded`, `ItemRemoved`, `ItemSpoiled`, `CapacityReached`

### 7. Quest System
**API:** `update_objective(quest, objective_id, progress) -> QuestUpdate`
**Events:** `ObjectiveCompleted`, `QuestCompleted`, `ChoiceMade`, `WorldStateChanged`

---

## Implementation Pattern

Each system follows a 3-step pattern:

### Step 1: Core Logic
Pure functions and formulas with no dependencies. All business logic lives here.

```python
def calculate_success_chance(knowledge: int, difficulty: int, ...) -> float:
    """Pure calculation - no side effects"""
    return max(0.0, min(1.0, 0.5 + (knowledge/200) - (difficulty/100)))
```

### Step 2: API + Events
System class wraps core logic, exposes APIs, emits events.

```python
class CraftingSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def craft(self, input: CraftInput) -> CraftResult:
        # Call pure logic
        success_chance = calculate_success_chance(...)

        # Calculate result
        result = self._execute_craft(success_chance, input)

        # Emit events
        self.event_bus.emit(CraftCompleted(result))
        if result.success:
            self.event_bus.emit(PotionCreated(result.potion))

        return result
```

### Step 3: Testbed + Integration
CLI developer tools for validation and cross-system integration tests.

```python
class CraftingTestbed:
    """Developer tool for testing crafting formulas"""
    def run(self):
        while True:
            cmd = input("> ")
            if cmd == "craft":
                self._craft_and_show_breakdown()
            elif cmd == "batch":
                self._batch_craft_statistics()
```

---

## Development Phases

### Phase 1: Foundation
**Event bus + Shared data structures**

**Deliverables:**
- Event bus implementation (pub/sub)
- All event type definitions
- Shared data structures (Recipe, NPC, Potion, etc.)
- Base test framework

**Files:**
```
core/
├── event_bus.py
├── events.py
├── data_structures.py
└── tests/
    └── test_event_bus.py
```

---

### Phase 2: Core Systems (Crafting + Progression)
**Number-crunching systems with formulas**

#### Crafting System
```python
class CraftingSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def craft(self, input: CraftInput) -> CraftResult:
        """
        API: Craft a potion

        1. Calculate success chance
        2. Roll dice
        3. Determine quality (if success)
        4. Create potion
        5. Calculate rewards
        6. Emit events
        """
        success_chance = calculate_success_chance(
            knowledge=input.stats.knowledge,
            difficulty=input.recipe.difficulty,
            tool_bonus=input.tool_bonus
        )

        success, roll = roll_craft_attempt(success_chance)

        if success:
            quality = determine_quality(...)
            potion = create_potion(...)

            self.event_bus.emit(PotionCreated(potion))
            self.event_bus.emit(CraftCompleted(success=True, quality=quality))

            return CraftResult(success=True, potion=potion, quality=quality)
        else:
            self.event_bus.emit(CraftCompleted(success=False))
            return CraftResult(success=False)
```

#### Progression System
```python
class ProgressionSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        # Listen to crafting events
        event_bus.subscribe(CraftCompleted, self.on_craft_completed)

    def add_xp(self, stat: str, amount: int, current_xp: int) -> StatChange:
        """API: Add XP and check for stat increases"""
        new_xp = current_xp + amount
        old_stat = xp_to_stat(current_xp)
        new_stat = xp_to_stat(new_xp)

        if new_stat > old_stat:
            self.event_bus.emit(StatIncreased(stat, old_stat, new_stat))

        return StatChange(xp_gained=amount, new_stat=new_stat)

    def on_craft_completed(self, event: CraftCompleted):
        """React to crafting events"""
        if event.success:
            self.add_xp('knowledge', 50, self.player.xp['knowledge'])
```

**Tests:**
```python
def test_crafting_success_formula():
    """Validate success calculation"""
    bus = EventBus()
    crafting = CraftingSystem(bus)

    # High stats, easy recipe → high success
    results = [crafting.craft(easy_input) for _ in range(1000)]
    assert 0.70 <= success_rate(results) <= 0.80

def test_xp_progression_curve():
    """Validate XP → stat conversion"""
    progression = ProgressionSystem(EventBus())

    assert xp_to_stat(0) == 0
    assert xp_to_stat(1000) == 20
    assert xp_to_stat(10000) == 100

def test_crafting_progression_integration():
    """Test event flow: craft → xp → stat increase"""
    bus = EventBus()
    crafting = CraftingSystem(bus)
    progression = ProgressionSystem(bus)

    player = Player(xp={'knowledge': 0})

    crafting.craft(test_input)

    assert player.xp['knowledge'] > 0
```

**Deliverables:**
- Crafting system API + tests
- Progression system API + tests
- Integration test (craft → XP → stat increase)
- Crafting CLI testbed

---

### Phase 3: State Systems (Relationship + Quest)
**State machines and consequence tracking**

#### Relationship System
```python
class RelationshipSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def apply_action(
        self,
        npc: NPC,
        action: Action,
        current_affinity: float
    ) -> AffinityChange:
        """Calculate personality-based affinity change"""
        delta = calculate_reaction(npc.personality, action)
        new_affinity = clamp(current_affinity + delta, -5, 5)

        # Check threshold crossings
        threshold = check_threshold(current_affinity, new_affinity)

        # Create memory if significant
        memory = None
        if abs(delta) >= 1.0:
            memory = Memory(action=action.id, delta=delta)
            self.event_bus.emit(MemoryCreated(npc.id, memory))

        self.event_bus.emit(AffinityChanged(npc.id, delta, new_affinity))

        if threshold:
            self.event_bus.emit(ThresholdCrossed(npc.id, threshold))

        return AffinityChange(delta=delta, new_affinity=new_affinity)
```

#### Quest System
```python
class QuestSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        # Listen to many events
        event_bus.subscribe(PotionCreated, self.on_potion_created)
        event_bus.subscribe(AffinityChanged, self.on_affinity_changed)

    def update_objective(
        self,
        quest: Quest,
        objective_id: str,
        progress: Any
    ) -> QuestUpdate:
        """Update objective progress"""
        objective = quest.get_objective(objective_id)
        objective.current = progress

        if objective.is_completed():
            self.event_bus.emit(ObjectiveCompleted(quest.id, objective_id))

            if quest.all_objectives_completed():
                self.event_bus.emit(QuestCompleted(quest.id))

        return QuestUpdate(quest=quest, objective_updated=objective_id)

    def on_potion_created(self, event: PotionCreated):
        """Auto-update crafting objectives"""
        for quest in self.active_quests:
            if quest.tracks_potion_creation(event.potion):
                self.update_objective(quest, "craft", ...)
```

**Deliverables:**
- Relationship system API + tests
- Quest system API + tests
- Integration tests (actions → affinity → quest unlocks)
- Relationship CLI testbed
- Quest CLI testbed

---

### Phase 4: Gameplay Systems (Combat + Economy)
**Complex interactions and formulas**

#### Combat System
```python
class CombatSystem:
    def __init__(self, event_bus: EventBus, esens_parser: ESENSParser):
        self.event_bus = event_bus
        self.parser = esens_parser

    def execute_turn(
        self,
        actor: Combatant,
        action: CombatAction,
        target: Combatant,
        state: CombatState
    ) -> TurnResult:
        """Execute one turn of combat"""
        # Apply start-of-turn triggers
        evaluate_triggers("^S", actor, state)

        # Execute action
        if action.type == "USE_POTION":
            effects = self.parser.parse(action.potion.esens)
            result = apply_effects(effects, actor, target)

            self.event_bus.emit(PotionUsed(actor.id, action.potion))
            self.event_bus.emit(DamageDealt(actor.id, target.id, result.damage))

        # Check victory
        if target.health <= 0:
            self.event_bus.emit(CombatEnded(winner=actor.id))

        return TurnResult(...)
```

#### Economy System
```python
class EconomySystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        event_bus.subscribe(SaleMade, self.on_sale_made)

    def calculate_price(
        self,
        potion: Potion,
        market_state: MarketState,
        shop_reputation: int
    ) -> Price:
        """Dynamic pricing formula"""
        base = ingredient_cost(potion) * difficulty_multiplier(potion)

        quality_bonus = QUALITY_MULTIPLIERS[potion.quality]
        supply_demand = market_state.get_modifier(potion.type)
        rep_bonus = 1.0 + (shop_reputation / 500)

        final = base * quality_bonus * supply_demand * rep_bonus

        return Price(base=base, final=final, breakdown={...})

    def make_sale(
        self,
        potion: Potion,
        price: Price,
        customer: Customer
    ) -> SaleResult:
        """Execute transaction"""
        market_update = update_supply_demand(potion.type, sold=True)

        self.event_bus.emit(SaleMade(potion, price, customer))
        self.event_bus.emit(MarketShifted(market_update))

        return SaleResult(gold=price.final, market=market_update)
```

**Deliverables:**
- Combat system API + tests
- Economy system API + tests
- ESENS parser integration tests
- Combat CLI testbed
- Economy CLI testbed

---

### Phase 5: Support System (Inventory)
**State management and time-based mechanics**

```python
class InventorySystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        event_bus.subscribe(PotionCreated, self.on_potion_created)
        event_bus.subscribe(SaleMade, self.on_sale_made)

    def add_item(
        self,
        item: Item,
        inventory: Inventory,
        timestamp: int
    ) -> InventoryChange:
        """Add item with capacity and freshness tracking"""
        if inventory.is_full():
            self.event_bus.emit(CapacityReached(inventory.id))
            return InventoryChange(success=False, reason="full")

        if isinstance(item, Ingredient):
            item.acquired_at = timestamp

        inventory.items.append(item)

        self.event_bus.emit(ItemAdded(item, inventory.id))

        return InventoryChange(success=True, item=item)

    def update_freshness(self, inventory: Inventory, current_time: int):
        """Apply time-based degradation"""
        for item in inventory.items:
            if isinstance(item, Ingredient) and item.can_spoil:
                days_old = current_time - item.acquired_at
                item.freshness = calculate_freshness(days_old, item.type)

                if item.freshness <= 0:
                    self.event_bus.emit(ItemSpoiled(item))
```

**Deliverables:**
- Inventory system API + tests
- Inventory CLI testbed

---

### Phase 6: Integration & Testing
**Full cross-system validation**

**Integration Tests:**
```python
def test_full_crafting_flow():
    """Craft potion → gain XP → increase stats → unlock recipe"""
    bus = EventBus()
    crafting = CraftingSystem(bus)
    progression = ProgressionSystem(bus)
    inventory = InventorySystem(bus)

    player = Player(stats={'knowledge': 10})

    # Craft a potion
    result = crafting.craft(CraftInput(...))

    # Verify potion added to inventory
    assert len(player.inventory.items) == 1

    # Verify XP gained
    assert player.stats['knowledge'] == 20

def test_relationship_affects_economy():
    """High affinity → better prices"""
    bus = EventBus()
    economy = EconomySystem(bus)
    relationship = RelationshipSystem(bus)

    merchant = NPC(id="merchant", affinity=0)

    # Build relationship
    relationship.apply_action(merchant, gift_action, 0)

    # Check price improvement
    price_low = economy.get_merchant_price(merchant, item)

    relationship.apply_action(merchant, gift_action, 1.0)

    price_high = economy.get_merchant_price(merchant, item)

    assert price_high < price_low
```

**Deliverables:**
- Full integration test suite
- Performance tests (1000s of operations)
- Data persistence (save/load)
- Cross-system event flow validation

---

### Phase 7: Polish & Documentation
**Production-ready implementation**

**CLI Testbed Example:**
```
CRAFTING TESTBED
================
Commands:
  stats <K> <P> <I>     Set stats
  tool <0-3>            Set tool quality
  craft <recipe_id>     Craft once, show breakdown
  batch <recipe_id> <n> Craft N times, statistics
  test                  Run test suite

> craft healing_basic
Stats: Knowledge=50, Precision=40, Intuition=30
Tool: Professional (+10%)
Recipe: Basic Healing (Difficulty=20)

Success Calculation:
  Base:           50.0%
  + Knowledge/2:  +25.0%
  + Tool:         +10.0%
  - Difficulty:   -20.0%
  + d20 (15):     +5.0%
  ─────────────────────
  TOTAL:          70.0%

Roll: 15 → SUCCESS
Quality: Fine (margin=20%)
Potion: Basic Healing Potion (Fine, 110% potency)

Events emitted:
  - CraftCompleted(success=True)
  - PotionCreated(potion_id="...")
```

**Deliverables:**
- 7 CLI testbeds (one per system)
- API documentation (docstrings + examples)
- Integration examples
- Performance benchmarks
- Godot port guide

---

## File Structure

```
potionworld_systems/
├── core/
│   ├── event_bus.py
│   ├── events.py
│   ├── data_structures.py
│   └── tests/
├── crafting/
│   ├── system.py
│   ├── formulas.py
│   ├── tests/
│   └── testbed.py
├── relationships/
│   ├── system.py
│   ├── personality.py
│   ├── affinity.py
│   ├── tests/
│   └── testbed.py
├── combat/
│   ├── system.py
│   ├── turn_manager.py
│   ├── status_effects.py
│   ├── ai.py
│   ├── tests/
│   └── testbed.py
├── economy/
│   ├── system.py
│   ├── pricing.py
│   ├── market.py
│   ├── tests/
│   └── testbed.py
├── progression/
│   ├── system.py
│   ├── xp_curves.py
│   ├── specializations.py
│   ├── tests/
│   └── testbed.py
├── inventory/
│   ├── system.py
│   ├── freshness.py
│   ├── tests/
│   └── testbed.py
├── quests/
│   ├── system.py
│   ├── objectives.py
│   ├── world_state.py
│   ├── tests/
│   └── testbed.py
├── integration/
│   └── tests/
│       ├── test_full_flows.py
│       ├── test_system_composition.py
│       └── test_performance.py
└── data/
    ├── recipes.json
    ├── npcs.json
    ├── potions.json
    └── quests.json
```

---

## Architecture Benefits

### Faster Development
- Focus on pure logic first
- No UI/UX dependencies
- Parallel system development

### Better Testing
- Unit tests for every formula
- Integration tests for system composition
- Automated validation

### Easier Godot Port
- Clean APIs port 1:1 to GDScript
- Events map to Godot signals
- Logic already validated

### Cleaner Architecture
- Systems loosely coupled via events
- Easy to modify one system independently
- Clear contracts for collaboration

### Reusable
- Systems work in multiple contexts
- Testbeds useful for designers
- Clear documentation for team

---

## Validation Targets

✅ **Formulas** - Math is correct
✅ **Balance** - Numbers feel right
✅ **Interactions** - Systems compose correctly
✅ **Edge cases** - Bugs caught early
✅ **Performance** - Fast enough for production

---

## Success Criteria

Each system is complete when:

1. ✅ All APIs implemented and documented
2. ✅ 90%+ test coverage
3. ✅ CLI testbed validates behavior
4. ✅ Integration tests pass
5. ✅ Performance benchmarks met
6. ✅ Ready for Godot port
