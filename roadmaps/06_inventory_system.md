# Inventory System: 3-Step Implementation

## Overview
Capacity management, item organization (sort/filter/search), and freshness degradation.

**Core Validation:** Capacity constraints create meaningful choices, organization helps find items quickly, freshness adds pressure without frustration.

---

## Step 1: Core Logic

### 1.1 Freshness Degradation
```python
def calculate_freshness(
    days_since_acquisition: int,
    ingredient_type: str,
    storage_quality: float = 1.0  # 0.5 to 2.0
) -> float:
    """
    Pure function: Calculate freshness (0.0 to 1.0)

    Returns: 1.0 = fresh, 0.0 = spoiled
    """
    # Different ingredients spoil at different rates
    spoil_rates = {
        "berries": 3,      # Spoils in 3 days
        "mushrooms": 5,
        "flowers": 7,
        "roots": 14,
        "tree_sap": 21,
        "minerals": 999,   # Never spoils
        "crystals": 999,
        "oils": 30
    }

    days_to_spoil = spoil_rates.get(ingredient_type, 14)

    # Storage quality affects spoilage
    effective_days = days_since_acquisition / storage_quality

    freshness = 1.0 - (effective_days / days_to_spoil)

    return max(0.0, min(1.0, freshness))

def get_freshness_level(freshness: float) -> str:
    """Convert freshness to category"""
    if freshness >= 0.9:
        return "Fresh"
    elif freshness >= 0.7:
        return "Aging"
    elif freshness >= 0.5:
        return "Stale"
    elif freshness >= 0.25:
        return "Spoiling"
    else:
        return "Ruined"

def freshness_quality_penalty(freshness: float) -> float:
    """
    Freshness affects potion quality

    Returns: multiplier (0.5 to 1.0)
    """
    if freshness >= 0.9:
        return 1.0  # No penalty
    elif freshness >= 0.7:
        return 0.95
    elif freshness >= 0.5:
        return 0.85
    elif freshness >= 0.25:
        return 0.70
    else:
        return 0.50  # Severe penalty
```

### 1.2 Capacity Management
```python
def can_add_item(
    inventory: list,
    capacity: int,
    item_to_add: Any,
    stackable: bool = True
) -> bool:
    """
    Check if item can be added to inventory

    Returns: True if space available
    """
    if len(inventory) < capacity:
        return True

    if stackable:
        # Check if we can stack with existing item
        for item in inventory:
            if items_can_stack(item, item_to_add):
                return True

    return False

def items_can_stack(item1, item2) -> bool:
    """Check if two items can stack together"""
    # Same type and quality
    return (item1.type == item2.type and
            item1.quality == item2.quality)

def stack_items(inventory: list):
    """
    Consolidate stackable items

    Returns: new inventory with stacked items
    """
    stacks = {}

    for item in inventory:
        key = (item.type, item.quality)

        if key in stacks:
            stacks[key].quantity += item.quantity
        else:
            stacks[key] = item

    return list(stacks.values())
```

### 1.3 Sorting & Filtering
```python
def sort_inventory(
    inventory: list,
    sort_by: str,  # "type", "rarity", "freshness", "alphabetical"
    ascending: bool = True
) -> list:
    """
    Pure function: Sort inventory

    Returns: new sorted list
    """
    sort_functions = {
        "type": lambda item: item.type,
        "rarity": lambda item: item.rarity_value(),
        "freshness": lambda item: getattr(item, 'freshness', 1.0),
        "alphabetical": lambda item: item.name,
        "quality": lambda item: item.quality_value()
    }

    sort_fn = sort_functions.get(sort_by, sort_functions["alphabetical"])

    return sorted(inventory, key=sort_fn, reverse=not ascending)

def filter_inventory(
    inventory: list,
    filters: dict
) -> list:
    """
    Pure function: Filter inventory by criteria

    filters = {
        "type": "root",
        "rarity": "rare",
        "freshness_min": 0.7
    }

    Returns: filtered list
    """
    filtered = inventory

    if "type" in filters:
        filtered = [i for i in filtered if i.type == filters["type"]]

    if "rarity" in filters:
        filtered = [i for i in filtered if i.rarity == filters["rarity"]]

    if "quality" in filters:
        filtered = [i for i in filtered if i.quality == filters["quality"]]

    if "freshness_min" in filters:
        filtered = [i for i in filtered
                   if getattr(i, 'freshness', 1.0) >= filters["freshness_min"]]

    return filtered

def search_inventory(
    inventory: list,
    query: str
) -> list:
    """
    Simple text search

    Returns: items matching query
    """
    query_lower = query.lower()

    return [item for item in inventory
            if query_lower in item.name.lower() or
               query_lower in item.type.lower()]
```

### Tests (Step 1)
```python
def test_freshness_degradation():
    """Fresh ingredients should spoil over time"""
    # Berries spoil in 3 days
    fresh = calculate_freshness(0, "berries")
    aging = calculate_freshness(1, "berries")
    spoiled = calculate_freshness(4, "berries")

    assert fresh == 1.0
    assert 0.5 < aging < 1.0
    assert spoiled <= 0.0

def test_storage_quality_affects_freshness():
    """Better storage should preserve freshness"""
    poor_storage = calculate_freshness(7, "berries", storage_quality=0.5)
    good_storage = calculate_freshness(7, "berries", storage_quality=2.0)

    assert good_storage > poor_storage

def test_minerals_dont_spoil():
    """Minerals should have permanent freshness"""
    freshness = calculate_freshness(9999, "minerals")
    assert freshness == 1.0

def test_capacity_constraint():
    """Can't add beyond capacity"""
    inventory = [Item("root") for _ in range(50)]
    capacity = 50

    assert not can_add_item(inventory, capacity, Item("berry"), stackable=False)

def test_sorting_works():
    """Sorting should order correctly"""
    items = [
        Item("zebra_flower", rarity="common"),
        Item("apple_berry", rarity="rare"),
        Item("crystal", rarity="legendary")
    ]

    by_alpha = sort_inventory(items, "alphabetical")
    assert by_alpha[0].name == "apple_berry"

    by_rarity = sort_inventory(items, "rarity")
    assert by_rarity[0].rarity == "common"
    assert by_rarity[2].rarity == "legendary"
```

---

## Step 2: API + Events

### 2.1 Data Structures
```python
@dataclass
class Inventory:
    id: str
    capacity: int
    items: list[Item]

@dataclass
class Item:
    id: str
    name: str
    type: str
    rarity: str
    quality: Quality
    quantity: int = 1
    acquisition_date: Optional[int] = None  # For freshness
    freshness: Optional[float] = None  # Cached

@dataclass
class InventoryChange:
    success: bool
    reason: str
    item: Optional[Item]
    new_count: int
```

### 2.2 Events
```python
@dataclass
class ItemAdded:
    inventory_id: str
    item: Item
    quantity: int

@dataclass
class ItemRemoved:
    inventory_id: str
    item_id: str
    quantity: int
    reason: str  # "used", "sold", "discarded", "spoiled"

@dataclass
class ItemSpoiled:
    inventory_id: str
    item: Item

@dataclass
class CapacityReached:
    inventory_id: str
    current_count: int
    max_capacity: int

@dataclass
class FreshnessWarning:
    inventory_id: str
    item: Item
    freshness: float
    days_until_spoiled: int
```

### 2.3 InventorySystem Class
```python
class InventorySystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        event_bus.subscribe(DayPassed, self.on_day_passed)
        event_bus.subscribe(PotionCreated, self.on_potion_created)

    def add_item(
        self,
        inventory: Inventory,
        item: Item,
        current_day: int
    ) -> InventoryChange:
        """
        API: Add item to inventory

        1. Check capacity
        2. Try to stack
        3. Add item
        4. Set acquisition date
        5. Emit events
        """
        # Check capacity
        if not can_add_item(inventory.items, inventory.capacity, item):
            self.event_bus.emit(CapacityReached(
                inventory_id=inventory.id,
                current_count=len(inventory.items),
                max_capacity=inventory.capacity
            ))

            return InventoryChange(
                success=False,
                reason="full",
                item=None,
                new_count=len(inventory.items)
            )

        # Set acquisition date for freshness tracking
        if item.acquisition_date is None:
            item.acquisition_date = current_day

        # Try to stack
        stacked = False
        for existing_item in inventory.items:
            if items_can_stack(existing_item, item):
                existing_item.quantity += item.quantity
                stacked = True
                break

        if not stacked:
            inventory.items.append(item)

        # Emit event
        self.event_bus.emit(ItemAdded(
            inventory_id=inventory.id,
            item=item,
            quantity=item.quantity
        ))

        return InventoryChange(
            success=True,
            reason="added",
            item=item,
            new_count=len(inventory.items)
        )

    def remove_item(
        self,
        inventory: Inventory,
        item_id: str,
        quantity: int = 1,
        reason: str = "used"
    ) -> InventoryChange:
        """API: Remove item from inventory"""
        for item in inventory.items:
            if item.id == item_id:
                if item.quantity >= quantity:
                    item.quantity -= quantity

                    if item.quantity == 0:
                        inventory.items.remove(item)

                    self.event_bus.emit(ItemRemoved(
                        inventory_id=inventory.id,
                        item_id=item_id,
                        quantity=quantity,
                        reason=reason
                    ))

                    return InventoryChange(
                        success=True,
                        reason=reason,
                        item=item,
                        new_count=len(inventory.items)
                    )

        return InventoryChange(
            success=False,
            reason="not_found",
            item=None,
            new_count=len(inventory.items)
        )

    def update_freshness(
        self,
        inventory: Inventory,
        current_day: int
    ):
        """Update freshness for all perishable items"""
        for item in inventory.items:
            if item.acquisition_date is None:
                continue  # Non-perishable or no date set

            days_old = current_day - item.acquisition_date
            old_freshness = item.freshness or 1.0
            item.freshness = calculate_freshness(days_old, item.type)

            # Check if spoiled
            if item.freshness <= 0 and old_freshness > 0:
                self.event_bus.emit(ItemSpoiled(
                    inventory_id=inventory.id,
                    item=item
                ))

            # Check if spoiling soon (warning)
            elif 0 < item.freshness < 0.3 and old_freshness >= 0.3:
                days_to_spoil = self._calculate_days_until_spoiled(item, current_day)
                self.event_bus.emit(FreshnessWarning(
                    inventory_id=inventory.id,
                    item=item,
                    freshness=item.freshness,
                    days_until_spoiled=days_to_spoil
                ))

    def get_sorted(
        self,
        inventory: Inventory,
        sort_by: str,
        ascending: bool = True
    ) -> list[Item]:
        """API: Get sorted view of inventory"""
        return sort_inventory(inventory.items, sort_by, ascending)

    def get_filtered(
        self,
        inventory: Inventory,
        filters: dict
    ) -> list[Item]:
        """API: Get filtered view of inventory"""
        return filter_inventory(inventory.items, filters)

    def on_day_passed(self, event: DayPassed):
        """Auto-update freshness when time passes"""
        # Would iterate all inventories
        pass

    def on_potion_created(self, event: PotionCreated):
        """Auto-add potions to inventory"""
        # Add to appropriate inventory
        pass
```

---

## Step 3: Testbed + Integration

### 3.1 Inventory Testbed
```python
class InventoryTestbed:
    def __init__(self):
        self.event_bus = EventBus()
        self.inventory_sys = InventorySystem(self.event_bus)

        self.inventory = Inventory(
            id="player",
            capacity=50,
            items=self._create_starter_items()
        )

        self.current_day = 0

        self.event_bus.subscribe(self._on_event)

    def run(self):
        """Main loop"""
        print("INVENTORY TESTBED")
        print("=" * 60)

        while True:
            self._display_inventory()
            cmd = input("\n> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "add":
                self._add_item(cmd[1])
            elif cmd[0] == "remove":
                self._remove_item(cmd[1])
            elif cmd[0] == "sort":
                self._sort_inventory(cmd[1])
            elif cmd[0] == "filter":
                self._filter_inventory(cmd[1:])
            elif cmd[0] == "search":
                self._search_inventory(" ".join(cmd[1:]))
            elif cmd[0] == "time":
                self._advance_time(int(cmd[1]))
            elif cmd[0] == "fresh":
                self._check_freshness()
            elif cmd[0] == "quit":
                break

    def _display_inventory(self):
        """Show inventory contents"""
        print(f"\n{'=' * 60}")
        print(f"INVENTORY ({len(self.inventory.items)}/{self.inventory.capacity})")
        print(f"Day: {self.current_day}")
        print(f"{'=' * 60}")

        for i, item in enumerate(self.inventory.items, 1):
            freshness_str = ""
            if item.freshness is not None:
                level = get_freshness_level(item.freshness)
                freshness_str = f" [{level} {item.freshness:.0%}]"

            print(f"  {i}. {item.name} x{item.quantity} ({item.rarity}){freshness_str}")

    def _check_freshness(self):
        """Show detailed freshness info"""
        print("\n═══ FRESHNESS STATUS ═══")

        for item in self.inventory.items:
            if item.acquisition_date is None:
                continue

            days_old = self.current_day - item.acquisition_date
            item.freshness = calculate_freshness(days_old, item.type)

            level = get_freshness_level(item.freshness)
            print(f"\n{item.name}")
            print(f"  Age: {days_old} days")
            print(f"  Freshness: {item.freshness:.0%} ({level})")
            print(f"  Quality Penalty: {freshness_quality_penalty(item.freshness):.0%}")

    def _advance_time(self, days: int):
        """Advance time and update freshness"""
        print(f"\nAdvancing {days} days...")
        self.current_day += days

        self.inventory_sys.update_freshness(self.inventory, self.current_day)

        spoiled = [i for i in self.inventory.items
                   if i.freshness is not None and i.freshness <= 0]

        if spoiled:
            print(f"\n⚠️  {len(spoiled)} item(s) spoiled!")
            for item in spoiled:
                print(f"  - {item.name}")
```

---

## Success Criteria

This system is complete when:

✅ **Capacity creates meaningful choices** - Can't hoard everything
✅ **Sorting helps find items quickly** - Multiple sort options work
✅ **Filtering reduces clutter** - Can focus on relevant items
✅ **Search finds items fast** - Text search works
✅ **Freshness adds pressure** - But not frustrating
✅ **Spoilage warnings are clear** - Know what's expiring
✅ **Events integrate properly** - Auto-adds from crafting, etc.
✅ **Testbed validates all features** - Can test organization manually
