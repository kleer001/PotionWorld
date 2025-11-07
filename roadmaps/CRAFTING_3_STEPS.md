# Crafting System: 3-Step Implementation

## The 3-Step Pattern

Every system follows this pattern:
1. **Core Logic** - Pure formulas, no dependencies
2. **API + Events** - Wrap logic with interface, emit events
3. **Testbed + Integration** - Validate behavior, connect systems

---

## Step 1: Core Crafting Logic (3-4 days)

### Goal
Implement pure functions for success calculation, quality determination, and XP rewards.

### Deliverables

#### 1.1 Success Formula
```python
def calculate_success_chance(
    knowledge: int,        # 0-100
    precision: int,        # 0-100
    intuition: int,        # 0-100
    recipe_difficulty: int,  # 0-100
    tool_bonus: float,     # 0.0-0.3
    prep_bonus: float = 0.0  # 0.0-0.1
) -> float:
    """
    Pure function: Calculate base success chance before dice roll

    Returns: float between 0.0 and 1.0
    """
    return max(0.0, min(1.0,
        0.5 +  # Base 50%
        (knowledge / 200.0) +  # +0% to +50%
        tool_bonus +           # +0% to +30%
        prep_bonus -           # +0% to +10%
        (recipe_difficulty / 100.0)  # -0% to -100%
    ))

def roll_craft_attempt(success_chance: float) -> tuple[bool, int]:
    """
    Roll d20 and determine success

    Returns: (success, roll_value)
    """
    roll = random.randint(1, 20)

    # Critical failure
    if roll == 1:
        return (False, roll)

    # Critical success
    if roll == 20:
        return (True, roll)

    # Normal roll: add (roll-10) as percentage
    adjusted_chance = success_chance + ((roll - 10) / 20.0)

    return (adjusted_chance >= 0.5, roll)
```

#### 1.2 Quality Determination
```python
def determine_quality(
    success_margin: float,  # How much over 50% threshold
    ingredient_quality: Quality,
    precision: int
) -> Quality:
    """
    Pure function: Calculate potion quality tier

    success_margin: 0.0 to 1.0 (how much overcame difficulty)
    """
    # Base quality from success margin
    if success_margin >= 0.5:
        base = Quality.EXCEPTIONAL
    elif success_margin >= 0.3:
        base = Quality.FINE
    elif success_margin >= 0.1:
        base = Quality.STANDARD
    else:
        base = Quality.POOR

    # Precision can upgrade quality
    if precision >= 80 and random.random() < 0.2:
        base = min(Quality.MASTERWORK, base + 1)

    # Ingredient quality can downgrade
    if ingredient_quality == Quality.POOR:
        base = max(Quality.POOR, base - 1)

    return base

def calculate_potency(quality: Quality, recipe_base: float = 1.0) -> float:
    """
    Convert quality to potency multiplier
    """
    multipliers = {
        Quality.POOR: 0.75,
        Quality.STANDARD: 1.0,
        Quality.FINE: 1.1,
        Quality.EXCEPTIONAL: 1.25,
        Quality.MASTERWORK: 1.5
    }
    return recipe_base * multipliers[quality]
```

#### 1.3 XP & Mastery
```python
def calculate_xp_reward(
    recipe_difficulty: int,
    success: bool,
    quality: Quality
) -> dict[str, int]:
    """
    Pure function: Calculate XP gains

    Returns: {"knowledge": X, "precision": Y, "intuition": Z}
    """
    base_xp = recipe_difficulty  # 0-100

    if not success:
        # Consolation XP
        return {
            "knowledge": base_xp // 10,  # 10% of base
            "precision": 0,
            "intuition": base_xp // 20
        }

    # Success multipliers
    quality_bonus = {
        Quality.POOR: 0.8,
        Quality.STANDARD: 1.0,
        Quality.FINE: 1.2,
        Quality.EXCEPTIONAL: 1.5,
        Quality.MASTERWORK: 2.0
    }[quality]

    return {
        "knowledge": int(base_xp * quality_bonus),
        "precision": int((base_xp / 2) * quality_bonus),
        "intuition": 0  # Only from experimentation
    }

def update_recipe_mastery(
    current_mastery: int,  # 0-100
    success: bool,
    quality: Quality
) -> int:
    """
    Pure function: Increase recipe mastery
    """
    if not success:
        gain = 1  # Small gain from failure
    else:
        gain = {
            Quality.POOR: 3,
            Quality.STANDARD: 5,
            Quality.FINE: 8,
            Quality.EXCEPTIONAL: 12,
            Quality.MASTERWORK: 15
        }[quality]

    return min(100, current_mastery + gain)
```

### Tests (Step 1)
```python
def test_success_formula_basic():
    """Test success chance calculation"""
    # High stats, easy recipe → high success
    chance = calculate_success_chance(
        knowledge=80,
        precision=70,
        intuition=60,
        recipe_difficulty=20,
        tool_bonus=0.1
    )
    assert chance >= 0.8

    # Low stats, hard recipe → low success
    chance = calculate_success_chance(
        knowledge=20,
        precision=20,
        intuition=20,
        recipe_difficulty=80,
        tool_bonus=0.0
    )
    assert chance <= 0.3

def test_critical_rolls():
    """Test that nat 1 always fails, nat 20 always succeeds"""
    # Even with 100% calculated success, nat 1 fails
    success, roll = roll_craft_attempt(1.0)
    if roll == 1:
        assert not success

    # Even with 0% calculated success, nat 20 succeeds
    success, roll = roll_craft_attempt(0.0)
    if roll == 20:
        assert success

def test_quality_scales_with_margin():
    """Test quality improves with success margin"""
    q1 = determine_quality(0.05, Quality.STANDARD, precision=50)
    q2 = determine_quality(0.30, Quality.STANDARD, precision=50)
    q3 = determine_quality(0.60, Quality.STANDARD, precision=50)

    assert q1 <= q2 <= q3

def test_xp_rewards_scale():
    """Test XP scales with difficulty and quality"""
    easy_xp = calculate_xp_reward(20, True, Quality.STANDARD)
    hard_xp = calculate_xp_reward(80, True, Quality.STANDARD)

    assert hard_xp["knowledge"] > easy_xp["knowledge"]

    standard_xp = calculate_xp_reward(50, True, Quality.STANDARD)
    exceptional_xp = calculate_xp_reward(50, True, Quality.EXCEPTIONAL)

    assert exceptional_xp["knowledge"] > standard_xp["knowledge"]
```

**Time: 3-4 days**
- Day 1: Success formula + tests
- Day 2: Quality determination + tests
- Day 3: XP/mastery + tests
- Day 4: Edge cases + documentation

---

## Step 2: API + Event System (2-3 days)

### Goal
Wrap pure logic with API interface and event emission.

### Deliverables

#### 2.1 Data Structures
```python
@dataclass
class CraftInput:
    recipe: Recipe
    ingredients: List[IngredientInstance]
    crafter_stats: CrafterStats
    tool_bonus: float
    prep_bonus: float = 0.0

@dataclass
class CraftResult:
    success: bool
    quality: Optional[Quality]
    potion: Optional[Potion]
    xp_rewards: dict[str, int]
    mastery_gain: int
    formula_breakdown: FormulaBreakdown  # For debugging

@dataclass
class FormulaBreakdown:
    """Show calculations for debugging"""
    base_chance: float
    knowledge_bonus: float
    tool_bonus: float
    difficulty_penalty: float
    dice_roll: int
    final_chance: float
    success_threshold: float
```

#### 2.2 Events
```python
@dataclass
class CraftCompleted:
    """Emitted after every craft attempt"""
    success: bool
    recipe_id: str
    quality: Optional[Quality]
    potion_id: Optional[str]
    crafter_id: str
    timestamp: int

@dataclass
class PotionCreated:
    """Emitted when potion successfully created"""
    potion: Potion
    quality: Quality
    potency: float
    crafter_id: str

@dataclass
class RecipeMasteryGained:
    """Emitted when mastery increases"""
    recipe_id: str
    old_mastery: int
    new_mastery: int
    crafter_id: str

@dataclass
class XPGained:
    """Emitted for each stat XP gain"""
    stat: str  # "knowledge", "precision", "intuition"
    amount: int
    crafter_id: str
```

#### 2.3 CraftingSystem Class
```python
class CraftingSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def craft(self, input: CraftInput, crafter_id: str) -> CraftResult:
        """
        Main API: Attempt to craft a potion

        1. Calculate success
        2. Roll dice
        3. Determine quality (if success)
        4. Create potion
        5. Calculate rewards
        6. Emit events
        """
        # Step 1: Calculate success chance
        success_chance = calculate_success_chance(
            knowledge=input.crafter_stats.knowledge,
            precision=input.crafter_stats.precision,
            intuition=input.crafter_stats.intuition,
            recipe_difficulty=input.recipe.difficulty,
            tool_bonus=input.tool_bonus,
            prep_bonus=input.prep_bonus
        )

        # Step 2: Roll
        success, roll = roll_craft_attempt(success_chance)

        # Build breakdown for debugging
        breakdown = FormulaBreakdown(
            base_chance=0.5,
            knowledge_bonus=input.crafter_stats.knowledge / 200.0,
            tool_bonus=input.tool_bonus,
            difficulty_penalty=input.recipe.difficulty / 100.0,
            dice_roll=roll,
            final_chance=success_chance + ((roll - 10) / 20.0),
            success_threshold=0.5
        )

        potion = None
        quality = None

        if success:
            # Step 3: Determine quality
            success_margin = breakdown.final_chance - breakdown.success_threshold
            avg_ingredient_quality = self._calculate_avg_ingredient_quality(input.ingredients)

            quality = determine_quality(
                success_margin=success_margin,
                ingredient_quality=avg_ingredient_quality,
                precision=input.crafter_stats.precision
            )

            # Step 4: Create potion
            potency = calculate_potency(quality, input.recipe.base_potency)
            potion = Potion(
                id=generate_id(),
                recipe_id=input.recipe.id,
                esens_notation=input.recipe.esens,
                quality=quality,
                potency=potency,
                created_by=crafter_id,
                created_at=time.time()
            )

            # Emit potion created
            self.event_bus.emit(PotionCreated(
                potion=potion,
                quality=quality,
                potency=potency,
                crafter_id=crafter_id
            ))

        # Step 5: Calculate rewards
        xp_rewards = calculate_xp_reward(
            recipe_difficulty=input.recipe.difficulty,
            success=success,
            quality=quality or Quality.POOR
        )

        # Emit XP gains
        for stat, amount in xp_rewards.items():
            if amount > 0:
                self.event_bus.emit(XPGained(
                    stat=stat,
                    amount=amount,
                    crafter_id=crafter_id
                ))

        # Step 6: Update mastery (would come from external state)
        # For now, just calculate the gain
        mastery_gain = update_recipe_mastery(
            current_mastery=0,  # Would query from state
            success=success,
            quality=quality or Quality.POOR
        )

        self.event_bus.emit(RecipeMasteryGained(
            recipe_id=input.recipe.id,
            old_mastery=0,  # Would query from state
            new_mastery=mastery_gain,
            crafter_id=crafter_id
        ))

        # Emit completion event
        self.event_bus.emit(CraftCompleted(
            success=success,
            recipe_id=input.recipe.id,
            quality=quality,
            potion_id=potion.id if potion else None,
            crafter_id=crafter_id,
            timestamp=int(time.time())
        ))

        return CraftResult(
            success=success,
            quality=quality,
            potion=potion,
            xp_rewards=xp_rewards,
            mastery_gain=mastery_gain,
            formula_breakdown=breakdown
        )
```

### Tests (Step 2)
```python
def test_craft_emits_events():
    """Test that crafting emits correct events"""
    events_received = []

    bus = EventBus()
    bus.subscribe(lambda e: events_received.append(e))

    crafting = CraftingSystem(bus)

    result = crafting.craft(create_test_input(), crafter_id="test")

    # Should have emitted multiple events
    assert len(events_received) > 0
    assert any(isinstance(e, CraftCompleted) for e in events_received)

    if result.success:
        assert any(isinstance(e, PotionCreated) for e in events_received)
        assert any(isinstance(e, XPGained) for e in events_received)

def test_craft_returns_breakdown():
    """Test that formula breakdown is returned"""
    bus = EventBus()
    crafting = CraftingSystem(bus)

    result = crafting.craft(create_test_input(), crafter_id="test")

    assert result.formula_breakdown is not None
    assert result.formula_breakdown.dice_roll >= 1
    assert result.formula_breakdown.dice_roll <= 20
```

**Time: 2-3 days**
- Day 1: Data structures + event definitions
- Day 2: CraftingSystem class implementation
- Day 3: Tests + edge cases

---

## Step 3: Testbed + Integration (2-3 days)

### Goal
Build CLI testbed for manual validation and connect to Progression system.

### Deliverables

#### 3.1 CLI Testbed
```python
class CraftingTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.crafting = CraftingSystem(self.event_bus)
        self.stats = CrafterStats(knowledge=50, precision=40, intuition=30)
        self.tool_bonus = 0.1

        # Subscribe to events for display
        self.event_bus.subscribe(self._on_event)

    def run(self):
        """Main CLI loop"""
        print("CRAFTING TESTBED")
        print("=" * 50)

        while True:
            self._display_status()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "stats":
                self._set_stats(cmd[1:])
            elif cmd[0] == "tool":
                self._set_tool(cmd[1])
            elif cmd[0] == "craft":
                self._craft(cmd[1])
            elif cmd[0] == "batch":
                self._batch_craft(cmd[1], int(cmd[2]))
            elif cmd[0] == "test":
                self._run_tests()
            elif cmd[0] == "help":
                self._show_help()
            elif cmd[0] == "quit":
                break

    def _craft(self, recipe_id: str):
        """Craft once and show detailed breakdown"""
        recipe = self._get_recipe(recipe_id)

        input = CraftInput(
            recipe=recipe,
            ingredients=self._get_ingredients(recipe),
            crafter_stats=self.stats,
            tool_bonus=self.tool_bonus
        )

        result = self.crafting.craft(input, crafter_id="testbed")

        self._display_craft_result(result)

    def _batch_craft(self, recipe_id: str, count: int):
        """Craft N times and show statistics"""
        print(f"\nCrafting {recipe_id} x{count}...")

        results = []
        for i in range(count):
            recipe = self._get_recipe(recipe_id)
            input = CraftInput(
                recipe=recipe,
                ingredients=self._get_ingredients(recipe),
                crafter_stats=self.stats,
                tool_bonus=self.tool_bonus
            )
            result = self.crafting.craft(input, crafter_id="testbed")
            results.append(result)

            if (i + 1) % 10 == 0:
                print(f"  {i + 1}/{count}...")

        self._display_batch_results(results)

    def _display_craft_result(self, result: CraftResult):
        """Pretty print a single craft result"""
        print("\n" + "=" * 50)
        print("CRAFT RESULT")
        print("=" * 50)

        breakdown = result.formula_breakdown
        print(f"\nSuccess Calculation:")
        print(f"  Base:            {breakdown.base_chance:>6.1%}")
        print(f"  + Knowledge/2:   {breakdown.knowledge_bonus:>+6.1%}")
        print(f"  + Tool Bonus:    {breakdown.tool_bonus:>+6.1%}")
        print(f"  - Difficulty:    {-breakdown.difficulty_penalty:>+6.1%}")
        print(f"  + d20 ({breakdown.dice_roll:>2}):    {(breakdown.dice_roll-10)/20:>+6.1%}")
        print(f"  {'-' * 30}")
        print(f"  TOTAL:           {breakdown.final_chance:>6.1%}")

        print(f"\n  Threshold: {breakdown.success_threshold:.1%}")
        print(f"  Result: {'SUCCESS' if result.success else 'FAILURE'}")

        if result.success:
            margin = breakdown.final_chance - breakdown.success_threshold
            print(f"  Margin: {margin:+.1%}")
            print(f"\n  Quality: {result.quality.name}")
            print(f"  Potency: {result.potion.potency:.1%}")
            print(f"  Potion: {result.potion.id}")

        print(f"\nXP Rewards:")
        for stat, xp in result.xp_rewards.items():
            if xp > 0:
                print(f"  {stat.capitalize():>12}: +{xp}")

        print(f"\nMastery Gain: +{result.mastery_gain}")

    def _display_batch_results(self, results: List[CraftResult]):
        """Show statistics for batch crafting"""
        total = len(results)
        successes = sum(1 for r in results if r.success)
        failures = total - successes

        print(f"\n{'=' * 50}")
        print(f"BATCH RESULTS (n={total})")
        print(f"{'=' * 50}")

        print(f"\nSuccess Rate: {successes}/{total} ({successes/total:.1%})")
        print(f"Failure Rate: {failures}/{total} ({failures/total:.1%})")

        if successes > 0:
            qualities = [r.quality for r in results if r.success]
            print(f"\nQuality Distribution:")
            for q in Quality:
                count = sum(1 for qual in qualities if qual == q)
                if count > 0:
                    print(f"  {q.name:>12}: {count:>3} ({count/successes:.1%})")

        avg_xp = {
            "knowledge": sum(r.xp_rewards["knowledge"] for r in results) / total,
            "precision": sum(r.xp_rewards["precision"] for r in results) / total,
            "intuition": sum(r.xp_rewards["intuition"] for r in results) / total
        }

        print(f"\nAverage XP per Craft:")
        for stat, xp in avg_xp.items():
            if xp > 0:
                print(f"  {stat.capitalize():>12}: {xp:.1f}")

if __name__ == "__main__":
    testbed = CraftingTestbed()
    testbed.run()
```

#### 3.2 Integration with Progression System
```python
class ProgressionSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

        # Listen to crafting events
        event_bus.subscribe(XPGained, self.on_xp_gained)
        event_bus.subscribe(RecipeMasteryGained, self.on_mastery_gained)

    def on_xp_gained(self, event: XPGained):
        """React to XP gain from crafting"""
        # Update player stat based on XP
        old_stat = self.get_stat(event.crafter_id, event.stat)
        new_xp = self.add_xp(event.crafter_id, event.stat, event.amount)
        new_stat = self.xp_to_stat(new_xp)

        if new_stat > old_stat:
            self.event_bus.emit(StatIncreased(
                crafter_id=event.crafter_id,
                stat=event.stat,
                old_value=old_stat,
                new_value=new_stat
            ))

    def on_mastery_gained(self, event: RecipeMasteryGained):
        """Track recipe mastery"""
        self.update_mastery(
            crafter_id=event.crafter_id,
            recipe_id=event.recipe_id,
            new_mastery=event.new_mastery
        )

# Integration test
def test_crafting_progression_integration():
    """Test that crafting → XP → stat increase works"""
    bus = EventBus()

    crafting = CraftingSystem(bus)
    progression = ProgressionSystem(bus)

    player = Player(id="test", knowledge=30)

    # Craft something
    recipe = Recipe(difficulty=40, ...)
    input = CraftInput(...)

    result = crafting.craft(input, crafter_id=player.id)

    # Check that progression system received XP
    new_knowledge = progression.get_stat(player.id, "knowledge")

    assert new_knowledge > 30  # Should have increased
```

**Time: 2-3 days**
- Day 1: Build CLI testbed
- Day 2: Integration with Progression system
- Day 3: Integration tests + documentation

---

## Total Time: Crafting System Complete

**8-10 days** (1.5-2 weeks)

---

## Can This Pattern Work for All Systems?

Let me evaluate...

### ✅ Systems That Fit This Pattern Perfectly:

1. **Crafting** ✓ (just did this)
2. **Progression** ✓
   - Step 1: XP curves, stat scaling formulas
   - Step 2: Add/remove XP API + StatIncreased events
   - Step 3: Testbed to set XP, see stat changes

3. **Combat** ✓
   - Step 1: Damage calculation, status effects, turn order
   - Step 2: execute_turn() API + combat events
   - Step 3: Combat simulator testbed

4. **Economy** ✓
   - Step 1: Pricing formula, supply/demand math
   - Step 2: calculate_price() API + market events
   - Step 3: Shop simulator testbed

### ⚠️ Systems That Need Slight Adjustment:

5. **Relationships** (Mostly fits)
   - Step 1: Personality reaction formulas, decay math ✓
   - Step 2: apply_action() API + affinity events ✓
   - Step 3: ⚠️ Less "testbed", more "scenario player"
   - **Adjustment:** Step 3 becomes "Scenario tester" where you run through pre-defined NPC interaction sequences

6. **Quests** (Mostly fits)
   - Step 1: ⚠️ Less formula-heavy, more state machine
   - Step 2: update_objective() API + quest events ✓
   - Step 3: Quest flow visualizer ✓
   - **Adjustment:** Step 1 becomes "State machine logic" rather than pure formulas

7. **Inventory** (Mostly fits)
   - Step 1: Freshness decay formulas, capacity logic ✓
   - Step 2: add_item(), remove_item() APIs + inventory events ✓
   - Step 3: Inventory simulator ✓

---

## Conclusion

**YES**, the 3-step pattern works for all systems with minor adjustments:

### Formula-Heavy Systems (Crafting, Combat, Economy, Progression):
- Step 1 = Pure math
- Step 2 = API wrapper + events
- Step 3 = Number-crunching testbed

### State-Heavy Systems (Relationships, Quests, Inventory):
- Step 1 = State machine logic + any formulas
- Step 2 = API wrapper + events (same)
- Step 3 = Scenario tester / flow visualizer

**Should I create the 3-step breakdown for all 7 systems now?**
