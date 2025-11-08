from src.core.event_bus import EventBus
from src.quests.system import QuestSystem
from src.quests.data_structures import (
    Quest, QuestState, Objective, ObjectiveType, MoralChoice
)
from src.quests.formulas import check_objective_complete
from src.quests.builder import QuestBuilder


class QuestTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.quest_system = QuestSystem(self.event_bus)

        self.player_state = {
            "knowledge": 50,
            "precision": 40,
            "intuition": 30,
            "business_acumen": 25,
            "combat_instinct": 35,
            "gold": 100,
            "reputation": 50,
            "affinity_elder": 0,
            "affinity_merchant": 0,
            "affinity_rival": 0
        }

        self.quests = self._create_test_quests()
        self.choices = self._create_test_choices()
        self.active_quest = None

        self.event_log = []
        self.event_bus.subscribe(self._log_event)

    def _log_event(self, event):
        self.event_log.append(event)

    def _create_test_quests(self):
        return {
            "craft_quest": (
                QuestBuilder("craft_quest")
                .name("The Apprentice's Trial")
                .description("Craft 5 healing potions to prove your skill")
                .craft_objective("healing_potion", 5)
                .build()
            ),
            "gather_quest": (
                QuestBuilder("gather_quest")
                .name("Herb Collector")
                .description("Gather ingredients for the elder")
                .gather_objective("moonleaf", 20)
                .deliver_objective("elder")
                .build()
            ),
            "advanced_quest": (
                QuestBuilder("advanced_quest")
                .name("Master Alchemist")
                .description("Achieve mastery in alchemy")
                .stat_objective("knowledge", 80)
                .craft_objective("any", 50, "Craft 50 potions of any type")
                .require_stat("knowledge", 60)
                .state(QuestState.LOCKED)
                .build()
            ),
            "duel_quest": (
                QuestBuilder("duel_quest")
                .name("Tournament Champion")
                .description("Win the local tournament")
                .duel_objective(3)
                .build()
            ),
            "merchant_quest": (
                QuestBuilder("merchant_quest")
                .name("Business Tycoon")
                .description("Build your trading empire")
                .gold_objective(1000, "Earn 1000 gold from sales")
                .affinity_objective("merchant", 2.0, "Build strong relationship with merchant")
                .build()
            )
        }

    def _create_test_choices(self):
        return {
            "help_villager": MoralChoice(
                id="help_villager",
                quest_id="gather_quest",
                description="A sick villager needs a potion but cannot pay. Help them?",
                options={
                    "help_free": {
                        "affinity_changes": {"elder": 1.0, "merchant": 0.5},
                        "reputation_change": 10,
                        "gold_change": 0
                    },
                    "charge_half": {
                        "affinity_changes": {"elder": 0.5},
                        "reputation_change": 5,
                        "gold_change": 25
                    },
                    "charge_full": {
                        "affinity_changes": {"elder": -0.5, "merchant": 1.0},
                        "reputation_change": -5,
                        "gold_change": 50
                    },
                    "refuse": {
                        "affinity_changes": {"elder": -1.0},
                        "reputation_change": -15,
                        "gold_change": 0
                    }
                }
            )
        }

    def run(self):
        print("\n" + "=" * 60)
        print("QUEST SYSTEM TESTBED")
        print("=" * 60)
        print("God mode enabled - full control over quest states")
        print("Type 'help' for commands\n")

        while True:
            self._display_status()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            try:
                if cmd[0] == "list":
                    self._list_quests()
                elif cmd[0] == "start" and len(cmd) > 1:
                    self._start_quest(cmd[1])
                elif cmd[0] == "progress":
                    self._show_progress()
                elif cmd[0] == "obj" and len(cmd) > 2:
                    self._increment_objective(cmd[1], int(cmd[2]))
                elif cmd[0] == "choice" and len(cmd) > 2:
                    self._make_choice(cmd[1], cmd[2])
                elif cmd[0] == "complete":
                    self._complete_quest()
                elif cmd[0] == "abandon":
                    self._abandon_quest()
                elif cmd[0] == "state" and len(cmd) > 2:
                    self._set_state(cmd[1], int(cmd[2]))
                elif cmd[0] == "affinity" and len(cmd) > 2:
                    self._set_affinity(cmd[1], float(cmd[2]))
                elif cmd[0] == "unlock" and len(cmd) > 1:
                    self._unlock_quest(cmd[1])
                elif cmd[0] == "events":
                    n = int(cmd[1]) if len(cmd) > 1 else 10
                    self._show_events(n)
                elif cmd[0] == "test":
                    self._run_scenario_tests()
                elif cmd[0] == "help":
                    self._show_help()
                elif cmd[0] == "quit":
                    break
                else:
                    print("Unknown command. Type 'help' for available commands.")
            except (IndexError, ValueError) as e:
                print(f"Error: {e}")
                print("Type 'help' for command usage.")

    def _display_status(self):
        print("\n" + "-" * 60)
        print("PLAYER STATE")
        print("-" * 60)
        print(f"Knowledge: {self.player_state['knowledge']:<3}  "
              f"Precision: {self.player_state['precision']:<3}  "
              f"Intuition: {self.player_state['intuition']:<3}")
        print(f"Business:  {self.player_state['business_acumen']:<3}  "
              f"Combat:    {self.player_state['combat_instinct']:<3}")
        print(f"Gold: {self.player_state['gold']:<5}  Reputation: {self.player_state['reputation']}")
        print()
        print("Affinities:")
        print(f"  Elder:    {self.player_state['affinity_elder']:>5.1f}")
        print(f"  Merchant: {self.player_state['affinity_merchant']:>5.1f}")
        print(f"  Rival:    {self.player_state['affinity_rival']:>5.1f}")

        if self.active_quest:
            print(f"\nActive Quest: {self.active_quest.name}")

    def _list_quests(self):
        print("\n" + "=" * 60)
        print("AVAILABLE QUESTS")
        print("=" * 60)

        for quest_id, quest in self.quests.items():
            state_symbol = {
                QuestState.LOCKED: "🔒",
                QuestState.AVAILABLE: "📋",
                QuestState.ACTIVE: "⚡",
                QuestState.COMPLETED: "✓",
                QuestState.FAILED: "✗"
            }.get(quest.state, "?")

            print(f"\n{state_symbol} [{quest.state.value.upper()}] {quest.name}")
            print(f"   ID: {quest_id}")
            print(f"   {quest.description}")
            print(f"   Objectives: {len(quest.objectives)}")

            if quest.prerequisites:
                print(f"   Prerequisites: {quest.prerequisites}")

    def _start_quest(self, quest_id: str):
        if quest_id not in self.quests:
            print(f"Quest '{quest_id}' not found")
            return

        quest = self.quests[quest_id]

        if quest.state == QuestState.LOCKED:
            print(f"Quest is locked. Use 'unlock {quest_id}' first.")
            return

        success, reason = self.quest_system.start_quest(
            quest, "player", self.player_state
        )

        if success:
            self.active_quest = quest
            print(f"✓ Started: {quest.name}")
            self._show_progress()
        else:
            print(f"✗ Cannot start: {reason}")

    def _show_progress(self):
        if not self.active_quest:
            print("No active quest")
            return

        progress = self.quest_system.get_quest_progress(
            self.active_quest, self.player_state
        )

        print("\n" + "=" * 60)
        print(f"QUEST: {self.active_quest.name}")
        print("=" * 60)
        print(f"State: {self.active_quest.state.value}")
        print(f"Progress: {progress.objectives_complete}/{progress.objectives_total}")

        print("\nObjectives:")
        for i, obj in enumerate(self.active_quest.objectives):
            obj_id = f"obj_{i}"
            current = self.active_quest.progress.get(obj_id, 0)
            complete = check_objective_complete(
                {
                    "type": obj.type.value,
                    "target": obj.target,
                    "quantity": obj.quantity,
                    "value": obj.value
                },
                current,
                self.player_state
            )

            status = "✓" if complete else " "

            if obj.type in [ObjectiveType.CRAFT_POTION, ObjectiveType.GATHER_ITEM, ObjectiveType.WIN_DUEL]:
                print(f"  [{status}] {obj.description} ({current}/{obj.quantity})")
            elif obj.type == ObjectiveType.EARN_GOLD:
                print(f"  [{status}] {obj.description} ({current}/{int(obj.value)})")
            elif obj.type in [ObjectiveType.REACH_AFFINITY, ObjectiveType.REACH_STAT]:
                current_val = self.player_state.get(f"{obj.target}" if obj.type == ObjectiveType.REACH_STAT else f"affinity_{obj.target}", 0)
                print(f"  [{status}] {obj.description} ({current_val}/{obj.value})")
            else:
                print(f"  [{status}] {obj.description}")

        if progress.can_complete:
            print("\n  → Quest can be completed! Use 'complete' command.")

    def _increment_objective(self, obj_id: str, amount: int):
        if not self.active_quest:
            print("No active quest")
            return

        self.quest_system.update_objective(
            self.active_quest, obj_id, amount, "player", self.player_state
        )

        print(f"✓ Incremented {obj_id} by {amount}")
        self._show_progress()

    def _make_choice(self, choice_id: str, option: str):
        if choice_id not in self.choices:
            print(f"Choice '{choice_id}' not found")
            return

        choice = self.choices[choice_id]

        if option not in choice.options:
            print(f"Option '{option}' not available")
            print(f"Available options: {', '.join(choice.options.keys())}")
            return

        print(f"\n{choice.description}")
        print(f"You chose: {option}")

        consequences = self.quest_system.make_choice(
            choice, option, "player", self.player_state
        )

        print("\nConsequences:")
        for npc, change in consequences.get("affinity_changes", {}).items():
            old_val = self.player_state.get(f"affinity_{npc}", 0)
            self.player_state[f"affinity_{npc}"] = old_val + change
            print(f"  {npc} affinity: {old_val:+.1f} → {old_val + change:+.1f}")

        if "reputation_change" in consequences:
            old_rep = self.player_state["reputation"]
            self.player_state["reputation"] += consequences["reputation_change"]
            print(f"  Reputation: {old_rep} → {self.player_state['reputation']}")

        if "gold_change" in consequences:
            old_gold = self.player_state["gold"]
            self.player_state["gold"] += consequences["gold_change"]
            print(f"  Gold: {old_gold} → {self.player_state['gold']}")

        for flag, value in consequences.get("world_flags", {}).items():
            print(f"  World flag set: {flag} = {value}")

    def _complete_quest(self):
        if not self.active_quest:
            print("No active quest")
            return

        success, reason = self.quest_system.complete_quest(
            self.active_quest, "player", self.player_state
        )

        if success:
            print(f"✓ Quest completed: {self.active_quest.name}")
            self.player_state[f"quest_{self.active_quest.id}"] = "completed"
            self.active_quest = None
        else:
            print(f"✗ Cannot complete: {reason}")

    def _abandon_quest(self):
        if not self.active_quest:
            print("No active quest")
            return

        success = self.quest_system.abandon_quest(self.active_quest, "player")

        if success:
            print(f"✓ Quest abandoned: {self.active_quest.name}")
            self.active_quest = None

    def _set_state(self, stat: str, value: int):
        self.player_state[stat] = value
        print(f"✓ Set {stat} = {value}")

    def _set_affinity(self, npc: str, value: float):
        self.player_state[f"affinity_{npc}"] = value
        print(f"✓ Set affinity_{npc} = {value}")

    def _unlock_quest(self, quest_id: str):
        if quest_id not in self.quests:
            print(f"Quest '{quest_id}' not found")
            return

        quest = self.quests[quest_id]
        success = self.quest_system.unlock_quest(quest, "player")

        if success:
            print(f"✓ Unlocked: {quest.name}")
        else:
            print(f"✗ Quest already unlocked or not in LOCKED state")

    def _show_events(self, n: int):
        print("\n" + "=" * 60)
        print(f"RECENT EVENTS (last {n})")
        print("=" * 60)

        for event in self.event_log[-n:]:
            print(f"  {event.__class__.__name__}")

    def _run_scenario_tests(self):
        print("\n" + "=" * 60)
        print("RUNNING SCENARIO TESTS")
        print("=" * 60)

        passed = 0
        total = 0

        total += 1
        print("\nTest 1: Complete linear quest")
        quest = self.quests["craft_quest"]
        quest.state = QuestState.AVAILABLE
        self.quest_system.start_quest(quest, "test", {})
        self.quest_system.update_objective(quest, "obj_0", 5, "test", {})
        success, _ = self.quest_system.complete_quest(quest, "test", {})
        if success:
            print("  ✓ PASS")
            passed += 1
        else:
            print("  ✗ FAIL")

        total += 1
        print("\nTest 2: Prerequisites blocking")
        quest = self.quests["advanced_quest"]
        success, _ = self.quest_system.start_quest(quest, "test", {"knowledge": 30})
        if not success:
            print("  ✓ PASS")
            passed += 1
        else:
            print("  ✗ FAIL")

        print("\n" + "=" * 60)
        print(f"Results: {passed}/{total} tests passed")
        print("=" * 60)

    def _show_help(self):
        print("\n" + "=" * 60)
        print("COMMANDS")
        print("=" * 60)
        print("list                       - List all quests")
        print("start <quest_id>           - Start a quest")
        print("progress                   - Show active quest progress")
        print("obj <id> <amount>          - Increment objective (god mode)")
        print("choice <id> <option>       - Make a moral choice")
        print("complete                   - Complete active quest")
        print("abandon                    - Abandon active quest")
        print("unlock <quest_id>          - Unlock a locked quest (god mode)")
        print("state <stat> <value>       - Set player stat (god mode)")
        print("affinity <npc> <value>     - Set NPC affinity (god mode)")
        print("events [n]                 - Show recent n events (default 10)")
        print("test                       - Run scenario tests")
        print("help                       - Show this help")
        print("quit                       - Exit testbed")


def main():
    testbed = QuestTestbed()
    testbed.run()


if __name__ == "__main__":
    main()
