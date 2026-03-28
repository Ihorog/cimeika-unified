"""Podija — Event prediction module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grok.engine import GrokEngine

_EVENT_KEYWORDS = ["event", "future", "next", "predict", "подія", "план"]


class PodijaModule:
    async def process(self, user_input: str, grok: "GrokEngine", memory) -> dict:
        result = await self.predict_next_step(user_input, grok)
        return {"status": "🔧", "result": result, "source": "podija"}

    async def predict_next_step(self, user_input: str, grok: "GrokEngine") -> str:
        prompt = f"Predict the next logical step or event based on: {user_input}"
        return await grok.reason(prompt)
