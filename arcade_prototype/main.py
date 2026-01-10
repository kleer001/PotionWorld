"""
PotionWorld - Season 0 MVP
Arcade + Python implementation

Entry point for the game.
"""
import arcade
import constants
from views.game_view import GameView
from systems.game_state import GameState
from systems.player_data import PlayerData


def main():
    """Main entry point."""
    print("=" * 60)
    print("🧪 PotionWorld - Season 0 MVP")
    print("=" * 60)
    print()
    print("Starting game...")
    print()

    # Create window
    window = arcade.Window(
        constants.WINDOW_WIDTH,
        constants.WINDOW_HEIGHT,
        constants.WINDOW_TITLE,
        resizable=False
    )

    # Initialize singletons (ensure they're created)
    game_state = GameState()
    player_data = PlayerData()

    # For MVP, set some default player data
    player_data.player_name = "Alchemist"
    player_data.background = "Rural Healer's Apprentice"

    # Give starting stats based on background
    player_data.add_stat("intuition", 5)
    player_data.add_stat("precision", 3)

    print(f"👤 Player: {player_data.player_name}")
    print(f"📖 Background: {player_data.background}")
    print()

    # Create and show game view
    game_view = GameView()
    game_view.setup()

    window.show_view(game_view)

    # Start the game loop
    arcade.run()


if __name__ == "__main__":
    main()
