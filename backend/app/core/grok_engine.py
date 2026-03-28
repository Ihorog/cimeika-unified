"""
Grok Engine — async LLM abstraction layer for Ci Agent System
Supports OpenAI, Anthropic, and deterministic fallback (no API key required)
"""
import logging
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)

# Lazy-initialized client caches
_openai_client: Any = None
_anthropic_client: Any = None


def _get_openai_client() -> Any:
    global _openai_client
    if _openai_client is None:
        from openai import AsyncOpenAI
        _openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _openai_client


def _get_anthropic_client() -> Any:
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic
        _anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _anthropic_client


class GrokEngine:
    """
    Async LLM abstraction layer.
    Backend selection:
      - OPENAI_API_KEY set → OpenAI gpt-4o-mini
      - ANTHROPIC_API_KEY set → Anthropic claude-3-haiku-20240307
      - neither → deterministic fallback (no external calls)
    """

    # ------------------------------------------------------------------ #
    # Public async methods                                                  #
    # ------------------------------------------------------------------ #

    async def reason(self, prompt: str) -> str:
        """General reasoning via LLM, or fallback."""
        if settings.OPENAI_API_KEY:
            try:
                return await self._openai_reason(prompt)
            except Exception as exc:
                logger.error("OpenAI reason error: %s", exc)
        elif settings.ANTHROPIC_API_KEY:
            try:
                return await self._anthropic_reason(prompt)
            except Exception as exc:
                logger.error("Anthropic reason error: %s", exc)
        return self._fallback_reason(prompt)

    async def classify(self, text: str, labels: list[str]) -> str:
        """Zero-shot classification via LLM, or fallback."""
        if settings.OPENAI_API_KEY:
            try:
                return await self._openai_classify(text, labels)
            except Exception as exc:
                logger.error("OpenAI classify error: %s", exc)
        elif settings.ANTHROPIC_API_KEY:
            try:
                return await self._anthropic_classify(text, labels)
            except Exception as exc:
                logger.error("Anthropic classify error: %s", exc)
        return self._fallback_classify(labels)

    async def summarise(self, text: str) -> str:
        """Summarisation via LLM, or fallback."""
        if settings.OPENAI_API_KEY:
            try:
                return await self._openai_summarise(text)
            except Exception as exc:
                logger.error("OpenAI summarise error: %s", exc)
        elif settings.ANTHROPIC_API_KEY:
            try:
                return await self._anthropic_summarise(text)
            except Exception as exc:
                logger.error("Anthropic summarise error: %s", exc)
        return self._fallback_summarise(text)

    # ------------------------------------------------------------------ #
    # Backend name property                                                 #
    # ------------------------------------------------------------------ #

    @property
    def backend_name(self) -> str:
        """Returns the active backend name."""
        if settings.OPENAI_API_KEY:
            return "openai"
        if settings.ANTHROPIC_API_KEY:
            return "anthropic"
        return "fallback"

    # ------------------------------------------------------------------ #
    # OpenAI implementations                                               #
    # ------------------------------------------------------------------ #

    async def _openai_reason(self, prompt: str) -> str:
        client = _get_openai_client()
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""

    async def _openai_classify(self, text: str, labels: list[str]) -> str:
        client = _get_openai_client()
        label_list = ", ".join(labels)
        prompt = (
            f"Classify the following text into exactly one of these labels: {label_list}.\n"
            f"Respond with only the label name.\n\nText: {text}"
        )
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        result = (response.choices[0].message.content or "").strip()
        return result if result in labels else (labels[0] if labels else "unknown")

    async def _openai_summarise(self, text: str) -> str:
        client = _get_openai_client()
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarise concisely."},
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content or ""

    # ------------------------------------------------------------------ #
    # Anthropic implementations                                            #
    # ------------------------------------------------------------------ #

    async def _anthropic_reason(self, prompt: str) -> str:
        client = _get_anthropic_client()
        message = await client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text if message.content else ""

    async def _anthropic_classify(self, text: str, labels: list[str]) -> str:
        client = _get_anthropic_client()
        label_list = ", ".join(labels)
        prompt = (
            f"Classify the following text into exactly one of these labels: {label_list}.\n"
            f"Respond with only the label name.\n\nText: {text}"
        )
        message = await client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=64,
            messages=[{"role": "user", "content": prompt}],
        )
        result = (message.content[0].text if message.content else "").strip()
        return result if result in labels else (labels[0] if labels else "unknown")

    async def _anthropic_summarise(self, text: str) -> str:
        client = _get_anthropic_client()
        message = await client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=512,
            messages=[
                {"role": "user", "content": f"Summarise concisely:\n\n{text}"},
            ],
        )
        return message.content[0].text if message.content else ""

    # ------------------------------------------------------------------ #
    # Fallback implementations (deterministic, no external calls)          #
    # ------------------------------------------------------------------ #

    def _fallback_reason(self, prompt: str) -> str:
        return f"[FALLBACK] Input processed: {prompt[:120]}"

    def _fallback_classify(self, labels: list[str]) -> str:
        return labels[0] if labels else "unknown"

    def _fallback_summarise(self, text: str) -> str:
        return text[:200] + "..." if len(text) > 200 else text


# Module-level singleton
grok = GrokEngine()
