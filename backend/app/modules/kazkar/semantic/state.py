"""
State — in-memory strict legend session state.

Strict mode: navigation and export require an active session.
Call activate() to start a session. The session resets to 'prysutnist'.
"""
from typing import List, Optional

_HISTORY_MAX_TAIL = 5


class LegendState:
    def __init__(self) -> None:
        self._active: bool = False
        self._current_node_id: Optional[str] = None
        self._history: List[str] = []

    @property
    def active(self) -> bool:
        return self._active

    @property
    def current_node_id(self) -> Optional[str]:
        return self._current_node_id

    @property
    def history(self) -> List[str]:
        return list(self._history)

    @property
    def history_tail(self) -> List[str]:
        return list(self._history[-_HISTORY_MAX_TAIL:])

    def activate(self, start_node_id: str = "prysutnist") -> None:
        self._active = True
        self._current_node_id = start_node_id
        self._history = [start_node_id]

    def navigate(self, node_id: str) -> None:
        if not self._active:
            raise RuntimeError("Legend session is not active")
        self._current_node_id = node_id
        # Avoid recording consecutive duplicate entries in history
        if not self._history or self._history[-1] != node_id:
            self._history.append(node_id)

    def reset(self) -> None:
        self._active = False
        self._current_node_id = None
        self._history = []


# Module-level singleton — one session per process
legend_state = LegendState()
