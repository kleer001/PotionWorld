from dataclasses import dataclass
from src.core.event_bus import EventBus


@dataclass
class TestEvent:
    value: int


@dataclass
class AnotherEvent:
    message: str


def test_subscribe_and_emit():
    bus = EventBus()
    received = []

    def handler(event):
        received.append(event)

    bus.subscribe(TestEvent, handler)
    bus.emit(TestEvent(42))

    assert len(received) == 1
    assert received[0].value == 42


def test_multiple_subscribers():
    bus = EventBus()
    received1 = []
    received2 = []

    bus.subscribe(TestEvent, lambda e: received1.append(e))
    bus.subscribe(TestEvent, lambda e: received2.append(e))

    bus.emit(TestEvent(100))

    assert len(received1) == 1
    assert len(received2) == 1


def test_different_event_types():
    bus = EventBus()
    test_events = []
    other_events = []

    bus.subscribe(TestEvent, lambda e: test_events.append(e))
    bus.subscribe(AnotherEvent, lambda e: other_events.append(e))

    bus.emit(TestEvent(1))
    bus.emit(AnotherEvent("hello"))
    bus.emit(TestEvent(2))

    assert len(test_events) == 2
    assert len(other_events) == 1


def test_subscribe_all():
    bus = EventBus()
    all_events = []

    bus.subscribe_all(lambda e: all_events.append(e))

    bus.emit(TestEvent(1))
    bus.emit(AnotherEvent("test"))

    assert len(all_events) == 2


def test_clear():
    bus = EventBus()
    received = []

    bus.subscribe(TestEvent, lambda e: received.append(e))
    bus.emit(TestEvent(1))

    assert len(received) == 1

    bus.clear()
    bus.emit(TestEvent(2))

    assert len(received) == 1


if __name__ == "__main__":
    test_subscribe_and_emit()
    test_multiple_subscribers()
    test_different_event_types()
    test_subscribe_all()
    test_clear()
    print("All event bus tests passed!")
