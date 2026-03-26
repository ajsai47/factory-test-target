"""Tests for async event handler module."""
import threading
from async_events import AsyncEventHandler


def test_emit_and_get_events():
    """Test basic emit and get_events functionality."""
    handler = AsyncEventHandler()
    
    handler.emit("event1")
    handler.emit("event2")
    handler.emit("event3")
    
    events = handler.get_events()
    assert events == ["event1", "event2", "event3"]
    
    assert handler.get_events() == []


def test_event_count():
    """Test event_count returns correct number of events."""
    handler = AsyncEventHandler()
    
    assert handler.event_count() == 0
    
    handler.emit("event1")
    assert handler.event_count() == 1
    
    handler.emit("event2")
    handler.emit("event3")
    assert handler.event_count() == 3
    
    handler.get_events()
    assert handler.event_count() == 0


def test_get_events_clears_queue():
    """Test that get_events clears the queue."""
    handler = AsyncEventHandler()
    
    handler.emit("event1")
    handler.emit("event2")
    
    assert handler.event_count() == 2
    events = handler.get_events()
    assert len(events) == 2
    assert handler.event_count() == 0
    assert handler.get_events() == []


def test_concurrent_emit_no_race_condition():
    """Test that concurrent emits don't drop events due to race conditions."""
    handler = AsyncEventHandler()
    num_threads = 10
    events_per_thread = 100
    expected_total = num_threads * events_per_thread
    
    def emit_events(thread_id: int):
        """Emit multiple events from a single thread."""
        for i in range(events_per_thread):
            handler.emit(f"thread_{thread_id}_event_{i}")
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=emit_events, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    assert handler.event_count() == expected_total
    
    events = handler.get_events()
    assert len(events) == expected_total
    
    for i in range(num_threads):
        thread_events = [e for e in events if e.startswith(f"thread_{i}_")]
        assert len(thread_events) == events_per_thread