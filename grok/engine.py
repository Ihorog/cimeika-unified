"""Grok AI engine wrapper — LLM reasoning, classification, summarisation."""

from __future__ import annotations

import os


class GrokEngine:
    def __init__(self, llm_client=None) -> None:
        if llm_client is not None:
            self._client = llm_client
        else:
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key:
                try:
                    from openai import AsyncOpenAI  # type: ignore[import]

                    self._client = AsyncOpenAI(api_key=api_key)
                except ImportError:
                    self._client = None
            else:
                self._client = None

    async def reason(self, prompt: str) -> str:
        """General reasoning via LLM (or stub)."""
        if self._client is None:
            return f"[stub] {prompt[:80]}"
        response = await self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
        )
        return response.choices[0].message.content or ""

    async def classify(self, text: str, labels: list[str]) -> str:
        """Multi-class classification via LLM (or stub)."""
        if self._client is None:
            return labels[0] if labels else "[stub] classification"
        prompt = (
            f"Classify the following text into exactly one of these labels: "
            f"{', '.join(labels)}.\n\nText: {text}\n\nLabel:"
        )
        response = await self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=16,
        )
        raw = (response.choices[0].message.content or "").strip()
        for label in labels:
            if label.lower() in raw.lower():
                return label
        return labels[0] if labels else raw

    async def summarise(self, text: str) -> str:
        """Summarisation via LLM (or stub)."""
        if self._client is None:
            return f"[stub] {text[:80]}"
        response = await self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarise concisely."},
                {"role": "user", "content": text},
            ],
            max_tokens=128,
        )
        return response.choices[0].message.content or ""
