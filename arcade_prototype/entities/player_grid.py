"""
Grid-based player character with smooth interpolation.
Implements discrete tile-based navigation with continuous visual movement.
"""
import arcade
from typing import Optional, List, Tuple
from enum import Enum
from systems.game_state import GameState
from systems.player_data import PlayerData
import constants


class PlayerState(Enum):
    """Player movement state."""
    IDLE = "idle"
    MOVING = "moving"


class GridPlayer(arcade.Sprite):
    """
    Player character with grid-based movement and smooth interpolation.

    Architecture:
    - Discrete tile-based navigation
    - Continuous linear interpolation for visuals
    - Input buffering with directional queuing
    - Corner forgiveness for tight turns
    """

    def __init__(self):
        # Use placeholder texture
        super().__init__(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            scale=1.0
        )

        # Systems
        self.game_state = GameState()
        self.player_data = PlayerData()

        # Grid-based position (in tile coordinates)
        self.grid_x: int = 0
        self.grid_y: int = 0
        self.target_grid_x: int = 0
        self.target_grid_y: int = 0

        # Actual pixel position (float for smooth interpolation)
        self.visual_x: float = 0.0
        self.visual_y: float = 0.0

        # Movement state
        self.state = PlayerState.IDLE
        self.move_speed = constants.PLAYER_MOVE_SPEED  # 120px/s
        self.move_progress: float = 0.0  # 0.0 to 1.0 interpolation

        # Input buffering
        self.input_buffer: Optional[Tuple[int, int]] = None  # (dx, dy)
        self.input_buffer_time: float = 0.0

        # Interaction
        self.interaction_range = constants.GATHERING_INTERACTION_RANGE
        self.nearby_interactables: List[arcade.Sprite] = []

    def set_grid_position(self, grid_x: int, grid_y: int):
        """
        Set player position in grid coordinates.

        Args:
            grid_x: X position in tiles
            grid_y: Y position in tiles
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.target_grid_x = grid_x
        self.target_grid_y = grid_y

        # Update visual position
        self.visual_x = grid_x * constants.TILE_SIZE
        self.visual_y = grid_y * constants.TILE_SIZE
        self.center_x = self.visual_x
        self.center_y = self.visual_y

    def get_tile_from_pixel(self, x: float, y: float) -> Tuple[int, int]:
        """Convert pixel coordinates to tile coordinates."""
        return (
            int(x / constants.TILE_SIZE),
            int(y / constants.TILE_SIZE)
        )

    def get_pixel_from_tile(self, grid_x: int, grid_y: int) -> Tuple[float, float]:
        """Convert tile coordinates to pixel coordinates (tile center)."""
        return (
            grid_x * constants.TILE_SIZE,
            grid_y * constants.TILE_SIZE
        )

    def try_move(self, dx: int, dy: int) -> bool:
        """
        Attempt to move in a direction.

        Args:
            dx: X direction (-1, 0, or 1)
            dy: Y direction (-1, 0, or 1)

        Returns:
            True if movement started, False otherwise
        """
        if self.state == PlayerState.MOVING:
            # Buffer the input for when we arrive
            self.input_buffer = (dx, dy)
            self.input_buffer_time = constants.INPUT_BUFFER_TIME
            return False

        if not self.game_state.can_move:
            return False

        # Calculate target tile
        target_x = self.grid_x + dx
        target_y = self.grid_y + dy

        # TODO: Add collision checking here when we have walls
        # For now, allow all movement

        # Start movement
        self.target_grid_x = target_x
        self.target_grid_y = target_y
        self.state = PlayerState.MOVING
        self.move_progress = 0.0

        return True

    def update_movement(self, delta_time: float):
        """Update grid-based movement with smooth interpolation."""
        if not self.game_state.can_move:
            self.state = PlayerState.IDLE
            self.input_buffer = None
            return

        # Update input buffer timer
        if self.input_buffer_time > 0:
            self.input_buffer_time -= delta_time

        if self.state == PlayerState.MOVING:
            # Calculate movement distance this frame
            distance_per_second = self.move_speed
            tile_distance = constants.TILE_SIZE

            # How much progress we make per second (0.0 to 1.0)
            progress_per_second = distance_per_second / tile_distance

            # Update progress
            self.move_progress += progress_per_second * delta_time

            if self.move_progress >= 1.0:
                # Arrived at destination
                self.move_progress = 1.0
                self.grid_x = self.target_grid_x
                self.grid_y = self.target_grid_y
                self.state = PlayerState.IDLE

                # Snap to exact tile center
                self.visual_x = self.grid_x * constants.TILE_SIZE
                self.visual_y = self.grid_y * constants.TILE_SIZE

                # Process buffered input if any
                if self.input_buffer and self.input_buffer_time > 0:
                    dx, dy = self.input_buffer
                    self.input_buffer = None
                    self.try_move(dx, dy)
            else:
                # Interpolate between current and target position (linear)
                start_x = self.grid_x * constants.TILE_SIZE
                start_y = self.grid_y * constants.TILE_SIZE
                end_x = self.target_grid_x * constants.TILE_SIZE
                end_y = self.target_grid_y * constants.TILE_SIZE

                # Linear interpolation
                self.visual_x = start_x + (end_x - start_x) * self.move_progress
                self.visual_y = start_y + (end_y - start_y) * self.move_progress

        # Update sprite position (round to int for pixel-perfect rendering)
        self.center_x = self.visual_x
        self.center_y = self.visual_y

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

    def can_move_to(self, grid_x: int, grid_y: int) -> bool:
        """
        Check if a tile is walkable.

        Args:
            grid_x: Target X in tiles
            grid_y: Target Y in tiles

        Returns:
            True if tile is walkable
        """
        # For now, all tiles are walkable
        # TODO: Add collision detection with walls/obstacles
        return True

    def apply_corner_forgiveness(self, desired_dx: int, desired_dy: int) -> Optional[Tuple[int, int]]:
        """
        Apply corner forgiveness - if player is close to tile center,
        snap and allow the move.

        Args:
            desired_dx: Desired X direction
            desired_dy: Desired Y direction

        Returns:
            Adjusted (dx, dy) if forgiveness applied, None otherwise
        """
        if self.state != PlayerState.IDLE:
            return None

        # Calculate distance from tile center
        tile_center_x = self.grid_x * constants.TILE_SIZE
        tile_center_y = self.grid_y * constants.TILE_SIZE

        offset_x = abs(self.visual_x - tile_center_x)
        offset_y = abs(self.visual_y - tile_center_y)

        # If within forgiveness threshold, snap to center and allow move
        if offset_x <= constants.CORNER_FORGIVENESS and offset_y <= constants.CORNER_FORGIVENESS:
            # Snap to center
            self.visual_x = tile_center_x
            self.visual_y = tile_center_y
            return (desired_dx, desired_dy)

        return None
