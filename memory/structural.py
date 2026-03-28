"""Invariant knowledge: Ci=centre, binary logic, module registry, simulation markers."""

from __future__ import annotations


class StructuralMemory:
    INVARIANTS: dict = {
        "ci_role": "global orchestrator and centre of Cimeika",
        "binary_logic": {"є": True, "нема": False},
        "simulation_markers": {
            "modelled": "🔧",
            "simulation": "🌀",
            "unavailable": "⚠️",
        },
        "module_registry": [
            "kazkar",
            "podija",
            "nastrij",
            "malya",
            "calendar",
            "gallery",
        ],
        "response_contract": "one-input-one-output",
    }

    def get(self, key: str):
        """Return a single invariant value by key."""
        return self.INVARIANTS.get(key)

    def all(self) -> dict:
        """Return all invariants."""
        return dict(self.INVARIANTS)
