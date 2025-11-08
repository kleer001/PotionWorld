#!/usr/bin/env python3

from src.core.event_bus import EventBus
from src.core.data_structures import NPC, Personality, Action
from src.relationships.system import RelationshipSystem


def scenario_1_personality_differences():
    print("=" * 70)
    print("SCENARIO 1: Same Action, Different Personalities")
    print("=" * 70)

    bus = EventBus()
    system = RelationshipSystem(bus)

    action = Action("innovate", "Show innovative potion", {"O": 1.5, "E": 0.5})

    npcs = [
        NPC("traditional", "Traditional Alchemist",
            Personality(openness=-1, conscientiousness=1, extraversion=-1, agreeableness=0, neuroticism=0)),
        NPC("innovative", "Innovative Researcher",
            Personality(openness=1, conscientiousness=0, extraversion=1, agreeableness=1, neuroticism=0)),
        NPC("neutral", "Neutral Merchant",
            Personality(openness=0, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0)),
    ]

    print(f"\nAction: {action.name}")
    print(f"Impacts: {action.personality_impacts}\n")

    for npc in npcs:
        result = system.apply_action(npc, action, current_day=1)
        print(f"{npc.name:25} O:{npc.personality.openness:+2d} E:{npc.personality.extraversion:+2d}  →  Δ{result.delta:+.1f}  =  {result.new_affinity:+.1f}")


def scenario_2_relationship_journey():
    print("\n" + "=" * 70)
    print("SCENARIO 2: Relationship Journey (Neutral → Friend → Decay)")
    print("=" * 70)

    bus = EventBus()
    system = RelationshipSystem(bus)
    events = []
    bus.subscribe_all(lambda e: events.append(e))

    npc = NPC("merchant", "Friendly Merchant",
              Personality(openness=0, conscientiousness=1, extraversion=1, agreeableness=1, neuroticism=0))

    gift = Action("gift", "Give thoughtful gift", {"E": 1.0, "A": 1.0})

    print(f"\nNPC: {npc.name} (E:+1, A:+1)")
    print(f"Action: {gift.name} (E+1.0, A+1.0)\n")

    print("Building relationship:")
    for day in range(5):
        result = system.apply_action(npc, gift, current_day=day)
        crossed = "⚠️  THRESHOLD!" if result.threshold_crossed else ""
        memory = "💭" if result.memory_created else "  "
        print(f"  Day {day}: {result.old_affinity:+.1f} → {result.new_affinity:+.1f}  {memory} {crossed}")

    print(f"\nFinal affinity: {npc.affinity:+.1f}")
    print(f"Memories: {len(npc.memories)}")

    print("\nTime passes (4 weeks without interaction):")
    for week in range(1, 5):
        day = week * 7
        result = system.apply_time_decay(npc, current_day=day)
        if result:
            print(f"  Week {week}: {result.old_affinity:+.1f} → {result.new_affinity:+.1f}")

    print(f"\nFinal affinity after decay: {npc.affinity:+.1f}")
    print(f"Memories preserved: {len(npc.memories)}")

    threshold_count = sum(1 for e in events if e.__class__.__name__ == 'ThresholdCrossed')
    print(f"Thresholds crossed: {threshold_count}")


def scenario_3_conflicting_traits():
    print("\n" + "=" * 70)
    print("SCENARIO 3: Actions with Conflicting Trait Impacts")
    print("=" * 70)

    bus = EventBus()
    system = RelationshipSystem(bus)

    npc = NPC("complex", "Complex Character",
              Personality(openness=1, conscientiousness=-1, extraversion=0, agreeableness=-1, neuroticism=0))

    actions = [
        Action("innovative_messy", "Innovative but messy work", {"O": 1.0, "C": -1.0}),
        Action("precise_boring", "Precise but traditional", {"O": -1.0, "C": 1.0}),
        Action("friendly_competition", "Friendly competition", {"E": 1.0, "A": -1.0}),
    ]

    print(f"\nNPC: {npc.name}")
    print(f"Personality: O:+1 (innovative), C:-1 (casual), A:-1 (competitive)\n")

    for action in actions:
        result = system.apply_action(npc, action, current_day=1)
        print(f"{action.name:25} {str(action.personality_impacts):30} → Δ{result.delta:+.1f}")


def scenario_4_memory_strength():
    print("\n" + "=" * 70)
    print("SCENARIO 4: Memory Strength and Decay Resistance")
    print("=" * 70)

    bus = EventBus()
    system = RelationshipSystem(bus)

    npc = NPC("friend", "Close Friend",
              Personality(openness=1, conscientiousness=0, extraversion=1, agreeableness=1, neuroticism=0))

    actions = [
        ("Small favor", {"A": 0.5}),
        ("Medium help", {"A": 1.2}),
        ("Major sacrifice", {"A": 2.0}),
    ]

    print("\nCreating memories of varying significance:\n")

    for i, (name, impacts) in enumerate(actions):
        action = Action(f"act_{i}", name, impacts)
        result = system.apply_action(npc, action, current_day=i)

        if result.memory_created:
            print(f"{name:20} Δ{result.delta:+.1f}  →  Memory (resistance: {result.memory_created.decay_resistance:.0%})")
        else:
            print(f"{name:20} Δ{result.delta:+.1f}  →  No memory (below threshold)")

    print(f"\nTotal memories: {len(npc.memories)}")
    print(f"Current affinity: {npc.affinity:+.1f}")

    print("\nDecay over 2 weeks:")
    result = system.apply_time_decay(npc, current_day=14)
    print(f"  {result.old_affinity:+.1f} → {result.new_affinity:+.1f}")
    print(f"  Decay: {abs(result.delta):.2f} (memories provided resistance)")


def scenario_5_threshold_unlocks():
    print("\n" + "=" * 70)
    print("SCENARIO 5: Threshold-Based Unlocks (Quest/Shop Simulation)")
    print("=" * 70)

    bus = EventBus()
    system = RelationshipSystem(bus)

    unlocked_features = {
        1: "Basic discount (5%)",
        2: "Improved discount (10%)",
        3: "Friendship quest unlocked",
        4: "Rare items available",
        5: "Master craftsman training",
    }

    threshold_events = []
    bus.subscribe_all(lambda e: threshold_events.append(e) if e.__class__.__name__ == 'ThresholdCrossed' else None)

    npc = NPC("master", "Master Alchemist",
              Personality(openness=0, conscientiousness=1, extraversion=0, agreeableness=1, neuroticism=0))

    help_action = Action("help", "Help with work", {"C": 0.8, "A": 0.8})

    print(f"\nBuilding relationship with {npc.name}:")
    print("Working together each day...\n")

    for day in range(10):
        result = system.apply_action(npc, help_action, current_day=day)

        if result.threshold_crossed:
            level = result.new_threshold_level
            feature = unlocked_features.get(level, "???")
            print(f"Day {day:2}: Affinity {result.new_affinity:+.1f}  →  ⭐ UNLOCKED: {feature}")
        elif day % 2 == 0:
            print(f"Day {day:2}: Affinity {result.new_affinity:+.1f}")

    print(f"\nFinal affinity: {npc.affinity:+.1f}")
    print(f"Features unlocked: {len(threshold_events)}")


if __name__ == '__main__':
    scenario_1_personality_differences()
    scenario_2_relationship_journey()
    scenario_3_conflicting_traits()
    scenario_4_memory_strength()
    scenario_5_threshold_unlocks()

    print("\n" + "=" * 70)
    print("All scenarios complete!")
    print("=" * 70)
