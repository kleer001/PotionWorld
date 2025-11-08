from typing import Dict, Optional, List, Tuple
from src.core.event_bus import EventBus
from src.core.events import (
    ItemAdded,
    ItemRemoved,
    ItemMoved,
    ItemStacked,
    InventoryFull,
)
from src.inventory.data_structures import (
    Inventory,
    InventorySlot,
    ItemStack,
)
from src.inventory.formulas import (
    can_add_item,
    find_slots_to_add,
    can_remove_item,
    find_slots_to_remove,
    calculate_item_weight,
    calculate_total_weight,
    can_stack_slots,
    calculate_stack_transfer,
    sort_inventory_slots,
    compact_inventory,
)
from src.inventory.config import (
    get_capacity_config,
    get_item_weights,
)


class InventorySystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.inventories: Dict[str, Inventory] = {}
        self.capacity_config = get_capacity_config()
        self.item_weights = get_item_weights()

    def create_inventory(
        self,
        owner_id: str,
        max_slots: Optional[int] = None,
        max_weight: Optional[float] = None
    ) -> Inventory:
        if owner_id in self.inventories:
            return self.inventories[owner_id]

        slots_count = max_slots or self.capacity_config["default_slots"]
        weight_limit = max_weight or self.capacity_config["max_weight"]

        slots = [InventorySlot(i) for i in range(slots_count)]
        inventory = Inventory(
            owner_id=owner_id,
            slots=slots,
            max_slots=slots_count,
            max_weight=weight_limit,
            current_weight=0.0
        )

        self.inventories[owner_id] = inventory
        return inventory

    def get_inventory(self, owner_id: str) -> Optional[Inventory]:
        if owner_id not in self.inventories:
            return self.create_inventory(owner_id)
        return self.inventories[owner_id]

    def add_item(
        self,
        owner_id: str,
        item_stack: ItemStack
    ) -> Tuple[bool, Optional[str]]:
        inventory = self.get_inventory(owner_id)

        can_add, reason = can_add_item(
            inventory,
            item_stack,
            self.capacity_config["max_stack_size"],
            self.item_weights
        )

        if not can_add:
            self.event_bus.emit(InventoryFull(
                owner_id=owner_id,
                attempted_item_id=item_stack.item_id,
                attempted_quantity=item_stack.quantity
            ))
            return False, reason

        slots_to_fill = find_slots_to_add(
            inventory,
            item_stack,
            self.capacity_config["max_stack_size"]
        )

        for slot_index, amount in slots_to_fill:
            slot = inventory.get_slot(slot_index)

            if slot.is_empty():
                slot.item_stack = ItemStack(
                    item_id=item_stack.item_id,
                    item_type=item_stack.item_type,
                    quantity=amount,
                    quality=item_stack.quality,
                    metadata=item_stack.metadata.copy()
                )
            else:
                slot.item_stack.quantity += amount

            self.event_bus.emit(ItemAdded(
                owner_id=owner_id,
                item_id=item_stack.item_id,
                item_type=item_stack.item_type,
                quantity=amount,
                slot_index=slot_index
            ))

        inventory.current_weight = calculate_total_weight(
            inventory,
            self.item_weights
        )

        return True, None

    def remove_item(
        self,
        owner_id: str,
        item_id: str,
        quantity: int
    ) -> Tuple[bool, Optional[str]]:
        inventory = self.get_inventory(owner_id)

        can_remove, reason = can_remove_item(inventory, item_id, quantity)

        if not can_remove:
            return False, reason

        slots_to_remove = find_slots_to_remove(inventory, item_id, quantity)

        for slot_index, amount in slots_to_remove:
            slot = inventory.get_slot(slot_index)
            item_type = slot.item_stack.item_type
            slot.item_stack.quantity -= amount

            if slot.item_stack.quantity <= 0:
                slot.item_stack = None

            self.event_bus.emit(ItemRemoved(
                owner_id=owner_id,
                item_id=item_id,
                item_type=item_type,
                quantity=amount,
                slot_index=slot_index
            ))

        inventory.current_weight = calculate_total_weight(
            inventory,
            self.item_weights
        )

        return True, None

    def move_item(
        self,
        from_owner_id: str,
        to_owner_id: str,
        item_id: str,
        quantity: int
    ) -> Tuple[bool, Optional[str]]:
        from_inventory = self.get_inventory(from_owner_id)

        can_remove, reason = can_remove_item(from_inventory, item_id, quantity)
        if not can_remove:
            return False, reason

        from_slot = from_inventory.find_item(item_id)[0]
        template_stack = from_inventory.get_slot(from_slot).item_stack

        item_stack = ItemStack(
            item_id=template_stack.item_id,
            item_type=template_stack.item_type,
            quantity=quantity,
            quality=template_stack.quality,
            metadata=template_stack.metadata.copy()
        )

        success, add_reason = self.add_item(to_owner_id, item_stack)

        if not success:
            return False, add_reason

        remove_success, _ = self.remove_item(from_owner_id, item_id, quantity)

        if remove_success:
            self.event_bus.emit(ItemMoved(
                from_owner_id=from_owner_id,
                to_owner_id=to_owner_id,
                item_id=item_id,
                item_type=item_stack.item_type,
                quantity=quantity
            ))

        return True, None

    def stack_items(
        self,
        owner_id: str,
        from_slot: int,
        to_slot: int
    ) -> Tuple[bool, Optional[str]]:
        inventory = self.get_inventory(owner_id)

        can_stack, reason = can_stack_slots(
            inventory,
            from_slot,
            to_slot,
            self.capacity_config["max_stack_size"]
        )

        if not can_stack:
            return False, reason

        from_slot_obj = inventory.get_slot(from_slot)
        to_slot_obj = inventory.get_slot(to_slot)

        if to_slot_obj.is_empty():
            to_slot_obj.item_stack = from_slot_obj.item_stack
            from_slot_obj.item_stack = None
            transfer_amount = to_slot_obj.item_stack.quantity
        else:
            transfer_amount, new_from, new_to = calculate_stack_transfer(
                from_slot_obj.item_stack.quantity,
                to_slot_obj.item_stack.quantity,
                self.capacity_config["max_stack_size"]
            )

            to_slot_obj.item_stack.quantity = new_to

            if new_from > 0:
                from_slot_obj.item_stack.quantity = new_from
            else:
                from_slot_obj.item_stack = None

        self.event_bus.emit(ItemStacked(
            owner_id=owner_id,
            item_id=to_slot_obj.item_stack.item_id,
            from_slot=from_slot,
            to_slot=to_slot,
            quantity=transfer_amount
        ))

        return True, None

    def sort_inventory(self, owner_id: str, sort_by: str = "type") -> bool:
        inventory = self.get_inventory(owner_id)

        sorted_slots = sort_inventory_slots(inventory.slots, sort_by)

        for i, slot in enumerate(sorted_slots):
            slot.slot_index = i

        inventory.slots = sorted_slots

        return True

    def compact_inventory(self, owner_id: str) -> bool:
        inventory = self.get_inventory(owner_id)

        compacted_slots = compact_inventory(
            inventory.slots,
            self.capacity_config["max_stack_size"]
        )

        inventory.slots = compacted_slots

        return True

    def get_item_count(self, owner_id: str, item_id: str) -> int:
        inventory = self.get_inventory(owner_id)
        return inventory.count_item(item_id)

    def has_item(self, owner_id: str, item_id: str, quantity: int = 1) -> bool:
        return self.get_item_count(owner_id, item_id) >= quantity
