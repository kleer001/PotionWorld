"""
Player data manager for all persistent player information.
This is what gets saved to disk.
"""
from typing import Dict, List
from systems.game_events import GameEvents
import constants


class PlayerData:
    """
    Singleton that manages all persistent player data.
    This is the data that gets saved/loaded.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Player identity
        self.player_name: str = ""
        self.appearance_index: int = 0
        self.background: str = ""

        # Stats (0-100)
        self.stats: Dict[str, int] = {
            "precision": 0,
            "knowledge": 0,
            "intuition": 0,
            "business": 0,
            "reputation": 0,
            "combat_instinct": 0
        }

        # Inventory
        self.ingredients: Dict[str, int] = {}  # {ingredient_id: amount}
        self.potions: List[Dict] = []  # [{name, quality, effects}, ...]

        # Relationships
        self.npc_affinity: Dict[str, float] = {}  # {npc_id: affinity_value}

        # Knowledge
        self.known_recipes: List[str] = []  # [recipe_id, ...]
        self.recipe_mastery: Dict[str, int] = {}  # {recipe_id: mastery_level}

        # Story progression
        self.choices_made: List[str] = []  # [choice_id, ...]
        self.story_flags: Dict[str, bool] = {}  # {flag_name: value}
        self.completed_quests: List[str] = []

        # Meta
        self.playtime: float = 0.0  # Total playtime in seconds
        self.day_count: int = 1
        self.season: int = 0

        # Event system
        self.events = GameEvents()

    def add_ingredient(self, ingredient_id: str, amount: int) -> None:
        """Add ingredients to inventory."""
        if ingredient_id in self.ingredients:
            self.ingredients[ingredient_id] += amount
        else:
            self.ingredients[ingredient_id] = amount

        self.events.ingredient_gathered(ingredient_id, amount)

    def remove_ingredient(self, ingredient_id: str, amount: int) -> bool:
        """
        Remove ingredients from inventory.
        Returns True if successful, False if not enough.
        """
        if ingredient_id not in self.ingredients:
            return False

        if self.ingredients[ingredient_id] < amount:
            return False

        self.ingredients[ingredient_id] -= amount
        if self.ingredients[ingredient_id] == 0:
            del self.ingredients[ingredient_id]

        return True

    def has_ingredient(self, ingredient_id: str, amount: int = 1) -> bool:
        """Check if player has enough of an ingredient."""
        return self.ingredients.get(ingredient_id, 0) >= amount

    def add_potion(self, potion_data: Dict) -> None:
        """Add a crafted potion to inventory."""
        self.potions.append(potion_data)
        self.events.potion_crafted(potion_data.get("name", "Unknown"), potion_data.get("quality", "Standard"))

    def add_stat(self, stat_name: str, amount: int) -> None:
        """
        Increase a stat, respecting the cap.
        Emits event if stat increases.
        """
        if stat_name not in self.stats:
            return

        old_value = self.stats[stat_name]
        new_value = min(old_value + amount, constants.STAT_CAP)
        self.stats[stat_name] = new_value

        if new_value > old_value:
            self.events.stat_increased(stat_name, old_value, new_value)

    def add_affinity(self, npc_id: str, amount: float) -> None:
        """
        Change affinity with an NPC, respecting min/max bounds.
        Emits event if affinity changes.
        """
        old_value = self.npc_affinity.get(npc_id, 0.0)
        new_value = max(constants.AFFINITY_MIN, min(constants.AFFINITY_MAX, old_value + amount))
        self.npc_affinity[npc_id] = new_value

        if new_value != old_value:
            self.events.affinity_changed(npc_id, old_value, new_value)

    def get_affinity(self, npc_id: str) -> float:
        """Get current affinity with an NPC."""
        return self.npc_affinity.get(npc_id, 0.0)

    def learn_recipe(self, recipe_id: str) -> bool:
        """
        Learn a new recipe.
        Returns True if newly learned, False if already known.
        """
        if recipe_id in self.known_recipes:
            return False

        self.known_recipes.append(recipe_id)
        self.recipe_mastery[recipe_id] = 0
        self.events.recipe_learned(recipe_id)
        return True

    def knows_recipe(self, recipe_id: str) -> bool:
        """Check if player knows a recipe."""
        return recipe_id in self.known_recipes

    def increase_recipe_mastery(self, recipe_id: str, amount: int = 1) -> None:
        """Increase mastery level for a recipe."""
        if recipe_id in self.recipe_mastery:
            self.recipe_mastery[recipe_id] = min(100, self.recipe_mastery[recipe_id] + amount)

    def make_choice(self, choice_id: str, option: str) -> None:
        """Record a story choice."""
        full_choice = f"{choice_id}:{option}"
        if full_choice not in self.choices_made:
            self.choices_made.append(full_choice)
            self.events.choice_made(choice_id, option)

    def has_made_choice(self, choice_id: str, option: str = None) -> bool:
        """Check if a specific choice was made."""
        if option:
            return f"{choice_id}:{option}" in self.choices_made
        else:
            # Check if any option for this choice was made
            return any(c.startswith(f"{choice_id}:") for c in self.choices_made)

    def set_story_flag(self, flag_name: str, value: bool = True) -> None:
        """Set a story flag."""
        self.story_flags[flag_name] = value

    def get_story_flag(self, flag_name: str, default: bool = False) -> bool:
        """Get a story flag value."""
        return self.story_flags.get(flag_name, default)

    def reset(self) -> None:
        """Reset all player data to initial state."""
        self.player_name = ""
        self.appearance_index = 0
        self.background = ""
        self.stats = {
            "precision": 0,
            "knowledge": 0,
            "intuition": 0,
            "business": 0,
            "reputation": 0,
            "combat_instinct": 0
        }
        self.ingredients.clear()
        self.potions.clear()
        self.npc_affinity.clear()
        self.known_recipes.clear()
        self.recipe_mastery.clear()
        self.choices_made.clear()
        self.story_flags.clear()
        self.completed_quests.clear()
        self.playtime = 0.0
        self.day_count = 1
        self.season = 0
