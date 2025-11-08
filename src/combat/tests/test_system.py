import unittest
from src.core.event_bus import EventBus
from src.core.data_structures import Personality, Quality
from src.crafting.data_structures import Potion
from src.combat.data_structures import (
    Combatant, CombatStats, CombatAction, StatusEffect, Trigger
)
from src.core.events import (
    TurnExecuted, DamageDealt, StatusApplied,
    CombatEnded
)
from src.combat.system import CombatSystem


class TestCombatSystem(unittest.TestCase):
    def setUp(self):
        self.event_bus = EventBus()
        self.combat = CombatSystem(self.event_bus)
        self.events = []

        def capture_event(event):
            self.events.append(event)

        self.event_bus.subscribe_all(capture_event)

    def test_turn_execution_emits_events(self):
        actor_stats = CombatStats(100, 100, 50, 30, 10, 5)
        target_stats = CombatStats(100, 100, 40, 25, 10, 5)

        actor = Combatant("player", "Player", actor_stats, [], [], None)
        target = Combatant("enemy", "Enemy", target_stats, [], [], None)

        damage_potion = Potion(
            "dmg1",
            "damage",
            "E#Damage20",
            Quality.STANDARD,
            1.0,
            "player",
            0
        )

        action = CombatAction(action_type="USE_POTION", potion=damage_potion)

        result = self.combat.execute_turn("test_combat", 1, actor, action, target)

        turn_events = [e for e in self.events if isinstance(e, TurnExecuted)]
        damage_events = [e for e in self.events if isinstance(e, DamageDealt)]

        self.assertEqual(len(turn_events), 1)
        self.assertEqual(len(damage_events), 1)
        self.assertEqual(damage_events[0].source_id, "player")
        self.assertEqual(damage_events[0].target_id, "enemy")

    def test_victory_emits_combat_ended(self):
        actor_stats = CombatStats(100, 100, 50, 30, 10, 5)
        target_stats = CombatStats(5, 100, 40, 25, 10, 5)

        actor = Combatant("player", "Player", actor_stats, [], [], None)
        target = Combatant("enemy", "Enemy", target_stats, [], [], None)

        big_damage_potion = Potion(
            "dmg1",
            "damage",
            "E#Damage50",
            Quality.STANDARD,
            1.0,
            "player",
            0
        )

        action = CombatAction(action_type="USE_POTION", potion=big_damage_potion)

        result = self.combat.execute_turn("test_combat", 1, actor, action, target)

        combat_ended_events = [e for e in self.events if isinstance(e, CombatEnded)]

        self.assertEqual(len(combat_ended_events), 1)
        self.assertEqual(combat_ended_events[0].winner_id, "player")
        self.assertEqual(result.victor, "player")

    def test_guard_action_boosts_defense(self):
        actor_stats = CombatStats(100, 100, 50, 30, 10, 5)
        target_stats = CombatStats(100, 100, 40, 25, 10, 5)

        actor = Combatant("player", "Player", actor_stats, [], [], None)
        target = Combatant("enemy", "Enemy", target_stats, [], [], None)

        action = CombatAction(action_type="GUARD")

        result = self.combat.execute_turn("test_combat", 1, actor, action, target)

        self.assertEqual(len(actor.active_effects), 1)
        self.assertEqual(actor.active_effects[0].name, "Guard")
        self.assertEqual(actor.active_effects[0].modifier, 1.5)

    def test_healing_potion_restores_health(self):
        actor_stats = CombatStats(50, 100, 50, 30, 10, 5)
        target_stats = CombatStats(100, 100, 40, 25, 10, 5)

        actor = Combatant("player", "Player", actor_stats, [], [], None)
        target = Combatant("enemy", "Enemy", target_stats, [], [], None)

        heal_potion = Potion(
            "heal1",
            "heal",
            "P+H30",
            Quality.STANDARD,
            1.0,
            "player",
            0
        )

        action = CombatAction(action_type="USE_POTION", potion=heal_potion)

        result = self.combat.execute_turn("test_combat", 1, actor, action, target)

        self.assertEqual(actor.stats.health, 80)

    def test_buff_potion_applies_status(self):
        actor_stats = CombatStats(100, 100, 50, 30, 10, 5)
        target_stats = CombatStats(100, 100, 40, 25, 10, 5)

        actor = Combatant("player", "Player", actor_stats, [], [], None)
        target = Combatant("enemy", "Enemy", target_stats, [], [], None)

        buff_potion = Potion(
            "buff1",
            "buff",
            "P+S30%3T",
            Quality.STANDARD,
            1.0,
            "player",
            0
        )

        action = CombatAction(action_type="USE_POTION", potion=buff_potion)

        result = self.combat.execute_turn("test_combat", 1, actor, action, target)

        self.assertEqual(len(actor.active_effects), 1)
        self.assertEqual(actor.active_effects[0].stat_affected, "strength")
        self.assertEqual(actor.active_effects[0].duration, 3)

        status_events = [e for e in self.events if isinstance(e, StatusApplied)]
        self.assertEqual(len(status_events), 1)

    def test_ai_chooses_potion(self):
        personality = Personality(
            openness=1,
            conscientiousness=1,
            extraversion=1,
            agreeableness=-1,
            neuroticism=0
        )

        actor_stats = CombatStats(100, 100, 50, 30, 10, 5)
        target_stats = CombatStats(100, 100, 40, 25, 10, 5)

        actor = Combatant("ai", "AI", actor_stats, [], [], personality)
        target = Combatant("player", "Player", target_stats, [], [], None)

        damage_potion = Potion(
            "dmg1",
            "damage",
            "E#Damage20",
            Quality.STANDARD,
            1.0,
            "ai",
            0
        )

        actor.combat_belt = [damage_potion]

        action = self.combat.create_ai_action(actor, target)

        self.assertEqual(action.action_type, "USE_POTION")
        self.assertIsNotNone(action.potion)

    def test_status_duration_decreases_each_turn(self):
        actor_stats = CombatStats(100, 100, 50, 30, 10, 5)
        target_stats = CombatStats(100, 100, 40, 25, 10, 5)

        actor = Combatant("player", "Player", actor_stats, [], [], None)
        target = Combatant("enemy", "Enemy", target_stats, [], [], None)

        buff_potion = Potion(
            "buff1",
            "buff",
            "P+S30%2T",
            Quality.STANDARD,
            1.0,
            "player",
            0
        )

        action1 = CombatAction(action_type="USE_POTION", potion=buff_potion)
        self.combat.execute_turn("test_combat", 1, actor, action1, target)

        self.assertEqual(actor.active_effects[0].duration, 2)

        action2 = CombatAction(action_type="OBSERVE")
        self.combat.execute_turn("test_combat", 2, target, action2, actor)

        self.assertEqual(actor.active_effects[0].duration, 1)

        action3 = CombatAction(action_type="OBSERVE")
        self.combat.execute_turn("test_combat", 3, target, action3, actor)

        self.assertEqual(len(actor.active_effects), 0)


class TestIntegrationScenarios(unittest.TestCase):
    def setUp(self):
        self.event_bus = EventBus()
        self.combat = CombatSystem(self.event_bus)

    def test_full_combat_sequence(self):
        player_stats = CombatStats(100, 100, 50, 30, 10, 5)
        enemy_stats = CombatStats(80, 80, 40, 25, 10, 5)

        player = Combatant("player", "Player", player_stats, [], [], None)
        enemy = Combatant("enemy", "Enemy", enemy_stats, [], [], None)

        damage_potion = Potion(
            "dmg1",
            "damage",
            "E#Damage30",
            Quality.STANDARD,
            1.0,
            "player",
            0
        )

        player.combat_belt = [damage_potion]

        turn = 1
        while player.stats.health > 0 and enemy.stats.health > 0 and turn < 20:
            if turn % 2 == 1:
                action = CombatAction(action_type="USE_POTION", potion=damage_potion)
                result = self.combat.execute_turn("test", turn, player, action, enemy)
            else:
                ai_action = self.combat.create_ai_action(enemy, player)
                result = self.combat.execute_turn("test", turn, enemy, ai_action, player)

            if result.victor:
                break

            turn += 1

        self.assertTrue(
            player.stats.health <= 0 or enemy.stats.health <= 0,
            "Combat should end with a victor"
        )


if __name__ == "__main__":
    unittest.main()
