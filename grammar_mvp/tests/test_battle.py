"""Tests for the grammar_mvp battle engine."""

import pytest

from grammar_mvp.battle import (
    apply_potion,
    check_battle_end,
    resolve_turn,
    tick_effects,
)
from grammar_mvp.game_state import Character, GameState


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _make_state(hero_hp=40, enemy_hp=25, hero_str=8, hero_def=5,
                enemy_str=7, enemy_def=3):
    return GameState(
        hero=Character("Hero", hero_hp, 40, hero_str, hero_def),
        enemy=Character("Enemy", enemy_hp, 25, enemy_str, enemy_def),
        mana=10, max_mana=10,
        deck=[], hand=[], lock=[None] * 5,
        slot_count=5, hand_size=5, phase="build",
    )


# ------------------------------------------------------------------
# resolve_turn
# ------------------------------------------------------------------

class TestResolveTurn:

    def test_basic_damage(self):
        state = _make_state()
        log = resolve_turn(state.hero, state.enemy)
        # damage = max(1, 8 - 3) = 5
        assert state.enemy.hp == 20
        assert "5 dmg" in log

    def test_minimum_damage_is_one(self):
        state = _make_state(hero_str=1, enemy_def=99)
        resolve_turn(state.hero, state.enemy)
        assert state.enemy.hp == 24  # 25 - 1

    def test_hp_floors_at_zero(self):
        state = _make_state(enemy_hp=2, hero_str=20, enemy_def=0)
        resolve_turn(state.hero, state.enemy)
        assert state.enemy.hp == 0

    def test_log_contains_names(self):
        state = _make_state()
        log = resolve_turn(state.hero, state.enemy)
        assert "Hero" in log
        assert "Enemy" in log

    def test_enemy_attacks_hero(self):
        state = _make_state()
        resolve_turn(state.enemy, state.hero)
        # damage = max(1, 7 - 5) = 2
        assert state.hero.hp == 38


# ------------------------------------------------------------------
# apply_potion
# ------------------------------------------------------------------

class TestApplyPotion:

    def test_heal_hero(self):
        state = _make_state(hero_hp=20)
        parsed = {
            "target": "P",
            "effect_type": "+",
            "stat_affected": "H",
            "magnitude": {"value": 10, "is_percentage": False, "is_full": False},
        }
        log = apply_potion(parsed, state)
        assert state.hero.hp == 30
        assert "+10" in log

    def test_heal_capped_at_max_hp(self):
        state = _make_state(hero_hp=35)
        parsed = {
            "target": "P",
            "effect_type": "+",
            "stat_affected": "H",
            "magnitude": {"value": 20, "is_percentage": False, "is_full": False},
        }
        apply_potion(parsed, state)
        assert state.hero.hp == 40  # max_hp

    def test_damage_enemy(self):
        state = _make_state()
        parsed = {
            "target": "E",
            "effect_type": "-",
            "stat_affected": "H",
            "magnitude": {"value": 7, "is_percentage": False, "is_full": False},
        }
        log = apply_potion(parsed, state)
        assert state.enemy.hp == 18
        assert "-7" in log

    def test_damage_floors_at_zero(self):
        state = _make_state(enemy_hp=3)
        parsed = {
            "target": "E",
            "effect_type": "-",
            "stat_affected": "H",
            "magnitude": {"value": 50, "is_percentage": False, "is_full": False},
        }
        apply_potion(parsed, state)
        assert state.enemy.hp == 0

    def test_buff_strength(self):
        state = _make_state()
        parsed = {
            "target": "P",
            "effect_type": "+",
            "stat_affected": "S",
            "magnitude": {"value": 3, "is_percentage": False, "is_full": False},
        }
        apply_potion(parsed, state)
        assert state.hero.strength == 11

    def test_debuff_defense(self):
        state = _make_state()
        parsed = {
            "target": "E",
            "effect_type": "-",
            "stat_affected": "D",
            "magnitude": {"value": 2, "is_percentage": False, "is_full": False},
        }
        apply_potion(parsed, state)
        assert state.enemy.defense == 1

    def test_unknown_stat_fizzles(self):
        state = _make_state()
        parsed = {
            "target": "P",
            "effect_type": "+",
            "stat_affected": "Z",
            "magnitude": {"value": 5, "is_percentage": False, "is_full": False},
        }
        log = apply_potion(parsed, state)
        assert "fizzle" in log.lower()

    def test_unknown_target_fizzles(self):
        state = _make_state()
        parsed = {
            "target": "X",
            "effect_type": "+",
            "stat_affected": "H",
            "magnitude": {"value": 5, "is_percentage": False, "is_full": False},
        }
        log = apply_potion(parsed, state)
        assert "fizzle" in log.lower()

    def test_no_magnitude_does_nothing(self):
        state = _make_state()
        parsed = {
            "target": "P",
            "effect_type": "+",
            "stat_affected": "H",
        }
        apply_potion(parsed, state)
        assert state.hero.hp == 40  # unchanged


# ------------------------------------------------------------------
# tick_effects
# ------------------------------------------------------------------

class TestTickEffects:

    def test_decrement_remaining(self):
        hero = Character("Hero", 40, 40, 8, 5)
        hero.active_effects = [{"remaining": 3, "stat": "S", "delta": 2}]
        tick_effects(hero)
        assert len(hero.active_effects) == 1
        assert hero.active_effects[0]["remaining"] == 2

    def test_remove_expired(self):
        hero = Character("Hero", 40, 40, 8, 5)
        hero.active_effects = [{"remaining": 1, "stat": "S", "delta": 2}]
        tick_effects(hero)
        assert len(hero.active_effects) == 0

    def test_mixed_effects(self):
        hero = Character("Hero", 40, 40, 8, 5)
        hero.active_effects = [
            {"remaining": 1, "stat": "S", "delta": 2},
            {"remaining": 5, "stat": "D", "delta": 1},
        ]
        tick_effects(hero)
        assert len(hero.active_effects) == 1
        assert hero.active_effects[0]["stat"] == "D"

    def test_empty_effects_no_error(self):
        hero = Character("Hero", 40, 40, 8, 5)
        tick_effects(hero)
        assert hero.active_effects == []


# ------------------------------------------------------------------
# check_battle_end
# ------------------------------------------------------------------

class TestCheckBattleEnd:

    def test_hero_alive_enemy_alive(self):
        state = _make_state()
        assert check_battle_end(state) is None

    def test_enemy_dead(self):
        state = _make_state(enemy_hp=0)
        assert check_battle_end(state) == "win"

    def test_hero_dead(self):
        state = _make_state(hero_hp=0)
        assert check_battle_end(state) == "lose"

    def test_both_dead_hero_loses(self):
        state = _make_state(hero_hp=0, enemy_hp=0)
        # hero checked first
        assert check_battle_end(state) == "lose"


# ------------------------------------------------------------------
# Integration: multi-turn combat
# ------------------------------------------------------------------

class TestCombatIntegration:

    def test_battle_resolves_to_completion(self):
        """Run turns until someone dies — should always terminate."""
        state = _make_state()
        hero_turn = True
        for _ in range(200):
            if hero_turn:
                resolve_turn(state.hero, state.enemy)
            else:
                resolve_turn(state.enemy, state.hero)
            hero_turn = not hero_turn
            result = check_battle_end(state)
            if result:
                assert result in ("win", "lose")
                return
        pytest.fail("Battle did not resolve in 200 turns")

    def test_potion_changes_battle_outcome(self):
        """A big STR buff should let the hero win faster."""
        state = _make_state()
        # Buff hero strength massively
        parsed = {
            "target": "P",
            "effect_type": "+",
            "stat_affected": "S",
            "magnitude": {"value": 50, "is_percentage": False, "is_full": False},
        }
        apply_potion(parsed, state)
        resolve_turn(state.hero, state.enemy)
        # damage = max(1, 58 - 3) = 55 — enemy should be dead
        assert state.enemy.hp == 0
        assert check_battle_end(state) == "win"
