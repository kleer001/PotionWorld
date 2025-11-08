from src.core.data_structures import Quality, PriceModifiers


def calculate_ingredient_base_price(rarity: str) -> int:
    prices = {
        "common": 10,
        "uncommon": 50,
        "rare": 200,
        "very_rare": 700,
        "legendary": 2000
    }
    return prices.get(rarity.lower(), 10)


def calculate_potion_base_price(
    ingredient_cost: int,
    difficulty: int
) -> int:
    difficulty_multiplier = 1.5 + (difficulty / 100.0)
    return int(ingredient_cost * difficulty_multiplier)


def apply_quality_modifier(base_price: int, quality: Quality) -> int:
    multipliers = {
        Quality.POOR: 0.75,
        Quality.STANDARD: 1.0,
        Quality.FINE: 1.25,
        Quality.EXCEPTIONAL: 1.50,
        Quality.MASTERWORK: 2.0
    }
    return int(base_price * multipliers[quality])


def calculate_reputation_modifier(reputation: int) -> float:
    normalized = max(0, min(100, reputation))
    return (normalized - 50) / 250.0


def calculate_affinity_modifier(affinity: float) -> float:
    clamped = max(-5.0, min(5.0, affinity))
    return -clamped / 25.0


def calculate_demand_multiplier(demand: float, supply: float) -> float:
    if supply <= 0:
        return 2.0

    ratio = demand / supply
    return max(0.5, min(2.0, ratio))


def calculate_final_price(
    base_price: int,
    modifiers: PriceModifiers
) -> int:
    price = float(base_price)

    price *= modifiers.base_multiplier
    price *= modifiers.quality_multiplier
    price *= modifiers.demand_multiplier
    price *= modifiers.rarity_multiplier
    price *= (1.0 + modifiers.reputation_modifier)
    price *= (1.0 + modifiers.affinity_modifier)

    return max(1, int(price))


def calculate_bulk_discount(quantity: int, unit_price: int) -> int:
    if quantity >= 10:
        discount = 0.15
    elif quantity >= 5:
        discount = 0.10
    elif quantity >= 3:
        discount = 0.05
    else:
        discount = 0.0

    return int(unit_price * (1.0 - discount))


def calculate_combat_reward(
    turn_count: int,
    difficulty: int,
    victory_margin: float
) -> int:
    base_reward = 100

    speed_bonus = max(0, (20 - turn_count) * 5)
    difficulty_bonus = difficulty * 2
    margin_bonus = int(victory_margin * 50)

    return base_reward + speed_bonus + difficulty_bonus + margin_bonus


def update_market_demand(
    current_demand: float,
    transactions_today: int,
    base_demand: float = 1.0
) -> float:
    demand_increase = transactions_today * 0.05
    new_demand = current_demand + demand_increase

    decay_rate = 0.1
    new_demand = new_demand * (1.0 - decay_rate) + base_demand * decay_rate

    return max(0.1, min(3.0, new_demand))


def update_market_supply(
    current_supply: float,
    items_added: int,
    items_sold: int
) -> float:
    net_change = items_added - items_sold
    new_supply = current_supply + (net_change * 0.1)

    return max(0.1, new_supply)


def calculate_profit_margin(
    selling_price: int,
    cost_basis: int
) -> float:
    if cost_basis <= 0:
        return 1.0

    profit = selling_price - cost_basis
    return profit / cost_basis
