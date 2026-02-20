"""
Tests for Stabilizer module
"""
import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set test environment variables before importing app
os.environ['ENVIRONMENT'] = 'test'
os.environ['LOG_LEVEL'] = 'ERROR'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_DB'] = 'test_db'
os.environ['POSTGRES_USER'] = 'test_user'
os.environ['POSTGRES_PASSWORD'] = 'test_pass'

from main import app

client = TestClient(app)


def test_stabilize_no_auth():
    resp = client.post("/stabilizer/stabilize", json={"draft": "test"})
    assert resp.status_code == 403


def test_stabilize_with_auth(monkeypatch):
    monkeypatch.setenv("CI_ADMIN_KEY", "test-key")
    resp = client.post(
        "/stabilizer/stabilize",
        json={"draft": "a" * 3000, "mode": "normal"},
        headers={"X-CI-Key": "test-key"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["final"]) <= 2000
    assert "char_limit" in data["report"]["cut_flags"]


def test_critical_mode_clarification(monkeypatch):
    monkeypatch.setenv("CI_ADMIN_KEY", "test-key")
    draft = "Option A: do X\nOption B: do Y\nOption C: do Z\n" * 3
    resp = client.post(
        "/stabilizer/stabilize",
        json={"intent": "", "draft": draft, "mode": "critical"},
        headers={"X-CI-Key": "test-key"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "?" in data["final"]
    assert "critical_clarification" in data["report"]["cut_flags"]


def test_axis_activation(monkeypatch):
    monkeypatch.setenv("CI_ADMIN_KEY", "test-key")
    resp = client.post(
        "/stabilizer/axis/activate",
        json={"profile": "strict"},
        headers={"X-CI-Key": "test-key"}
    )
    assert resp.status_code == 200
    assert resp.json()["active_profile"] == "strict"


def test_determinism(monkeypatch):
    monkeypatch.setenv("CI_ADMIN_KEY", "test-key")
    payload = {"draft": "Same input text", "mode": "normal"}
    resp1 = client.post("/stabilizer/stabilize", json=payload, headers={"X-CI-Key": "test-key"})
    resp2 = client.post("/stabilizer/stabilize", json=payload, headers={"X-CI-Key": "test-key"})
    assert resp1.json()["final"] == resp2.json()["final"]
    assert resp1.json()["report"]["deterministic_score"] == resp2.json()["report"]["deterministic_score"]


def test_profile_code(monkeypatch):
    monkeypatch.setenv("CI_ADMIN_KEY", "test-key")
    # Activate code profile
    client.post("/stabilizer/axis/activate", json={"profile": "code"}, headers={"X-CI-Key": "test-key"})

    resp = client.post(
        "/stabilizer/stabilize",
        json={"draft": "a" * 5000, "mode": "normal"},
        headers={"X-CI-Key": "test-key"}
    )
    assert resp.status_code == 200
    # Code profile allows 4000 chars in normal mode
    assert len(resp.json()["final"]) <= 4000


def test_profile_chat(monkeypatch):
    monkeypatch.setenv("CI_ADMIN_KEY", "test-key")
    client.post("/stabilizer/axis/activate", json={"profile": "chat"}, headers={"X-CI-Key": "test-key"})

    resp = client.post(
        "/stabilizer/stabilize",
        json={"draft": "a" * 2000, "mode": "normal"},
        headers={"X-CI-Key": "test-key"}
    )
    assert resp.status_code == 200
    # Chat profile allows 1500 chars in normal mode
    assert len(resp.json()["final"]) <= 1500
