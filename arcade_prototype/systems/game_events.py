"""
Global event bus for decoupled communication between systems.
Uses observer pattern with callbacks.
"""
from typing import Callable, Dict, List, Any


class GameEvents:
    """
    Singleton event bus for game-wide events.
    Systems can register callbacks and emit events.
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

        # Event listeners: {event_name: [callback1, callback2, ...]}
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """
        Subscribe to an event.

        Args:
            event_name: Name of the event to listen for
            callback: Function to call when event is emitted
        """
        if event_name not in self._listeners:
            self._listeners[event_name] = []

        if callback not in self._listeners[event_name]:
            self._listeners[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """
        Unsubscribe from an event.

        Args:
            event_name: Name of the event
            callback: Function to remove
        """
        if event_name in self._listeners:
            if callback in self._listeners[event_name]:
                self._listeners[event_name].remove(callback)

    def emit(self, event_name: str, **kwargs: Any) -> None:
        """
        Emit an event to all subscribers.

        Args:
            event_name: Name of the event
            **kwargs: Event data to pass to callbacks
        """
        if event_name in self._listeners:
            for callback in self._listeners[event_name]:
                try:
                    callback(**kwargs)
                except Exception as e:
                    print(f"Error in event callback for '{event_name}': {e}")

    def clear_all(self) -> None:
        """Clear all event listeners."""
        self._listeners.clear()

    # Convenience methods for common events

    def ingredient_gathered(self, ingredient_id: str, amount: int) -> None:
        """Emit ingredient gathered event."""
        self.emit("ingredient_gathered", ingredient_id=ingredient_id, amount=amount)

    def gathering_spot_depleted(self, spot_id: str) -> None:
        """Emit gathering spot depleted event."""
        self.emit("gathering_spot_depleted", spot_id=spot_id)

    def gathering_spot_respawned(self, spot_id: str) -> None:
        """Emit gathering spot respawned event."""
        self.emit("gathering_spot_respawned", spot_id=spot_id)

    def potion_crafted(self, potion_name: str, quality: str) -> None:
        """Emit potion crafted event."""
        self.emit("potion_crafted", potion_name=potion_name, quality=quality)

    def crafting_failed(self, reason: str) -> None:
        """Emit crafting failed event."""
        self.emit("crafting_failed", reason=reason)

    def recipe_learned(self, recipe_id: str) -> None:
        """Emit recipe learned event."""
        self.emit("recipe_learned", recipe_id=recipe_id)

    def affinity_changed(self, npc_id: str, old_value: float, new_value: float) -> None:
        """Emit affinity changed event."""
        self.emit("affinity_changed", npc_id=npc_id, old_value=old_value, new_value=new_value)

    def stat_increased(self, stat_name: str, old_value: int, new_value: int) -> None:
        """Emit stat increased event."""
        self.emit("stat_increased", stat_name=stat_name, old_value=old_value, new_value=new_value)

    def choice_made(self, choice_id: str, option: str) -> None:
        """Emit choice made event."""
        self.emit("choice_made", choice_id=choice_id, option=option)

    def dialogue_started(self, npc_id: str) -> None:
        """Emit dialogue started event."""
        self.emit("dialogue_started", npc_id=npc_id)

    def dialogue_ended(self, npc_id: str) -> None:
        """Emit dialogue ended event."""
        self.emit("dialogue_ended", npc_id=npc_id)

    def scene_transition_requested(self, scene_name: str) -> None:
        """Emit scene transition request."""
        self.emit("scene_transition_requested", scene_name=scene_name)

    def notification_requested(self, message: str, notification_type: str = "info") -> None:
        """
        Emit notification request.

        Args:
            message: Notification text
            notification_type: Type of notification ("success", "warning", "error", "info")
        """
        self.emit("notification_requested", message=message, notification_type=notification_type)

    def music_change_requested(self, music_name: str) -> None:
        """Emit music change request."""
        self.emit("music_change_requested", music_name=music_name)

    def sfx_requested(self, sfx_name: str, volume: float = 1.0) -> None:
        """Emit sound effect request."""
        self.emit("sfx_requested", sfx_name=sfx_name, volume=volume)
