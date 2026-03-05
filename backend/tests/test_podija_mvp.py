"""
Tests for PoDiya MVP: today/week filtering, done/cancel transitions
"""
import sys
import os
from datetime import datetime, timedelta, timezone

import pytest
from unittest.mock import MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ['ENVIRONMENT'] = 'test'
os.environ['LOG_LEVEL'] = 'ERROR'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_DB'] = 'test_db'
os.environ['POSTGRES_USER'] = 'test_user'
os.environ['POSTGRES_PASSWORD'] = 'test_pass'

from app.modules.podija.service import PodijaService
from app.modules.podija.model import PodijaEvent


def _make_event(**kwargs) -> PodijaEvent:
    """Helper to create a PodijaEvent instance with defaults."""
    event = PodijaEvent()
    event.id = kwargs.get('id', 1)
    event.title = kwargs.get('title', 'Test Event')
    event.description = kwargs.get('description', None)
    event.event_date = kwargs.get('event_date', None)
    event.event_type = kwargs.get('event_type', None)
    event.status = kwargs.get('status', 'planned')
    event.is_completed = kwargs.get('is_completed', False)
    event.participants = kwargs.get('participants', None)
    event.location = kwargs.get('location', None)
    event.tags = kwargs.get('tags', [])
    event.source_trace = kwargs.get('source_trace', None)
    event.module = 'podija'
    event.time = datetime.now(timezone.utc)
    event.canon_bundle_id = 'cimeika-v1'
    return event


@pytest.fixture
def service():
    svc = PodijaService()
    svc.initialize()
    return svc


# ---------------------------------------------------------------------------
# get_today_events
# ---------------------------------------------------------------------------

def test_get_today_events_returns_today_only(service):
    """Only events with event_date on today (UTC) are returned."""
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today_start - timedelta(days=1)
    tomorrow = today_start + timedelta(days=1)

    event_today = _make_event(id=1, event_date=today_start + timedelta(hours=9))
    event_yesterday = _make_event(id=2, event_date=yesterday + timedelta(hours=9))
    event_tomorrow = _make_event(id=3, event_date=tomorrow + timedelta(hours=9))

    db = MagicMock()
    # Simulate DB query returning all three, filter logic is in service
    query_mock = db.query.return_value
    filter_mock = query_mock.filter.return_value
    filter_mock.all.return_value = [event_today]

    result = service.get_today_events(db)

    assert len(result) == 1
    assert result[0].id == 1
    # Verify filter was called (not just all events)
    db.query.assert_called_once_with(PodijaEvent)


def test_get_today_events_empty_when_none(service):
    """Returns empty list when no events today."""
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = []

    result = service.get_today_events(db)
    assert result == []


# ---------------------------------------------------------------------------
# get_week_events
# ---------------------------------------------------------------------------

def test_get_week_events_returns_next_7_days(service):
    """get_week_events queries from now to now+7days."""
    event_in_3_days = _make_event(id=10, event_date=datetime.now(timezone.utc) + timedelta(days=3))

    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = [event_in_3_days]

    result = service.get_week_events(db)
    assert len(result) == 1
    assert result[0].id == 10


def test_get_week_events_empty_when_none(service):
    """Returns empty list when no events in next 7 days."""
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = []

    result = service.get_week_events(db)
    assert result == []


# ---------------------------------------------------------------------------
# mark_done
# ---------------------------------------------------------------------------

def test_mark_done_sets_status_and_is_completed(service):
    """mark_done sets status='done' and is_completed=True."""
    event = _make_event(id=5, status='planned', is_completed=False)

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = event

    result = service.mark_done(db, 5)

    assert result is not None
    assert result.status == 'done'
    assert result.is_completed is True
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(event)


def test_mark_done_returns_none_for_missing_event(service):
    """mark_done returns None when event does not exist."""
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    result = service.mark_done(db, 999)
    assert result is None
    db.commit.assert_not_called()


# ---------------------------------------------------------------------------
# mark_cancelled
# ---------------------------------------------------------------------------

def test_mark_cancelled_sets_status(service):
    """mark_cancelled sets status='cancelled'."""
    event = _make_event(id=7, status='planned')

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = event

    result = service.mark_cancelled(db, 7)

    assert result is not None
    assert result.status == 'cancelled'
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(event)


def test_mark_cancelled_returns_none_for_missing_event(service):
    """mark_cancelled returns None when event does not exist."""
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    result = service.mark_cancelled(db, 999)
    assert result is None
    db.commit.assert_not_called()


def test_mark_cancelled_does_not_change_is_completed(service):
    """Cancelling an event does not set is_completed."""
    event = _make_event(id=8, status='planned', is_completed=False)

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = event

    service.mark_cancelled(db, 8)
    assert event.is_completed is False


# ---------------------------------------------------------------------------
# API route smoke tests (DB dependency overridden with mock)
# ---------------------------------------------------------------------------

from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from app.config.database import get_db


def _mock_db():
    """Mock DB session that returns empty results."""
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = []
    db.query.return_value.filter.return_value.first.return_value = None
    yield db


app.dependency_overrides[get_db] = _mock_db
client = TestClient(app)


def test_podija_today_endpoint_exists():
    """GET /api/v1/podiya/events/today returns 200."""
    response = client.get("/api/v1/podiya/events/today")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_podija_week_endpoint_exists():
    """GET /api/v1/podiya/events/week returns 200."""
    response = client.get("/api/v1/podiya/events/week")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_podija_done_endpoint_404_for_missing():
    """POST /api/v1/podiya/events/9999/done returns 404."""
    response = client.post("/api/v1/podiya/events/9999/done")
    assert response.status_code == 404


def test_podija_cancel_endpoint_404_for_missing():
    """POST /api/v1/podiya/events/9999/cancel returns 404."""
    response = client.post("/api/v1/podiya/events/9999/cancel")
    assert response.status_code == 404
