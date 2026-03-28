"""
Ci Agent — central agent orchestrator for Ci Agent System v1
Connects GrokEngine, Memory Layer, ModuleRegistry, and CiCoordinator
"""
import asyncio
import logging
from enum import Enum
from typing import Any

from pydantic import BaseModel

from app.core.grok_engine import grok
from app.core.memory.active import ActiveMemory
from app.core.memory.long_term import LongTermMemory
from app.core.memory.structural import structural
from app.core.orchestrator import registry

logger = logging.getLogger(__name__)

# Modules list from structural knowledge
_MODULES: list[str] = structural.get("modules") or [
    "ci", "kazkar", "podija", "nastrij", "malya", "gallery", "calendar"
]


class OutputStatus(str, Enum):
    FACT = "fact"
    SIMULATION = "simulation"
    UNAVAILABLE = "unavailable"


class AgentResponse(BaseModel):
    intent: str
    source: str
    status: OutputStatus
    result: str
    marker: str = ""
    next_action: str | None = None
    grok_backend: str = "fallback"
    session_context: dict = {}


class CiAgent:
    """
    Central agent orchestrator.
    Detects intent, routes to modules, validates output, manages memory.
    """

    def __init__(self) -> None:
        self.active_memory = ActiveMemory()
        self.long_term = LongTermMemory()
        self.structural = structural
        self._keyword_map: dict[str, str] = {
            "історія": "kazkar",
            "спогад": "kazkar",
            "минуле": "kazkar",
            "пам'ять": "kazkar",
            "згадка": "kazkar",
            "подія": "podija",
            "план": "podija",
            "майбутнє": "podija",
            "захід": "podija",
            "зустріч": "podija",
            "заплануй": "podija",
            "настрій": "nastrij",
            "емоція": "nastrij",
            "почуття": "nastrij",
            "відчуття": "nastrij",
            "як ти": "nastrij",
            "ідея": "malya",
            "творчість": "malya",
            "креатив": "malya",
            "створи": "malya",
            "малюнок": "malya",
            "дизайн": "malya",
            "фото": "gallery",
            "зображення": "gallery",
            "картинка": "gallery",
            "галерея": "gallery",
            "медіа": "gallery",
            "час": "calendar",
            "календар": "calendar",
            "дата": "calendar",
            "коли": "calendar",
            "розклад": "calendar",
            "термін": "calendar",
        }

    async def _detect_intent(self, text: str) -> str:
        """
        Two-stage intent detection:
        1. Keyword scan (fast, no LLM cost)
        2. If no keyword match → ask Grok to classify into one of the 7 module names
        Returns module name string (e.g. "kazkar", "ci", etc.)
        """
        text_lower = text.lower()

        # Stage 1: keyword scan
        scores: dict[str, int] = {}
        for keyword, module in self._keyword_map.items():
            if keyword in text_lower:
                scores[module] = scores.get(module, 0) + 1

        if scores:
            return max(scores, key=lambda m: scores[m])

        # Stage 2: Grok classification
        try:
            result = await grok.classify(text, _MODULES)
            if result in _MODULES:
                return result
        except Exception as exc:
            logger.error("CiAgent._detect_intent grok.classify error: %s", exc)

        return "ci"

    def _validate_output(self, raw: dict) -> tuple[OutputStatus, str]:
        """
        Determine OutputStatus from raw module output dict.
        - If raw has key "status" in ["fact","simulation","unavailable"] → use it
        - If raw has key "error" → OutputStatus.UNAVAILABLE
        - Else → OutputStatus.FACT
        Returns (status, marker_string)
        """
        if "error" in raw:
            status = OutputStatus.UNAVAILABLE
            marker = self.structural.get_marker("unavailable")
            return status, marker

        raw_status = raw.get("status", "")
        if self.structural.validate_status(str(raw_status)):
            status = OutputStatus(raw_status)
        else:
            status = OutputStatus.FACT

        marker_kind = status.value if status != OutputStatus.FACT else ""
        marker = self.structural.get_marker(marker_kind) if marker_kind else ""
        return status, marker

    async def process(self, user_input: str, session_id: str = "default") -> AgentResponse:
        """
        Full pipeline:
        1. Detect intent → module name
        2. Write input to active_memory (key: f"last_input:{session_id}", TTL=300s)
        3. Get module from registry; if not found → return UNAVAILABLE response
        4. Call module.process({"input": user_input, "session_id": session_id})
        5. Ask Grok to summarise the result string
        6. Validate output → determine status + marker
        7. Write result to active_memory (key: f"last_result:{session_id}", TTL=300s)
        8. Optionally write to long_term if status == FACT
        9. Build and return AgentResponse
        """
        # 1. Intent detection
        intent = await self._detect_intent(user_input)

        # 2. Write input to active memory
        self.active_memory.write(f"last_input:{session_id}", user_input, ttl_seconds=300)

        # 3. Get module from registry
        module = registry.get(intent)
        if module is None:
            logger.warning("CiAgent: module '%s' not found in registry", intent)
            return AgentResponse(
                intent=intent,
                source="ci",
                status=OutputStatus.UNAVAILABLE,
                result=f"Module '{intent}' is not available.",
                marker=self.structural.get_marker("unavailable"),
                grok_backend=grok.backend_name,
            )

        # 4. Call module.process
        try:
            raw: Any = await self._call_module(module, user_input, session_id)
        except Exception as exc:
            logger.error("CiAgent: module '%s' process error: %s", intent, exc)
            raw = {"error": str(exc)}

        # Normalise to dict
        if not isinstance(raw, dict):
            raw = {"result": str(raw)}

        # 5. Summarise result
        raw_result_str = str(raw.get("result", raw))
        try:
            summarised = await grok.summarise(raw_result_str)
        except Exception as exc:
            logger.error("CiAgent: grok.summarise error: %s", exc)
            summarised = raw_result_str

        # 6. Validate output
        status, marker = self._validate_output(raw)

        # 7. Write result to active memory
        self.active_memory.write(f"last_result:{session_id}", summarised, ttl_seconds=300)

        # 8. Write to long-term if FACT
        if status == OutputStatus.FACT:
            self.long_term.write(f"fact:{session_id}:{intent}", summarised)

        # 9. Build response
        source = str(raw.get("source", intent))
        return AgentResponse(
            intent=intent,
            source=source,
            status=status,
            result=summarised,
            marker=marker,
            next_action=raw.get("next_action") if isinstance(raw, dict) else None,
            grok_backend=grok.backend_name,
            session_context={},
        )

    @staticmethod
    async def _call_module(module: Any, user_input: str, session_id: str) -> Any:
        """Call module.process, handling both sync and async implementations."""
        result = module.process({"input": user_input, "session_id": session_id})
        if asyncio.iscoroutine(result):
            result = await result
        return result


# Module-level singleton
ci_agent = CiAgent()
