"""
Gathering spot entity for harvesting ingredients.
"""
import arcade
import random
from systems.player_data import PlayerData
from systems.game_events import GameEvents
import constants


class GatheringSpot(arcade.Sprite):
    """
    A resource node that can be gathered from and respawns after time.
    """

    def __init__(self, ingredient_id: str, x: float, y: float):
        # Use placeholder texture for now (colored circle)
        super().__init__()

        # Create a simple colored circle as placeholder
        self.texture = arcade.make_circle_texture(64, arcade.color.GREEN)

        # Position
        self.center_x = x
        self.center_y = y

        # Configuration
        self.ingredient_id = ingredient_id
        self.min_yield = 2
        self.max_yield = 4
        self.respawn_time = constants.DEFAULT_RESPAWN_TIME

        # State
        self.is_depleted = False
        self.respawn_timer = 0.0

        # Systems
        self.player_data = PlayerData()
        self.events = GameEvents()

        # Visuals
        self.normal_color = arcade.color.GREEN
        self.depleted_color = arcade.color.DARK_GRAY
        self._update_appearance()

    def interact(self):
        """Called when player gathers from this spot."""
        if self.is_depleted:
            self.events.notification_requested(
                f"This {self.ingredient_id} spot is depleted",
                "warning"
            )
            return

        # Generate yield
        yield_amount = random.randint(self.min_yield, self.max_yield)

        # Add to player inventory
        self.player_data.add_ingredient(self.ingredient_id, yield_amount)

        # Show notification
        self.events.notification_requested(
            f"Gathered {yield_amount}x {self.ingredient_id.replace('_', ' ').title()}",
            "success"
        )

        # Play sound effect
        self.events.sfx_requested("gather", 0.5)

        # Deplete the spot
        self.deplete()

    def deplete(self):
        """Mark this spot as depleted."""
        self.is_depleted = True
        self.respawn_timer = self.respawn_time
        self._update_appearance()
        self.events.gathering_spot_depleted(self.ingredient_id)

    def respawn(self):
        """Restore this spot."""
        self.is_depleted = False
        self.respawn_timer = 0.0
        self._update_appearance()
        self.events.gathering_spot_respawned(self.ingredient_id)

    def update(self, delta_time: float = 1/60):
        """Update respawn timer."""
        if self.is_depleted:
            self.respawn_timer -= delta_time
            if self.respawn_timer <= 0:
                self.respawn()

    def _update_appearance(self):
        """Update sprite appearance based on depleted state."""
        color = self.depleted_color if self.is_depleted else self.normal_color
        self.texture = arcade.make_circle_texture(64, color)

    def set_colors(self, normal_color, depleted_color):
        """
        Set custom colors for this gathering spot.

        Args:
            normal_color: Color when available
            depleted_color: Color when depleted
        """
        self.normal_color = normal_color
        self.depleted_color = depleted_color
        self._update_appearance()
