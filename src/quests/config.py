import configparser
from pathlib import Path
from typing import Dict, Any


class QuestConfig:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self._config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent.parent / "config" / "quests.ini"

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


_config = QuestConfig()


def get_quest_limits() -> Dict[str, int]:
    return {
        "max_active": _config.get_int("Limits", "max_active_quests", 10),
        "max_daily": _config.get_int("Limits", "max_daily_quests", 5),
        "max_total": _config.get_int("Limits", "max_total_quests", 100)
    }


def get_objective_timeouts() -> Dict[str, int]:
    return {
        "craft_potion": _config.get_int("Timeouts", "craft_potion", 0),
        "gather_item": _config.get_int("Timeouts", "gather_item", 0),
        "talk_to_npc": _config.get_int("Timeouts", "talk_to_npc", 0),
        "reach_affinity": _config.get_int("Timeouts", "reach_affinity", 0),
        "reach_stat": _config.get_int("Timeouts", "reach_stat", 0),
        "deliver_item": _config.get_int("Timeouts", "deliver_item", 86400),
        "win_duel": _config.get_int("Timeouts", "win_duel", 0),
        "earn_gold": _config.get_int("Timeouts", "earn_gold", 0)
    }


def get_base_rewards() -> Dict[str, int]:
    return {
        "gold_easy": _config.get_int("Base_Rewards", "gold_easy", 50),
        "gold_medium": _config.get_int("Base_Rewards", "gold_medium", 100),
        "gold_hard": _config.get_int("Base_Rewards", "gold_hard", 250),
        "xp_easy": _config.get_int("Base_Rewards", "xp_easy", 100),
        "xp_medium": _config.get_int("Base_Rewards", "xp_medium", 250),
        "xp_hard": _config.get_int("Base_Rewards", "xp_hard", 500),
        "reputation_easy": _config.get_int("Base_Rewards", "reputation_easy", 5),
        "reputation_medium": _config.get_int("Base_Rewards", "reputation_medium", 10),
        "reputation_hard": _config.get_int("Base_Rewards", "reputation_hard", 20)
    }


def get_moral_choice_settings() -> Dict[str, Any]:
    return {
        "track_patterns": _config.get_bool("Moral_Choices", "track_patterns", True),
        "affect_reputation": _config.get_bool("Moral_Choices", "affect_reputation", True),
        "min_impact": _config.get_float("Moral_Choices", "min_impact", 0.5)
    }


def get_auto_progression_settings() -> Dict[str, bool]:
    return {
        "enabled": _config.get_bool("Auto_Progression", "enabled", True),
        "track_crafting": _config.get_bool("Auto_Progression", "track_crafting", True),
        "track_gathering": _config.get_bool("Auto_Progression", "track_gathering", True),
        "track_combat": _config.get_bool("Auto_Progression", "track_combat", True),
        "track_economy": _config.get_bool("Auto_Progression", "track_economy", True),
        "track_social": _config.get_bool("Auto_Progression", "track_social", True)
    }
