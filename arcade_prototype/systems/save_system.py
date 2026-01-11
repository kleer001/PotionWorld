"""
Save/load system using JSON files.
"""
import json
from pathlib import Path
from typing import Optional
from systems.player_data import PlayerData


class SaveSystem:
    """Handles saving and loading game data."""

    SAVE_DIR = Path.home() / ".potionworld" / "saves"
    AUTO_SAVE_FILE = "autosave.json"

    def __init__(self):
        # Ensure save directory exists
        self.SAVE_DIR.mkdir(parents=True, exist_ok=True)

    def save_game(self, slot: int = -1) -> bool:
        """
        Save game to a slot.

        Args:
            slot: Save slot number (0-9), or -1 for autosave

        Returns:
            True if save successful, False otherwise
        """
        try:
            player_data = PlayerData()

            # Build save data dictionary
            save_data = {
                "player_name": player_data.player_name,
                "appearance_index": player_data.appearance_index,
                "background": player_data.background,
                "stats": player_data.stats.copy(),
                "ingredients": player_data.ingredients.copy(),
                "potions": player_data.potions.copy(),
                "npc_affinity": player_data.npc_affinity.copy(),
                "known_recipes": player_data.known_recipes.copy(),
                "recipe_mastery": player_data.recipe_mastery.copy(),
                "choices_made": player_data.choices_made.copy(),
                "story_flags": player_data.story_flags.copy(),
                "completed_quests": player_data.completed_quests.copy(),
                "playtime": player_data.playtime,
                "day_count": player_data.day_count,
                "season": player_data.season,
            }

            # Get save file path
            save_path = self._get_save_path(slot)

            # Write to file
            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=2)

            print(f"✅ Game saved to {save_path.name}")
            return True

        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False

    def load_game(self, slot: int = -1) -> bool:
        """
        Load game from a slot.

        Args:
            slot: Save slot number (0-9), or -1 for autosave

        Returns:
            True if load successful, False otherwise
        """
        try:
            save_path = self._get_save_path(slot)

            if not save_path.exists():
                print(f"❌ Save file not found: {save_path.name}")
                return False

            # Read from file
            with open(save_path, 'r') as f:
                save_data = json.load(f)

            # Load into PlayerData
            player_data = PlayerData()
            player_data.player_name = save_data.get("player_name", "")
            player_data.appearance_index = save_data.get("appearance_index", 0)
            player_data.background = save_data.get("background", "")
            player_data.stats = save_data.get("stats", {})
            player_data.ingredients = save_data.get("ingredients", {})
            player_data.potions = save_data.get("potions", [])
            player_data.npc_affinity = save_data.get("npc_affinity", {})
            player_data.known_recipes = save_data.get("known_recipes", [])
            player_data.recipe_mastery = save_data.get("recipe_mastery", {})
            player_data.choices_made = save_data.get("choices_made", [])
            player_data.story_flags = save_data.get("story_flags", {})
            player_data.completed_quests = save_data.get("completed_quests", [])
            player_data.playtime = save_data.get("playtime", 0.0)
            player_data.day_count = save_data.get("day_count", 1)
            player_data.season = save_data.get("season", 0)

            print(f"✅ Game loaded from {save_path.name}")
            return True

        except Exception as e:
            print(f"❌ Load failed: {e}")
            return False

    def save_exists(self, slot: int = -1) -> bool:
        """Check if a save file exists."""
        return self._get_save_path(slot).exists()

    def delete_save(self, slot: int = -1) -> bool:
        """Delete a save file."""
        try:
            save_path = self._get_save_path(slot)
            if save_path.exists():
                save_path.unlink()
                print(f"✅ Save deleted: {save_path.name}")
                return True
            return False
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False

    def list_saves(self) -> list:
        """
        List all available save files.

        Returns:
            List of (slot, filename, player_name, playtime) tuples
        """
        saves = []

        # Check autosave
        if self.save_exists(-1):
            try:
                with open(self._get_save_path(-1), 'r') as f:
                    data = json.load(f)
                saves.append((-1, "Autosave", data.get("player_name", "Unknown"), data.get("playtime", 0)))
            except:
                pass

        # Check manual saves (0-9)
        for slot in range(10):
            if self.save_exists(slot):
                try:
                    with open(self._get_save_path(slot), 'r') as f:
                        data = json.load(f)
                    saves.append((slot, f"Save {slot}", data.get("player_name", "Unknown"), data.get("playtime", 0)))
                except:
                    pass

        return saves

    def _get_save_path(self, slot: int) -> Path:
        """Get the file path for a save slot."""
        if slot == -1:
            return self.SAVE_DIR / self.AUTO_SAVE_FILE
        return self.SAVE_DIR / f"save_{slot:02d}.json"

    def auto_save(self) -> bool:
        """Perform an autosave."""
        return self.save_game(slot=-1)
