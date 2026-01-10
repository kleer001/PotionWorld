"""
Game state manager for current session state.
Tracks what phase the game is in and what the player can do.
"""
from enum import Enum
from typing import Optional


class GamePhase(Enum):
    """Current game phase/mode."""
    MENU = "menu"
    GAMEPLAY = "gameplay"
    DIALOGUE = "dialogue"
    CRAFTING = "crafting"
    CUTSCENE = "cutscene"
    PAUSED = "paused"


class GameState:
    """
    Singleton that manages current game session state.
    This is NOT persistent data (see PlayerData for that).
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

        # Current phase
        self.current_phase: GamePhase = GamePhase.MENU
        self.previous_phase: Optional[GamePhase] = None

        # Player capabilities (based on current phase)
        self.can_move: bool = True
        self.can_interact: bool = True
        self.can_open_inventory: bool = True
        self.can_open_journal: bool = True
        self.can_pause: bool = True

        # Current scene/location
        self.current_scene: str = "menu"

        # Active NPC (for dialogue)
        self.active_npc_id: Optional[str] = None

    def enter_gameplay(self) -> None:
        """Enter gameplay mode."""
        self.previous_phase = self.current_phase
        self.current_phase = GamePhase.GAMEPLAY
        self.can_move = True
        self.can_interact = True
        self.can_open_inventory = True
        self.can_open_journal = True
        self.can_pause = True
        self.active_npc_id = None

    def enter_dialogue(self, npc_id: str = "") -> None:
        """Enter dialogue mode."""
        self.previous_phase = self.current_phase
        self.current_phase = GamePhase.DIALOGUE
        self.can_move = False
        self.can_interact = False
        self.can_open_inventory = False
        self.can_open_journal = False
        self.can_pause = False
        self.active_npc_id = npc_id

    def exit_dialogue(self) -> None:
        """Exit dialogue mode, return to previous state."""
        self.current_phase = self.previous_phase or GamePhase.GAMEPLAY
        self.can_move = True
        self.can_interact = True
        self.can_open_inventory = True
        self.can_open_journal = True
        self.can_pause = True
        self.active_npc_id = None

    def enter_crafting(self) -> None:
        """Enter crafting mode."""
        self.previous_phase = self.current_phase
        self.current_phase = GamePhase.CRAFTING
        self.can_move = False
        self.can_interact = False
        self.can_open_inventory = False
        self.can_open_journal = False
        self.can_pause = True

    def exit_crafting(self) -> None:
        """Exit crafting mode."""
        self.current_phase = self.previous_phase or GamePhase.GAMEPLAY
        self.can_move = True
        self.can_interact = True
        self.can_open_inventory = True
        self.can_open_journal = True
        self.can_pause = True

    def enter_cutscene(self) -> None:
        """Enter cutscene mode."""
        self.previous_phase = self.current_phase
        self.current_phase = GamePhase.CUTSCENE
        self.can_move = False
        self.can_interact = False
        self.can_open_inventory = False
        self.can_open_journal = False
        self.can_pause = False

    def exit_cutscene(self) -> None:
        """Exit cutscene mode."""
        self.current_phase = self.previous_phase or GamePhase.GAMEPLAY
        self.can_move = True
        self.can_interact = True
        self.can_open_inventory = True
        self.can_open_journal = True
        self.can_pause = True

    def pause(self) -> None:
        """Pause the game."""
        if self.can_pause:
            self.previous_phase = self.current_phase
            self.current_phase = GamePhase.PAUSED
            self.can_move = False
            self.can_interact = False

    def unpause(self) -> None:
        """Unpause the game."""
        if self.current_phase == GamePhase.PAUSED:
            self.current_phase = self.previous_phase or GamePhase.GAMEPLAY
            # Restore capabilities based on phase
            if self.current_phase == GamePhase.GAMEPLAY:
                self.can_move = True
                self.can_interact = True

    def reset(self) -> None:
        """Reset to initial state."""
        self.current_phase = GamePhase.MENU
        self.previous_phase = None
        self.can_move = True
        self.can_interact = True
        self.can_open_inventory = True
        self.can_open_journal = True
        self.can_pause = True
        self.current_scene = "menu"
        self.active_npc_id = None
