"""Malya — Creative/visual ideas module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grok.engine import GrokEngine


class MalyaModule:
    async def process(self, user_input: str, grok: "GrokEngine", memory) -> dict:
        result = await self.generate_visual_idea(user_input, grok)
        return {"status": "🌀", "result": result, "source": "malya"}

    async def generate_visual_idea(self, user_input: str, grok: "GrokEngine") -> str:
        prompt = (
            f"Generate a creative visual concept or art direction prompt inspired by: {user_input}"
        )
        return await grok.reason(prompt)
