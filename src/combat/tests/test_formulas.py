import unittest
from src.core.data_structures import Personality, Quality
from src.crafting.data_structures import Potion
from src.combat.data_structures import (
    Combatant, CombatStats, StatusEffect, Trigger
)
from src.combat.formulas import (
    calculate_damage,
    calculate_modified_stat,
    apply_status_effect,
    remove_status_effect,
    trigger_matches_phase,
    evaluate_triggers,
    update_durations,
    evaluate_potion_value,
    choose_best_potion,
    parse_simple_esens_damage,
    parse_simple_esens_healing,
    parse_simple_esens_buff,
    parse_simple_esens_debuff
)


class TestDamageCalculation(unittest.TestCase):
    def test_basic_damage(self):
        damage = calculate_damage(
            attacker_strength=50,
            defender_defense=30,
            base_damage=20
        )
        self.assertTrue(20 <= damage <= 22)

    def test_minimum_damage(self):
        damage = calculate_damage(
            attacker_strength=0,
            defender_defense=99,
            base_damage=1
        )
        self.assertEqual(damage, 1)

    def test_high_strength_multiplier(self):
        damage = calculate_damage(
            attacker_strength=100,
            defender_defense=0,
            base_damage=10
        )
        self.assertEqual(damage, 20)


class TestStatusEffects(unittest.TestCase):
    def test_stackable_effects_accumulate(self):
        stats = CombatStats(100, 100, 50, 30, 10, 5)
        combatant = Combatant("test", "Test", stats, [], [], None)

        stackable = StatusEffect(
            "Strength Boost",
            "potion1",
            "strength",
            1.3,
            3,
            [],
            True,
            True
        )

        apply_status_effect(combatant, stackable)
        apply_status_effect(combatant, stackable)

        self.assertEqual(
            len([e for e in combatant.active_effects if e.name == "Strength Boost"]),
            2
        )

    def test_non_stackable_effects_replace(self):
        stats = CombatStats(100, 100, 50, 30, 10, 5)
        combatant = Combatant("test", "Test", stats, [], [], None)

        effect1 = StatusEffect(
            "Shield",
            "potion1",
            "defense",
            1.5,
            3,
            [],
            True,
            False
        )

        effect2 = StatusEffect(
            "Shield",
            "potion2",
            "defense",
            1.8,
            5,
            [],
            True,
            False
        )

        apply_status_effect(combatant, effect1)
        apply_status_effect(combatant, effect2)

        shield_effects = [e for e in combatant.active_effects if e.name == "Shield"]
        self.assertEqual(len(shield_effects), 1)
        self.assertEqual(shield_effects[0].modifier, 1.8)

    def test_modified_stat_calculation(self):
        effect1 = StatusEffect(
            "Boost",
            "potion1",
            "strength",
            1.5,
            3,
            [],
            True,
            True
        )

        effect2 = StatusEffect(
            "Weaken",
            "potion2",
            "strength",
            0.8,
            3,
            [],
            True,
            True
        )

        modified = calculate_modified_stat(100, [effect1, effect2], "strength")
        self.assertEqual(modified, 120)


class TestTriggers(unittest.TestCase):
    def test_trigger_phase_matching(self):
        self.assertTrue(trigger_matches_phase("^S", "start_turn"))
        self.assertTrue(trigger_matches_phase("vE", "end_turn"))
        self.assertTrue(trigger_matches_phase(">A", "on_attack"))
        self.assertFalse(trigger_matches_phase("^S", "end_turn"))

    def test_evaluate_triggers(self):
        stats = CombatStats(100, 100, 50, 30, 10, 5)
        combatant = Combatant("test", "Test", stats, [], [], None)

        trigger = Trigger("^S", "P+H10")
        regen_effect = StatusEffect(
            "Regen",
            "potion1",
            "health",
            1.0,
            3,
            [trigger],
            True,
            False
        )

        combatant.active_effects.append(regen_effect)

        start_triggers = evaluate_triggers("start_turn", combatant, {})
        self.assertEqual(len(start_triggers), 1)
        self.assertEqual(start_triggers[0][0], "Regen")

        end_triggers = evaluate_triggers("end_turn", combatant, {})
        self.assertEqual(len(end_triggers), 0)


class TestDurations(unittest.TestCase):
    def test_duration_decreases(self):
        stats = CombatStats(100, 100, 50, 30, 10, 5)
        combatant = Combatant("test", "Test", stats, [], [], None)

        effect = StatusEffect(
            "Temp Buff",
            "potion1",
            "strength",
            1.5,
            2,
            [],
            True,
            False
        )

        combatant.active_effects.append(effect)
        removed = update_durations(combatant)

        self.assertEqual(len(removed), 0)
        self.assertEqual(combatant.active_effects[0].duration, 1)

    def test_expired_effects_removed(self):
        stats = CombatStats(100, 100, 50, 30, 10, 5)
        combatant = Combatant("test", "Test", stats, [], [], None)

        effect = StatusEffect(
            "Temp Buff",
            "potion1",
            "strength",
            1.5,
            1,
            [],
            True,
            False
        )

        combatant.active_effects.append(effect)
        removed = update_durations(combatant)

        self.assertEqual(len(removed), 1)
        self.assertEqual(removed[0], "Temp Buff")
        self.assertEqual(len(combatant.active_effects), 0)

    def test_permanent_effects_persist(self):
        stats = CombatStats(100, 100, 50, 30, 10, 5)
        combatant = Combatant("test", "Test", stats, [], [], None)

        effect = StatusEffect(
            "Permanent Curse",
            "item1",
            "strength",
            0.9,
            -1,
            [],
            False,
            False
        )

        combatant.active_effects.append(effect)
        removed = update_durations(combatant)

        self.assertEqual(len(removed), 0)
        self.assertEqual(len(combatant.active_effects), 1)
        self.assertEqual(combatant.active_effects[0].duration, -1)


class TestAI(unittest.TestCase):
    def test_aggressive_personality_prefers_damage(self):
        aggressive = Personality(
            openness=0,
            conscientiousness=1,
            extraversion=1,
            agreeableness=-1,
            neuroticism=0
        )

        stats = CombatStats(80, 100, 50, 30, 10, 5)
        actor = Combatant("actor", "Actor", stats, [], [], aggressive)
        target = Combatant("target", "Target", stats, [], [], None)

        damage_potion = Potion(
            "dmg1",
            "damage",
            "E#Damage30",
            Quality.STANDARD,
            1.0,
            "system",
            0
        )

        heal_potion = Potion(
            "heal1",
            "heal",
            "P+H20",
            Quality.STANDARD,
            1.0,
            "system",
            0
        )

        damage_score = evaluate_potion_value(
            damage_potion,
            actor,
            target,
            aggressive
        )

        heal_score = evaluate_potion_value(
            heal_potion,
            actor,
            target,
            aggressive
        )

        self.assertGreater(damage_score, heal_score)

    def test_low_health_prioritizes_healing(self):
        cautious = Personality(
            openness=0,
            conscientiousness=1,
            extraversion=-1,
            agreeableness=1,
            neuroticism=1
        )

        stats = CombatStats(20, 100, 50, 30, 10, 5)
        actor = Combatant("actor", "Actor", stats, [], [], cautious)
        target = Combatant("target", "Target", stats, [], [], None)

        damage_potion = Potion(
            "dmg1",
            "damage",
            "E#Damage30",
            Quality.STANDARD,
            1.0,
            "system",
            0
        )

        heal_potion = Potion(
            "heal1",
            "heal",
            "P+H20",
            Quality.STANDARD,
            1.0,
            "system",
            0
        )

        damage_score = evaluate_potion_value(
            damage_potion,
            actor,
            target,
            cautious
        )

        heal_score = evaluate_potion_value(
            heal_potion,
            actor,
            target,
            cautious
        )

        self.assertGreater(heal_score, damage_score)


class TestESENSParsing(unittest.TestCase):
    def test_parse_damage(self):
        self.assertEqual(parse_simple_esens_damage("E#Damage30"), 30)
        self.assertEqual(parse_simple_esens_damage("E-H25"), 25)
        self.assertEqual(parse_simple_esens_damage("P+H20"), 0)

    def test_parse_healing(self):
        self.assertEqual(parse_simple_esens_healing("P+H20"), 20)
        self.assertEqual(parse_simple_esens_healing("P+H50"), 50)
        self.assertEqual(parse_simple_esens_healing("E#Damage30"), 0)

    def test_parse_buff(self):
        result = parse_simple_esens_buff("P+S30%3T")
        self.assertIsNotNone(result)
        stat, modifier, duration = result
        self.assertEqual(stat, "strength")
        self.assertEqual(modifier, 1.3)
        self.assertEqual(duration, 3)

    def test_parse_debuff(self):
        result = parse_simple_esens_debuff("E-D20%2T")
        self.assertIsNotNone(result)
        stat, modifier, duration = result
        self.assertEqual(stat, "defense")
        self.assertEqual(modifier, 0.8)
        self.assertEqual(duration, 2)


if __name__ == "__main__":
    unittest.main()
