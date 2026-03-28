"""Calendar — Temporal/schedule module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grok.engine import GrokEngine


class CalendarModule:
    async def process(self, user_input: str, grok: "GrokEngine", memory) -> dict:
        result = await self.extract_schedule(user_input, grok)
        return {"status": "fact", "result": result, "source": "calendar"}

    async def extract_schedule(self, user_input: str, grok: "GrokEngine") -> str:
        prompt = f"Extract schedule, time references, or reminders from: {user_input}"
        return await grok.reason(prompt)
