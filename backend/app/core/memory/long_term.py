"""
Long-Term Memory — persistent JSON-file key-value store
Thread-safe, stdlib only
"""
import json
import logging
import os
import threading
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_PATH = Path(os.getenv("LONG_TERM_MEMORY_PATH", "/tmp/cimeika_long_term.json"))


class LongTermMemory:
    """
    Persistent JSON-file memory.
    Auto-creates the file if missing; handles corrupt JSON gracefully.
    """

    def __init__(self, path: Path = _DEFAULT_PATH) -> None:
        self._path = path
        self._lock = threading.Lock()
        self._ensure_file()

    # ------------------------------------------------------------------ #
    # Public methods                                                        #
    # ------------------------------------------------------------------ #

    def write(self, key: str, value: Any) -> None:
        """Upsert key into the JSON file."""
        with self._lock:
            data = self._load()
            data[key] = value
            self._save(data)

    def read(self, key: str) -> Any | None:
        """Return value or None."""
        with self._lock:
            data = self._load()
            return data.get(key)

    def all(self) -> dict:
        """Return all persisted entries."""
        with self._lock:
            return dict(self._load())

    def delete(self, key: str) -> bool:
        """Remove key; return True if it existed."""
        with self._lock:
            data = self._load()
            if key not in data:
                return False
            del data[key]
            self._save(data)
            return True

    # ------------------------------------------------------------------ #
    # Private helpers                                                       #
    # ------------------------------------------------------------------ #

    def _ensure_file(self) -> None:
        """Create the file with an empty dict if it does not exist."""
        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text("{}", encoding="utf-8")

    def _load(self) -> dict:
        """Load JSON from file; reset to {} on corruption."""
        try:
            text = self._path.read_text(encoding="utf-8")
            return json.loads(text)
        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning("LongTermMemory: corrupt JSON at %s — resetting. Error: %s", self._path, exc)
            self._save({})
            return {}
        except OSError as exc:
            logger.error("LongTermMemory: cannot read %s: %s", self._path, exc)
            return {}

    def _save(self, data: dict) -> None:
        """Persist data to JSON file."""
        try:
            self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as exc:
            logger.error("LongTermMemory: cannot write %s: %s", self._path, exc)
