# PotionWorld: Hybrid API + Event Architecture Roadmap

## Vision: Systems as APIs, Not Minigames

Instead of building 7 separate "minigames," we're building **7 system libraries** with:
- **Clean APIs** (clear input/output contracts)
- **Pure logic** (testable formulas)
- **Event emission** (for side effects and system integration)
- **Comprehensive tests** (unit + integration)
- **Simple testbeds** (god-mode UIs for manual validation)

**Timeline: 6-8 weeks total** (not 35 weeks)

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

## Development Timeline (6-8 Weeks)

### Week 1: Architecture + Core Contracts
**Goal:** Define all APIs and event types

**Deliverables:**
- Event bus implementation (simple pub/sub)
- All API signatures defined (Python dataclasses)
- Event type definitions
- Shared data structures (Recipe, NPC, Potion, etc.)

**Files:**
```
core/
├── event_bus.py           # Pub/sub event system
├── events.py              # All event definitions
├── data_structures.py     # Shared models (Recipe, NPC, etc.)
└── tests/
    └── test_event_bus.py
```

---

### Week 2: Crafting + Progression Systems
**Goal:** Implement and test core number crunching

#### Crafting System
```python
class CraftingSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def craft(self, input: CraftInput) -> CraftResult:
        """
        Pure calculation: success chance, quality, potency
        Emits: CraftCompleted, PotionCreated, RecipeMasteryGained
        """
        success_chance = self._calculate_success(input)
        roll = random.randint(1, 20)

        if self._check_success(success_chance, roll):
            quality = self._determine_quality(...)
            potion = self._create_potion(...)

            # Emit events
            self.event_bus.emit(CraftCompleted(success=True, ...))
            self.event_bus.emit(PotionCreated(potion))

            return CraftResult(success=True, potion=potion, ...)
        else:
            self.event_bus.emit(CraftCompleted(success=False, ...))
            return CraftResult(success=False, ...)

    def _calculate_success(self, input: CraftInput) -> float:
        """Pure function - no side effects"""
        return (
            0.5 +  # Base
            (input.stats.knowledge / 2 / 100) +
            input.tool_bonus -
            (input.recipe.difficulty / 100)
        )
```

#### Progression System
```python
class ProgressionSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        # Listen to other systems
        event_bus.subscribe(CraftCompleted, self.on_craft_completed)

    def add_xp(self, stat: str, amount: int, current_xp: int) -> StatChange:
        """Pure XP calculation"""
        new_xp = current_xp + amount
        old_stat = self._xp_to_stat(current_xp)
        new_stat = self._xp_to_stat(new_xp)

        result = StatChange(
            stat=stat,
            xp_gained=amount,
            new_xp=new_xp,
            stat_increased=(new_stat > old_stat),
            new_stat_value=new_stat
        )

        self.event_bus.emit(StatIncreased(result))

        if self._check_milestone(old_stat, new_stat):
            self.event_bus.emit(MilestoneReached(...))

        return result

    def on_craft_completed(self, event: CraftCompleted):
        """React to crafting events"""
        if event.success:
            self.add_xp('knowledge', 50, self.player.xp['knowledge'])
```

**Tests:**
```python
def test_crafting_success_formula():
    bus = EventBus()
    crafting = CraftingSystem(bus)

    input = CraftInput(
        recipe=Recipe(difficulty=60),
        ingredients=[...],
        stats=CrafterStats(knowledge=50, precision=40, intuition=30),
        tool_bonus=0.1
    )

    # Run 10000 times
    results = [crafting.craft(input) for _ in range(10000)]
    success_rate = sum(r.success for r in results) / 10000

    # Expected: 50% + 25% + 10% - 60% = 25% base + d20 variance
    assert 0.20 <= success_rate <= 0.30

def test_xp_to_stat_conversion():
    progression = ProgressionSystem(EventBus())

    assert progression._xp_to_stat(0) == 0
    assert progression._xp_to_stat(1000) == 20  # Novice threshold
    assert progression._xp_to_stat(10000) == 100  # Master
```

**Deliverables:**
- Crafting system API + tests
- Progression system API + tests
- Integration test (craft → xp gain → stat increase)
- Simple testbed CLI for crafting

---

### Week 3: Relationship + Quest Systems
**Goal:** State machines and consequence tracking

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
        delta = self._calculate_affinity_delta(npc.personality, action)
        new_affinity = self._clamp(current_affinity + delta, -5, 5)

        # Check threshold crossings
        threshold_crossed = self._check_threshold(current_affinity, new_affinity)

        # Create memory if significant
        memory = None
        if abs(delta) >= 1.0:
            memory = Memory(action=action.id, delta=delta, ...)
            self.event_bus.emit(MemoryCreated(npc.id, memory))

        result = AffinityChange(
            npc_id=npc.id,
            delta=delta,
            new_affinity=new_affinity,
            threshold_crossed=threshold_crossed,
            memory_created=memory
        )

        self.event_bus.emit(AffinityChanged(result))

        if threshold_crossed:
            self.event_bus.emit(ThresholdCrossed(npc.id, new_affinity))

        return result

    def apply_decay(self, npc: NPC, days_passed: int) -> AffinityChange:
        """Time-based decay toward neutral"""
        decay_amount = days_passed * 0.5 * (1 if npc.affinity > 0 else -1)
        new_affinity = npc.affinity - min(abs(decay_amount), abs(npc.affinity))

        result = AffinityChange(
            npc_id=npc.id,
            delta=-decay_amount,
            new_affinity=new_affinity,
            reason="decay"
        )

        self.event_bus.emit(AffinityChanged(result))
        return result
```

#### Quest System
```python
class QuestSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        # Listen to many events
        event_bus.subscribe(PotionCreated, self.on_potion_created)
        event_bus.subscribe(AffinityChanged, self.on_affinity_changed)
        # etc.

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
        """Auto-update crafting quest objectives"""
        for quest in self.active_quests:
            if quest.tracks_potion_creation(event.potion):
                self.update_objective(quest, "craft", ...)
```

**Tests:**
```python
def test_personality_affects_affinity():
    bus = EventBus()
    rel = RelationshipSystem(bus)

    # High Openness NPC
    npc_open = NPC(personality=Personality(O=1, C=0, E=0, A=0, N=0))
    # Low Openness NPC
    npc_traditional = NPC(personality=Personality(O=-1, C=0, E=0, A=0, N=0))

    action = Action("InnovativePotion", personality_impacts={"O": 1.0})

    result_open = rel.apply_action(npc_open, action, current_affinity=0)
    result_trad = rel.apply_action(npc_traditional, action, current_affinity=0)

    assert result_open.delta > 0  # Likes innovation
    assert result_trad.delta < 0  # Dislikes innovation

def test_quest_objective_tracking():
    bus = EventBus()
    quest_sys = QuestSystem(bus)

    quest = Quest(objectives=[
        Objective(id="craft_3_potions", target=3, current=0)
    ])

    # Emit potion creation events
    bus.emit(PotionCreated(Potion("healing")))
    bus.emit(PotionCreated(Potion("healing")))

    assert quest.get_objective("craft_3_potions").current == 2
    assert not quest.is_completed()

    bus.emit(PotionCreated(Potion("healing")))

    assert quest.is_completed()
```

**Deliverables:**
- Relationship system API + tests
- Quest system API + tests
- Integration tests (actions → affinity → quest unlocks)
- Testbed for relationship testing

---

### Week 4: Combat + Economy Systems
**Goal:** Turn-based logic and pricing algorithms

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
        self._evaluate_triggers("^S", actor, state)

        # Execute action
        if action.type == "USE_POTION":
            potion_result = self._apply_potion(action.potion, actor, target)
            self.event_bus.emit(PotionUsed(actor.id, action.potion))

            if potion_result.damage > 0:
                self.event_bus.emit(DamageDealt(
                    source=actor.id,
                    target=target.id,
                    amount=potion_result.damage
                ))

            for status in potion_result.statuses:
                self.event_bus.emit(StatusApplied(target.id, status))

        # Apply end-of-turn triggers
        self._evaluate_triggers("vE", actor, state)

        # Update status durations
        self._update_statuses(actor)

        # Check victory
        if target.health <= 0:
            self.event_bus.emit(CombatEnded(winner=actor.id))

        return TurnResult(...)

    def _apply_potion(self, potion: Potion, actor: Combatant, target: Combatant):
        """Parse ESENS and apply effects"""
        effects = self.parser.parse(potion.esens_notation)

        for effect in effects:
            if effect.target == "P":  # Player/self
                self._apply_status(actor, effect)
            elif effect.target == "E":  # Enemy
                self._apply_status(target, effect)
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

        base_price = self._ingredient_cost(potion) * self._difficulty_multiplier(potion)

        # Quality bonus
        quality_bonus = {
            Quality.POOR: 0.75,
            Quality.STANDARD: 1.0,
            Quality.FINE: 1.25,
            Quality.EXCEPTIONAL: 1.5,
            Quality.MASTERWORK: 2.0
        }[potion.quality]

        # Supply/demand
        supply_demand = market_state.get_modifier(potion.type)

        # Reputation
        rep_bonus = 1.0 + (shop_reputation / 500)  # 0-20% bonus

        final_price = base_price * quality_bonus * supply_demand * rep_bonus

        return Price(
            base=base_price,
            final=final_price,
            breakdown={
                "ingredients": self._ingredient_cost(potion),
                "difficulty": self._difficulty_multiplier(potion),
                "quality": quality_bonus,
                "supply_demand": supply_demand,
                "reputation": rep_bonus
            }
        )

    def make_sale(
        self,
        potion: Potion,
        price: Price,
        customer: Customer
    ) -> SaleResult:
        """Execute transaction"""

        # Update market state
        market_update = self._update_supply_demand(potion.type, sold=True)

        result = SaleResult(
            gold_earned=price.final,
            reputation_change=self._calculate_rep_change(customer, price),
            market_update=market_update
        )

        self.event_bus.emit(SaleMade(potion, price, customer))
        self.event_bus.emit(MarketShifted(market_update))

        return result
```

**Tests:**
```python
def test_combat_turn_structure():
    bus = EventBus()
    combat = CombatSystem(bus, ESENS_Parser())

    actor = Combatant(health=100, ...)
    target = Combatant(health=100, ...)

    potion = Potion(esens="E#Damage10")  # Direct damage
    action = CombatAction(type="USE_POTION", potion=potion)

    result = combat.execute_turn(actor, action, target, CombatState())

    assert target.health == 90
    assert result.damage_dealt == 10

def test_price_calculation_formula():
    bus = EventBus()
    economy = EconomySystem(bus)

    potion = Potion(
        type="healing",
        quality=Quality.FINE,
        ingredient_cost=100
    )

    market = MarketState(supply_demand={"healing": 1.2})  # High demand

    price = economy.calculate_price(potion, market, reputation=50)

    # Base=100, Difficulty=2.0, Quality=1.25, Demand=1.2, Rep=1.1
    expected = 100 * 2.0 * 1.25 * 1.2 * 1.1

    assert abs(price.final - expected) < 0.01
```

**Deliverables:**
- Combat system API + tests
- Economy system API + tests
- ESENS parser integration tests
- Combat testbed
- Economy testbed

---

### Week 5: Inventory System + Integration
**Goal:** State management and cross-system testing

#### Inventory System
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

        # Set acquisition time for freshness
        if isinstance(item, Ingredient):
            item.acquired_at = timestamp

        inventory.items.append(item)

        result = InventoryChange(
            success=True,
            item=item,
            new_count=inventory.count()
        )

        self.event_bus.emit(ItemAdded(item, inventory.id))

        return result

    def update_freshness(self, inventory: Inventory, current_time: int):
        """Apply time-based degradation"""
        for item in inventory.items:
            if isinstance(item, Ingredient) and item.can_spoil:
                days_old = current_time - item.acquired_at
                old_freshness = item.freshness
                item.freshness = self._calculate_freshness(days_old, item.type)

                if item.freshness <= 0 and old_freshness > 0:
                    self.event_bus.emit(ItemSpoiled(item))
```

**Integration Tests:**
```python
def test_full_crafting_flow():
    """Test: Craft potion → gain XP → increase stats → unlock recipe"""
    bus = EventBus()

    crafting = CraftingSystem(bus)
    progression = ProgressionSystem(bus)
    inventory = InventorySystem(bus)

    player = Player(stats={"knowledge": 10}, inventory=Inventory())

    # Craft a potion
    recipe = Recipe(difficulty=20, xp_reward=100)
    ingredients = [Ingredient("root"), Ingredient("berry")]

    craft_result = crafting.craft(CraftInput(
        recipe=recipe,
        ingredients=ingredients,
        stats=player.stats,
        tool_bonus=0
    ))

    # Verify potion created
    assert craft_result.success
    assert len(player.inventory.items) == 1

    # Verify XP gained
    assert player.stats["knowledge"] == 20  # Increased from XP

def test_relationship_affects_economy():
    """Test: High affinity → better prices"""
    bus = EventBus()

    economy = EconomySystem(bus)
    relationship = RelationshipSystem(bus)

    merchant = NPC(id="merchant", affinity=0)

    # Build relationship
    relationship.apply_action(
        merchant,
        Action("gift", personality_impacts={"A": 1.0}),
        current_affinity=0
    )

    # Check price improvement
    base_price = economy.get_merchant_price(merchant, Ingredient("crystal"))

    # After +affinity
    relationship.apply_action(merchant, Action("gift"), current_affinity=1.0)
    better_price = economy.get_merchant_price(merchant, Ingredient("crystal"))

    assert better_price < base_price
```

**Deliverables:**
- Inventory system API + tests
- Full integration test suite
- Performance tests (1000s of operations)
- Data persistence (save/load)

---

### Week 6: Testbeds + Documentation
**Goal:** Manual validation tools and API docs

#### Testbed Requirements

Each system gets a simple CLI testbed:

**Crafting Testbed:**
```
CRAFTING TESTBED
================
Commands:
  stats <K> <P> <I>     Set stats
  tool <0-3>            Set tool quality
  craft <recipe_id>     Craft once, show breakdown
  batch <recipe_id> <n> Craft N times, stats
  test                  Run full test suite

> craft healing_basic
Stats: Knowledge=50, Precision=40, Intuition=30
Tool: Professional (+10%)
Recipe: Basic Healing (Difficulty=20)

Success Calculation:
  Base:           50.0%
  + Knowledge/2:  +25.0%  (50/2)
  + Tool:         +10.0%
  - Difficulty:   -20.0%
  + d20 (15):     +5.0%   ((15-10)/20)
  ─────────────────────
  TOTAL:          70.0%

Roll: 15 → SUCCESS
Quality: Fine (margin=20%)
Potion: Basic Healing Potion (Fine, 110% potency)

Events emitted:
  - CraftCompleted(success=True)
  - PotionCreated(potion_id="...")
  - RecipeMasteryGained(recipe="healing_basic", +5 mastery)
```

**Relationship Testbed:**
```
RELATIONSHIP TESTBED
====================
NPCs:
  1. Thornwood (O:-1, C:+1, E:0, A:-1, N:0) - Affinity: 0.0
  2. Wisteria (O:0, C:+1, E:-1, A:+1, N:-1) - Affinity: 0.0

Actions:
  1. InnovativePotion (O:+1.0, E:+0.5, N:-0.5)
  2. TraditionalPotion (O:-0.5, C:+0.5)
  3. Gift (E:+1.0, A:+0.5)
  4. Haggle (C:-0.5, A:-1.0)

> apply 1 1
Applying "InnovativePotion" to Thornwood...

Personality Calculation:
  Openness:      -1 * 1.0 = -1.0
  Extraversion:   0 * 0.5 =  0.0
  Neuroticism:    0 * -0.5 = 0.0
  ─────────────────────────
  Total Delta:           -1.0

Result:
  Old Affinity: 0.0
  New Affinity: -1.0
  Threshold Crossed: 0→-1 (Becomes Cooler)

Events emitted:
  - AffinityChanged(npc=thornwood, delta=-1.0)
  - ThresholdCrossed(npc=thornwood, new_level=-1)

> time 7
Advancing time 7 days...
Applying decay to all NPCs...

Thornwood: -1.0 → -0.5 (moved 0.5 toward neutral)
```

**Deliverables:**
- 7 CLI testbeds (one per system)
- API documentation (docstrings + examples)
- Integration examples
- Performance benchmarks

---

### Week 7-8: Polish + Godot Prep (Optional)
**Goal:** Production-ready Python implementation

- Code cleanup and refactoring
- Comprehensive documentation
- Example integrations
- Godot port planning
- Performance optimization
- Edge case handling

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

## Benefits of This Approach

### ✅ Faster Development
- **6-8 weeks** instead of 35 weeks
- No redundant UI work
- Focus on pure logic

### ✅ Better Testing
- Unit tests for every formula
- Integration tests for system composition
- Automated validation vs. manual playtesting

### ✅ Easier Godot Port
- Clean APIs to port 1:1
- Events map to Godot signals
- Logic already validated

### ✅ Cleaner Architecture
- Systems don't depend on each other
- Easy to modify one system without breaking others
- Events provide flexibility

### ✅ Reusable
- Systems can be used in multiple games
- Testbeds useful for game designers
- Clear contracts for collaboration

---

## What Gets Validated

✅ **Formulas** - Math is correct
✅ **Balance** - Numbers feel right
✅ **Interactions** - Systems compose correctly
✅ **Edge cases** - Bugs caught early
✅ **Performance** - Fast enough for real game

❌ **Feel/Polish** - Still needs playtesting in Godot
❌ **Art/Animation** - Separate concern
❌ **Story** - Writing happens in Godot

---

## Success Criteria

Each system is "done" when:
1. ✅ All APIs implemented and documented
2. ✅ 90%+ test coverage
3. ✅ Testbed validates behavior manually
4. ✅ Integration tests pass
5. ✅ Performance benchmarks met
6. ✅ Team can use it confidently in Godot

---

## Next Steps

1. **Review this architecture** - Does it make sense?
2. **Start with Week 1** - Event bus + contracts
3. **Pick first system** - Crafting or Progression?
4. **Build incrementally** - One system at a time
5. **Test continuously** - Write tests as you go

**Ready to start?** Which system should we tackle first?
