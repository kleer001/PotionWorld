"""
Main gameplay view for exploring and gathering.
"""
import arcade
from systems.game_state import GameState, GamePhase
from systems.player_data import PlayerData
from systems.game_events import GameEvents
from systems.audio_manager import AudioManager
from entities.player import Player
from entities.gathering_spot import GatheringSpot
from ui.notification import NotificationManager
import constants


class GameView(arcade.View):
    """
    Main gameplay view - garden/exploration scene.
    """

    def __init__(self):
        super().__init__()

        # Systems
        self.game_state = GameState()
        self.player_data = PlayerData()
        self.events = GameEvents()
        self.audio = AudioManager()

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.gathering_spots = arcade.SpriteList()

        # Entities
        self.player: Player = None

        # Camera
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # UI
        self.notification_manager = NotificationManager(
            constants.WINDOW_WIDTH,
            constants.WINDOW_HEIGHT
        )

        # Input tracking
        self.pressed_keys = set()

        # Setup event listeners
        self.events.subscribe("notification_requested", self.on_notification_requested)

        # Background color
        self.background_color = arcade.color.AMAZON

    def setup(self):
        """Initialize the game scene."""
        # Create player
        self.player = Player()
        self.player.center_x = constants.WINDOW_WIDTH // 2
        self.player.center_y = constants.WINDOW_HEIGHT // 2
        self.player_list.append(self.player)

        # Create gathering spots in a grid pattern
        spot_configs = [
            ("common_mushroom", arcade.color.BROWN, arcade.color.DARK_GRAY),
            ("forest_berries", arcade.color.RED, arcade.color.DARK_GRAY),
            ("earthen_root", arcade.color.DARK_GREEN, arcade.color.DARK_GRAY),
            ("tree_sap", arcade.color.AMBER, arcade.color.DARK_GRAY),
        ]

        # Create spots in a scattered pattern
        import random
        random.seed(42)  # Consistent layout

        for i in range(12):
            # Pick random ingredient type
            ingredient_id, normal_color, depleted_color = random.choice(spot_configs)

            # Random position around the center
            x = constants.WINDOW_WIDTH // 2 + random.randint(-400, 400)
            y = constants.WINDOW_HEIGHT // 2 + random.randint(-300, 300)

            spot = GatheringSpot(ingredient_id, x, y)
            spot.set_colors(normal_color, depleted_color)
            self.gathering_spots.append(spot)

        # Set game state
        self.game_state.enter_gameplay()
        self.game_state.current_scene = "garden"

        # Play music (will fail gracefully if file doesn't exist)
        self.audio.play_music("garden_theme")

        print("🎮 Game setup complete! Use WASD to move, E to gather.")
        print(f"📍 Player at ({self.player.center_x}, {self.player.center_y})")

    def on_show_view(self):
        """Called when this view is shown."""
        self.window.set_mouse_visible(True)

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Use game camera for world
        self.camera.use()

        # Draw ground (simple green background)
        arcade.draw_lrtb_rectangle_filled(
            -5000, 5000, 5000, -5000,
            arcade.color.DARK_GREEN
        )

        # Draw gathering spots
        self.gathering_spots.draw()

        # Draw player
        self.player_list.draw()

        # Draw interaction hint for nearby spots
        for spot in self.player.nearby_interactables:
            if not spot.is_depleted:
                arcade.draw_circle_outline(
                    spot.center_x, spot.center_y,
                    40, arcade.color.YELLOW, 2
                )

        # Use GUI camera for UI
        self.gui_camera.use()

        # Draw UI
        self._draw_ui()

        # Draw notifications
        self.notification_manager.draw()

    def _draw_ui(self):
        """Draw UI elements."""
        # Instructions
        arcade.draw_text(
            "WASD: Move | E: Gather | I: Inventory (TODO) | ESC: Menu (TODO)",
            10, constants.WINDOW_HEIGHT - 30,
            arcade.color.WHITE, 14
        )

        # Player stats (simple display)
        y_offset = constants.WINDOW_HEIGHT - 60
        arcade.draw_text(
            f"Ingredients: {len(self.player_data.ingredients)} types",
            10, y_offset,
            arcade.color.WHITE, 12
        )

        # Show ingredient counts
        y_offset -= 25
        for ingredient_id, amount in list(self.player_data.ingredients.items())[:5]:
            arcade.draw_text(
                f"  {ingredient_id.replace('_', ' ').title()}: {amount}",
                20, y_offset,
                arcade.color.LIGHT_GRAY, 11
            )
            y_offset -= 20

        # Stats
        y_offset = 120
        arcade.draw_text(
            "Stats:",
            10, y_offset,
            arcade.color.WHITE, 12, bold=True
        )
        y_offset -= 20

        for stat_name, value in self.player_data.stats.items():
            arcade.draw_text(
                f"  {stat_name.replace('_', ' ').title()}: {value}",
                15, y_offset,
                arcade.color.LIGHT_GRAY, 10
            )
            y_offset -= 18

    def on_update(self, delta_time: float):
        """Update game logic."""
        # Update player input direction based on pressed keys
        dx = 0.0
        dy = 0.0

        if arcade.key.A in self.pressed_keys or arcade.key.LEFT in self.pressed_keys:
            dx -= 1.0
        if arcade.key.D in self.pressed_keys or arcade.key.RIGHT in self.pressed_keys:
            dx += 1.0
        if arcade.key.S in self.pressed_keys or arcade.key.DOWN in self.pressed_keys:
            dy -= 1.0
        if arcade.key.W in self.pressed_keys or arcade.key.UP in self.pressed_keys:
            dy += 1.0

        self.player.set_input_direction(dx, dy)

        # Update entities
        self.player.update_movement(delta_time)
        self.gathering_spots.update(delta_time)

        # Update nearby interactables
        self.player.update_nearby_interactables(self.gathering_spots)

        # Center camera on player
        target_x = self.player.center_x - self.window.width / 2
        target_y = self.player.center_y - self.window.height / 2

        # Smooth camera following
        current_x, current_y = self.camera.position
        new_x = current_x + (target_x - current_x) * constants.CAMERA_SPEED
        new_y = current_y + (target_y - current_y) * constants.CAMERA_SPEED
        self.camera.position = (new_x, new_y)

        # Update notifications
        self.notification_manager.update(delta_time)

        # Update playtime
        self.player_data.playtime += delta_time

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        self.pressed_keys.add(key)

        # Interaction
        if key == arcade.key.E:
            self.player.try_interact()

        # Inventory (TODO)
        if key == arcade.key.I:
            self.notification_manager.add_notification("Inventory system coming soon!", "info")

        # Debug: Add random stat increase
        if key == arcade.key.P:
            self.player_data.add_stat("precision", 5)

    def on_key_release(self, key, modifiers):
        """Handle key releases."""
        self.pressed_keys.discard(key)

    def on_notification_requested(self, message: str, notification_type: str = "info"):
        """Handle notification event."""
        self.notification_manager.add_notification(message, notification_type)
