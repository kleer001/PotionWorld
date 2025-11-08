from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from src.core.data_structures import Quality


@dataclass
class ItemStack:
    item_id: str
    item_type: str
    quantity: int
    quality: Optional[Quality] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def can_stack_with(self, other: 'ItemStack') -> bool:
        return (
            self.item_type == other.item_type and
            self.quality == other.quality and
            self.metadata == other.metadata
        )


@dataclass
class InventorySlot:
    slot_index: int
    item_stack: Optional[ItemStack] = None

    def is_empty(self) -> bool:
        return self.item_stack is None or self.item_stack.quantity == 0

    def available_space(self, max_stack_size: int) -> int:
        if self.is_empty():
            return max_stack_size
        return max_stack_size - self.item_stack.quantity


@dataclass
class Inventory:
    owner_id: str
    slots: List[InventorySlot]
    max_slots: int
    max_weight: float = float('inf')
    current_weight: float = 0.0

    def get_slot(self, index: int) -> Optional[InventorySlot]:
        if 0 <= index < len(self.slots):
            return self.slots[index]
        return None

    def find_item(self, item_id: str) -> List[int]:
        return [
            slot.slot_index
            for slot in self.slots
            if not slot.is_empty() and slot.item_stack.item_id == item_id
        ]

    def count_item(self, item_id: str) -> int:
        return sum(
            slot.item_stack.quantity
            for slot in self.slots
            if not slot.is_empty() and slot.item_stack.item_id == item_id
        )

    def get_empty_slots(self) -> List[int]:
        return [slot.slot_index for slot in self.slots if slot.is_empty()]

    def find_stackable_slot(
        self,
        item_stack: ItemStack,
        max_stack_size: int
    ) -> Optional[int]:
        for slot in self.slots:
            if (not slot.is_empty() and
                slot.item_stack.can_stack_with(item_stack) and
                slot.available_space(max_stack_size) > 0):
                return slot.slot_index
        return None


@dataclass
class InventoryConfig:
    default_slots: int = 20
    max_stack_size: int = 99
    potion_weight: float = 0.5
    ingredient_weight: float = 0.2
    equipment_weight: float = 2.0
