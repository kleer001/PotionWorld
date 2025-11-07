# Progression System: 3-Step Implementation

## Overview
XP curves, stat scaling, reputation tracking, recipe mastery, and specialization choices.

**Core Validation:** XP→stat conversion feels fair, mastery progression is rewarding, specializations create meaningful builds, reputation unlocks matter.

---

## Step 1: Core Logic

### 1.1 XP to Stat Conversion
```python
def xp_to_stat(xp: int) -> int:
    """
    Pure function: Convert XP to stat value (0-100)

    Diminishing returns: early levels fast, later levels slower
    """
    if xp <= 0:
        return 0
    if xp >= 100000:
        return 100

    # Logarithmic curve
    # 0 XP = 0
    # 1000 XP = 20 (Novice→Competent)
    # 5000 XP = 40 (Competent→Proficient)
    # 15000 XP = 60 (Proficient→Expert)
    # 40000 XP = 80 (Expert→Master)
    # 100000 XP = 100 (Master cap)

    import math
    return int(min(100, 100 * math.log(xp + 1) / math.log(100001)))

def stat_to_xp(stat: int) -> int:
    """Inverse: stat value to XP required"""
    if stat <= 0:
        return 0
    if stat >= 100:
        return 100000

    import math
    return int(math.exp((stat / 100) * math.log(100001)) - 1)

def xp_for_next_milestone(current_xp: int) -> int:
    """How much XP until next milestone (every 20 stat points)?"""
    current_stat = xp_to_stat(current_xp)
    next_milestone = ((current_stat // 20) + 1) * 20

    if next_milestone > 100:
        return 0  # Already at max

    return stat_to_xp(next_milestone) - current_xp
```

### 1.2 Mastery System
```python
def update_mastery(
    current_mastery: int,  # 0-100
    success: bool,
    quality: Quality
) -> int:
    """
    Pure function: Increase recipe mastery

    Returns: new mastery value (0-100)
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

    # Diminishing returns as you approach mastery
    if current_mastery >= 80:
        gain //= 2
    elif current_mastery >= 60:
        gain = int(gain * 0.75)

    return min(100, current_mastery + gain)

def get_mastery_bonuses(mastery: int) -> dict:
    """
    Get bonuses at current mastery level

    Returns: dict of bonuses
    """
    # Thresholds at 20, 40, 60, 80
    level = mastery // 20

    bonuses = {
        0: {  # Novice (0-20)
            "success_bonus": 0.0,
            "quality_bonus": 0.0,
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        1: {  # Competent (21-40)
            "success_bonus": 0.10,
            "quality_bonus": 0.0,
            "waste_reduction": 0.10,
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        2: {  # Proficient (41-60)
            "success_bonus": 0.20,
            "quality_bonus": 0.10,
            "waste_reduction": 0.10,
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        3: {  # Expert (61-80)
            "success_bonus": 0.30,
            "quality_bonus": 0.20,
            "waste_reduction": 0.10,
            "can_teach": True,
            "can_innovate": False,
            "batch_craft": True
        },
        4: {  # Master (81-100)
            "success_bonus": 0.40,
            "quality_bonus": 0.30,
            "waste_reduction": 0.10,
            "can_teach": True,
            "can_innovate": True,
            "batch_craft": True
        }
    }

    return bonuses.get(min(4, level), bonuses[0])
```

### 1.3 Reputation System
```python
def calculate_reputation_level(reputation: int) -> str:
    """Convert reputation (0-100) to level name"""
    if reputation >= 81:
        return "Legendary"
    elif reputation >= 61:
        return "Renowned"
    elif reputation >= 41:
        return "Respected"
    elif reputation >= 21:
        return "Known"
    else:
        return "Unknown"

def get_reputation_modifiers(reputation: int) -> dict:
    """Get gameplay effects of reputation"""
    level = calculate_reputation_level(reputation)

    modifiers = {
        "Unknown": {
            "price_modifier": 0.90,  # -10% prices (unknown)
            "quest_access": 1,
            "npc_initial_affinity": -0.5
        },
        "Known": {
            "price_modifier": 1.0,
            "quest_access": 2,
            "npc_initial_affinity": 0.0
        },
        "Respected": {
            "price_modifier": 1.05,
            "quest_access": 3,
            "npc_initial_affinity": +0.5
        },
        "Renowned": {
            "price_modifier": 1.10,
            "quest_access": 4,
            "npc_initial_affinity": +1.0
        },
        "Legendary": {
            "price_modifier": 1.20,
            "quest_access": 5,
            "npc_initial_affinity": +1.5
        }
    }

    return modifiers[level]
```

### 1.4 Specializations
```python
@dataclass
class Specialization:
    id: str
    name: str
    category: str  # "crafting", "social", "research"
    bonuses: dict
    prerequisites: dict  # stat requirements

SPECIALIZATIONS = [
    # Crafting
    Specialization(
        id="perfectionist",
        name="Perfectionist",
        category="crafting",
        bonuses={"precision": +20, "quality_bonus": +0.10},
        prerequisites={"precision": 60}
    ),
    Specialization(
        id="innovator",
        name="Innovator",
        category="crafting",
        bonuses={"intuition": +15, "can_substitute": True},
        prerequisites={"intuition": 60}
    ),
    Specialization(
        id="speed_brewer",
        name="Speed Brewer",
        category="crafting",
        bonuses={"craft_time": -0.25, "precision": -5},
        prerequisites={"knowledge": 50}
    ),

    # Social
    Specialization(
        id="diplomat",
        name="Diplomat",
        category="social",
        bonuses={"affinity_gain": +15},
        prerequisites={"reputation": 40}
    ),
    Specialization(
        id="merchant",
        name="Merchant",
        category="social",
        bonuses={"profit_margin": +0.20},
        prerequisites={"business_acumen": 50}
    ),

    # Research
    Specialization(
        id="analyst",
        name="Analyst",
        category="research",
        bonuses={"reverse_engineer_speed": +0.50},
        prerequisites={"knowledge": 70}
    ),
    Specialization(
        id="ethicist",
        name="Ethicist",
        category="research",
        bonuses={"moral_rep_bonus": +2},
        prerequisites={"reputation": 60}
    )
]

def can_choose_specialization(spec: Specialization, player_stats: dict) -> bool:
    """Check if player meets prerequisites"""
    for stat, required_value in spec.prerequisites.items():
        if player_stats.get(stat, 0) < required_value:
            return False
    return True

def apply_specialization_bonuses(player_stats: dict, specs: list[Specialization]) -> dict:
    """Apply all chosen specialization bonuses"""
    modified = player_stats.copy()

    for spec in specs:
        for stat, bonus in spec.bonuses.items():
            if stat in modified:
                modified[stat] += bonus

    return modified
```

### Tests (Step 1)
```python
def test_xp_curve_logarithmic():
    """XP should increase exponentially for later levels"""
    xp_for_20 = stat_to_xp(20)
    xp_for_40 = stat_to_xp(40)
    xp_for_60 = stat_to_xp(60)
    xp_for_80 = stat_to_xp(80)

    # Each 20 stat points should require more XP than the last
    assert (xp_for_40 - xp_for_20) < (xp_for_60 - xp_for_40)
    assert (xp_for_60 - xp_for_40) < (xp_for_80 - xp_for_60)

def test_mastery_diminishing_returns():
    """Mastery gains should slow at higher levels"""
    low_mastery_gain = update_mastery(10, True, Quality.STANDARD)
    mid_mastery_gain = update_mastery(50, True, Quality.STANDARD)
    high_mastery_gain = update_mastery(85, True, Quality.STANDARD)

    assert (low_mastery_gain - 10) > (mid_mastery_gain - 50)
    assert (mid_mastery_gain - 50) > (high_mastery_gain - 85)

def test_reputation_modifiers_scale():
    """Higher reputation should give better bonuses"""
    low_rep = get_reputation_modifiers(10)
    high_rep = get_reputation_modifiers(90)

    assert high_rep["price_modifier"] > low_rep["price_modifier"]
    assert high_rep["quest_access"] > low_rep["quest_access"]

def test_specialization_prerequisites():
    """Can't choose spec without meeting requirements"""
    perfectionist = next(s for s in SPECIALIZATIONS if s.id == "perfectionist")

    low_stats = {"precision": 30}
    high_stats = {"precision": 70}

    assert not can_choose_specialization(perfectionist, low_stats)
    assert can_choose_specialization(perfectionist, high_stats)
```

---

## Step 2: API + Events

### 2.1 Data Structures
```python
@dataclass
class PlayerStats:
    knowledge: int
    precision: int
    intuition: int
    business_acumen: int
    combat_instinct: int

    knowledge_xp: int
    precision_xp: int
    intuition_xp: int
    business_xp: int
    combat_xp: int

@dataclass
class StatChange:
    stat: str
    xp_gained: int
    old_xp: int
    new_xp: int
    old_stat: int
    new_stat: int
    milestone_reached: bool
```

### 2.2 Events
```python
@dataclass
class XPGained:
    player_id: str
    stat: str
    amount: int

@dataclass
class StatIncreased:
    player_id: str
    stat: str
    old_value: int
    new_value: int

@dataclass
class MilestoneReached:
    player_id: str
    stat: str
    milestone: int  # 20, 40, 60, 80, 100
    unlocks: list[str]

@dataclass
class SpecializationChosen:
    player_id: str
    specialization: Specialization

@dataclass
class ReputationChanged:
    player_id: str
    region: str
    old_value: int
    new_value: int
    reason: str
```

### 2.3 ProgressionSystem Class
```python
class ProgressionSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

        # Listen to other systems
        event_bus.subscribe(CraftCompleted, self.on_craft_completed)
        event_bus.subscribe(CombatEnded, self.on_combat_ended)
        event_bus.subscribe(SaleMade, self.on_sale_made)

    def add_xp(
        self,
        player_id: str,
        stat: str,
        amount: int,
        current_xp: int
    ) -> StatChange:
        """
        API: Add XP to stat

        1. Add XP
        2. Convert to stat value
        3. Check milestone
        4. Emit events
        """
        old_xp = current_xp
        new_xp = old_xp + amount

        old_stat = xp_to_stat(old_xp)
        new_stat = xp_to_stat(new_xp)

        milestone_reached = False
        if (new_stat // 20) > (old_stat // 20):
            milestone_reached = True

        result = StatChange(
            stat=stat,
            xp_gained=amount,
            old_xp=old_xp,
            new_xp=new_xp,
            old_stat=old_stat,
            new_stat=new_stat,
            milestone_reached=milestone_reached
        )

        # Emit events
        self.event_bus.emit(XPGained(
            player_id=player_id,
            stat=stat,
            amount=amount
        ))

        if new_stat > old_stat:
            self.event_bus.emit(StatIncreased(
                player_id=player_id,
                stat=stat,
                old_value=old_stat,
                new_value=new_stat
            ))

        if milestone_reached:
            milestone = (new_stat // 20) * 20
            unlocks = self._get_milestone_unlocks(stat, milestone)

            self.event_bus.emit(MilestoneReached(
                player_id=player_id,
                stat=stat,
                milestone=milestone,
                unlocks=unlocks
            ))

        return result

    def choose_specialization(
        self,
        player_id: str,
        spec_id: str,
        player_stats: dict
    ) -> bool:
        """
        API: Choose specialization if eligible

        Returns: True if successful, False if not eligible
        """
        spec = next((s for s in SPECIALIZATIONS if s.id == spec_id), None)

        if not spec:
            return False

        if not can_choose_specialization(spec, player_stats):
            return False

        # Success - emit event
        self.event_bus.emit(SpecializationChosen(
            player_id=player_id,
            specialization=spec
        ))

        return True

    def on_craft_completed(self, event: CraftCompleted):
        """Auto-award XP for crafting"""
        if event.success:
            # Award knowledge XP based on difficulty
            xp = event.recipe.difficulty
            self.add_xp(event.crafter_id, "knowledge", xp, ...)

    def on_combat_ended(self, event: CombatEnded):
        """Auto-award XP for combat victory"""
        if event.winner_id:
            xp = 100 + (event.turn_count * 10)
            self.add_xp(event.winner_id, "combat_instinct", xp, ...)

    def on_sale_made(self, event: SaleMade):
        """Auto-award XP for transactions"""
        xp = event.price // 10  # 1 XP per 10 gold
        self.add_xp(event.shop.owner_id, "business_acumen", xp, ...)
```

---

## Step 3: Testbed + Integration

### 3.1 Progression Testbed
```python
class ProgressionTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.progression = ProgressionSystem(self.event_bus)

        self.player_stats = {
            "knowledge": 0,
            "precision": 0,
            "intuition": 0,
            "business_acumen": 0,
            "combat_instinct": 0
        }

        self.player_xp = {
            "knowledge": 0,
            "precision": 0,
            "intuition": 0,
            "business_acumen": 0,
            "combat_instinct": 0
        }

        self.specializations = []

        self.event_bus.subscribe(self._on_event)

    def run(self):
        """Main loop"""
        print("PROGRESSION TESTBED")
        print("=" * 60)

        while True:
            self._display_status()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "add":
                self._add_xp(cmd[1], int(cmd[2]))
            elif cmd[0] == "set":
                self._set_xp(cmd[1], int(cmd[2]))
            elif cmd[0] == "spec":
                self._choose_spec(cmd[1])
            elif cmd[0] == "specs":
                self._list_specializations()
            elif cmd[0] == "sim":
                self._simulate_progression()
            elif cmd[0] == "quit":
                break

    def _add_xp(self, stat: str, amount: int):
        """Add XP to stat"""
        result = self.progression.add_xp(
            "player",
            stat,
            amount,
            self.player_xp[stat]
        )

        self.player_xp[stat] = result.new_xp
        self.player_stats[stat] = result.new_stat

        print(f"\n+{amount} XP to {stat}")
        print(f"  {result.old_stat} → {result.new_stat}")
        print(f"  ({result.new_xp}/{xp_for_next_milestone(result.new_xp)} to next milestone)")

        if result.milestone_reached:
            print(f"  🎉 MILESTONE REACHED: {result.new_stat}!")

    def _simulate_progression(self):
        """Simulate full progression curve"""
        print("\n═══ SIMULATING PROGRESSION ═══")
        print("Crafting 100 potions of increasing difficulty...\n")

        for i in range(100):
            difficulty = min(100, 20 + i)
            xp = difficulty

            result = self.progression.add_xp(
                "player",
                "knowledge",
                xp,
                self.player_xp["knowledge"]
            )

            self.player_xp["knowledge"] = result.new_xp
            self.player_stats["knowledge"] = result.new_stat

            if result.milestone_reached:
                print(f"Craft #{i+1}: MILESTONE {result.new_stat}!")

        print(f"\nFinal Knowledge: {self.player_stats['knowledge']}")
        print(f"Total XP: {self.player_xp['knowledge']}")
```

---

## Success Criteria

This system is complete when:

✅ **XP curves feel fair** - Early progress fast, later slower but achievable
✅ **Stat milestones feel meaningful** - Unlocks matter
✅ **Mastery progression is rewarding** - Bonuses make difference
✅ **Specializations create builds** - Distinct playstyles
✅ **Reputation affects gameplay** - Price/quest/NPC modifiers
✅ **Events integrate properly** - Auto-awards XP from other systems
✅ **Testbed validates curves** - Can simulate full progression
