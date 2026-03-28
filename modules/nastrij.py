"""Nastrij — State/mood analysis module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grok.engine import GrokEngine


class NastrijModule:
    async def process(self, user_input: str, grok: "GrokEngine", memory) -> dict:
        result = await self.analyse_mood(user_input, grok)
        return {"status": "fact", "result": result, "source": "nastrij"}

    async def analyse_mood(self, user_input: str, grok: "GrokEngine") -> str:
        prompt = f"Analyse the mood and emotional state expressed in: {user_input}"
        return await grok.reason(prompt)
