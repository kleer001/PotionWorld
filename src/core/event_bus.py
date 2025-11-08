from typing import Callable, Dict, List, Type, Any
from collections import defaultdict


class EventBus:
    def __init__(self):
        self._subscribers: Dict[Type, List[Callable]] = defaultdict(list)
        self._all_subscribers: List[Callable] = []

    def subscribe(self, event_type: Type, callback: Callable) -> None:
        self._subscribers[event_type].append(callback)

    def subscribe_all(self, callback: Callable) -> None:
        self._all_subscribers.append(callback)

    def emit(self, event: Any) -> None:
        event_type = type(event)

        for callback in self._subscribers[event_type]:
            callback(event)

        for callback in self._all_subscribers:
            callback(event)

    def clear(self) -> None:
        self._subscribers.clear()
        self._all_subscribers.clear()
