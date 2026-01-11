"""
Player character entity with movement and interaction.
"""
import arcade
from typing import Optional, List
from systems.game_state import GameState
from systems.player_data import PlayerData
import constants


class Player(arcade.Sprite):
    """
    Player character with WASD movement and interaction capabilities.
    """

    def __init__(self):
        # Use placeholder texture for now
        super().__init__(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            scale=1.0
        )

        # Systems
        self.game_state = GameState()
        self.player_data = PlayerData()

        # Movement
        self.move_speed = constants.PLAYER_MOVE_SPEED
        self.input_direction = [0.0, 0.0]  # [x, y]

        # Interaction
        self.interaction_range = constants.GATHERING_INTERACTION_RANGE
        self.nearby_interactables: List[arcade.Sprite] = []

    def update_movement(self, delta_time: float):
        """Update player movement based on input direction."""
        if not self.game_state.can_move:
            self.change_x = 0
            self.change_y = 0
            return

        # Normalize diagonal movement
        magnitude = (self.input_direction[0] ** 2 + self.input_direction[1] ** 2) ** 0.5
        if magnitude > 0:
            normalized_x = self.input_direction[0] / magnitude
            normalized_y = self.input_direction[1] / magnitude
        else:
            normalized_x = 0
            normalized_y = 0

        # Apply velocity
        self.change_x = normalized_x * self.move_speed * delta_time
        self.change_y = normalized_y * self.move_speed * delta_time

        # Update position
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update_nearby_interactables(self, interactable_list: arcade.SpriteList):
        """
        Update list of nearby interactable objects.

        Args:
            interactable_list: SpriteList of objects that can be interacted with
        """
        self.nearby_interactables.clear()

        for sprite in interactable_list:
            distance = arcade.get_distance_between_sprites(self, sprite)
            if distance <= self.interaction_range:
                self.nearby_interactables.append(sprite)

    def try_interact(self) -> bool:
        """
        Try to interact with the nearest interactable object.

        Returns:
            True if interaction occurred, False otherwise
        """
        if not self.game_state.can_interact:
            return False

        if not self.nearby_interactables:
            return False

        # Find closest interactable
        closest = min(
            self.nearby_interactables,
            key=lambda s: arcade.get_distance_between_sprites(self, s)
        )

        # Call its interact method if it has one
        if hasattr(closest, 'interact') and callable(closest.interact):
            closest.interact()
            return True

        return False

    def set_input_direction(self, dx: float, dy: float):
        """
        Set the input direction for movement.

        Args:
            dx: X direction (-1, 0, or 1)
            dy: Y direction (-1, 0, or 1)
        """
        self.input_direction = [dx, dy]
