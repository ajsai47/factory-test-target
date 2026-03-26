"""Async event handler module with thread-safe operations."""
import threading
from typing import List


class AsyncEventHandler:
    """Thread-safe event handler for async operations."""
    
    def __init__(self):
        """Initialize event handler with empty queue and lock."""
        self._event_queue: List[str] = []
        self._lock = threading.Lock()
    
    def emit(self, event: str) -> None:
        """Add an event to the queue."""
        with self._lock:
            self._event_queue.append(event)
    
    def get_events(self) -> List[str]:
        """Return a copy of all events and clear the queue."""
        with self._lock:
            events = self._event_queue.copy()
            self._event_queue.clear()
            return events
    
    def event_count(self) -> int:
        """Return the number of events in the queue."""
        with self._lock:
            return len(self._event_queue)