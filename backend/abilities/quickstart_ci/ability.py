"""
QuickstartCI Ability Module
Provides a normalized Quickstart CI WidgetSpec (template + JSON schema + defaults).
"""
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from ..base import Ability

logger = logging.getLogger(__name__)

_SPEC_PATH = Path(__file__).parent / "widgetspec.v1.json"

_TYPE_MAP = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "array": list,
    "object": dict,
}


def _validate_against_schema(data: Any, schema: Dict) -> List[str]:
    """
    Minimal JSON-Schema validator (draft-07 subset).

    Supported keywords: type, required, properties, items, enum.
    Returns a list of error messages; empty list means valid.
    """
    errors: List[str] = []

    schema_type = schema.get("type")
    if schema_type:
        expected = _TYPE_MAP.get(schema_type)
        if expected and not isinstance(data, expected):
            errors.append(
                f"Expected type '{schema_type}', got '{type(data).__name__}'"
            )
            return errors  # no point checking further if type is wrong

    if isinstance(data, dict):
        for required_key in schema.get("required", []):
            if required_key not in data:
                errors.append(f"Missing required field: '{required_key}'")

        for prop_name, prop_schema in schema.get("properties", {}).items():
            if prop_name in data:
                sub_errors = _validate_against_schema(data[prop_name], prop_schema)
                for e in sub_errors:
                    errors.append(f"{prop_name}: {e}")

    if isinstance(data, list):
        items_schema = schema.get("items")
        if items_schema:
            for idx, item in enumerate(data):
                sub_errors = _validate_against_schema(item, items_schema)
                for e in sub_errors:
                    errors.append(f"[{idx}]: {e}")

    enum_values = schema.get("enum")
    if enum_values is not None and data not in enum_values:
        errors.append(f"Value {data!r} is not one of {enum_values}")

    return errors


class QuickstartCiAbility(Ability):
    """
    Quickstart CI Widget ability.

    Provides a normalized WidgetSpec (Jinja2 template + JSON schema + defaults)
    that renders a list of one-click CI action buttons for the UI DSL.

    Activation Triggers:
    - User requests Quickstart CI panel
    - System needs to expose CI quick-action buttons

    States:
    - Dormant: WidgetSpec loaded but not served; no background processes
    - Active: Ready to serve spec, list quick items, and validate models
    """

    def __init__(self) -> None:
        """Initialize quickstart_ci ability in dormant state."""
        self._active = False
        self._spec: Dict[str, Any] = {}

    @property
    def name(self) -> str:
        """Unique ability identifier."""
        return "quickstart_ci"

    @property
    def version(self) -> str:
        """Semantic version."""
        return "0.1.0"

    async def activate(self) -> None:
        """
        Transition from dormant to active state.
        Load the WidgetSpec from disk.
        """
        if not self._active:
            try:
                with open(_SPEC_PATH, "r", encoding="utf-8") as f:
                    self._spec = json.load(f)
            except Exception as exc:
                logger.error("Failed to load widgetspec.v1.json: %s", exc)
                self._spec = {}
            self._active = True

    async def deactivate(self) -> None:
        """
        Return to dormant state.
        Release loaded spec from memory.
        """
        if self._active:
            self._spec = {}
            self._active = False

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute quickstart_ci operations.

        Args:
            context: Operation context with keys:
                - action: "get_spec" | "list_quick" | "validate"
                - model: (validate only) dict to validate against jsonSchema

        Supported actions:
            get_spec   - Returns the full WidgetSpec dict.
            list_quick - Returns the quick_items list from outputJsonPreview.
            validate   - Validates ``context["model"]`` against the spec's
                         jsonSchema. Returns {"valid": bool, "errors": list}.

        Returns:
            Result dict with operation output or {"error": str} on failure.
        """
        if not self._active:
            return {"error": "quickstart_ci ability is not active"}

        action = context.get("action")

        if action == "get_spec":
            return {"status": "success", "spec": self._spec}

        if action == "list_quick":
            preview = self._spec.get("outputJsonPreview", {})
            children = preview.get("children", [])
            quick_items = [
                {
                    "id": child.get("action", {}).get("payload", {}).get("id", ""),
                    "label": child.get("label", ""),
                }
                for child in children
                if child.get("type") == "button"
            ]
            return {"status": "success", "quick_items": quick_items}

        if action == "validate":
            model = context.get("model")
            if model is None:
                return {"error": "validate action requires 'model' in context"}
            schema = self._spec.get("jsonSchema", {})
            errors = _validate_against_schema(model, schema)
            return {"valid": len(errors) == 0, "errors": errors}

        return {"error": f"Unknown action: {action}"}
