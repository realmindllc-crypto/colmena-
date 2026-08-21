"""Event system for PROYECTO COLMENA."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Callable, Optional
import sqlite3
import json
import logging
import uuid


@dataclass
class Event:
    """Represents a system event."""
    id: str
    type: str  # "task_created", "result_received", etc.
    timestamp: datetime
    source_agent: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp.isoformat(),
            "source_agent": self.source_agent,
            "payload": self.payload,
        }


class EventSystem:
    """Simple SQLite-based event system."""

    def __init__(self, db_path: str = "colmena_events.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("EventSystem")
        self.subscribers: Dict[str, List[Callable]] = {}
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    timestamp TEXT,
                    source_agent TEXT,
                    payload TEXT
                )
            """)
            conn.commit()

    def emit(self, event: Event):
        """Emit and persist an event."""
        # Persist to database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO events (id, type, timestamp, source_agent, payload)
                VALUES (?, ?, ?, ?, ?)
            """, (
                event.id,
                event.type,
                event.timestamp.isoformat(),
                event.source_agent,
                json.dumps(event.payload, default=str),
            ))
            conn.commit()

        # Notify subscribers
        if event.type in self.subscribers:
            for callback in self.subscribers[event.type]:
                try:
                    callback(event)
                except Exception as e:
                    self.logger.error(f"Error in callback: {e}")

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to an event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def get_events_by_type(self, event_type: str) -> List[Event]:
        """Retrieve historical events by type."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT id, type, timestamp, source_agent, payload
                FROM events WHERE type = ?
                ORDER BY timestamp DESC
            """, (event_type,)).fetchall()

        events = []
        for row in rows:
            events.append(Event(
                id=row[0],
                type=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                source_agent=row[3],
                payload=json.loads(row[4])
            ))

        return events

    def get_all_events(self) -> List[Event]:
        """Retrieve all events."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT id, type, timestamp, source_agent, payload
                FROM events ORDER BY timestamp DESC
            """).fetchall()

        events = []
        for row in rows:
            events.append(Event(
                id=row[0],
                type=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                source_agent=row[3],
                payload=json.loads(row[4])
            ))

        return events
