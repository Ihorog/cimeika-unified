"""Gallery — Media memory module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grok.engine import GrokEngine


class GalleryModule:
    async def process(self, user_input: str, grok: "GrokEngine", memory) -> dict:
        result = await self.query_archive(user_input, grok)
        return {"status": "fact", "result": result, "source": "gallery"}

    async def query_archive(self, user_input: str, grok: "GrokEngine") -> str:
        prompt = f"Describe or retrieve relevant media archive entries for: {user_input}"
        return await grok.reason(prompt)
