import configparser
from pathlib import Path
from typing import Dict


class InventoryConfig:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self._config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent.parent / "config" / "inventory.ini"

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


_config = InventoryConfig()


def get_capacity_config() -> Dict[str, float]:
    return {
        "default_slots": _config.get_int("Capacity", "default_slots", 20),
        "max_stack_size": _config.get_int("Capacity", "max_stack_size", 99),
        "max_weight": _config.get_float("Capacity", "max_weight", 100.0)
    }


def get_item_weights() -> Dict[str, float]:
    return {
        "potion": _config.get_float("Item_Weights", "potion", 0.5),
        "ingredient": _config.get_float("Item_Weights", "ingredient", 0.2),
        "equipment": _config.get_float("Item_Weights", "equipment", 2.0),
        "quest_item": _config.get_float("Item_Weights", "quest_item", 0.1),
        "material": _config.get_float("Item_Weights", "material", 0.3)
    }


def get_auto_sort_config() -> Dict[str, any]:
    return {
        "enabled": _config.get_bool("Auto_Sort", "enabled", True),
        "sort_by": _config.get_str("Auto_Sort", "sort_by", "type"),
        "compact_on_pickup": _config.get_bool("Auto_Sort", "compact_on_pickup", False)
    }
