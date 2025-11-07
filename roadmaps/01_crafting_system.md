# Crafting System: 3-Step Implementation

## Overview
Success calculation, quality determination, XP rewards, and recipe mastery progression.

**Core Validation:** Success formula creates risk/reward balance, quality scales meaningfully with skill, XP progression feels earned, mastery bonuses encourage specialization.

---

## Step 1: Core Logic

### 1.1 Success Formula
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
    import random
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

### 1.2 Quality Determination
```python
from enum import IntEnum

class Quality(IntEnum):
    POOR = 1
    STANDARD = 2
    FINE = 3
    EXCEPTIONAL = 4
    MASTERWORK = 5

def determine_quality(
    success_margin: float,  # How much over 50% threshold
    ingredient_quality: Quality,
    precision: int
) -> Quality:
    """
    Pure function: Calculate potion quality tier

    success_margin: 0.0 to 1.0 (how much overcame difficulty)
    """
    import random

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

### 1.3 XP & Mastery
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

def get_mastery_bonus(mastery: int) -> float:
    """
    Convert mastery to success bonus
    """
    if mastery >= 75:
        return 0.20  # +20% at expert
    elif mastery >= 50:
        return 0.15  # +15% at proficient
    elif mastery >= 25:
        return 0.10  # +10% at competent
    else:
        return 0.0   # No bonus for novice
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
    # Even with 0% calculated success, nat 20 succeeds
    results = []
    for _ in range(100):
        success, roll = roll_craft_attempt(1.0)
        if roll == 1:
            assert not success
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

def test_mastery_progression():
    """Test mastery increases with practice"""
    mastery = 0

    # Failed attempt should still gain
    mastery = update_recipe_mastery(mastery, False, Quality.POOR)
    assert mastery == 1

    # Successful attempts gain more
    mastery = update_recipe_mastery(mastery, True, Quality.FINE)
    assert mastery > 1

    # Masterwork gives huge gain
    old = mastery
    mastery = update_recipe_mastery(mastery, True, Quality.MASTERWORK)
    assert mastery >= old + 15
```

---

## Step 2: API + Events

### 2.1 Data Structures
```python
from dataclasses import dataclass
from typing import Optional, List
import time

@dataclass
class Recipe:
    id: str
    name: str
    difficulty: int  # 0-100
    esens: str
    base_potency: float
    ingredients: List[str]

@dataclass
class IngredientInstance:
    id: str
    type: str
    quality: Quality
    freshness: float

@dataclass
class CrafterStats:
    knowledge: int
    precision: int
    intuition: int

@dataclass
class CraftInput:
    recipe: Recipe
    ingredients: List[IngredientInstance]
    crafter_stats: CrafterStats
    tool_bonus: float
    prep_bonus: float = 0.0
    mastery_bonus: float = 0.0

@dataclass
class Potion:
    id: str
    recipe_id: str
    esens_notation: str
    quality: Quality
    potency: float
    created_by: str
    created_at: float

@dataclass
class CraftResult:
    success: bool
    quality: Optional[Quality]
    potion: Optional[Potion]
    xp_rewards: dict[str, int]
    mastery_gain: int
    formula_breakdown: 'FormulaBreakdown'

@dataclass
class FormulaBreakdown:
    """Show calculations for debugging"""
    base_chance: float
    knowledge_bonus: float
    tool_bonus: float
    mastery_bonus: float
    difficulty_penalty: float
    dice_roll: int
    final_chance: float
    success_threshold: float
```

### 2.2 Events
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

@dataclass
class IngredientsConsumed:
    """Emitted when ingredients used in crafting"""
    ingredient_ids: List[str]
    recipe_id: str
    crafter_id: str
```

### 2.3 CraftingSystem Class
```python
class CraftingSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def craft(
        self,
        input: CraftInput,
        crafter_id: str,
        current_mastery: int = 0
    ) -> CraftResult:
        """
        API: Attempt to craft a potion

        1. Calculate success chance
        2. Roll dice
        3. Determine quality (if success)
        4. Create potion
        5. Calculate rewards
        6. Emit events
        """
        # Step 1: Calculate success chance with mastery
        mastery_bonus = get_mastery_bonus(current_mastery)

        success_chance = calculate_success_chance(
            knowledge=input.crafter_stats.knowledge,
            precision=input.crafter_stats.precision,
            intuition=input.crafter_stats.intuition,
            recipe_difficulty=input.recipe.difficulty,
            tool_bonus=input.tool_bonus,
            prep_bonus=input.prep_bonus
        ) + mastery_bonus

        # Step 2: Roll
        success, roll = roll_craft_attempt(success_chance)

        # Build breakdown for debugging
        breakdown = FormulaBreakdown(
            base_chance=0.5,
            knowledge_bonus=input.crafter_stats.knowledge / 200.0,
            tool_bonus=input.tool_bonus,
            mastery_bonus=mastery_bonus,
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
            avg_ingredient_quality = self._calculate_avg_ingredient_quality(
                input.ingredients
            )

            quality = determine_quality(
                success_margin=success_margin,
                ingredient_quality=avg_ingredient_quality,
                precision=input.crafter_stats.precision
            )

            # Step 4: Create potion
            potency = calculate_potency(quality, input.recipe.base_potency)
            potion = Potion(
                id=self._generate_id(),
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

        # Step 6: Update mastery
        new_mastery = update_recipe_mastery(
            current_mastery=current_mastery,
            success=success,
            quality=quality or Quality.POOR
        )

        if new_mastery > current_mastery:
            self.event_bus.emit(RecipeMasteryGained(
                recipe_id=input.recipe.id,
                old_mastery=current_mastery,
                new_mastery=new_mastery,
                crafter_id=crafter_id
            ))

        # Emit ingredients consumed
        self.event_bus.emit(IngredientsConsumed(
            ingredient_ids=[i.id for i in input.ingredients],
            recipe_id=input.recipe.id,
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
            mastery_gain=new_mastery - current_mastery,
            formula_breakdown=breakdown
        )

    def _calculate_avg_ingredient_quality(
        self,
        ingredients: List[IngredientInstance]
    ) -> Quality:
        """Calculate average quality of ingredients"""
        if not ingredients:
            return Quality.STANDARD

        avg = sum(i.quality for i in ingredients) / len(ingredients)
        return Quality(round(avg))

    def _generate_id(self) -> str:
        """Generate unique potion ID"""
        import uuid
        return f"potion_{uuid.uuid4().hex[:8]}"
```

---

## Step 3: Testbed + Integration

### 3.1 Crafting Testbed
```python
class CraftingTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.crafting = CraftingSystem(self.event_bus)

        # God mode: instant stat setting
        self.stats = CrafterStats(knowledge=50, precision=40, intuition=30)
        self.tool_bonus = 0.1
        self.mastery = {}  # recipe_id -> mastery level

        # Track all events
        self.event_log = []
        self.event_bus.subscribe(self._on_event)

    def run(self):
        """Main CLI loop"""
        print("CRAFTING TESTBED (God Mode)")
        print("=" * 60)

        while True:
            self._display_status()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "stats":
                # God mode: set stats instantly
                self._set_stats(cmd[1:])
            elif cmd[0] == "tool":
                self._set_tool(float(cmd[1]))
            elif cmd[0] == "mastery":
                self._set_mastery(cmd[1], int(cmd[2]))
            elif cmd[0] == "craft":
                self._craft(cmd[1])
            elif cmd[0] == "batch":
                self._batch_craft(cmd[1], int(cmd[2]))
            elif cmd[0] == "test":
                self._run_validation_tests()
            elif cmd[0] == "events":
                self._show_events()
            elif cmd[0] == "help":
                self._show_help()
            elif cmd[0] == "quit":
                break

    def _craft(self, recipe_id: str):
        """Craft once and show detailed breakdown"""
        recipe = self._get_recipe(recipe_id)

        input = CraftInput(
            recipe=recipe,
            ingredients=self._create_test_ingredients(recipe),
            crafter_stats=self.stats,
            tool_bonus=self.tool_bonus
        )

        current_mastery = self.mastery.get(recipe_id, 0)
        result = self.crafting.craft(input, crafter_id="testbed", current_mastery=current_mastery)

        # Update mastery
        self.mastery[recipe_id] = current_mastery + result.mastery_gain

        self._display_craft_result(result)

    def _batch_craft(self, recipe_id: str, count: int):
        """Craft N times and show statistics"""
        print(f"\nBatch crafting {recipe_id} x{count}...")

        results = []
        for i in range(count):
            recipe = self._get_recipe(recipe_id)
            input = CraftInput(
                recipe=recipe,
                ingredients=self._create_test_ingredients(recipe),
                crafter_stats=self.stats,
                tool_bonus=self.tool_bonus
            )

            current_mastery = self.mastery.get(recipe_id, 0)
            result = self.crafting.craft(input, crafter_id="testbed", current_mastery=current_mastery)
            results.append(result)

            # Update mastery
            self.mastery[recipe_id] = current_mastery + result.mastery_gain

            if (i + 1) % 10 == 0:
                print(f"  {i + 1}/{count}...")

        self._display_batch_results(results)

    def _display_craft_result(self, result: CraftResult):
        """Pretty print a single craft result"""
        print("\n" + "=" * 60)
        print("CRAFT RESULT")
        print("=" * 60)

        breakdown = result.formula_breakdown
        print(f"\nSuccess Calculation:")
        print(f"  Base:            {breakdown.base_chance:>6.1%}")
        print(f"  + Knowledge/2:   {breakdown.knowledge_bonus:>+6.1%}")
        print(f"  + Tool Bonus:    {breakdown.tool_bonus:>+6.1%}")
        print(f"  + Mastery:       {breakdown.mastery_bonus:>+6.1%}")
        print(f"  - Difficulty:    {-breakdown.difficulty_penalty:>+6.1%}")
        print(f"  + d20 ({breakdown.dice_roll:>2}):    {(breakdown.dice_roll-10)/20:>+6.1%}")
        print(f"  {'-' * 30}")
        print(f"  TOTAL:           {breakdown.final_chance:>6.1%}")

        print(f"\n  Threshold: {breakdown.success_threshold:.1%}")
        print(f"  Result: {'✓ SUCCESS' if result.success else '✗ FAILURE'}")

        if result.success:
            margin = breakdown.final_chance - breakdown.success_threshold
            print(f"  Margin: {margin:+.1%}")
            print(f"\n  Quality: {result.quality.name}")
            print(f"  Potency: {result.potion.potency:.1%}")
            print(f"  Potion ID: {result.potion.id}")

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

        print(f"\n{'=' * 60}")
        print(f"BATCH RESULTS (n={total})")
        print(f"{'=' * 60}")

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

        total_mastery = sum(r.mastery_gain for r in results)
        print(f"\nTotal Mastery Gained: {total_mastery}")

    def _set_stats(self, args):
        """God mode: instantly set stats"""
        # stats 80 70 60 = K:80, P:70, I:60
        if len(args) >= 3:
            self.stats.knowledge = int(args[0])
            self.stats.precision = int(args[1])
            self.stats.intuition = int(args[2])
            print(f"Stats set to K:{args[0]} P:{args[1]} I:{args[2]}")

    def _show_help(self):
        print("\nCommands:")
        print("  stats <K> <P> <I>    - Set crafter stats (god mode)")
        print("  tool <bonus>         - Set tool bonus (0.0-0.3)")
        print("  mastery <recipe> <n> - Set recipe mastery (god mode)")
        print("  craft <recipe>       - Craft once with breakdown")
        print("  batch <recipe> <n>   - Craft N times, show stats")
        print("  test                 - Run validation tests")
        print("  events               - Show recent events")
        print("  help                 - Show this help")
        print("  quit                 - Exit")

    def _on_event(self, event):
        """Log all events"""
        self.event_log.append(event)
```

### 3.2 Integration with Progression System
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
        # (this would interact with progression system's XP tracking)
        pass

    def on_mastery_gained(self, event: RecipeMasteryGained):
        """Track recipe mastery"""
        # Store mastery level for recipe
        pass
```

### 3.3 Integration with Inventory System
```python
class InventorySystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

        # Listen to crafting events
        event_bus.subscribe(PotionCreated, self.on_potion_created)
        event_bus.subscribe(IngredientsConsumed, self.on_ingredients_consumed)

    def on_potion_created(self, event: PotionCreated):
        """Auto-add new potion to inventory"""
        # Add event.potion to crafter's inventory
        pass

    def on_ingredients_consumed(self, event: IngredientsConsumed):
        """Remove consumed ingredients from inventory"""
        # Remove ingredients from crafter's inventory
        pass
```

---

## Success Criteria

This system is complete when:

✅ **Success formula feels balanced** - Not too easy, not impossible
✅ **d20 roll adds excitement** - Critical hits/misses create moments
✅ **Quality scales with skill** - Better crafters make better potions
✅ **Mastery progression feels rewarding** - Practice improves results
✅ **XP rewards encourage diverse crafting** - Hard recipes give more XP
✅ **Events integrate properly** - Progression/Inventory systems respond
✅ **Testbed validates all scenarios** - Can test edge cases easily
✅ **Formula breakdown aids balancing** - Can see exactly why craft succeeded/failed
