import os
import configparser
from pathlib import Path
from typing import Dict, Any


class ProgressionConfig:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self._config = configparser.ConfigParser()

        config_path = Path(__file__).parent.parent.parent / "config" / "progression.ini"

        if config_path.exists():
            self._config.read(config_path)

    def get_int(self, section: str, key: str, default: int) -> int:
        try:
            return self._config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default

    def get_float(self, section: str, key: str, default: float) -> float:
        try:
            return self._config.getfloat(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default

    def get_bool(self, section: str, key: str, default: bool) -> bool:
        try:
            return self._config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default

    def get_str(self, section: str, key: str, default: str) -> str:
        try:
            return self._config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default


_config = ProgressionConfig()


def get_xp_curve_params() -> Dict[str, int]:
    return {
        "max_xp": _config.get_int("XP_Curve", "max_xp", 100000),
        "max_stat": _config.get_int("XP_Curve", "max_stat", 100),
        "scale": _config.get_int("XP_Curve", "curve_scale", 40),
        "offset": _config.get_int("XP_Curve", "curve_offset", 100)
    }


def get_mastery_gains() -> Dict[str, int]:
    return {
        "failure": _config.get_int("Mastery_Gains", "failure", 1),
        "poor": _config.get_int("Mastery_Gains", "poor", 3),
        "standard": _config.get_int("Mastery_Gains", "standard", 5),
        "fine": _config.get_int("Mastery_Gains", "fine", 8),
        "exceptional": _config.get_int("Mastery_Gains", "exceptional", 12),
        "masterwork": _config.get_int("Mastery_Gains", "masterwork", 15)
    }


def get_mastery_diminishing() -> Dict[str, float]:
    return {
        "threshold_high": _config.get_int("Mastery_Diminishing", "threshold_high", 80),
        "threshold_mid": _config.get_int("Mastery_Diminishing", "threshold_mid", 60),
        "multiplier_high": _config.get_float("Mastery_Diminishing", "multiplier_high", 0.5),
        "multiplier_mid": _config.get_float("Mastery_Diminishing", "multiplier_mid", 0.75)
    }


def get_mastery_bonus_config() -> Dict[str, Dict[str, Any]]:
    return {
        0: {
            "success_bonus": _config.get_float("Mastery_Bonuses", "novice_success", 0.0),
            "quality_bonus": _config.get_float("Mastery_Bonuses", "novice_quality", 0.0),
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        1: {
            "success_bonus": _config.get_float("Mastery_Bonuses", "competent_success", 0.10),
            "quality_bonus": 0.0,
            "waste_reduction": _config.get_float("Mastery_Bonuses", "waste_reduction", 0.10),
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        2: {
            "success_bonus": _config.get_float("Mastery_Bonuses", "proficient_success", 0.20),
            "quality_bonus": _config.get_float("Mastery_Bonuses", "proficient_quality", 0.10),
            "waste_reduction": _config.get_float("Mastery_Bonuses", "waste_reduction", 0.10),
            "can_teach": False,
            "can_innovate": False,
            "batch_craft": False
        },
        3: {
            "success_bonus": _config.get_float("Mastery_Bonuses", "expert_success", 0.30),
            "quality_bonus": _config.get_float("Mastery_Bonuses", "expert_quality", 0.20),
            "waste_reduction": _config.get_float("Mastery_Bonuses", "waste_reduction", 0.10),
            "can_teach": True,
            "can_innovate": False,
            "batch_craft": True
        },
        4: {
            "success_bonus": _config.get_float("Mastery_Bonuses", "master_success", 0.40),
            "quality_bonus": _config.get_float("Mastery_Bonuses", "master_quality", 0.30),
            "waste_reduction": _config.get_float("Mastery_Bonuses", "waste_reduction", 0.10),
            "can_teach": True,
            "can_innovate": True,
            "batch_craft": True
        }
    }


def get_reputation_thresholds() -> Dict[str, int]:
    return {
        "known": _config.get_int("Reputation_Thresholds", "known", 21),
        "respected": _config.get_int("Reputation_Thresholds", "respected", 41),
        "renowned": _config.get_int("Reputation_Thresholds", "renowned", 61),
        "legendary": _config.get_int("Reputation_Thresholds", "legendary", 81)
    }


def get_reputation_modifier_config() -> Dict[str, Dict[str, float]]:
    return {
        "Unknown": {
            "price_modifier": _config.get_float("Reputation_Modifiers", "unknown_price", 0.90),
            "quest_access": _config.get_int("Reputation_Modifiers", "unknown_quests", 1),
            "npc_initial_affinity": _config.get_float("Reputation_Modifiers", "unknown_affinity", -0.5)
        },
        "Known": {
            "price_modifier": _config.get_float("Reputation_Modifiers", "known_price", 1.0),
            "quest_access": _config.get_int("Reputation_Modifiers", "known_quests", 2),
            "npc_initial_affinity": _config.get_float("Reputation_Modifiers", "known_affinity", 0.0)
        },
        "Respected": {
            "price_modifier": _config.get_float("Reputation_Modifiers", "respected_price", 1.05),
            "quest_access": _config.get_int("Reputation_Modifiers", "respected_quests", 3),
            "npc_initial_affinity": _config.get_float("Reputation_Modifiers", "respected_affinity", 0.5)
        },
        "Renowned": {
            "price_modifier": _config.get_float("Reputation_Modifiers", "renowned_price", 1.10),
            "quest_access": _config.get_int("Reputation_Modifiers", "renowned_quests", 4),
            "npc_initial_affinity": _config.get_float("Reputation_Modifiers", "renowned_affinity", 1.0)
        },
        "Legendary": {
            "price_modifier": _config.get_float("Reputation_Modifiers", "legendary_price", 1.20),
            "quest_access": _config.get_int("Reputation_Modifiers", "legendary_quests", 5),
            "npc_initial_affinity": _config.get_float("Reputation_Modifiers", "legendary_affinity", 1.5)
        }
    }


def get_milestone_interval() -> int:
    return _config.get_int("Milestones", "interval", 20)


def load_specialization_from_config(spec_id: str, name: str) -> Dict[str, Any]:
    section = f"Specializations.{name.replace(' ', '')}"

    category = _config.get_str(section, "category", "crafting")

    prerequisites = {}
    bonuses = {}

    for key in _config._config.options(section) if _config._config.has_section(section) else []:
        if key.startswith("prereq_"):
            stat_name = key.replace("prereq_", "")
            prerequisites[stat_name] = _config.get_int(section, key, 50)
        elif key.startswith("bonus_"):
            bonus_name = key.replace("bonus_", "")
            value = _config.get_str(section, key, "0")

            if value.lower() == "true":
                bonuses[bonus_name] = True
            elif value.lower() == "false":
                bonuses[bonus_name] = False
            else:
                try:
                    if "." in value:
                        bonuses[bonus_name] = float(value)
                    else:
                        bonuses[bonus_name] = int(value)
                except ValueError:
                    bonuses[bonus_name] = value

    return {
        "id": spec_id,
        "name": name,
        "category": category,
        "prerequisites": prerequisites,
        "bonuses": bonuses
    }
