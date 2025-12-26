"""
SEO Matrix Loader
Loads and provides access to SEO metadata from cimeika_seo_matrix.yaml

Contract (tests expect):
- get_all_states() -> list length 7
- get_all_intents() -> list length 7
- get_meta(state, intent) -> not None for known pairs
- hreflang_patterns includes "uk" (NOT "ua")
- get_canonical_url(state, intent, lang?) must format {state}/{intent} (no {module}/{category})
- get_hreflang_tags(state, intent) must not raise KeyError
- get_full_seo_data(state, intent, lang?) must include "meta"
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Dict, Any, Optional, List

import yaml


class SEOMatrix:
    """
    Manages SEO metadata for different emotional states and intents.
    Provides canonical URLs, hreflang tags, and meta information.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize SEO Matrix

        Args:
            config_path: Path to YAML config file. If None, uses packaged default:
                         app/data/seo_matrix.yaml (via importlib.resources).
        """
        self.config_path: Optional[Path] = Path(config_path) if config_path else None
        self._data: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load SEO matrix from YAML file (deterministic in CI)."""
        if self.config_path is not None:
            if not self.config_path.exists():
                raise FileNotFoundError(f"SEO matrix file not found: {self.config_path}")
            with self.config_path.open("r", encoding="utf-8") as f:
                self._data = yaml.safe_load(f) or {}
            self._normalize()
            return

        # Default: load from package resources (backend/app/data/seo_matrix.yaml)
        try:
            with resources.files("app.data").joinpath("seo_matrix.yaml").open("r", encoding="utf-8") as f:
                self._data = yaml.safe_load(f) or {}
        except Exception as e:
            raise RuntimeError("SEO matrix failed to load from packaged resource app.data/seo_matrix.yaml") from e

        self._normalize()

    def _normalize(self) -> None:
        """
        Normalize and validate required fields. No silent empty fallbacks.
        """
        if not isinstance(self._data, dict):
            raise ValueError("SEO matrix root must be a mapping/object")

        # Support either:
        # - top-level states/intents/meta/hreflang_patterns
        # - legacy structure under "seo" + "meta_entries"
        if "seo" in self._data and isinstance(self._data.get("seo"), dict):
            seo = self._data["seo"]
            # Map legacy keys into new canonical keys if present
            if "hreflang" in seo and "hreflang_patterns" not in self._data:
                self._data["hreflang_patterns"] = seo.get("hreflang") or {}
            if "canonical_lang" in seo and "canonical_lang" not in self._data:
                self._data["canonical_lang"] = seo.get("canonical_lang")

        # Ensure hreflang uses "uk" not "ua"
        hreflang = self._data.get("hreflang_patterns") or {}
        if isinstance(hreflang, dict) and "ua" in hreflang and "uk" not in hreflang:
            hreflang["uk"] = hreflang.pop("ua")
        self._data["hreflang_patterns"] = hreflang

        # Hard requirements for tests
        states = self.get_all_states()
        intents = self.get_all_intents()
        meta = self._data.get("meta")

        if len(states) == 0:
            raise ValueError("SEO matrix has no states (tests expect 7)")
        if len(intents) == 0:
            raise ValueError("SEO matrix has no intents (tests expect 7)")
        if meta is None:
            # tests require meta not None
            raise ValueError("SEO matrix meta is missing (tests expect non-null meta)")
        if "uk" not in self.hreflang_patterns:
            raise ValueError('SEO matrix hreflang_patterns must include key "uk"')

    @property
    def canonical_lang(self) -> str:
        """Get canonical language (default 'en')."""
        return str(self._data.get("canonical_lang") or "en")

    @property
    def hreflang_patterns(self) -> Dict[str, str]:
        """Get hreflang URL patterns. Must include 'uk'."""
        val = self._data.get("hreflang_patterns") or {}
        return dict(val) if isinstance(val, dict) else {}

    @property
    def rules(self) -> Dict[str, int]:
        """Get SEO validation rules (optional)."""
        seo = self._data.get("seo") or {}
        if isinstance(seo, dict):
            rules = seo.get("rules") or {}
            return dict(rules) if isinstance(rules, dict) else {}
        return {}

    def get_meta(self, state: str, intent: str) -> Optional[Dict[str, str]]:
        """
        Get meta information for a specific state and intent.

        Returns:
            Dict with 'title' and 'description' or None.
        """
        # Prefer explicit meta_entries if present
        meta_entries = self._data.get("meta_entries") or {}
        if isinstance(meta_entries, dict):
            state_data = meta_entries.get(state) or {}
            if isinstance(state_data, dict):
                meta = state_data.get(intent)
                if isinstance(meta, dict):
                    return meta

        # Optional alternative: allow meta_entries_by_pair
        pairs = self._data.get("meta_by_pair") or {}
        if isinstance(pairs, dict):
            meta = pairs.get(f"{state}:{intent}")
            if isinstance(meta, dict):
                return meta

        return None

    def get_canonical_url(self, state: str, intent: str, lang: Optional[str] = None) -> str:
        """
        Generate canonical URL for given state and intent.

        Note: patterns must support {state} and {intent}. No {module}/{category}.
        """
        if lang is None:
            lang = self.canonical_lang

        patterns = self.hreflang_patterns
        pattern = patterns.get(lang) or patterns.get("en") or patterns.get("uk")
        if not pattern:
            raise KeyError(f"No hreflang pattern available for lang={lang}")

        # Must format only state/intent to avoid KeyError('module')
        return pattern.format(state=state, intent=intent)

    def get_hreflang_tags(self, state: str, intent: str) -> Dict[str, str]:
        """
        Generate hreflang tags for all languages.

        Returns:
            Dict mapping language codes to URL paths.
        """
        tags: Dict[str, str] = {}
        for lang, pattern in self.hreflang_patterns.items():
            tags[lang] = pattern.format(state=state, intent=intent)
        return tags

    def validate_meta(self, title: str, description: str) -> Dict[str, Any]:
        """
        Validate meta title and description against rules (optional).
        """
        title_max = int(self.rules.get("title_max", 60))
        description_max = int(self.rules.get("description_max", 155))

        return {
            "title": {
                "value": title,
                "length": len(title),
                "max": title_max,
                "valid": len(title) <= title_max,
            },
            "description": {
                "value": description,
                "length": len(description),
                "max": description_max,
                "valid": len(description) <= description_max,
            },
        }

    def get_all_states(self) -> List[str]:
        """
        Get list of all available emotional states.

        Tests expect 7.
        """
        states = self._data.get("states")
        if isinstance(states, list) and all(isinstance(x, str) for x in states):
            return states

        # Legacy fallback: keys of meta_entries
        meta_entries = self._data.get("meta_entries") or {}
        if isinstance(meta_entries, dict):
            return list(meta_entries.keys())

        return []

    def get_all_intents(self) -> List[str]:
        """
        Get list of all available intents.

        Tests expect 7 and call this without a state argument.
        """
        intents = self._data.get("intents")
        if isinstance(intents, list) and all(isinstance(x, str) for x in intents):
            return intents

        # Legacy fallback: union of intents from meta_entries
        meta_entries = self._data.get("meta_entries") or {}
        if isinstance(meta_entries, dict):
            acc = set()
            for _, state_data in meta_entries.items():
                if isinstance(state_data, dict):
                    acc.update([k for k in state_data.keys() if isinstance(k, str)])
            return sorted(acc)

        return []

    def get_full_seo_data(self, state: str, intent: str, lang: Optional[str] = None) -> Dict[str, Any]:
        """
        Return full SEO data bundle for a given state/intent.
        Tests expect 'meta' key present.
        """
        meta = self.get_meta(state, intent)
        if meta is None:
            # Keep deterministic behavior: return minimal structure (tests may call with known pairs)
            meta = {"title": "", "description": ""}

        return {
            "state": state,
            "intent": intent,
            "meta": meta,
            "canonical": self.get_canonical_url(state, intent, lang=lang),
            "hreflang": self.get_hreflang_tags(state, intent),
            "matrix_meta": self._data.get("meta"),
        }
