import hashlib
import re
from typing import List, Tuple


class StabilizerEngine:
    def __init__(self, axis_manager):
        self.axis = axis_manager

    def stabilize(self, intent: str, draft: str, mode: str) -> Tuple[str, dict]:
        limits = self.axis.get_limits(mode)
        max_chars = limits.get("max_chars", 2000)
        max_paragraphs = limits.get("max_paragraphs", 5)

        report = {
            "cut_flags": [],
            "trimmed_chars": 0,
            "removed_new_topics": 0,
        }

        # Critical mode: if no intent and draft is branching, return single question
        if mode == "critical" and not intent.strip() and self._is_branching(draft):
            report["cut_flags"].append("critical_clarification")
            return self._generate_clarification(draft), report

        result = draft

        # Remove variants/options blocks
        result, removed_variants = self._remove_variants(result)
        if removed_variants:
            report["cut_flags"].append("variants_removed")

        # Enforce paragraph limit
        result, para_cut = self._limit_paragraphs(result, max_paragraphs)
        if para_cut:
            report["cut_flags"].append("paragraph_limit")

        # Enforce char limit
        if len(result) > max_chars:
            report["trimmed_chars"] = len(result) - max_chars
            cutoff = max_chars - 1  # reserve 1 char for the ellipsis
            truncated = result[:cutoff]
            result = truncated.rsplit(' ', 1)[0] + "…"
            report["cut_flags"].append("char_limit")

        # Remove new topics not in intent
        result, new_topics = self._filter_new_topics(result, intent)
        report["removed_new_topics"] = new_topics

        return result, report

    def _is_branching(self, text: str) -> bool:
        option_patterns = len(re.findall(r'\b(option|variant|alternative|or)\b', text, re.I))
        lists = len(re.findall(r'^\s*[-*•]\s', text, re.M))
        return option_patterns > 2 or lists > 8

    def _generate_clarification(self, draft: str) -> str:
        match = re.search(r'\b(option|variant|alternative)\b', draft, re.I)
        if match:
            return "Which specific option do you want to proceed with?"
        return "What is your primary goal for this request?"

    def _remove_variants(self, text: str) -> Tuple[str, bool]:
        original = text
        text = re.sub(
            r'(?:^|\n)(?:Option|Variant|Alternative)\s+[A-Z0-9]:\s*.*?'
            r'(?=\n(?:Option|Variant|Alternative)\s+[A-Z0-9]:|\Z)',
            '', text, flags=re.I | re.S
        )
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip(), len(original) != len(text)

    def _limit_paragraphs(self, text: str, max_para: int) -> Tuple[str, bool]:
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        if len(paragraphs) <= max_para:
            return text, False
        return '\n\n'.join(paragraphs[:max_para]), True

    def _filter_new_topics(self, text: str, intent: str) -> Tuple[str, int]:
        if not intent.strip():
            return text, 0

        intent_keywords = set(re.findall(r'\b\w{4,}\b', intent.lower()))
        sentences = re.split(r'(?<=[.!?])\s+', text)
        kept = []
        removed = 0

        for sent in sentences:
            sent_keywords = set(re.findall(r'\b\w{4,}\b', sent.lower()))
            overlap = len(intent_keywords & sent_keywords)
            if overlap > 0 or len(intent_keywords) == 0:
                kept.append(sent)
            else:
                removed += 1

        return ' '.join(kept), removed

    def deterministic_score(self, text: str) -> float:
        h = hashlib.sha256(text.encode()).digest()
        return int.from_bytes(h[:4], 'big') / (2**32)
