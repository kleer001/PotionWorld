from typing import List, Optional, Tuple
from src.inventory.data_structures import (
    Inventory,
    InventorySlot,
    ItemStack,
)


def calculate_item_weight(item_type: str, quantity: int, weights: dict) -> float:
    base_weight = weights.get(item_type, 1.0)
    return base_weight * quantity


def can_add_item(
    inventory: Inventory,
    item_stack: ItemStack,
    max_stack_size: int,
    weights: dict
) -> Tuple[bool, Optional[str]]:
    if item_stack.quantity <= 0:
        return False, "quantity_invalid"

    item_weight = calculate_item_weight(
        item_stack.item_type,
        item_stack.quantity,
        weights
    )

    if inventory.current_weight + item_weight > inventory.max_weight:
        return False, "weight_exceeded"

    total_space_needed = item_stack.quantity
    available_space = calculate_available_space(
        inventory,
        item_stack,
        max_stack_size
    )

    if available_space < total_space_needed:
        return False, "insufficient_space"

    return True, None


def calculate_available_space(
    inventory: Inventory,
    item_stack: ItemStack,
    max_stack_size: int
) -> int:
    total_space = 0

    for slot in inventory.slots:
        if slot.is_empty():
            total_space += max_stack_size
        elif slot.item_stack.can_stack_with(item_stack):
            total_space += slot.available_space(max_stack_size)

    return total_space


def find_slots_to_add(
    inventory: Inventory,
    item_stack: ItemStack,
    max_stack_size: int
) -> List[Tuple[int, int]]:
    slots_to_fill = []
    remaining = item_stack.quantity

    for slot in inventory.slots:
        if remaining <= 0:
            break

        if not slot.is_empty() and slot.item_stack.can_stack_with(item_stack):
            available = slot.available_space(max_stack_size)
            if available > 0:
                amount = min(remaining, available)
                slots_to_fill.append((slot.slot_index, amount))
                remaining -= amount

    for slot in inventory.slots:
        if remaining <= 0:
            break

        if slot.is_empty():
            amount = min(remaining, max_stack_size)
            slots_to_fill.append((slot.slot_index, amount))
            remaining -= amount

    return slots_to_fill


def can_remove_item(
    inventory: Inventory,
    item_id: str,
    quantity: int
) -> Tuple[bool, Optional[str]]:
    if quantity <= 0:
        return False, "quantity_invalid"

    available = inventory.count_item(item_id)

    if available < quantity:
        return False, "insufficient_quantity"

    return True, None


def find_slots_to_remove(
    inventory: Inventory,
    item_id: str,
    quantity: int
) -> List[Tuple[int, int]]:
    slots_to_remove = []
    remaining = quantity

    for slot in inventory.slots:
        if remaining <= 0:
            break

        if not slot.is_empty() and slot.item_stack.item_id == item_id:
            amount = min(remaining, slot.item_stack.quantity)
            slots_to_remove.append((slot.slot_index, amount))
            remaining -= amount

    return slots_to_remove


def calculate_total_weight(inventory: Inventory, weights: dict) -> float:
    total = 0.0
    for slot in inventory.slots:
        if not slot.is_empty():
            total += calculate_item_weight(
                slot.item_stack.item_type,
                slot.item_stack.quantity,
                weights
            )
    return total


def can_stack_slots(
    inventory: Inventory,
    from_slot: int,
    to_slot: int,
    max_stack_size: int
) -> Tuple[bool, Optional[str]]:
    from_slot_obj = inventory.get_slot(from_slot)
    to_slot_obj = inventory.get_slot(to_slot)

    if not from_slot_obj or not to_slot_obj:
        return False, "invalid_slot"

    if from_slot_obj.is_empty():
        return False, "from_slot_empty"

    if to_slot_obj.is_empty():
        return True, None

    if not from_slot_obj.item_stack.can_stack_with(to_slot_obj.item_stack):
        return False, "not_stackable"

    if to_slot_obj.item_stack.quantity >= max_stack_size:
        return False, "to_slot_full"

    return True, None


def calculate_stack_transfer(
    from_quantity: int,
    to_quantity: int,
    max_stack_size: int
) -> Tuple[int, int, int]:
    available_space = max_stack_size - to_quantity
    transfer_amount = min(from_quantity, available_space)

    new_from = from_quantity - transfer_amount
    new_to = to_quantity + transfer_amount

    return transfer_amount, new_from, new_to


def sort_inventory_slots(
    slots: List[InventorySlot],
    sort_by: str = "type"
) -> List[InventorySlot]:
    filled_slots = [s for s in slots if not s.is_empty()]
    empty_slots = [s for s in slots if s.is_empty()]

    if sort_by == "type":
        filled_slots.sort(
            key=lambda s: (s.item_stack.item_type, s.item_stack.item_id)
        )
    elif sort_by == "quantity":
        filled_slots.sort(
            key=lambda s: (-s.item_stack.quantity, s.item_stack.item_type)
        )
    elif sort_by == "quality":
        filled_slots.sort(
            key=lambda s: (
                s.item_stack.quality.value if s.item_stack.quality else 0,
                s.item_stack.item_type
            )
        )

    return filled_slots + empty_slots


def compact_inventory(
    slots: List[InventorySlot],
    max_stack_size: int
) -> List[InventorySlot]:
    item_groups = {}

    for slot in slots:
        if slot.is_empty():
            continue

        key = (
            slot.item_stack.item_type,
            slot.item_stack.quality,
            tuple(sorted(slot.item_stack.metadata.items()))
        )

        if key not in item_groups:
            item_groups[key] = []

        item_groups[key].append(slot.item_stack)

    new_slots = []
    slot_index = 0

    for item_stacks in item_groups.values():
        total_quantity = sum(stack.quantity for stack in item_stacks)
        template_stack = item_stacks[0]

        while total_quantity > 0:
            quantity = min(total_quantity, max_stack_size)
            new_stack = ItemStack(
                item_id=template_stack.item_id,
                item_type=template_stack.item_type,
                quantity=quantity,
                quality=template_stack.quality,
                metadata=template_stack.metadata.copy()
            )
            new_slots.append(InventorySlot(slot_index, new_stack))
            slot_index += 1
            total_quantity -= quantity

    while slot_index < len(slots):
        new_slots.append(InventorySlot(slot_index, None))
        slot_index += 1

    return new_slots
