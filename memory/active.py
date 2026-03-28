"""Session-level memory (in-memory list, async-safe for single-process use)."""

from __future__ import annotations


class ActiveMemory:
    def __init__(self) -> None:
        self._store: list[dict] = []

    def write(self, entry: dict) -> None:
        """Append an entry to the session store."""
        self._store.append(entry)

    def read_last(self, n: int = 5) -> list[dict]:
        """Return the last *n* entries."""
        return self._store[-n:]

    def clear(self) -> None:
        """Clear all entries from the session store."""
        self._store.clear()
