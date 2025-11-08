from src.crafting.testbed import CraftingTestbed


def main():
    print("PotionWorld - Phase 1: Potion Crafting System")
    print("Launching Crafting Testbed...\n")

    testbed = CraftingTestbed()
    testbed.run()


if __name__ == "__main__":
    main()