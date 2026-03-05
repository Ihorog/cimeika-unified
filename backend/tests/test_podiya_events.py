"""
Tests for ПоДія (podiya) event API endpoints:
- POST   /api/v1/podiya/events
- GET    /api/v1/podiya/events?range=today|week
- PATCH  /api/v1/podiya/events/{id}
- POST   /api/v1/podiya/events/{id}/done
- POST   /api/v1/podiya/events/{id}/cancel
- GET    /api/v1/health
- GET    /api/v1/status
"""
import sys
import os
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment before importing app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('ENVIRONMENT', 'test')
os.environ.setdefault('LOG_LEVEL', 'ERROR')
os.environ.setdefault('POSTGRES_HOST', 'localhost')
os.environ.setdefault('POSTGRES_DB', 'test_db')
os.environ.setdefault('POSTGRES_USER', 'test_user')
os.environ.setdefault('POSTGRES_PASSWORD', 'test_pass')

from app.config.database import Base, get_db
from main import app

# ── In-memory SQLite for tests ────────────────────────────────────────────────
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    """Drop and recreate tables before each test for isolation."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# ── Helpers ───────────────────────────────────────────────────────────────────
def _create_event(title="Test ПоДія", event_date=None):
    payload = {
        "title": title,
        "description": "Test description",
        "event_date": event_date or (datetime.utcnow() + timedelta(hours=1)).isoformat(),
    }
    return client.post("/api/v1/podiya/events", json=payload)


# ── POST /events ───────────────────────────────────────────────────────────────
def test_create_event_returns_201():
    resp = _create_event()
    assert resp.status_code == 201


def test_create_event_returns_correct_payload():
    resp = _create_event("Моя ПоДія")
    data = resp.json()
    assert data["title"] == "Моя ПоДія"
    assert data["status"] == "planned"
    assert data["module"] == "podija"
    assert "id" in data


def test_create_event_has_no_google_event_id():
    resp = _create_event()
    data = resp.json()
    assert "google_event_id" not in data


# ── GET /events ────────────────────────────────────────────────────────────────
def test_list_events_empty():
    resp = client.get("/api/v1/podiya/events")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_events_returns_created():
    _create_event("First")
    _create_event("Second")
    resp = client.get("/api/v1/podiya/events")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_list_events_range_today():
    # Create one event today and one in the future (next week)
    today = datetime.utcnow().replace(hour=12, minute=0, second=0, microsecond=0)
    next_week = today + timedelta(days=8)
    _create_event("Today Event", today.isoformat())
    _create_event("Next Week Event", next_week.isoformat())

    resp = client.get("/api/v1/podiya/events?range=today")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Today Event"


def test_list_events_range_week():
    today = datetime.utcnow().replace(hour=12, minute=0, second=0, microsecond=0)
    in_three_days = today + timedelta(days=3)
    next_month = today + timedelta(days=30)
    _create_event("This Week", in_three_days.isoformat())
    _create_event("Next Month", next_month.isoformat())

    resp = client.get("/api/v1/podiya/events?range=week")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "This Week"


def test_list_events_invalid_range_returns_400():
    resp = client.get("/api/v1/podiya/events?range=month")
    assert resp.status_code == 400


# ── PATCH /events/{id} ─────────────────────────────────────────────────────────
def test_patch_event_updates_title():
    event_id = _create_event().json()["id"]
    resp = client.patch(f"/api/v1/podiya/events/{event_id}", json={"title": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated"


def test_patch_event_not_found():
    resp = client.patch("/api/v1/podiya/events/9999", json={"title": "X"})
    assert resp.status_code == 404


def test_patch_invalid_status_transition():
    event_id = _create_event().json()["id"]
    # First mark done
    client.post(f"/api/v1/podiya/events/{event_id}/done")
    # Now try to transition done → cancelled via PATCH (should fail)
    resp = client.patch(f"/api/v1/podiya/events/{event_id}", json={"status": "cancelled"})
    assert resp.status_code == 422


# ── POST /events/{id}/done ─────────────────────────────────────────────────────
def test_mark_done_sets_status():
    event_id = _create_event().json()["id"]
    resp = client.post(f"/api/v1/podiya/events/{event_id}/done")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "done"
    assert data["is_completed"] is True


def test_mark_done_not_found():
    resp = client.post("/api/v1/podiya/events/9999/done")
    assert resp.status_code == 404


def test_mark_done_twice_returns_422():
    event_id = _create_event().json()["id"]
    client.post(f"/api/v1/podiya/events/{event_id}/done")
    resp = client.post(f"/api/v1/podiya/events/{event_id}/done")
    assert resp.status_code == 422


# ── POST /events/{id}/cancel ───────────────────────────────────────────────────
def test_cancel_event_sets_status():
    event_id = _create_event().json()["id"]
    resp = client.post(f"/api/v1/podiya/events/{event_id}/cancel")
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


def test_cancel_not_found():
    resp = client.post("/api/v1/podiya/events/9999/cancel")
    assert resp.status_code == 404


def test_cancel_done_event_returns_422():
    event_id = _create_event().json()["id"]
    client.post(f"/api/v1/podiya/events/{event_id}/done")
    resp = client.post(f"/api/v1/podiya/events/{event_id}/cancel")
    assert resp.status_code == 422


# ── GET /api/v1/health ─────────────────────────────────────────────────────────
def test_v1_health_returns_200():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200


def test_v1_health_has_status_ok():
    resp = client.get("/api/v1/health")
    data = resp.json()
    assert data["status"] == "ok"
    assert "version" in data


# ── GET /api/v1/status ─────────────────────────────────────────────────────────
def test_v1_status_returns_200():
    resp = client.get("/api/v1/status")
    assert resp.status_code == 200


def test_v1_status_has_required_fields():
    resp = client.get("/api/v1/status")
    data = resp.json()
    assert "status" in data
    assert "version" in data
    assert data["status"] == "running"
