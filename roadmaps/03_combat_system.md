# Combat System: 3-Step Implementation

## Overview
Turn-based potion combat with ESENS-driven effects, status management, triggers, and personality-based AI.

**Core Validation:** Turn structure works, ESENS effects apply correctly, triggers chain properly, AI makes personality-appropriate decisions.

---

## Step 1: Core Logic

### 1.1 Combat Stats & Damage
```python
@dataclass
class CombatStats:
    health: int
    max_health: int
    strength: int
    defense: int
    initiative: int
    resistance: int  # Status effect resistance

def calculate_damage(
    attacker_strength: int,
    defender_defense: int,
    base_damage: int,
    element: Optional[str] = None
) -> int:
    """
    Pure function: Calculate final damage after defense

    Returns: int damage amount
    """
    # Base damage modified by strength
    modified_damage = base_damage * (1 + attacker_strength / 100)

    # Reduced by defense
    damage_reduction = defender_defense / 100
    final_damage = modified_damage * (1 - damage_reduction)

    # Element bonus/penalty (if implemented)
    if element:
        final_damage *= get_element_multiplier(element, defender)

    return max(1, int(final_damage))  # Minimum 1 damage
```

### 1.2 Status Effects
```python
@dataclass
class StatusEffect:
    name: str
    source: str  # potion that applied it
    stat_affected: str  # "strength", "defense", etc.
    modifier: float  # +30% = 1.3, -20% = 0.8
    duration: int  # turns remaining, -1 for permanent
    triggers: list[Trigger]
    removable: bool  # .RN flag
    stackable: bool  # .ST flag
    element: Optional[str]

def apply_status(combatant: Combatant, effect: StatusEffect):
    """Apply status effect, handle stacking"""
    if effect.stackable:
        combatant.active_effects.append(effect)
    else:
        # Remove existing effect of same type
        combatant.active_effects = [
            e for e in combatant.active_effects
            if e.name != effect.name
        ]
        combatant.active_effects.append(effect)

def calculate_modified_stat(
    base_stat: int,
    effects: list[StatusEffect],
    stat_name: str
) -> int:
    """Calculate stat after all status modifiers"""
    modified = base_stat

    for effect in effects:
        if effect.stat_affected == stat_name:
            if effect.modifier < 1.0:
                # Debuff: multiply base
                modified *= effect.modifier
            else:
                # Buff: additive
                modified *= effect.modifier

    return int(modified)
```

### 1.3 Trigger System
```python
@dataclass
class Trigger:
    trigger_type: str  # "^S", "vE", ">A", "<D", ">Sprd"
    effect_esens: str
    condition: Optional[callable] = None

def evaluate_triggers(
    phase: str,  # "start_turn", "end_turn", "on_attack", "on_defend"
    combatant: Combatant,
    context: dict
) -> list[StatusEffect]:
    """
    Evaluate all triggers for current phase

    Returns: list of new effects to apply
    """
    new_effects = []

    for effect in combatant.active_effects:
        for trigger in effect.triggers:
            if trigger_matches_phase(trigger.trigger_type, phase):
                if trigger.condition is None or trigger.condition(context):
                    # Parse ESENS and create new effect
                    new_effect = parse_trigger_effect(trigger.effect_esens)
                    new_effects.append(new_effect)

    return new_effects

def trigger_matches_phase(trigger_type: str, phase: str) -> bool:
    """Map trigger types to phases"""
    mapping = {
        "^S": "start_turn",
        "vE": "end_turn",
        ">A": "on_attack",
        "<D": "on_defend",
        ">Sprd": "on_spread"
    }
    return mapping.get(trigger_type) == phase
```

### 1.4 Turn Resolution
```python
def resolve_turn(
    actor: Combatant,
    action: CombatAction,
    target: Combatant
) -> TurnResult:
    """
    Pure function: Resolve one combat turn

    1. Start-of-turn triggers
    2. Execute action
    3. End-of-turn triggers
    4. Update durations
    5. Check victory

    Returns: TurnResult with all changes
    """
    changes = []

    # Phase 1: Start-of-turn
    start_effects = evaluate_triggers("start_turn", actor, {})
    for effect in start_effects:
        apply_status(actor, effect)
        changes.append(f"Trigger: {effect.name}")

    # Phase 2: Execute action
    if action.type == "USE_POTION":
        potion_result = apply_potion(action.potion, actor, target)
        changes.extend(potion_result.changes)

    elif action.type == "GUARD":
        # Temp defense boost
        guard_effect = StatusEffect(
            name="Guard",
            stat_affected="defense",
            modifier=1.5,
            duration=1,
            removable=False,
            stackable=False
        )
        apply_status(actor, guard_effect)
        changes.append("Actor guards (+50% defense this turn)")

    # Phase 3: End-of-turn triggers
    end_effects = evaluate_triggers("end_turn", actor, {})
    for effect in end_effects:
        apply_status(actor, effect)
        changes.append(f"End trigger: {effect.name}")

    # Phase 4: Update durations
    update_durations(actor)
    update_durations(target)

    # Phase 5: Check victory
    victor = None
    if target.health <= 0:
        victor = actor.id
    elif actor.health <= 0:
        victor = target.id

    return TurnResult(
        changes=changes,
        actor_health=actor.health,
        target_health=target.health,
        victor=victor
    )
```

### 1.5 AI Decision Making
```python
def evaluate_potion_value(
    potion: Potion,
    actor: Combatant,
    target: Combatant,
    personality: Personality
) -> float:
    """
    Score a potion choice based on situation and personality

    Returns: float score (higher = better choice)
    """
    score = 0.0

    # Analyze potion effects
    effects = parse_esens(potion.esens_notation)

    for effect in effects:
        # Offensive effects
        if effect.target == "E" and effect.type == "damage":
            score += effect.magnitude * 2
            # High Extraversion = more aggressive
            if personality.extraversion > 0:
                score *= 1.5

        # Defensive effects
        if effect.target == "P" and effect.type == "defense":
            score += effect.magnitude
            # High Agreeableness = more defensive
            if personality.agreeableness > 0:
                score *= 1.3

        # Healing
        if effect.type == "heal":
            health_deficit = actor.max_health - actor.health
            score += (health_deficit / actor.max_health) * 100

        # Status effects
        if effect.type == "status":
            # High Openness = likes complex status effects
            if personality.openness > 0:
                score += 20

    # Situation modifiers
    if actor.health < actor.max_health * 0.3:
        # Low health = panic behavior if high Neuroticism
        if personality.neuroticism > 0:
            # Prioritize healing
            if "heal" in [e.type for e in effects]:
                score *= 2.0

    return score

def choose_best_potion(
    available_potions: list[Potion],
    actor: Combatant,
    target: Combatant,
    personality: Personality
) -> Potion:
    """
    AI: Choose best potion based on situation and personality
    """
    scores = [
        (potion, evaluate_potion_value(potion, actor, target, personality))
        for potion in available_potions
    ]

    # High Conscientiousness = consistent choices
    if personality.conscientiousness > 0:
        # Pick best
        return max(scores, key=lambda x: x[1])[0]
    else:
        # Add some randomness
        weighted_random = random.choices(
            [p for p, s in scores],
            weights=[s for p, s in scores]
        )[0]
        return weighted_random
```

### Tests (Step 1)
```python
def test_damage_calculation():
    """Verify damage formula"""
    damage = calculate_damage(
        attacker_strength=50,
        defender_defense=30,
        base_damage=20
    )
    # 20 * 1.5 * 0.7 = 21
    assert 20 <= damage <= 22

def test_status_stacking():
    """Stackable effects should accumulate"""
    combatant = Combatant()

    stackable = StatusEffect("Strength", stackable=True, modifier=1.3)
    apply_status(combatant, stackable)
    apply_status(combatant, stackable)

    assert len([e for e in combatant.active_effects if e.name == "Strength"]) == 2

    modified = calculate_modified_stat(100, combatant.active_effects, "strength")
    assert modified == 169  # 100 * 1.3 * 1.3

def test_trigger_evaluation():
    """Triggers should fire in correct phase"""
    combatant = Combatant()

    regen_effect = StatusEffect(
        "Regen",
        triggers=[Trigger("^S", "P+H10")]
    )
    combatant.active_effects.append(regen_effect)

    # Should fire on start turn
    start_triggers = evaluate_triggers("start_turn", combatant, {})
    assert len(start_triggers) > 0

    # Should not fire on end turn
    end_triggers = evaluate_triggers("end_turn", combatant, {})
    assert len(end_triggers) == 0

def test_ai_personality_affects_choices():
    """AI should make personality-appropriate choices"""
    aggressive_npc = Personality(E=1, A=-1)
    defensive_npc = Personality(E=-1, A=1)

    damage_potion = Potion(esens="E#Damage30")
    heal_potion = Potion(esens="P+H20")

    agg_choice = choose_best_potion(
        [damage_potion, heal_potion],
        Combatant(health=80),
        Combatant(health=50),
        aggressive_npc
    )

    def_choice = choose_best_potion(
        [damage_potion, heal_potion],
        Combatant(health=80),
        Combatant(health=50),
        defensive_npc
    )

    # Aggressive should prefer damage
    # Defensive should prefer healing
    # (Would need multiple runs to prove statistically)
```

---

## Step 2: API + Events

### 2.1 Data Structures
```python
@dataclass
class Combatant:
    id: str
    name: str
    stats: CombatStats
    active_effects: list[StatusEffect]
    combat_belt: list[Potion]  # max 10
    personality: Optional[Personality] = None  # For AI

@dataclass
class CombatAction:
    type: str  # "USE_POTION", "GUARD", "OBSERVE"
    potion: Optional[Potion] = None

@dataclass
class TurnResult:
    changes: list[str]
    actor_health: int
    target_health: int
    status_applied: list[StatusEffect]
    status_removed: list[str]
    victor: Optional[str]
```

### 2.2 Events
```python
@dataclass
class TurnExecuted:
    combat_id: str
    turn_number: int
    actor_id: str
    action: CombatAction
    result: TurnResult

@dataclass
class DamageDealt:
    source_id: str
    target_id: str
    amount: int
    element: Optional[str]

@dataclass
class StatusApplied:
    target_id: str
    effect: StatusEffect
    source: str

@dataclass
class TriggerActivated:
    combatant_id: str
    trigger_type: str
    effect: StatusEffect

@dataclass
class CombatEnded:
    combat_id: str
    winner_id: str
    turn_count: int
```

### 2.3 CombatSystem Class
```python
class CombatSystem:
    def __init__(self, event_bus: EventBus, esens_parser: ESENSParser):
        self.event_bus = event_bus
        self.parser = esens_parser

    def execute_turn(
        self,
        combat_id: str,
        turn_number: int,
        actor: Combatant,
        action: CombatAction,
        target: Combatant
    ) -> TurnResult:
        """
        Main API: Execute one combat turn

        1. Evaluate start-of-turn triggers
        2. Execute action
        3. Evaluate end-of-turn triggers
        4. Update durations
        5. Check victory
        6. Emit events
        """
        result = resolve_turn(actor, action, target)

        # Emit detailed events
        for change in result.changes:
            if "damage" in change.lower():
                # Parse damage from change string
                damage = parse_damage_from_string(change)
                self.event_bus.emit(DamageDealt(
                    source_id=actor.id,
                    target_id=target.id,
                    amount=damage
                ))

        for effect in result.status_applied:
            self.event_bus.emit(StatusApplied(
                target_id=target.id,
                effect=effect,
                source=actor.id
            ))

        # Emit turn completion
        self.event_bus.emit(TurnExecuted(
            combat_id=combat_id,
            turn_number=turn_number,
            actor_id=actor.id,
            action=action,
            result=result
        ))

        # Check victory
        if result.victor:
            self.event_bus.emit(CombatEnded(
                combat_id=combat_id,
                winner_id=result.victor,
                turn_count=turn_number
            ))

        return result

    def create_ai_action(
        self,
        actor: Combatant,
        target: Combatant
    ) -> CombatAction:
        """
        AI: Choose action for NPC combatant
        """
        if not actor.personality:
            # Default: choose random potion
            potion = random.choice(actor.combat_belt)
            return CombatAction(type="USE_POTION", potion=potion)

        # Personality-based choice
        potion = choose_best_potion(
            actor.combat_belt,
            actor,
            target,
            actor.personality
        )

        return CombatAction(type="USE_POTION", potion=potion)
```

### Tests (Step 2)
```python
def test_turn_execution_emits_events():
    """Executing turn should emit events"""
    events = []
    bus = EventBus()
    bus.subscribe(lambda e: events.append(e))

    combat = CombatSystem(bus, ESENSParser())

    actor = Combatant(...)
    target = Combatant(...)
    action = CombatAction(type="USE_POTION", potion=damage_potion)

    result = combat.execute_turn("test", 1, actor, action, target)

    assert any(isinstance(e, TurnExecuted) for e in events)
    assert any(isinstance(e, DamageDealt) for e in events)

def test_victory_emits_combat_ended():
    """Reducing opponent to 0 HP emits CombatEnded"""
    events = []
    bus = EventBus()
    bus.subscribe(lambda e: events.append(e))

    combat = CombatSystem(bus, ESENSParser())

    actor = Combatant(health=100)
    target = Combatant(health=1)  # Will die
    action = CombatAction(type="USE_POTION", potion=big_damage_potion)

    result = combat.execute_turn("test", 1, actor, action, target)

    assert any(isinstance(e, CombatEnded) for e in events)
    assert result.victor == actor.id
```

---

## Step 3: Testbed + Integration

### 3.1 Combat Testbed
```python
class CombatTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.combat = CombatSystem(self.event_bus, ESENSParser())

        # Create player and opponent
        self.player = Combatant(
            id="player",
            name="Player",
            stats=CombatStats(health=100, max_health=100, strength=50, defense=30, ...),
            combat_belt=self._create_default_belt(),
            active_effects=[]
        )

        self.opponent = Combatant(
            id="opponent",
            name="Test Opponent",
            stats=CombatStats(health=100, max_health=100, strength=40, defense=25, ...),
            combat_belt=self._create_enemy_belt(),
            active_effects=[],
            personality=Personality(O=1, C=0, E=1, A=-1, N=0)  # Aggressive
        )

        self.turn = 0
        self.combat_id = "testbed"

        # Listen to events
        self.event_bus.subscribe(self._on_event)

    def run(self):
        """Main combat loop"""
        print("COMBAT TESTBED")
        print("=" * 60)

        while True:
            self._display_combat_state()

            if self.player.stats.health <= 0:
                print("\n💀 DEFEAT!")
                break
            if self.opponent.stats.health <= 0:
                print("\n🎉 VICTORY!")
                break

            # Player turn
            print(f"\n[Turn {self.turn + 1}] YOUR TURN")
            action = self._get_player_action()

            if action:
                self._execute_player_turn(action)

                # Check if opponent died
                if self.opponent.stats.health <= 0:
                    continue

                # Opponent turn
                self._execute_opponent_turn()

    def _display_combat_state(self):
        """Show current combat state"""
        print(f"\n{'=' * 60}")
        print(f"TURN {self.turn}")
        print(f"{'=' * 60}")

        print(f"\n{self.player.name}")
        print(f"  HP: {self.player.stats.health}/{self.player.stats.max_health}")
        if self.player.active_effects:
            print(f"  Effects: {', '.join(e.name for e in self.player.active_effects)}")

        print(f"\n{self.opponent.name}")
        print(f"  HP: {self.opponent.stats.health}/{self.opponent.stats.max_health}")
        if self.opponent.active_effects:
            print(f"  Effects: {', '.join(e.name for e in self.opponent.active_effects)}")

    def _get_player_action(self) -> CombatAction:
        """Prompt player for action"""
        print("\nYour Potions:")
        for i, potion in enumerate(self.player.combat_belt, 1):
            print(f"  {i}. {potion.name} - {potion.esens_notation}")

        print("\nActions:")
        print("  [1-10] Use potion")
        print("  [g] Guard")
        print("  [o] Observe")
        print("  [q] Quit")

        choice = input("\n> ").strip().lower()

        if choice == 'q':
            return None
        elif choice == 'g':
            return CombatAction(type="GUARD")
        elif choice == 'o':
            return CombatAction(type="OBSERVE")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.combat_belt):
                return CombatAction(
                    type="USE_POTION",
                    potion=self.player.combat_belt[idx]
                )

        return self._get_player_action()  # Invalid, try again

    def _execute_player_turn(self, action: CombatAction):
        """Execute player's turn"""
        result = self.combat.execute_turn(
            self.combat_id,
            self.turn,
            self.player,
            action,
            self.opponent
        )

        print("\n" + "\n".join(result.changes))
        self.turn += 1

    def _execute_opponent_turn(self):
        """AI opponent's turn"""
        print(f"\n[Turn {self.turn + 1}] OPPONENT'S TURN")

        action = self.combat.create_ai_action(self.opponent, self.player)

        print(f"  {self.opponent.name} uses {action.potion.name}!")

        result = self.combat.execute_turn(
            self.combat_id,
            self.turn,
            self.opponent,
            action,
            self.player
        )

        print("\n".join(result.changes))
        self.turn += 1
```

### 3.2 Integration with Progression
```python
class ProgressionSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        event_bus.subscribe(CombatEnded, self.on_combat_ended)

    def on_combat_ended(self, event: CombatEnded):
        """Award XP for combat victory"""
        if event.winner_id == "player":
            # Award Combat Instinct XP
            xp_amount = 100 + (event.turn_count * 10)  # Bonus for quick wins
            self.add_xp("player", "combat_instinct", xp_amount)

# Integration test
def test_combat_victory_grants_xp():
    """Winning combat should award Combat Instinct XP"""
    bus = EventBus()
    combat = CombatSystem(bus, ESENSParser())
    progression = ProgressionSystem(bus)

    player = Combatant(id="player", ...)
    enemy = Combatant(id="enemy", health=1, ...)  # Easy kill

    # Execute turn that kills enemy
    result = combat.execute_turn("test", 1, player, kill_action, enemy)

    # Check XP was awarded
    assert progression.get_stat("player", "combat_instinct") > 0
```

---

## Success Criteria

This system is complete when:

✅ **Turn structure flows correctly** - Phases execute in order
✅ **Damage calculation works** - Strength/defense matter
✅ **Status effects apply/stack properly** - .ST and .RN flags work
✅ **Triggers fire at correct times** - ^S, vE, >A, <D work
✅ **Trigger chains don't infinite loop** - Safety mechanisms
✅ **AI makes personality-based choices** - Distinct behaviors
✅ **Combat feels strategic** - Not just random
✅ **Events integrate with other systems** - XP, quests, etc.
✅ **Testbed validates all mechanics** - Can play full combat manually
