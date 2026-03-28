"""
Structural Memory — immutable invariant knowledge store for Ci Agent System
"""
from typing import Any

STRUCTURAL_KNOWLEDGE: dict = {
    "ci_identity": "Ci є центром. Ci координує. Ci не виконує — Ci делегує.",
    "binary_logic": {"є": True, "нема": False},
    "simulation_markers": {"modelled": "🔧", "simulation": "🌀", "unavailable": "⚠️"},
    "output_statuses": ["fact", "simulation", "unavailable"],
    "modules": ["ci", "kazkar", "podija", "nastrij", "malya", "gallery", "calendar"],
    "communication_rule": "Modules never call each other directly. All routing goes through Ci.",
    "memory_hierarchy": ["active", "long_term", "structural"],
    "language": "uk",
}


class StructuralMemory:
    """Read-only access to invariant system knowledge."""

    def get(self, key: str) -> Any | None:
        """Return value for key, or None if not found."""
        return STRUCTURAL_KNOWLEDGE.get(key)

    def all(self) -> dict:
        """Return a copy of all structural knowledge."""
        return dict(STRUCTURAL_KNOWLEDGE)

    def validate_status(self, status: str) -> bool:
        """Check whether status is one of the valid output statuses."""
        return status in STRUCTURAL_KNOWLEDGE["output_statuses"]

    def get_marker(self, kind: str) -> str:
        """Return simulation marker for kind, or '' if not found."""
        markers: dict = STRUCTURAL_KNOWLEDGE.get("simulation_markers", {})
        return markers.get(kind, "")


# Module-level singleton
structural = StructuralMemory()
