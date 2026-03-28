"""Kazkar — Narrative/mythology module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grok.engine import GrokEngine


class KazkarModule:
    async def process(self, user_input: str, grok: "GrokEngine", memory) -> dict:
        if "symbol" in user_input.lower():
            interpretation = await self.interpret_symbol(user_input, grok)
            return {"status": "fact", "result": interpretation, "source": "kazkar"}
        story = await self.generate_narrative(user_input, grok)
        return {"status": "🌀", "result": story, "source": "kazkar"}

    async def interpret_symbol(self, symbol: str, grok: "GrokEngine") -> str:
        prompt = f"Interpret the symbolic meaning of '{symbol}' in a mythological context."
        return await grok.reason(prompt)

    async def generate_narrative(self, query: str, grok: "GrokEngine") -> str:
        prompt = f"Create a short mythological story based on: {query}"
        return await grok.reason(prompt)
