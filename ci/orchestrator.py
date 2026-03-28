"""Ci Orchestrator — routes requests to domain modules."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grok.engine import GrokEngine
    from memory.active import ActiveMemory


VALID_STATUSES = {"fact", "🔧", "🌀", "⚠️"}


class Orchestrator:
    def __init__(
        self,
        memory_store: "ActiveMemory",
        intent_classifier,
        grok_engine: "GrokEngine",
        modules: dict,
    ) -> None:
        self.memory = memory_store
        self.intent_classifier = intent_classifier
        self.grok = grok_engine
        self.modules = modules

    async def handle_request(self, user_input: str) -> dict:
        """Detect intent → select module → process → validate → store → return."""
        intent = self.intent_classifier.detect(user_input)
        module = self.modules.get(intent)

        if module is None:
            result = {
                "intent": intent,
                "source": "ci",
                "status": "⚠️",
                "result": "Unknown intent — no module matched.",
                "next_action": None,
            }
            self.memory.write(result)
            return result

        raw_result = await module.process(user_input, self.grok, self.memory)
        validated = self.validate(raw_result)

        response = {
            "intent": intent,
            "source": validated.get("source", intent),
            "status": validated.get("status", "fact"),
            "result": validated.get("result", ""),
            "next_action": validated.get("next_action", None),
        }
        self.memory.write(response)
        return response

    def validate(self, raw_result: dict) -> dict:
        """Ensure status is one of the allowed values; default to 'fact'."""
        result = dict(raw_result)
        if result.get("status") not in VALID_STATUSES:
            result["status"] = "fact"
        return result
