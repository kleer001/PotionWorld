import unittest
from src.core.event_bus import EventBus
from src.core.data_structures import Quality
from src.core.events import (
    ItemAdded,
    ItemRemoved,
    ItemMoved,
    ItemStacked,
    InventoryFull,
)
from src.inventory.system import InventorySystem
from src.inventory.data_structures import ItemStack


class TestInventorySystem(unittest.TestCase):

    def setUp(self):
        self.event_bus = EventBus()
        self.system = InventorySystem(self.event_bus)
        self.events = []

        def capture_event(event):
            self.events.append(event)

        self.event_bus.subscribe(ItemAdded, capture_event)
        self.event_bus.subscribe(ItemRemoved, capture_event)
        self.event_bus.subscribe(ItemMoved, capture_event)
        self.event_bus.subscribe(ItemStacked, capture_event)
        self.event_bus.subscribe(InventoryFull, capture_event)

    def test_create_inventory(self):
        inventory = self.system.create_inventory("player1")

        self.assertEqual(inventory.owner_id, "player1")
        self.assertEqual(len(inventory.slots), 20)
        self.assertEqual(inventory.max_weight, 100.0)

    def test_create_inventory_with_custom_params(self):
        inventory = self.system.create_inventory(
            "player2",
            max_slots=10,
            max_weight=50.0
        )

        self.assertEqual(inventory.max_slots, 10)
        self.assertEqual(inventory.max_weight, 50.0)

    def test_add_item_success(self):
        item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)

        success, reason = self.system.add_item("player1", item_stack)

        self.assertTrue(success)
        self.assertIsNone(reason)

        inventory = self.system.get_inventory("player1")
        self.assertEqual(inventory.count_item("potion1"), 10)

        self.assertEqual(len(self.events), 1)
        self.assertIsInstance(self.events[0], ItemAdded)
        self.assertEqual(self.events[0].item_id, "potion1")
        self.assertEqual(self.events[0].quantity, 10)

    def test_add_item_multiple_stacks(self):
        item_stack = ItemStack("potion1", "potion", 150, Quality.STANDARD)

        success, reason = self.system.add_item("player1", item_stack)

        self.assertTrue(success)

        inventory = self.system.get_inventory("player1")
        self.assertEqual(inventory.count_item("potion1"), 150)

        self.assertEqual(len(self.events), 2)

    def test_add_item_weight_exceeded(self):
        self.system.create_inventory("player1", max_weight=2.0)

        item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)

        success, reason = self.system.add_item("player1", item_stack)

        self.assertFalse(success)
        self.assertEqual(reason, "weight_exceeded")

        full_events = [e for e in self.events if isinstance(e, InventoryFull)]
        self.assertEqual(len(full_events), 1)

    def test_remove_item_success(self):
        item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)
        self.system.add_item("player1", item_stack)
        self.events.clear()

        success, reason = self.system.remove_item("player1", "potion1", 30)

        self.assertTrue(success)
        self.assertIsNone(reason)

        inventory = self.system.get_inventory("player1")
        self.assertEqual(inventory.count_item("potion1"), 20)

        remove_events = [e for e in self.events if isinstance(e, ItemRemoved)]
        self.assertEqual(len(remove_events), 1)
        self.assertEqual(remove_events[0].quantity, 30)

    def test_remove_item_insufficient_quantity(self):
        item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)
        self.system.add_item("player1", item_stack)

        success, reason = self.system.remove_item("player1", "potion1", 50)

        self.assertFalse(success)
        self.assertEqual(reason, "insufficient_quantity")

    def test_remove_item_multiple_stacks(self):
        item_stack1 = ItemStack("potion1", "potion", 99, Quality.STANDARD)
        item_stack2 = ItemStack("potion1", "potion", 50, Quality.STANDARD)
        self.system.add_item("player1", item_stack1)
        self.system.add_item("player1", item_stack2)
        self.events.clear()

        success, reason = self.system.remove_item("player1", "potion1", 120)

        self.assertTrue(success)

        inventory = self.system.get_inventory("player1")
        self.assertEqual(inventory.count_item("potion1"), 29)

    def test_move_item_success(self):
        item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)
        self.system.add_item("player1", item_stack)
        self.events.clear()

        success, reason = self.system.move_item(
            "player1",
            "player2",
            "potion1",
            30
        )

        self.assertTrue(success)
        self.assertIsNone(reason)

        inventory1 = self.system.get_inventory("player1")
        inventory2 = self.system.get_inventory("player2")

        self.assertEqual(inventory1.count_item("potion1"), 20)
        self.assertEqual(inventory2.count_item("potion1"), 30)

        move_events = [e for e in self.events if isinstance(e, ItemMoved)]
        self.assertEqual(len(move_events), 1)
        self.assertEqual(move_events[0].quantity, 30)

    def test_move_item_insufficient_quantity(self):
        item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)
        self.system.add_item("player1", item_stack)

        success, reason = self.system.move_item(
            "player1",
            "player2",
            "potion1",
            50
        )

        self.assertFalse(success)
        self.assertEqual(reason, "insufficient_quantity")

    def test_stack_items_success(self):
        self.system.create_inventory("player1")
        inventory = self.system.get_inventory("player1")

        inventory.slots[0].item_stack = ItemStack("potion1", "potion", 30, Quality.STANDARD)
        inventory.slots[1].item_stack = ItemStack("potion1", "potion", 40, Quality.STANDARD)

        success, reason = self.system.stack_items("player1", 0, 1)

        self.assertTrue(success)
        self.assertIsNone(reason)

        self.assertTrue(inventory.slots[0].is_empty())
        self.assertEqual(inventory.slots[1].item_stack.quantity, 70)

        stack_events = [e for e in self.events if isinstance(e, ItemStacked)]
        self.assertEqual(len(stack_events), 1)

    def test_stack_items_partial_transfer(self):
        self.system.create_inventory("player1")
        inventory = self.system.get_inventory("player1")

        inventory.slots[0].item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)
        inventory.slots[1].item_stack = ItemStack("potion1", "potion", 90, Quality.STANDARD)

        success, reason = self.system.stack_items("player1", 0, 1)

        self.assertTrue(success)

        self.assertEqual(inventory.slots[0].item_stack.quantity, 41)
        self.assertEqual(inventory.slots[1].item_stack.quantity, 99)

    def test_stack_items_not_stackable(self):
        self.system.create_inventory("player1")
        inventory = self.system.get_inventory("player1")

        inventory.slots[0].item_stack = ItemStack("potion1", "potion", 30, Quality.STANDARD)
        inventory.slots[1].item_stack = ItemStack("potion2", "potion", 40, Quality.FINE)

        success, reason = self.system.stack_items("player1", 0, 1)

        self.assertFalse(success)
        self.assertEqual(reason, "not_stackable")

    def test_sort_inventory(self):
        self.system.create_inventory("player1")
        inventory = self.system.get_inventory("player1")

        inventory.slots[0].item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)
        inventory.slots[1].item_stack = ItemStack("herb1", "ingredient", 5, Quality.FINE)
        inventory.slots[2].item_stack = ItemStack("sword1", "equipment", 1, Quality.EXCEPTIONAL)

        success = self.system.sort_inventory("player1", "type")

        self.assertTrue(success)

        self.assertEqual(inventory.slots[0].item_stack.item_type, "equipment")
        self.assertEqual(inventory.slots[1].item_stack.item_type, "ingredient")
        self.assertEqual(inventory.slots[2].item_stack.item_type, "potion")

    def test_compact_inventory(self):
        self.system.create_inventory("player1")
        inventory = self.system.get_inventory("player1")

        inventory.slots[0].item_stack = ItemStack("potion1", "potion", 30, Quality.STANDARD)
        inventory.slots[1].item_stack = ItemStack("potion1", "potion", 40, Quality.STANDARD)
        inventory.slots[2].item_stack = ItemStack("herb1", "ingredient", 150, Quality.FINE)

        success = self.system.compact_inventory("player1")

        self.assertTrue(success)

        self.assertEqual(inventory.slots[0].item_stack.quantity, 70)
        self.assertEqual(inventory.slots[1].item_stack.quantity, 99)
        self.assertEqual(inventory.slots[2].item_stack.quantity, 51)

    def test_get_item_count(self):
        item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)
        self.system.add_item("player1", item_stack)

        count = self.system.get_item_count("player1", "potion1")
        self.assertEqual(count, 50)

        count = self.system.get_item_count("player1", "nonexistent")
        self.assertEqual(count, 0)

    def test_has_item(self):
        item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)
        self.system.add_item("player1", item_stack)

        self.assertTrue(self.system.has_item("player1", "potion1", 30))
        self.assertTrue(self.system.has_item("player1", "potion1", 50))
        self.assertFalse(self.system.has_item("player1", "potion1", 51))
        self.assertFalse(self.system.has_item("player1", "nonexistent"))


if __name__ == "__main__":
    unittest.main()
