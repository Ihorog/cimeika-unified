"""Unit tests for Ci Agent System v1.

Run with: pytest tests/test_system.py -v
"""

from __future__ import annotations

import json
import sys
import os
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

# Ensure repo root is on the path when running from the repo root.
sys.path.insert(0, str(Path(__file__).parent.parent))

from ci.intent_classifier import IntentClassifier
from ci.orchestrator import Orchestrator
from grok.engine import GrokEngine
from memory.active import ActiveMemory
from memory.long_term import LongTermMemory
from memory.structural import StructuralMemory
from modules.kazkar import KazkarModule


# ---------------------------------------------------------------------------
# 1. IntentClassifier.detect — all 6 intents + unknown fallback
# ---------------------------------------------------------------------------

class TestIntentClassifier:
    def setup_method(self):
        self.clf = IntentClassifier()

    def test_detect_kazkar_english(self):
        assert self.clf.detect("Tell me a myth about dragons") == "kazkar"

    def test_detect_kazkar_symbol(self):
        assert self.clf.detect("What does this symbol mean?") == "kazkar"

    def test_detect_podija(self):
        assert self.clf.detect("Predict the next event") == "podija"

    def test_detect_nastrij(self):
        assert self.clf.detect("What is my current mood?") == "nastrij"

    def test_detect_malya(self):
        assert self.clf.detect("Create a visual design") == "malya"

    def test_detect_calendar(self):
        assert self.clf.detect("Remind me about the schedule") == "calendar"

    def test_detect_gallery(self):
        assert self.clf.detect("Show me the photo archive") == "gallery"

    def test_detect_unknown(self):
        assert self.clf.detect("Hello world") == "unknown"

    def test_detect_case_insensitive(self):
        assert self.clf.detect("MYTH and LEGEND") == "kazkar"

    def test_detect_ukrainian_kazkar(self):
        assert self.clf.detect("казкар розповідь") == "kazkar"


# ---------------------------------------------------------------------------
# 2. Orchestrator.handle_request — mock module, verify return shape
# ---------------------------------------------------------------------------

class TestOrchestrator:
    def setup_method(self):
        self.memory = ActiveMemory()
        self.clf = IntentClassifier()
        self.grok = GrokEngine()  # stub (no API key)

        mock_module = MagicMock()
        mock_module.process = AsyncMock(
            return_value={
                "status": "fact",
                "result": "A great myth",
                "source": "kazkar",
            }
        )
        self.modules = {"kazkar": mock_module}
        self.orchestrator = Orchestrator(
            memory_store=self.memory,
            intent_classifier=self.clf,
            grok_engine=self.grok,
            modules=self.modules,
        )

    @pytest.mark.asyncio
    async def test_handle_request_returns_expected_shape(self):
        resp = await self.orchestrator.handle_request("Tell me a myth")
        assert set(resp.keys()) == {"intent", "source", "status", "result", "next_action"}

    @pytest.mark.asyncio
    async def test_handle_request_intent_field(self):
        resp = await self.orchestrator.handle_request("Tell me a myth")
        assert resp["intent"] == "kazkar"

    @pytest.mark.asyncio
    async def test_handle_request_unknown_intent(self):
        resp = await self.orchestrator.handle_request("gibberish xyz abc")
        assert resp["status"] == "⚠️"
        assert resp["source"] == "ci"

    @pytest.mark.asyncio
    async def test_handle_request_writes_to_memory(self):
        self.memory.clear()
        await self.orchestrator.handle_request("Tell me a myth")
        assert len(self.memory.read_last(10)) == 1

    def test_validate_defaults_status_to_fact(self):
        result = self.orchestrator.validate({"result": "x", "source": "s"})
        assert result["status"] == "fact"

    def test_validate_keeps_valid_status(self):
        for status in ("fact", "🔧", "🌀", "⚠️"):
            result = self.orchestrator.validate({"status": status})
            assert result["status"] == status

    def test_validate_replaces_invalid_status(self):
        result = self.orchestrator.validate({"status": "invalid"})
        assert result["status"] == "fact"


# ---------------------------------------------------------------------------
# 3. ActiveMemory — write / read_last / clear
# ---------------------------------------------------------------------------

class TestActiveMemory:
    def test_write_and_read_last(self):
        mem = ActiveMemory()
        mem.write({"a": 1})
        mem.write({"b": 2})
        last = mem.read_last(1)
        assert last == [{"b": 2}]

    def test_read_last_n(self):
        mem = ActiveMemory()
        for i in range(10):
            mem.write({"i": i})
        assert len(mem.read_last(5)) == 5

    def test_clear(self):
        mem = ActiveMemory()
        mem.write({"x": 1})
        mem.clear()
        assert mem.read_last() == []

    def test_read_last_empty(self):
        mem = ActiveMemory()
        assert mem.read_last() == []


# ---------------------------------------------------------------------------
# 4. LongTermMemory — write / read with temp dir
# ---------------------------------------------------------------------------

class TestLongTermMemory:
    def test_write_and_read(self, tmp_path):
        path = tmp_path / "memory.json"
        ltm = LongTermMemory(str(path))
        ltm.write("name", "Cimeika")
        assert ltm.read("name") == "Cimeika"

    def test_read_default(self, tmp_path):
        path = tmp_path / "memory.json"
        ltm = LongTermMemory(str(path))
        assert ltm.read("missing", default="fallback") == "fallback"

    def test_all(self, tmp_path):
        path = tmp_path / "memory.json"
        ltm = LongTermMemory(str(path))
        ltm.write("k1", "v1")
        ltm.write("k2", "v2")
        data = ltm.all()
        assert data == {"k1": "v1", "k2": "v2"}

    def test_overwrites_existing_key(self, tmp_path):
        path = tmp_path / "memory.json"
        ltm = LongTermMemory(str(path))
        ltm.write("key", "old")
        ltm.write("key", "new")
        assert ltm.read("key") == "new"


# ---------------------------------------------------------------------------
# 5. StructuralMemory — get invariants
# ---------------------------------------------------------------------------

class TestStructuralMemory:
    def test_get_ci_role(self):
        sm = StructuralMemory()
        assert sm.get("ci_role") == "global orchestrator and centre of Cimeika"

    def test_get_binary_logic(self):
        sm = StructuralMemory()
        bl = sm.get("binary_logic")
        assert bl["є"] is True
        assert bl["нема"] is False

    def test_get_module_registry(self):
        sm = StructuralMemory()
        registry = sm.get("module_registry")
        assert "kazkar" in registry
        assert len(registry) == 6

    def test_get_missing_key(self):
        sm = StructuralMemory()
        assert sm.get("nonexistent") is None

    def test_all_returns_dict(self):
        sm = StructuralMemory()
        all_inv = sm.all()
        assert isinstance(all_inv, dict)
        assert "response_contract" in all_inv


# ---------------------------------------------------------------------------
# 6. Module .process() with stub GrokEngine
# ---------------------------------------------------------------------------

class TestKazkarModule:
    @pytest.mark.asyncio
    async def test_process_symbol(self):
        module = KazkarModule()
        grok = GrokEngine()  # stub
        mem = ActiveMemory()
        result = await module.process("What does this symbol represent?", grok, mem)
        assert result["status"] == "fact"
        assert result["source"] == "kazkar"
        assert isinstance(result["result"], str)

    @pytest.mark.asyncio
    async def test_process_narrative(self):
        module = KazkarModule()
        grok = GrokEngine()  # stub
        mem = ActiveMemory()
        result = await module.process("Tell me a myth about the sea", grok, mem)
        assert result["status"] == "🌀"
        assert result["source"] == "kazkar"
        assert isinstance(result["result"], str)
