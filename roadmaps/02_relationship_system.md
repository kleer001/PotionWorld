# Relationship System: 3-Step Implementation

## Overview
Big 5 personality-based NPC relationships with affinity tracking, memory system, and decay mechanics.

**Core Validation:** Personality traits meaningfully affect reactions, affinity progresses naturally, decay creates maintenance gameplay, memories persist.

---

## Step 1: Core Logic

### 1.1 Personality Reaction Calculation
```python
@dataclass
class Personality:
    openness: int        # -1, 0, +1
    conscientiousness: int
    extraversion: int
    agreeableness: int
    neuroticism: int

def calculate_reaction(personality: Personality, action: Action) -> float:
    """
    Pure function: Calculate affinity delta based on personality match

    Returns: float between -2.0 and +2.0
    """
    delta = 0.0

    # Each trait contributes if action has that impact
    for trait_name, trait_value in personality.__dict__.items():
        if trait_name in action.personality_impacts:
            impact = action.personality_impacts[trait_name]
            delta += trait_value * impact

    return max(-2.0, min(2.0, delta))

@dataclass
class Action:
    id: str
    name: str
    personality_impacts: dict[str, float]  # e.g., {"O": 1.0, "E": 0.5}
    creates_memory_threshold: float = 1.0
```

**Example:**
```python
# Innovative action
action = Action(
    id="innovative_potion",
    name="Show innovative potion",
    personality_impacts={"O": 1.0, "E": 0.5, "N": -0.5}
)

# Traditional NPC (Low Openness)
npc_traditional = Personality(O=-1, C=1, E=0, A=0, N=0)
delta = calculate_reaction(npc_traditional, action)
# Result: -1.0 (dislikes innovation)

# Open NPC (High Openness)
npc_open = Personality(O=1, C=0, E=1, A=0, N=0)
delta = calculate_reaction(npc_open, action)
# Result: 1.5 (likes innovation + energetic)
```

### 1.2 Affinity Decay
```python
def calculate_decay(
    current_affinity: float,  # -5.0 to +5.0
    days_passed: int,
    decay_rate: float = 0.5   # per week
) -> float:
    """
    Pure function: Regression toward neutral over time

    Returns: new affinity value
    """
    if current_affinity == 0:
        return 0

    weeks_passed = days_passed / 7.0
    decay_amount = weeks_passed * decay_rate

    # Move toward zero
    if current_affinity > 0:
        return max(0, current_affinity - decay_amount)
    else:
        return min(0, current_affinity + decay_amount)
```

### 1.3 Memory System
```python
@dataclass
class Memory:
    event: str
    affinity_change: float
    day_created: int
    decay_resistance: float  # 0.0 to 1.0

def should_create_memory(affinity_delta: float, threshold: float = 1.0) -> bool:
    """Significant events become memories"""
    return abs(affinity_delta) >= threshold

def calculate_decay_with_memories(
    current_affinity: float,
    days_passed: int,
    memories: list[Memory],
    decay_rate: float = 0.5
) -> float:
    """
    Memories resist decay proportionally to their strength
    """
    base_decay = calculate_decay(current_affinity, days_passed, decay_rate)

    # Memories reduce decay
    memory_resistance = sum(m.decay_resistance for m in memories) / max(1, len(memories))
    actual_decay = current_affinity + (base_decay - current_affinity) * (1 - memory_resistance)

    return actual_decay
```

### 1.4 Threshold Detection
```python
def check_threshold_crossed(old_affinity: float, new_affinity: float) -> tuple[bool, int]:
    """
    Detect when affinity crosses integer boundaries

    Returns: (crossed, new_level)
    """
    old_level = int(old_affinity)
    new_level = int(new_affinity)

    if old_level != new_level:
        return (True, new_level)

    return (False, old_level)
```

### Tests (Step 1)
```python
def test_personality_reaction_matches_traits():
    """High O likes innovation, low O dislikes it"""
    action = Action("innovate", personality_impacts={"O": 1.0})

    high_o = Personality(O=1, C=0, E=0, A=0, N=0)
    low_o = Personality(O=-1, C=0, E=0, A=0, N=0)

    assert calculate_reaction(high_o, action) == 1.0
    assert calculate_reaction(low_o, action) == -1.0

def test_multiple_traits_combine():
    """Multiple personality traits should combine"""
    action = Action("social_gift", personality_impacts={"E": 1.0, "A": 0.5})

    npc = Personality(O=0, C=0, E=1, A=1, N=0)
    delta = calculate_reaction(npc, action)

    assert delta == 1.5  # 1.0 + 0.5

def test_decay_moves_toward_neutral():
    """Affinity decays toward zero over time"""
    positive = calculate_decay(current_affinity=3.0, days_passed=7)
    assert 0 < positive < 3.0

    negative = calculate_decay(current_affinity=-3.0, days_passed=7)
    assert -3.0 < negative < 0

def test_memories_resist_decay():
    """Memories slow decay"""
    memories = [Memory("helped", 2.0, 0, decay_resistance=0.5)]

    with_memories = calculate_decay_with_memories(3.0, 7, memories)
    without_memories = calculate_decay(3.0, 7)

    assert with_memories > without_memories

def test_threshold_detection():
    """Detect crossing integer boundaries"""
    crossed, level = check_threshold_crossed(0.9, 1.1)
    assert crossed == True
    assert level == 1

    not_crossed, _ = check_threshold_crossed(1.1, 1.3)
    assert not_crossed == False
```

---

## Step 2: API + Events

### 2.1 Data Structures
```python
@dataclass
class NPC:
    id: str
    name: str
    personality: Personality
    affinity: float = 0.0
    memories: list[Memory] = field(default_factory=list)
    last_interaction: int = 0  # day number

@dataclass
class AffinityChange:
    npc_id: str
    delta: float
    new_affinity: float
    old_affinity: float
    threshold_crossed: bool
    new_threshold_level: int
    memory_created: Optional[Memory]
    reason: str  # action_id or "decay"
```

### 2.2 Events
```python
@dataclass
class AffinityChanged:
    npc_id: str
    delta: float
    new_affinity: float
    reason: str
    timestamp: int

@dataclass
class ThresholdCrossed:
    npc_id: str
    old_level: int
    new_level: int
    direction: str  # "positive" or "negative"

@dataclass
class MemoryCreated:
    npc_id: str
    memory: Memory

@dataclass
class RelationshipDecayed:
    npc_id: str
    old_affinity: float
    new_affinity: float
    days_passed: int
```

### 2.3 RelationshipSystem Class
```python
class RelationshipSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        # Could listen to time passage events
        event_bus.subscribe(DayPassed, self.on_day_passed)

    def apply_action(
        self,
        npc: NPC,
        action: Action,
        current_day: int
    ) -> AffinityChange:
        """
        Main API: Apply action to NPC, calculate affinity change

        1. Calculate reaction based on personality
        2. Apply to affinity (clamped -5 to +5)
        3. Check threshold crossing
        4. Create memory if significant
        5. Emit events
        """
        # Calculate delta
        delta = calculate_reaction(npc.personality, action)

        old_affinity = npc.affinity
        new_affinity = max(-5.0, min(5.0, old_affinity + delta))

        # Check threshold
        threshold_crossed, new_level = check_threshold_crossed(old_affinity, new_affinity)

        # Create memory if significant
        memory = None
        if should_create_memory(delta, action.creates_memory_threshold):
            memory = Memory(
                event=action.id,
                affinity_change=delta,
                day_created=current_day,
                decay_resistance=min(1.0, abs(delta) / 2.0)
            )
            npc.memories.append(memory)
            self.event_bus.emit(MemoryCreated(npc.id, memory))

        # Update NPC state
        npc.affinity = new_affinity
        npc.last_interaction = current_day

        # Emit events
        self.event_bus.emit(AffinityChanged(
            npc_id=npc.id,
            delta=delta,
            new_affinity=new_affinity,
            reason=action.id,
            timestamp=current_day
        ))

        if threshold_crossed:
            direction = "positive" if new_level > int(old_affinity) else "negative"
            self.event_bus.emit(ThresholdCrossed(
                npc_id=npc.id,
                old_level=int(old_affinity),
                new_level=new_level,
                direction=direction
            ))

        return AffinityChange(
            npc_id=npc.id,
            delta=delta,
            new_affinity=new_affinity,
            old_affinity=old_affinity,
            threshold_crossed=threshold_crossed,
            new_threshold_level=new_level,
            memory_created=memory,
            reason=action.id
        )

    def apply_time_decay(
        self,
        npc: NPC,
        current_day: int,
        decay_rate: float = 0.5
    ) -> AffinityChange:
        """
        Apply time-based decay to affinity
        """
        days_passed = current_day - npc.last_interaction

        if days_passed == 0:
            return None

        old_affinity = npc.affinity
        new_affinity = calculate_decay_with_memories(
            old_affinity,
            days_passed,
            npc.memories,
            decay_rate
        )

        npc.affinity = new_affinity

        delta = new_affinity - old_affinity

        self.event_bus.emit(RelationshipDecayed(
            npc_id=npc.id,
            old_affinity=old_affinity,
            new_affinity=new_affinity,
            days_passed=days_passed
        ))

        return AffinityChange(
            npc_id=npc.id,
            delta=delta,
            new_affinity=new_affinity,
            old_affinity=old_affinity,
            threshold_crossed=False,
            new_threshold_level=int(new_affinity),
            memory_created=None,
            reason="decay"
        )

    def on_day_passed(self, event: DayPassed):
        """Auto-apply decay when time passes"""
        # Would iterate all NPCs and apply decay
        pass
```

### Tests (Step 2)
```python
def test_apply_action_emits_events():
    """Applying action should emit AffinityChanged event"""
    events = []
    bus = EventBus()
    bus.subscribe(lambda e: events.append(e))

    rel = RelationshipSystem(bus)
    npc = NPC("test", "Test", Personality(O=1, C=0, E=0, A=0, N=0))
    action = Action("innovate", personality_impacts={"O": 1.0})

    result = rel.apply_action(npc, action, current_day=1)

    assert any(isinstance(e, AffinityChanged) for e in events)
    assert result.new_affinity == 1.0

def test_threshold_crossing_emits_event():
    """Crossing threshold emits ThresholdCrossed event"""
    events = []
    bus = EventBus()
    bus.subscribe(lambda e: events.append(e))

    rel = RelationshipSystem(bus)
    npc = NPC("test", "Test", Personality(O=1, C=0, E=0, A=0, N=0), affinity=0.5)
    action = Action("big_help", personality_impacts={"O": 1.0})

    result = rel.apply_action(npc, action, current_day=1)

    assert result.threshold_crossed
    assert any(isinstance(e, ThresholdCrossed) for e in events)

def test_memory_creation():
    """Significant events create memories"""
    bus = EventBus()
    rel = RelationshipSystem(bus)
    npc = NPC("test", "Test", Personality(O=1, C=0, E=0, A=0, N=0))

    # Big impact action
    action = Action("huge_favor", personality_impacts={"O": 2.0})

    result = rel.apply_action(npc, action, current_day=1)

    assert result.memory_created is not None
    assert len(npc.memories) == 1
```

---

## Step 3: Testbed + Integration

### 3.1 Relationship Testbed
```python
class RelationshipTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.relationships = RelationshipSystem(self.event_bus)
        self.current_day = 0

        # Load NPCs
        self.npcs = {
            "thornwood": NPC(
                "thornwood", "Instructor Thornwood",
                Personality(O=-1, C=1, E=0, A=-1, N=0)
            ),
            "wisteria": NPC(
                "wisteria", "Healer Wisteria",
                Personality(O=0, C=1, E=-1, A=1, N=-1)
            ),
            "kael": NPC(
                "kael", "Rival Kael",
                Personality(O=1, C=0, E=1, A=-1, N=0)
            )
        }

        # Load actions
        self.actions = {
            "innovative": Action("innovative", "Show innovative potion",
                                {"O": 1.0, "E": 0.5, "N": -0.5}),
            "traditional": Action("traditional", "Follow traditional method",
                                 {"O": -0.5, "C": 0.5, "N": 0.5}),
            "gift": Action("gift", "Give thoughtful gift",
                          {"E": 1.0, "A": 0.5}),
            "haggle": Action("haggle", "Haggle on price",
                            {"C": -0.5, "A": -1.0, "E": 0.5})
        }

        # Listen to events
        self.event_bus.subscribe(self._on_event)

    def run(self):
        """Main CLI loop"""
        print("RELATIONSHIP TESTBED")
        print("=" * 60)

        while True:
            self._display_status()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "apply":
                self._apply_action(cmd[1], cmd[2])
            elif cmd[0] == "time":
                self._advance_time(int(cmd[1]))
            elif cmd[0] == "npcs":
                self._list_npcs()
            elif cmd[0] == "actions":
                self._list_actions()
            elif cmd[0] == "memories":
                self._show_memories(cmd[1])
            elif cmd[0] == "test":
                self._run_scenario_tests()
            elif cmd[0] == "quit":
                break

    def _apply_action(self, npc_id: str, action_id: str):
        """Apply action to NPC and display result"""
        npc = self.npcs[npc_id]
        action = self.actions[action_id]

        print(f"\nApplying '{action.name}' to {npc.name}...")
        print(f"\nPersonality: O:{npc.personality.openness:+d} "
              f"C:{npc.personality.conscientiousness:+d} "
              f"E:{npc.personality.extraversion:+d} "
              f"A:{npc.personality.agreeableness:+d} "
              f"N:{npc.personality.neuroticism:+d}")

        # Calculate what will happen
        delta = calculate_reaction(npc.personality, action)

        print(f"\nReaction Calculation:")
        for trait, impact in action.personality_impacts.items():
            trait_value = getattr(npc.personality, trait.lower() +
                                ("penness" if trait == "O" else
                                 "onscientiousness" if trait == "C" else
                                 "xtraversion" if trait == "E" else
                                 "greeableness" if trait == "A" else
                                 "euroticism"))
            contribution = trait_value * impact
            print(f"  {trait}: {trait_value:+d} × {impact:+.1f} = {contribution:+.1f}")
        print(f"  {'─' * 30}")
        print(f"  Total Delta: {delta:+.1f}")

        # Apply
        result = self.relationships.apply_action(npc, action, self.current_day)

        print(f"\nResult:")
        print(f"  Old Affinity: {result.old_affinity:+.1f}")
        print(f"  New Affinity: {result.new_affinity:+.1f}")

        if result.threshold_crossed:
            print(f"  ⚠️  THRESHOLD CROSSED: {result.new_threshold_level}")
            self._describe_threshold_level(result.new_threshold_level)

        if result.memory_created:
            print(f"  💭 Memory Created: {result.memory_created.event}")

    def _advance_time(self, days: int):
        """Advance time and apply decay"""
        print(f"\nAdvancing {days} days...")
        self.current_day += days

        print(f"\nApplying decay to all NPCs:")
        for npc_id, npc in self.npcs.items():
            old_affinity = npc.affinity
            result = self.relationships.apply_time_decay(npc, self.current_day)

            if result:
                print(f"  {npc.name}: {old_affinity:+.1f} → {result.new_affinity:+.1f}")

    def _show_memories(self, npc_id: str):
        """Display NPC's memories"""
        npc = self.npcs[npc_id]

        print(f"\n{npc.name}'s Memories:")
        if not npc.memories:
            print("  (none)")
            return

        for i, memory in enumerate(npc.memories, 1):
            print(f"\n  {i}. {memory.event}")
            print(f"     Impact: {memory.affinity_change:+.1f}")
            print(f"     Day: {memory.day_created}")
            print(f"     Decay Resistance: {memory.decay_resistance:.1%}")

    def _run_scenario_tests(self):
        """Run pre-defined scenario tests"""
        print("\n" + "=" * 60)
        print("SCENARIO TESTS")
        print("=" * 60)

        # Test 1: Build relationship with traditional NPC
        print("\n[Test 1] Building relationship with traditional NPC")
        npc = NPC("test", "Test", Personality(O=-1, C=1, E=0, A=0, N=0))

        for i in range(5):
            action = self.actions["traditional"]
            result = self.relationships.apply_action(npc, action, i)
            print(f"  Day {i}: Affinity = {result.new_affinity:+.1f}")

        print(f"  Final: {npc.affinity:+.1f} (Expected: ~2.5)")

        # Test 2: Decay over time
        print("\n[Test 2] Decay without interaction")
        original_affinity = npc.affinity
        self.relationships.apply_time_decay(npc, current_day=i+14)  # 2 weeks
        print(f"  After 2 weeks: {npc.affinity:+.1f} (was {original_affinity:+.1f})")

    def _describe_threshold_level(self, level: int):
        """Describe what this affinity level means"""
        descriptions = {
            -5: "Nemesis - Actively sabotages you",
            -4: "Antagonistic - Works against you indirectly",
            -3: "Hostile - May refuse service",
            -2: "Unfriendly - Reluctant, price increases",
            -1: "Cool - Mild dislike",
            0: "Neutral - Professional, transactional",
            1: "Positive - Slightly favorable",
            2: "Warm - Positive interactions",
            3: "Friendly - Helps willingly, discounts",
            4: "Loyal - Actively supports you",
            5: "Devoted - Would sacrifice for you"
        }
        print(f"     {descriptions.get(level, 'Unknown')}")
```

### 3.2 Integration with Quest System
```python
class QuestSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

        # Listen to relationship events
        event_bus.subscribe(ThresholdCrossed, self.on_threshold_crossed)

    def on_threshold_crossed(self, event: ThresholdCrossed):
        """Unlock quests when reaching certain affinity levels"""
        if event.new_level >= 3:
            # Unlock friendship quest
            self.unlock_quest(f"friendship_{event.npc_id}")
        elif event.new_level <= -3:
            # Unlock rivalry quest
            self.unlock_quest(f"rivalry_{event.npc_id}")

# Integration test
def test_relationship_unlocks_quest():
    """High affinity should unlock NPC quest"""
    bus = EventBus()
    relationships = RelationshipSystem(bus)
    quests = QuestSystem(bus)

    npc = NPC("test", "Test", Personality(O=1, C=0, E=0, A=0, N=0), affinity=2.5)
    action = Action("big_favor", personality_impacts={"O": 1.0})

    # This should cross threshold to +3
    result = relationships.apply_action(npc, action, current_day=1)

    # Quest system should have received event and unlocked quest
    assert "friendship_test" in quests.unlocked_quests
```

---

## Success Criteria

This system is complete when:

✅ **Personality reactions feel distinct** - Each Big 5 trait matters
✅ **Affinity progression feels earned** - Not too easy/hard
✅ **Decay creates maintenance** - But not frustrating
✅ **Memories prevent decay appropriately** - Significant events stick
✅ **Threshold events trigger** - At correct affinity levels
✅ **Events integrate with other systems** - Quest unlocks, economy prices, etc.
✅ **Testbed validates all mechanics** - Can manually verify behavior
