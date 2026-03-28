"""
Active Memory — session-scoped in-memory store with optional TTL
Thread-safe, no external dependencies
"""
import time
import threading
from typing import Any


class ActiveMemory:
    """
    Session-scoped in-memory store.
    Entries are stored as {key: {"value": Any, "expires_at": float | None}}.
    """

    def __init__(self) -> None:
        self._store: dict[str, dict] = {}
        self._lock = threading.Lock()

    def write(self, key: str, value: Any, ttl_seconds: float | None = None) -> None:
        """Store a value with optional TTL."""
        expires_at = time.time() + ttl_seconds if ttl_seconds is not None else None
        with self._lock:
            self._store[key] = {"value": value, "expires_at": expires_at}

    def read(self, key: str) -> Any | None:
        """Return value or None if expired/missing; auto-deletes expired entries."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            expires_at = entry.get("expires_at")
            if expires_at is not None and time.time() > expires_at:
                del self._store[key]
                return None
            return entry["value"]

    def clear(self) -> None:
        """Wipe all entries."""
        with self._lock:
            self._store.clear()

    def snapshot(self) -> dict:
        """Return copy of all non-expired entries as {key: value}."""
        now = time.time()
        with self._lock:
            result = {}
            for key, entry in list(self._store.items()):
                expires_at = entry.get("expires_at")
                if expires_at is not None and now > expires_at:
                    continue
                result[key] = entry["value"]
            return result
