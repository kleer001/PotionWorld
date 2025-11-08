import unittest
from src.core.data_structures import Quality
from src.inventory.data_structures import (
    Inventory,
    InventorySlot,
    ItemStack,
)
from src.inventory.formulas import (
    calculate_item_weight,
    can_add_item,
    calculate_available_space,
    find_slots_to_add,
    can_remove_item,
    find_slots_to_remove,
    calculate_total_weight,
    can_stack_slots,
    calculate_stack_transfer,
    sort_inventory_slots,
    compact_inventory,
)


class TestInventoryFormulas(unittest.TestCase):

    def setUp(self):
        self.weights = {
            "potion": 0.5,
            "ingredient": 0.2,
            "equipment": 2.0
        }

    def test_calculate_item_weight(self):
        weight = calculate_item_weight("potion", 10, self.weights)
        self.assertEqual(weight, 5.0)

        weight = calculate_item_weight("ingredient", 5, self.weights)
        self.assertEqual(weight, 1.0)

        weight = calculate_item_weight("unknown", 1, self.weights)
        self.assertEqual(weight, 1.0)

    def test_can_add_item_success(self):
        slots = [InventorySlot(i) for i in range(5)]
        inventory = Inventory("test", slots, 5, 100.0, 0.0)

        item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)

        can_add, reason = can_add_item(inventory, item_stack, 99, self.weights)
        self.assertTrue(can_add)
        self.assertIsNone(reason)

    def test_can_add_item_weight_exceeded(self):
        slots = [InventorySlot(i) for i in range(5)]
        inventory = Inventory("test", slots, 5, 2.0, 0.0)

        item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)

        can_add, reason = can_add_item(inventory, item_stack, 99, self.weights)
        self.assertFalse(can_add)
        self.assertEqual(reason, "weight_exceeded")

    def test_can_add_item_insufficient_space(self):
        slots = [InventorySlot(i) for i in range(2)]
        inventory = Inventory("test", slots, 2, 100.0, 0.0)

        item_stack = ItemStack("potion1", "potion", 200, Quality.STANDARD)

        can_add, reason = can_add_item(inventory, item_stack, 99, self.weights)
        self.assertFalse(can_add)
        self.assertEqual(reason, "insufficient_space")

    def test_calculate_available_space_empty_inventory(self):
        slots = [InventorySlot(i) for i in range(5)]
        inventory = Inventory("test", slots, 5, 100.0, 0.0)

        item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)

        space = calculate_available_space(inventory, item_stack, 99)
        self.assertEqual(space, 99 * 5)

    def test_calculate_available_space_with_stackable_items(self):
        slots = [InventorySlot(i) for i in range(3)]
        slots[0].item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)

        inventory = Inventory("test", slots, 3, 100.0, 0.0)

        item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)

        space = calculate_available_space(inventory, item_stack, 99)
        self.assertEqual(space, 49 + 99 * 2)

    def test_find_slots_to_add_empty_inventory(self):
        slots = [InventorySlot(i) for i in range(5)]
        inventory = Inventory("test", slots, 5, 100.0, 0.0)

        item_stack = ItemStack("potion1", "potion", 150, Quality.STANDARD)

        slots_to_fill = find_slots_to_add(inventory, item_stack, 99)

        self.assertEqual(len(slots_to_fill), 2)
        self.assertEqual(slots_to_fill[0], (0, 99))
        self.assertEqual(slots_to_fill[1], (1, 51))

    def test_find_slots_to_add_with_existing_stack(self):
        slots = [InventorySlot(i) for i in range(3)]
        slots[0].item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)

        inventory = Inventory("test", slots, 3, 100.0, 0.0)

        item_stack = ItemStack("potion1", "potion", 100, Quality.STANDARD)

        slots_to_fill = find_slots_to_add(inventory, item_stack, 99)

        self.assertEqual(len(slots_to_fill), 2)
        self.assertEqual(slots_to_fill[0], (0, 49))
        self.assertEqual(slots_to_fill[1], (1, 51))

    def test_can_remove_item_success(self):
        slots = [InventorySlot(i) for i in range(2)]
        slots[0].item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)
        inventory = Inventory("test", slots, 2, 100.0, 0.0)

        can_remove, reason = can_remove_item(inventory, "potion1", 30)
        self.assertTrue(can_remove)
        self.assertIsNone(reason)

    def test_can_remove_item_insufficient_quantity(self):
        slots = [InventorySlot(i) for i in range(2)]
        slots[0].item_stack = ItemStack("potion1", "potion", 50, Quality.STANDARD)
        inventory = Inventory("test", slots, 2, 100.0, 0.0)

        can_remove, reason = can_remove_item(inventory, "potion1", 100)
        self.assertFalse(can_remove)
        self.assertEqual(reason, "insufficient_quantity")

    def test_find_slots_to_remove(self):
        slots = [InventorySlot(i) for i in range(3)]
        slots[0].item_stack = ItemStack("potion1", "potion", 30, Quality.STANDARD)
        slots[1].item_stack = ItemStack("potion1", "potion", 40, Quality.STANDARD)
        inventory = Inventory("test", slots, 3, 100.0, 0.0)

        slots_to_remove = find_slots_to_remove(inventory, "potion1", 50)

        self.assertEqual(len(slots_to_remove), 2)
        self.assertEqual(slots_to_remove[0], (0, 30))
        self.assertEqual(slots_to_remove[1], (1, 20))

    def test_calculate_total_weight(self):
        slots = [InventorySlot(i) for i in range(3)]
        slots[0].item_stack = ItemStack("potion1", "potion", 10, Quality.STANDARD)
        slots[1].item_stack = ItemStack("herb1", "ingredient", 20, Quality.STANDARD)
        inventory = Inventory("test", slots, 3, 100.0, 0.0)

        total_weight = calculate_total_weight(inventory, self.weights)
        self.assertEqual(total_weight, 5.0 + 4.0)

    def test_can_stack_slots_success(self):
        slots = [InventorySlot(i) for i in range(3)]
        slots[0].item_stack = ItemStack("potion1", "potion", 30, Quality.STANDARD)
        slots[1].item_stack = ItemStack("potion1", "potion", 40, Quality.STANDARD)
        inventory = Inventory("test", slots, 3, 100.0, 0.0)

        can_stack, reason = can_stack_slots(inventory, 0, 1, 99)
        self.assertTrue(can_stack)
        self.assertIsNone(reason)

    def test_can_stack_slots_not_stackable(self):
        slots = [InventorySlot(i) for i in range(3)]
        slots[0].item_stack = ItemStack("potion1", "potion", 30, Quality.STANDARD)
        slots[1].item_stack = ItemStack("potion2", "potion", 40, Quality.FINE)
        inventory = Inventory("test", slots, 3, 100.0, 0.0)

        can_stack, reason = can_stack_slots(inventory, 0, 1, 99)
        self.assertFalse(can_stack)
        self.assertEqual(reason, "not_stackable")

    def test_can_stack_slots_to_slot_full(self):
        slots = [InventorySlot(i) for i in range(3)]
        slots[0].item_stack = ItemStack("potion1", "potion", 30, Quality.STANDARD)
        slots[1].item_stack = ItemStack("potion1", "potion", 99, Quality.STANDARD)
        inventory = Inventory("test", slots, 3, 100.0, 0.0)

        can_stack, reason = can_stack_slots(inventory, 0, 1, 99)
        self.assertFalse(can_stack)
        self.assertEqual(reason, "to_slot_full")

    def test_calculate_stack_transfer_full_transfer(self):
        transfer, new_from, new_to = calculate_stack_transfer(30, 40, 99)

        self.assertEqual(transfer, 30)
        self.assertEqual(new_from, 0)
        self.assertEqual(new_to, 70)

    def test_calculate_stack_transfer_partial_transfer(self):
        transfer, new_from, new_to = calculate_stack_transfer(50, 90, 99)

        self.assertEqual(transfer, 9)
        self.assertEqual(new_from, 41)
        self.assertEqual(new_to, 99)

    def test_sort_inventory_slots_by_type(self):
        slots = [
            InventorySlot(0, ItemStack("potion1", "potion", 10, Quality.STANDARD)),
            InventorySlot(1, ItemStack("herb1", "ingredient", 5, Quality.FINE)),
            InventorySlot(2, None),
            InventorySlot(3, ItemStack("sword1", "equipment", 1, Quality.EXCEPTIONAL)),
        ]

        sorted_slots = sort_inventory_slots(slots, "type")

        self.assertEqual(sorted_slots[0].item_stack.item_type, "equipment")
        self.assertEqual(sorted_slots[1].item_stack.item_type, "ingredient")
        self.assertEqual(sorted_slots[2].item_stack.item_type, "potion")
        self.assertTrue(sorted_slots[3].is_empty())

    def test_sort_inventory_slots_by_quantity(self):
        slots = [
            InventorySlot(0, ItemStack("potion1", "potion", 10, Quality.STANDARD)),
            InventorySlot(1, ItemStack("herb1", "ingredient", 50, Quality.FINE)),
            InventorySlot(2, ItemStack("sword1", "equipment", 1, Quality.EXCEPTIONAL)),
        ]

        sorted_slots = sort_inventory_slots(slots, "quantity")

        self.assertEqual(sorted_slots[0].item_stack.quantity, 50)
        self.assertEqual(sorted_slots[1].item_stack.quantity, 10)
        self.assertEqual(sorted_slots[2].item_stack.quantity, 1)

    def test_compact_inventory(self):
        slots = [
            InventorySlot(0, ItemStack("potion1", "potion", 30, Quality.STANDARD)),
            InventorySlot(1, ItemStack("potion1", "potion", 40, Quality.STANDARD)),
            InventorySlot(2, ItemStack("herb1", "ingredient", 150, Quality.FINE)),
            InventorySlot(3, None),
            InventorySlot(4, None),
        ]

        compacted = compact_inventory(slots, 99)

        self.assertEqual(len(compacted), 5)
        self.assertEqual(compacted[0].item_stack.quantity, 70)
        self.assertEqual(compacted[1].item_stack.quantity, 99)
        self.assertEqual(compacted[2].item_stack.quantity, 51)
        self.assertTrue(compacted[3].is_empty())
        self.assertTrue(compacted[4].is_empty())


if __name__ == "__main__":
    unittest.main()
