import time
from src.core.event_bus import EventBus
from src.core.data_structures import Quality, Potion, PriceModifiers
from src.core.events import TransactionCompleted, GoldChanged, MarketShifted
from src.economy.system import EconomySystem


class EconomyTestbed:
    def __init__(self):
        self.bus = EventBus()
        self.economy = EconomySystem(self.bus)
        self.events = []

        self.bus.subscribe(TransactionCompleted, self.log_event)
        self.bus.subscribe(GoldChanged, self.log_event)
        self.bus.subscribe(MarketShifted, self.log_event)

        self._setup_test_data()

    def _setup_test_data(self):
        self.economy.add_gold("player", 1000, "starting_gold")
        self.economy.add_gold("merchant", 5000, "merchant_inventory")
        self.economy.add_gold("rival", 500, "rival_funds")

    def log_event(self, event):
        self.events.append(event)

    def show_wallets(self):
        print("\nWallet Balances:")
        print("=" * 60)
        for owner_id, wallet in self.economy.wallets.items():
            print(f"{owner_id:15} {wallet.gold:6} gold  "
                  f"({len(wallet.transaction_history)} transactions)")

    def show_market(self):
        print("\nMarket Conditions:")
        print("=" * 60)
        if not self.economy.market_conditions:
            print("No market data yet")
            return

        for item_id, condition in self.economy.market_conditions.items():
            print(f"{item_id:20} "
                  f"Demand: {condition.demand_level:.2f}  "
                  f"Supply: {condition.supply_level:.2f}  "
                  f"Multiplier: {condition.current_multiplier:.2f}x")

    def show_recent_events(self, count=5):
        print(f"\nRecent Events (last {count}):")
        print("=" * 60)
        for event in self.events[-count:]:
            if isinstance(event, TransactionCompleted):
                print(f"Transaction: {event.buyer_id} -> {event.seller_id}  "
                      f"{event.quantity}x {event.item_type}  "
                      f"{event.total_price} gold")
            elif isinstance(event, GoldChanged):
                symbol = "+" if event.delta > 0 else ""
                print(f"Gold: {event.owner_id}  "
                      f"{symbol}{event.delta}  "
                      f"Balance: {event.new_balance}  "
                      f"({event.reason})")
            elif isinstance(event, MarketShifted):
                print(f"Market: {event.item_id}  "
                      f"Demand: {event.old_demand:.2f} -> {event.new_demand:.2f}  "
                      f"Supply: {event.old_supply:.2f} -> {event.new_supply:.2f}")

    def test_potion_pricing(self):
        print("\nTesting Potion Pricing:")
        print("=" * 60)

        qualities = [Quality.POOR, Quality.STANDARD, Quality.FINE,
                     Quality.EXCEPTIONAL, Quality.MASTERWORK]

        for quality in qualities:
            potion = Potion(
                id=f"potion_{quality.name}",
                recipe_id="healing",
                esens_notation="P+H20",
                quality=quality,
                potency=1.0,
                created_by="player",
                created_at=time.time()
            )

            price, modifiers = self.economy.calculate_potion_price(
                potion=potion,
                ingredient_cost=50,
                difficulty=30
            )

            print(f"{quality.name:15} {price:6} gold  "
                  f"(quality: {modifiers.quality_multiplier:.2f}x)")

    def test_affinity_pricing(self):
        print("\nTesting Affinity-Based Pricing:")
        print("=" * 60)

        potion = Potion(
            id="test_potion",
            recipe_id="healing",
            esens_notation="P+H20",
            quality=Quality.STANDARD,
            potency=1.0,
            created_by="player",
            created_at=time.time()
        )

        affinities = [(-5.0, "Nemesis"), (0.0, "Neutral"), (5.0, "Devoted")]

        for affinity, label in affinities:
            price, modifiers = self.economy.calculate_potion_price(
                potion=potion,
                ingredient_cost=50,
                difficulty=30,
                seller_affinity=affinity
            )

            print(f"{label:15} {price:6} gold  "
                  f"(modifier: {modifiers.affinity_modifier:+.2f})")

    def test_market_dynamics(self):
        print("\nTesting Market Dynamics:")
        print("=" * 60)

        item_id = "healing_potion"

        print("\nInitial state:")
        condition = self.economy.get_market_condition(item_id)
        print(f"Demand: {condition.demand_level:.2f}  "
              f"Supply: {condition.supply_level:.2f}")

        print("\nAfter high transaction volume:")
        self.economy.update_market(item_id, transactions_today=20)
        condition = self.economy.get_market_condition(item_id)
        print(f"Demand: {condition.demand_level:.2f}  "
              f"Supply: {condition.supply_level:.2f}")

        print("\nAfter selling more than adding:")
        self.economy.update_market(item_id, items_added=5, items_sold=15)
        condition = self.economy.get_market_condition(item_id)
        print(f"Demand: {condition.demand_level:.2f}  "
              f"Supply: {condition.supply_level:.2f}")

    def test_transaction_flow(self):
        print("\nTesting Transaction Flow:")
        print("=" * 60)

        potion = Potion(
            id="healing_1",
            recipe_id="healing",
            esens_notation="P+H20",
            quality=Quality.FINE,
            potency=1.1,
            created_by="merchant",
            created_at=time.time()
        )

        price, modifiers = self.economy.calculate_potion_price(
            potion=potion,
            ingredient_cost=50,
            difficulty=30,
            buyer_reputation=60,
            seller_affinity=2.0
        )

        print(f"\nPotion price: {price} gold")
        print(f"Player balance before: {self.economy.get_wallet('player').gold}")

        transaction = self.economy.execute_transaction(
            buyer_id="player",
            seller_id="merchant",
            item_id=potion.id,
            item_type="potion",
            quantity=1,
            unit_price=price,
            modifiers=modifiers
        )

        if transaction:
            print(f"Transaction successful!")
            print(f"Player balance after: {self.economy.get_wallet('player').gold}")
            print(f"Merchant balance after: "
                  f"{self.economy.get_wallet('merchant').gold}")
        else:
            print("Transaction failed (insufficient funds)")

    def test_combat_rewards(self):
        print("\nTesting Combat Rewards:")
        print("=" * 60)

        scenarios = [
            (5, 80, 0.8, "Fast, Hard, Dominant"),
            (10, 50, 0.5, "Normal Combat"),
            (20, 30, 0.2, "Slow, Easy, Close"),
        ]

        for turns, difficulty, margin, label in scenarios:
            initial = self.economy.get_wallet("player").gold
            reward = self.economy.award_combat_reward(
                "player", turns, difficulty, margin
            )
            final = self.economy.get_wallet("player").gold

            print(f"{label:25} {reward:4} gold  (Total: {final})")

    def run_all_tests(self):
        print("\nECONOMY TESTBED")
        print("=" * 60)

        self.test_potion_pricing()
        self.test_affinity_pricing()
        self.test_market_dynamics()
        self.test_transaction_flow()
        self.test_combat_rewards()

        self.show_wallets()
        self.show_market()
        self.show_recent_events(10)

        print("\n" + "=" * 60)
        print("All tests completed!")

    def interactive_mode(self):
        print("\nECONOMY INTERACTIVE MODE")
        print("=" * 60)
        print("Commands:")
        print("  wallets       - Show wallet balances")
        print("  market        - Show market conditions")
        print("  events [n]    - Show recent events")
        print("  price         - Test potion pricing")
        print("  transaction   - Test transaction")
        print("  combat        - Test combat rewards")
        print("  test          - Run all tests")
        print("  help          - Show this help")
        print("  quit          - Exit")
        print()

        while True:
            try:
                cmd = input("> ").strip().lower()

                if cmd == "quit":
                    break
                elif cmd == "wallets":
                    self.show_wallets()
                elif cmd == "market":
                    self.show_market()
                elif cmd.startswith("events"):
                    parts = cmd.split()
                    count = int(parts[1]) if len(parts) > 1 else 5
                    self.show_recent_events(count)
                elif cmd == "price":
                    self.test_potion_pricing()
                elif cmd == "transaction":
                    self.test_transaction_flow()
                elif cmd == "combat":
                    self.test_combat_rewards()
                elif cmd == "test":
                    self.run_all_tests()
                elif cmd == "help":
                    self.interactive_mode()
                    break
                else:
                    print(f"Unknown command: {cmd}")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    testbed = EconomyTestbed()
    testbed.run_all_tests()
    testbed.interactive_mode()
