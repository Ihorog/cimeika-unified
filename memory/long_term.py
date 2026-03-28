"""Persistent memory backed by a JSON file at ~/.cimeika/memory.json."""

from __future__ import annotations

import json
import os
from pathlib import Path


class LongTermMemory:
    def __init__(self, path: str = "~/.cimeika/memory.json") -> None:
        self._path = Path(path).expanduser()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text("{}", encoding="utf-8")

    def _load(self) -> dict:
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _save(self, data: dict) -> None:
        self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def write(self, key: str, value) -> None:
        """Persist *key*/*value* to the JSON store."""
        data = self._load()
        data[key] = value
        self._save(data)

    def read(self, key: str, default=None):
        """Read a value by key; return *default* if absent."""
        return self._load().get(key, default)

    def all(self) -> dict:
        """Return the full contents of the JSON store."""
        return self._load()
