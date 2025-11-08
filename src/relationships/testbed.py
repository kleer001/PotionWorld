from src.core.event_bus import EventBus
from src.core.data_structures import Personality
from src.relationships.data_structures import NPC, Action
from src.relationships.system import RelationshipSystem
from src.relationships.formulas import calculate_reaction


class RelationshipTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.system = RelationshipSystem(self.event_bus)
        self.current_day = 0
        self.event_log = []

        self.npcs = {
            "thornwood": NPC(
                "thornwood", "Instructor Thornwood",
                Personality(openness=-1, conscientiousness=1, extraversion=0, agreeableness=-1, neuroticism=0)
            ),
            "wisteria": NPC(
                "wisteria", "Healer Wisteria",
                Personality(openness=0, conscientiousness=1, extraversion=-1, agreeableness=1, neuroticism=-1)
            ),
            "kael": NPC(
                "kael", "Rival Kael",
                Personality(openness=1, conscientiousness=0, extraversion=1, agreeableness=-1, neuroticism=0)
            )
        }

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

        self.event_bus.subscribe_all(self._on_event)

    def run(self):
        print("=" * 70)
        print("RELATIONSHIP SYSTEM TESTBED")
        print("=" * 70)
        print()

        while True:
            self._display_status()
            print()
            cmd = input("> ").strip().split()

            if not cmd:
                continue

            try:
                if cmd[0] == "apply" and len(cmd) == 3:
                    self._apply_action(cmd[1], cmd[2])
                elif cmd[0] == "time" and len(cmd) == 2:
                    self._advance_time(int(cmd[1]))
                elif cmd[0] == "npcs":
                    self._list_npcs()
                elif cmd[0] == "actions":
                    self._list_actions()
                elif cmd[0] == "memories" and len(cmd) == 2:
                    self._show_memories(cmd[1])
                elif cmd[0] == "test":
                    self._run_scenario_tests()
                elif cmd[0] == "events":
                    self._show_events()
                elif cmd[0] == "help":
                    self._show_help()
                elif cmd[0] == "quit":
                    break
                else:
                    print("Invalid command. Type 'help' for usage.")
            except (KeyError, ValueError, IndexError) as e:
                print(f"Error: {e}")
                print("Type 'help' for usage.")

    def _display_status(self):
        print(f"\nDay {self.current_day}")
        print("-" * 70)
        for npc_id, npc in self.npcs.items():
            level = int(npc.affinity)
            bar = self._affinity_bar(npc.affinity)
            memories = f"({len(npc.memories)} memories)" if npc.memories else ""
            print(f"{npc.name:20} [{level:+2}] {bar} {npc.affinity:+.1f} {memories}")

    def _affinity_bar(self, affinity):
        width = 20
        normalized = (affinity + 5) / 10
        filled = int(normalized * width)
        return "█" * filled + "░" * (width - filled)

    def _apply_action(self, npc_id, action_id):
        npc = self.npcs[npc_id]
        action = self.actions[action_id]

        print()
        print("=" * 70)
        print(f"Applying '{action.name}' to {npc.name}")
        print("=" * 70)

        self._show_personality(npc.personality)
        self._show_reaction_calculation(npc.personality, action)

        result = self.system.apply_action(npc, action, self.current_day)

        print()
        print("RESULT")
        print("-" * 70)
        print(f"Old Affinity: {result.old_affinity:+.1f}")
        print(f"Delta:        {result.delta:+.1f}")
        print(f"New Affinity: {result.new_affinity:+.1f}")

        if result.threshold_crossed:
            print()
            print(f"⚠️  THRESHOLD CROSSED: {result.new_threshold_level:+d}")
            self._describe_threshold_level(result.new_threshold_level)

        if result.memory_created:
            print()
            print(f"💭 Memory Created: {result.memory_created.event}")
            print(f"   Decay Resistance: {result.memory_created.decay_resistance:.0%}")

    def _show_personality(self, p):
        print()
        print("PERSONALITY")
        print("-" * 70)
        print(f"Openness:          {p.openness:+2d}  {'(Traditional)' if p.openness < 0 else '(Innovative)' if p.openness > 0 else '(Balanced)'}")
        print(f"Conscientiousness: {p.conscientiousness:+2d}  {'(Casual)' if p.conscientiousness < 0 else '(Meticulous)' if p.conscientiousness > 0 else '(Balanced)'}")
        print(f"Extraversion:      {p.extraversion:+2d}  {'(Introverted)' if p.extraversion < 0 else '(Extraverted)' if p.extraversion > 0 else '(Balanced)'}")
        print(f"Agreeableness:     {p.agreeableness:+2d}  {'(Competitive)' if p.agreeableness < 0 else '(Cooperative)' if p.agreeableness > 0 else '(Balanced)'}")
        print(f"Neuroticism:       {p.neuroticism:+2d}  {'(Stable)' if p.neuroticism < 0 else '(Anxious)' if p.neuroticism > 0 else '(Balanced)'}")

    def _show_reaction_calculation(self, personality, action):
        print()
        print("REACTION CALCULATION")
        print("-" * 70)

        trait_map = {
            'O': ('Openness', personality.openness),
            'C': ('Conscientiousness', personality.conscientiousness),
            'E': ('Extraversion', personality.extraversion),
            'A': ('Agreeableness', personality.agreeableness),
            'N': ('Neuroticism', personality.neuroticism),
        }

        total = 0.0
        for trait_key, impact in action.personality_impacts.items():
            trait_name, trait_value = trait_map[trait_key]
            contribution = trait_value * impact
            total += contribution
            print(f"{trait_name:18} {trait_value:+2d} × {impact:+.1f} = {contribution:+.1f}")

        print("-" * 70)
        print(f"{'Total Delta':18} {total:+.1f}")

    def _advance_time(self, days):
        print()
        print(f"Advancing {days} days...")
        self.current_day += days

        print()
        print("DECAY APPLIED")
        print("-" * 70)

        for npc_id, npc in self.npcs.items():
            old_affinity = npc.affinity
            result = self.system.apply_time_decay(npc, self.current_day)

            if result:
                print(f"{npc.name:20} {old_affinity:+.1f} → {result.new_affinity:+.1f} (Δ {result.delta:+.1f})")
            else:
                print(f"{npc.name:20} {old_affinity:+.1f} (no change)")

    def _show_memories(self, npc_id):
        npc = self.npcs[npc_id]

        print()
        print(f"{npc.name}'s Memories")
        print("=" * 70)

        if not npc.memories:
            print("(none)")
            return

        for i, memory in enumerate(npc.memories, 1):
            print()
            print(f"{i}. {memory.event}")
            print(f"   Impact:           {memory.affinity_change:+.1f}")
            print(f"   Day Created:      {memory.day_created}")
            print(f"   Decay Resistance: {memory.decay_resistance:.0%}")

    def _list_npcs(self):
        print()
        print("AVAILABLE NPCs")
        print("=" * 70)
        for npc_id, npc in self.npcs.items():
            print()
            print(f"{npc_id}: {npc.name}")
            self._show_personality(npc.personality)

    def _list_actions(self):
        print()
        print("AVAILABLE ACTIONS")
        print("=" * 70)
        for action_id, action in self.actions.items():
            print()
            print(f"{action_id}: {action.name}")
            print(f"   Impacts: {action.personality_impacts}")

    def _run_scenario_tests(self):
        print()
        print("=" * 70)
        print("SCENARIO TESTS")
        print("=" * 70)

        print()
        print("[Test 1] Building relationship with traditional NPC")
        print("-" * 70)
        npc = NPC("test", "Traditional Tester", Personality(openness=-1, conscientiousness=1, extraversion=0, agreeableness=0, neuroticism=0))

        for i in range(5):
            action = self.actions["traditional"]
            result = self.system.apply_action(npc, action, i)
            print(f"Day {i}: Affinity = {result.new_affinity:+.1f}")

        print(f"Final: {npc.affinity:+.1f} (Expected: ~2.5)")

        print()
        print("[Test 2] Decay without interaction")
        print("-" * 70)
        original_affinity = npc.affinity
        self.system.apply_time_decay(npc, current_day=18)
        print(f"After 2 weeks: {npc.affinity:+.1f} (was {original_affinity:+.1f})")

        print()
        print("[Test 3] Threshold crossing")
        print("-" * 70)
        npc2 = NPC("test2", "Tester 2", Personality(openness=1, conscientiousness=0, extraversion=0, agreeableness=0, neuroticism=0), affinity=0.5)
        action = Action("big", "Big Help", {"O": 1.0})
        result = self.system.apply_action(npc2, action, 20)
        print(f"Crossed: {result.threshold_crossed}, New Level: {result.new_threshold_level}")

    def _show_events(self):
        print()
        print("RECENT EVENTS")
        print("=" * 70)
        for event in self.event_log[-10:]:
            print(f"- {event.__class__.__name__}: {event}")

    def _describe_threshold_level(self, level):
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
        print(f"   {descriptions.get(level, 'Unknown')}")

    def _show_help(self):
        print()
        print("COMMANDS")
        print("=" * 70)
        print("apply <npc> <action>  - Apply action to NPC")
        print("time <days>           - Advance time and apply decay")
        print("npcs                  - List all NPCs with personalities")
        print("actions               - List all available actions")
        print("memories <npc>        - Show NPC's memories")
        print("test                  - Run scenario tests")
        print("events                - Show recent events")
        print("help                  - Show this help")
        print("quit                  - Exit testbed")

    def _on_event(self, event):
        self.event_log.append(event)


if __name__ == '__main__':
    testbed = RelationshipTestbed()
    testbed.run()
