"""
Tests for the calendar sync worker (calendar_entries Google Calendar sync).
"""
import sys
import os
from datetime import datetime
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('ENVIRONMENT', 'test')
os.environ.setdefault('LOG_LEVEL', 'ERROR')
os.environ.setdefault('POSTGRES_HOST', 'localhost')

from app.modules.calendar.model import CalendarEntry
from app.modules.calendar.worker import (
    sync_pending_entries,
    cancel_entry,
    run_sync,
    SYNC_STATUS_PENDING,
    SYNC_STATUS_SYNCED,
    SYNC_STATUS_FAILED,
    SYNC_STATUS_CANCELLED,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _make_entry(entry_id: int, sync_status: str = 'pending', external_id=None) -> CalendarEntry:
    entry = CalendarEntry()
    entry.id = entry_id
    entry.title = f"Test event {entry_id}"
    entry.scheduled_at = datetime(2025, 6, 1, 10, 0, 0)
    entry.end_time = datetime(2025, 6, 1, 11, 0, 0)
    entry.description = "desc"
    entry.location = "Kyiv"
    entry.sync_status = sync_status
    entry.external_id = external_id
    entry.last_error = None
    return entry


# ---------------------------------------------------------------------------
# sync_pending_entries tests
# ---------------------------------------------------------------------------

def test_sync_pending_success():
    """Pending entry is synced: external_id set, sync_status=synced."""
    entry = _make_entry(1)
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = [entry]

    with patch(
        'app.modules.calendar.worker.create_google_event',
        return_value='google-event-id-123',
    ):
        result = sync_pending_entries(db)

    assert result == {'synced': 1, 'failed': 0}
    assert entry.sync_status == SYNC_STATUS_SYNCED
    assert entry.external_id == 'google-event-id-123'
    assert entry.last_error is None
    db.commit.assert_called()


def test_sync_pending_failure():
    """When Google API raises, sync_status=failed and last_error is set."""
    entry = _make_entry(2)
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = [entry]

    with patch(
        'app.modules.calendar.worker.create_google_event',
        side_effect=RuntimeError("API error"),
    ):
        result = sync_pending_entries(db)

    assert result == {'synced': 0, 'failed': 1}
    assert entry.sync_status == SYNC_STATUS_FAILED
    assert "API error" in entry.last_error
    db.rollback.assert_called()
    db.commit.assert_called()


def test_sync_no_pending():
    """No pending entries: returns zeros."""
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = []

    result = sync_pending_entries(db)

    assert result == {'synced': 0, 'failed': 0}


def test_sync_multiple_entries():
    """Multiple pending entries: each processed independently."""
    entries = [_make_entry(i) for i in range(1, 4)]
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = entries

    call_count = [0]

    def fake_create(**kwargs):
        call_count[0] += 1
        if call_count[0] == 2:
            raise RuntimeError("transient error")
        return f"google-event-{call_count[0]}"

    with patch('app.modules.calendar.worker.create_google_event', side_effect=fake_create):
        result = sync_pending_entries(db)

    assert result == {'synced': 2, 'failed': 1}
    assert entries[0].sync_status == SYNC_STATUS_SYNCED
    assert entries[1].sync_status == SYNC_STATUS_FAILED
    assert entries[2].sync_status == SYNC_STATUS_SYNCED


# ---------------------------------------------------------------------------
# cancel_entry tests
# ---------------------------------------------------------------------------

def test_cancel_entry_with_external_id():
    """cancel_entry deletes Google event and sets sync_status=cancelled."""
    entry = _make_entry(10, sync_status='synced', external_id='g-event-abc')
    db = MagicMock()

    with patch('app.modules.calendar.worker.delete_google_event') as mock_delete:
        cancel_entry(db, entry)

    mock_delete.assert_called_once_with('g-event-abc')
    assert entry.sync_status == SYNC_STATUS_CANCELLED
    db.commit.assert_called_once()


def test_cancel_entry_without_external_id():
    """cancel_entry for pending entry (no external_id): no Google delete call."""
    entry = _make_entry(11, sync_status='pending', external_id=None)
    db = MagicMock()

    with patch('app.modules.calendar.worker.delete_google_event') as mock_delete:
        cancel_entry(db, entry)

    mock_delete.assert_not_called()
    assert entry.sync_status == SYNC_STATUS_CANCELLED


def test_cancel_entry_google_delete_error_does_not_raise():
    """If Google delete fails, cancel_entry still sets sync_status=cancelled."""
    entry = _make_entry(12, sync_status='synced', external_id='g-event-xyz')
    db = MagicMock()

    with patch(
        'app.modules.calendar.worker.delete_google_event',
        side_effect=RuntimeError("network error"),
    ):
        cancel_entry(db, entry)  # Should not raise

    assert entry.sync_status == SYNC_STATUS_CANCELLED


# ---------------------------------------------------------------------------
# run_sync tests
# ---------------------------------------------------------------------------

def test_run_sync_delegates_to_sync_pending():
    """run_sync returns result from sync_pending_entries."""
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = []

    result = run_sync(db)

    assert result == {'synced': 0, 'failed': 0}
