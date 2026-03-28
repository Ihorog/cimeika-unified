"""Intent detection → module key mapping."""

from __future__ import annotations


class IntentClassifier:
    INTENT_MAP: dict[str, list[str]] = {
        "kazkar": ["symbol", "myth", "legend", "story", "казкар"],
        "podija": ["event", "future", "next", "predict", "подія"],
        "nastrij": ["mood", "feel", "state", "настрій"],
        "malya": ["create", "visual", "image", "design", "маля"],
        "calendar": ["calendar", "schedule", "time", "remind", "календар"],
        "gallery": ["gallery", "photo", "media", "archive", "галерея"],
    }

    def detect(self, text: str) -> str:
        """Return the module key for the first keyword match, or 'unknown'."""
        lower = text.lower()
        for module_key, keywords in self.INTENT_MAP.items():
            for keyword in keywords:
                if keyword in lower:
                    return module_key
        return "unknown"
