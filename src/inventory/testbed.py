import sys
from src.core.event_bus import EventBus
from src.core.data_structures import Quality
from src.inventory.system import InventorySystem
from src.inventory.data_structures import ItemStack


class InventoryTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.system = InventorySystem(self.event_bus)
        self.events = []

        self.event_bus.subscribe_all(self.capture_event)

        self.system.create_inventory("player", max_slots=20, max_weight=100.0)

    def capture_event(self, event):
        self.events.append(event)

    def print_inventory(self, owner_id: str):
        inventory = self.system.get_inventory(owner_id)
        print(f"\n{'=' * 60}")
        print(f"INVENTORY: {owner_id}")
        print(f"{'=' * 60}")
        print(f"Slots: {inventory.max_slots}")
        print(f"Weight: {inventory.current_weight:.1f} / {inventory.max_weight:.1f}")
        print(f"{'-' * 60}")

        for slot in inventory.slots:
            if not slot.is_empty():
                stack = slot.item_stack
                quality_str = f"[{stack.quality.name}]" if stack.quality else ""
                print(f"[{slot.slot_index:2d}] {stack.item_id:15s} "
                      f"x{stack.quantity:3d}  {stack.item_type:12s} {quality_str}")

        empty_count = len(inventory.get_empty_slots())
        print(f"{'-' * 60}")
        print(f"Empty slots: {empty_count}/{inventory.max_slots}")

    def run_tests(self):
        print("\nRUNNING INVENTORY TESTS")
        print("=" * 60)

        print("\n1. Testing add_item...")
        item = ItemStack("healing_potion", "potion", 50, Quality.STANDARD)
        success, _ = self.system.add_item("player", item)
        print(f"   Added 50 healing potions: {success}")

        print("\n2. Testing add_item with stacking...")
        item = ItemStack("healing_potion", "potion", 100, Quality.STANDARD)
        success, _ = self.system.add_item("player", item)
        print(f"   Added 100 more healing potions: {success}")
        count = self.system.get_item_count("player", "healing_potion")
        print(f"   Total healing potions: {count}")

        print("\n3. Testing add_item different quality...")
        item = ItemStack("mana_potion", "potion", 30, Quality.FINE)
        success, _ = self.system.add_item("player", item)
        print(f"   Added 30 mana potions (FINE): {success}")

        print("\n4. Testing add_item ingredients...")
        item = ItemStack("moonleaf", "ingredient", 150, Quality.STANDARD)
        success, _ = self.system.add_item("player", item)
        print(f"   Added 150 moonleaf: {success}")

        print("\n5. Testing remove_item...")
        success, _ = self.system.remove_item("player", "healing_potion", 75)
        print(f"   Removed 75 healing potions: {success}")
        count = self.system.get_item_count("player", "healing_potion")
        print(f"   Remaining healing potions: {count}")

        print("\n6. Testing sort_inventory...")
        item = ItemStack("sword", "equipment", 1, Quality.EXCEPTIONAL)
        self.system.add_item("player", item)
        self.system.sort_inventory("player", "type")
        print("   Sorted inventory by type")

        print("\n7. Testing compact_inventory...")
        self.system.compact_inventory("player")
        print("   Compacted inventory")

        print("\n8. Testing move_item...")
        self.system.create_inventory("merchant", max_slots=10)
        success, _ = self.system.move_item("player", "merchant", "moonleaf", 50)
        print(f"   Moved 50 moonleaf to merchant: {success}")

        print("\n9. Final inventory states:")
        self.print_inventory("player")
        self.print_inventory("merchant")

        print(f"\n10. Total events emitted: {len(self.events)}")

    def run_interactive(self):
        print("\nINVENTORY TESTBED")
        print("=" * 60)
        self.print_help()

        while True:
            try:
                command = input("\n> ").strip().split()

                if not command:
                    continue

                cmd = command[0].lower()

                if cmd == "quit" or cmd == "exit":
                    break

                elif cmd == "help":
                    self.print_help()

                elif cmd == "inv":
                    owner = command[1] if len(command) > 1 else "player"
                    self.print_inventory(owner)

                elif cmd == "add":
                    if len(command) < 4:
                        print("Usage: add <owner> <item_id> <quantity> [type] [quality]")
                        continue

                    owner = command[1]
                    item_id = command[2]
                    quantity = int(command[3])
                    item_type = command[4] if len(command) > 4 else "potion"
                    quality_str = command[5] if len(command) > 5 else "STANDARD"
                    quality = Quality[quality_str.upper()]

                    item = ItemStack(item_id, item_type, quantity, quality)
                    success, reason = self.system.add_item(owner, item)

                    if success:
                        print(f"✓ Added {quantity}x {item_id}")
                    else:
                        print(f"✗ Failed: {reason}")

                elif cmd == "remove":
                    if len(command) < 4:
                        print("Usage: remove <owner> <item_id> <quantity>")
                        continue

                    owner = command[1]
                    item_id = command[2]
                    quantity = int(command[3])

                    success, reason = self.system.remove_item(owner, item_id, quantity)

                    if success:
                        print(f"✓ Removed {quantity}x {item_id}")
                    else:
                        print(f"✗ Failed: {reason}")

                elif cmd == "move":
                    if len(command) < 5:
                        print("Usage: move <from> <to> <item_id> <quantity>")
                        continue

                    from_owner = command[1]
                    to_owner = command[2]
                    item_id = command[3]
                    quantity = int(command[4])

                    success, reason = self.system.move_item(
                        from_owner, to_owner, item_id, quantity
                    )

                    if success:
                        print(f"✓ Moved {quantity}x {item_id} from {from_owner} to {to_owner}")
                    else:
                        print(f"✗ Failed: {reason}")

                elif cmd == "sort":
                    owner = command[1] if len(command) > 1 else "player"
                    sort_by = command[2] if len(command) > 2 else "type"

                    self.system.sort_inventory(owner, sort_by)
                    print(f"✓ Sorted {owner}'s inventory by {sort_by}")

                elif cmd == "compact":
                    owner = command[1] if len(command) > 1 else "player"

                    self.system.compact_inventory(owner)
                    print(f"✓ Compacted {owner}'s inventory")

                elif cmd == "count":
                    if len(command) < 3:
                        print("Usage: count <owner> <item_id>")
                        continue

                    owner = command[1]
                    item_id = command[2]
                    count = self.system.get_item_count(owner, item_id)
                    print(f"{owner} has {count}x {item_id}")

                elif cmd == "events":
                    n = int(command[1]) if len(command) > 1 else 10
                    print(f"\nRecent {n} events:")
                    for event in self.events[-n:]:
                        print(f"  {event}")

                elif cmd == "test":
                    self.run_tests()

                else:
                    print(f"Unknown command: {cmd}")
                    print("Type 'help' for available commands")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def print_help(self):
        print("\nAvailable commands:")
        print("-" * 60)
        print("inv [owner]                      - Show inventory")
        print("add <owner> <item> <qty> [type] [quality] - Add item")
        print("remove <owner> <item> <qty>      - Remove item")
        print("move <from> <to> <item> <qty>    - Move item between inventories")
        print("sort [owner] [by]                - Sort inventory (type/quantity/quality)")
        print("compact [owner]                  - Compact inventory")
        print("count <owner> <item>             - Count item quantity")
        print("events [n]                       - Show recent n events")
        print("test                             - Run automated tests")
        print("help                             - Show this help")
        print("quit                             - Exit testbed")


def main():
    testbed = InventoryTestbed()

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        testbed.run_tests()
    else:
        testbed.run_interactive()


if __name__ == "__main__":
    main()
