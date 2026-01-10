"""
Simple notification system for toast messages.
"""
import arcade
from typing import List, Tuple
import constants


class Notification:
    """A single notification message."""

    def __init__(self, message: str, notification_type: str = "info"):
        self.message = message
        self.notification_type = notification_type
        self.lifetime = 3.0  # Show for 3 seconds
        self.fade_time = 0.5  # Fade out over 0.5 seconds

        # Color based on type
        color_map = {
            "success": constants.COLOR_SUCCESS,
            "warning": constants.COLOR_WARNING,
            "error": constants.COLOR_ERROR,
            "info": constants.COLOR_INFO,
        }
        self.color = color_map.get(notification_type, constants.COLOR_NEUTRAL)

    def update(self, delta_time: float) -> bool:
        """
        Update notification lifetime.

        Returns:
            True if notification should be removed, False otherwise
        """
        self.lifetime -= delta_time
        return self.lifetime <= -self.fade_time

    def get_alpha(self) -> int:
        """Get current alpha value based on lifetime."""
        if self.lifetime > self.fade_time:
            return 255
        elif self.lifetime > 0:
            return 255
        else:
            # Fading out
            fade_progress = 1.0 + (self.lifetime / self.fade_time)
            return int(255 * max(0, fade_progress))


class NotificationManager:
    """Manages on-screen notifications."""

    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height
        self.notifications: List[Notification] = []

        self.spacing = 40  # Vertical spacing between notifications
        self.start_y = window_height - 80  # Starting Y position

    def add_notification(self, message: str, notification_type: str = "info"):
        """Add a new notification."""
        notification = Notification(message, notification_type)
        self.notifications.append(notification)

    def update(self, delta_time: float):
        """Update all notifications."""
        # Update and remove expired notifications
        self.notifications = [
            n for n in self.notifications
            if not n.update(delta_time)
        ]

    def draw(self):
        """Draw all notifications."""
        y_offset = self.start_y

        for notification in self.notifications:
            alpha = notification.get_alpha()

            # Add alpha to color
            color = (*notification.color, alpha)

            # Draw background
            bg_color = (0, 0, 0, alpha // 2)
            arcade.draw_lrtb_rectangle_filled(
                self.window_width - 420,
                self.window_width - 20,
                y_offset + 15,
                y_offset - 15,
                bg_color
            )

            # Draw text
            arcade.draw_text(
                notification.message,
                self.window_width - 400,
                y_offset,
                color,
                14,
                anchor_x="left",
                anchor_y="center"
            )

            y_offset -= self.spacing
