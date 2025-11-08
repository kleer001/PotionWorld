#!/usr/bin/env python3
"""PotionWorld - Unified system testbed launcher."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description='PotionWorld - System Testbeds',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python systest.py --crafting          Launch crafting testbed
  python systest.py --relationship      Launch relationship testbed
  python systest.py --combat            Launch combat testbed
  python systest.py --economy           Launch economy testbed
  python systest.py --progression       Launch progression testbed
  python systest.py --inventory         Launch inventory testbed
  python systest.py --quest             Launch quest testbed
        """
    )

    parser.add_argument(
        '--crafting',
        action='store_true',
        help='Launch the crafting system testbed'
    )

    parser.add_argument(
        '--relationship',
        action='store_true',
        help='Launch the relationship system testbed'
    )

    parser.add_argument(
        '--combat',
        action='store_true',
        help='Launch the combat system testbed'
    )

    parser.add_argument(
        '--economy',
        action='store_true',
        help='Launch the economy system testbed'
    )

    parser.add_argument(
        '--progression',
        action='store_true',
        help='Launch the progression system testbed'
    )

    parser.add_argument(
        '--inventory',
        action='store_true',
        help='Launch the inventory system testbed'
    )

    parser.add_argument(
        '--quest',
        action='store_true',
        help='Launch the quest system testbed'
    )

    args = parser.parse_args()

    # Count how many systems were specified
    systems = [args.crafting, args.relationship, args.combat,
               args.economy, args.progression, args.inventory, args.quest]
    selected_count = sum(systems)

    if selected_count == 0:
        print("PotionWorld - Phase 1: Potion Crafting System")
        print("=" * 60)
        print("\nNo system specified. Use --crafting to launch the crafting testbed.")
        print("Use --help to see all available options.")
        sys.exit(0)

    if selected_count > 1:
        print("Error: Please specify only one system at a time.")
        sys.exit(1)

    # Launch the appropriate system
    if args.crafting:
        print("PotionWorld - Phase 1: Potion Crafting System")
        print("Launching Crafting Testbed...\n")
        from src.crafting.testbed import CraftingTestbed
        testbed = CraftingTestbed()
        testbed.run()

    elif args.relationship:
        print("PotionWorld - Phase 2: Relationship System")
        print("Launching Relationship Testbed...\n")
        from src.relationships.testbed import RelationshipTestbed
        testbed = RelationshipTestbed()
        testbed.run()

    elif args.combat:
        print("PotionWorld - Phase 3: Combat System")
        print("Launching Combat Testbed...\n")
        from src.combat.testbed import CombatTestbed
        testbed = CombatTestbed()
        testbed.run()

    elif args.economy:
        print("PotionWorld - Phase 4: Economy System")
        print("Launching Economy Testbed...\n")
        from src.economy.testbed import EconomyTestbed
        testbed = EconomyTestbed()
        testbed.run_all_tests()
        testbed.interactive_mode()

    elif args.progression:
        print("PotionWorld - Phase 5: Progression System")
        print("Launching Progression Testbed...\n")
        from src.progression.testbed import ProgressionTestbed
        testbed = ProgressionTestbed()
        testbed.run()

    elif args.inventory:
        print("PotionWorld - Phase 6: Inventory System")
        print("Launching Inventory Testbed...\n")
        from src.inventory.testbed import InventoryTestbed
        testbed = InventoryTestbed()
        testbed.run()

    elif args.quest:
        print("PotionWorld - Phase 7: Quest System")
        print("Launching Quest Testbed...\n")
        from src.quests.testbed import QuestTestbed
        testbed = QuestTestbed()
        testbed.run()


if __name__ == "__main__":
    main()
