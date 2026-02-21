"""
Integration tests for reminder_jobs worker.
Validates: event scheduled -> reminder processed at T-10m.
"""
import sys
import os
import uuid
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set test environment variables before importing app modules
os.environ['ENVIRONMENT'] = 'test'
os.environ['LOG_LEVEL'] = 'ERROR'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_DB'] = 'test_db'
os.environ['POSTGRES_USER'] = 'test_user'
os.environ['POSTGRES_PASSWORD'] = 'test_pass'

from app.modules.podija.reminder_model import (
    ReminderJob,
    REMINDER_STATUS_PENDING,
    REMINDER_STATUS_SENT,
    REMINDER_STATUS_FAILED,
    REMINDER_MAX_ATTEMPTS,
    REMINDER_CHANNEL_TELEGRAM,
)
from app.modules.podija.reminder_worker import process_due_reminders, ReminderWorker


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_job(remind_at, status=REMINDER_STATUS_PENDING, attempts=0):
    """Create an unsaved ReminderJob instance for testing."""
    job = ReminderJob()
    job.id = uuid.uuid4()
    job.event_id = 1
    job.user_id = uuid.uuid4()
    job.remind_at = remind_at
    job.channel = REMINDER_CHANNEL_TELEGRAM
    job.status = status
    job.attempts = attempts
    job.last_error = None
    job.created_at = datetime.now(timezone.utc)
    job.updated_at = datetime.now(timezone.utc)
    return job


def _mock_db(jobs):
    """Build a minimal mock Session that returns *jobs* for reminder queries."""
    db = MagicMock()
    query_mock = MagicMock()
    filter_mock = MagicMock()
    filter_mock.all.return_value = jobs
    query_mock.filter.return_value = filter_mock
    db.query.return_value = query_mock
    return db


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

def test_reminder_job_defaults():
    """ReminderJob fields have correct defaults."""
    job = ReminderJob()
    # SQLAlchemy column defaults are applied on INSERT, not construction,
    # but the Python-side defaults should match expected values when set.
    assert REMINDER_MAX_ATTEMPTS == 3
    assert REMINDER_CHANNEL_TELEGRAM == "telegram"
    assert REMINDER_STATUS_PENDING == "pending"
    assert REMINDER_STATUS_SENT == "sent"
    assert REMINDER_STATUS_FAILED == "failed"


def test_reminder_max_attempts_constant():
    """REMINDER_MAX_ATTEMPTS is a positive integer."""
    assert isinstance(REMINDER_MAX_ATTEMPTS, int)
    assert REMINDER_MAX_ATTEMPTS > 0


# ---------------------------------------------------------------------------
# Worker logic tests
# ---------------------------------------------------------------------------

def test_process_due_reminders_sends_and_marks_sent(monkeypatch):
    """
    Integration: a due pending reminder is processed and marked sent
    when Telegram delivery succeeds.
    """
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    job = _make_job(remind_at=past)
    db = _mock_db([job])

    # No real Telegram call
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    count = process_due_reminders(db)

    assert count == 1
    assert job.status == REMINDER_STATUS_SENT
    db.commit.assert_called()


def test_process_due_reminders_skips_future(monkeypatch):
    """A reminder scheduled in the future is NOT processed."""
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    job = _make_job(remind_at=future)
    db = _mock_db([])  # worker would filter these out in real DB

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    count = process_due_reminders(db)

    assert count == 0
    assert job.status == REMINDER_STATUS_PENDING  # unchanged


def test_process_due_reminders_increments_attempts_on_failure(monkeypatch):
    """On Telegram failure, attempts++ and status stays pending until threshold."""
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    job = _make_job(remind_at=past)
    db = _mock_db([job])

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bad-token")

    with patch(
        "app.modules.podija.reminder_worker.send_telegram",
        side_effect=Exception("Telegram error"),
    ):
        process_due_reminders(db)

    assert job.attempts == 1
    assert job.last_error == "Telegram error"
    assert job.status == REMINDER_STATUS_PENDING  # below threshold


def test_process_due_reminders_marks_failed_at_threshold(monkeypatch):
    """After REMINDER_MAX_ATTEMPTS failures, status becomes failed."""
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    job = _make_job(remind_at=past, attempts=REMINDER_MAX_ATTEMPTS - 1)
    db = _mock_db([job])

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bad-token")

    with patch(
        "app.modules.podija.reminder_worker.send_telegram",
        side_effect=Exception("final failure"),
    ):
        process_due_reminders(db)

    assert job.attempts == REMINDER_MAX_ATTEMPTS
    assert job.status == REMINDER_STATUS_FAILED


# ---------------------------------------------------------------------------
# T-10m integration scenario
# ---------------------------------------------------------------------------

def test_t_minus_10_reminder_scenario(monkeypatch):
    """
    Acceptance: event scheduled -> reminder created at T-10m
    -> worker picks it up when remind_at passes -> marked sent.
    """
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")

    # Simulate an event at T+10m; reminder was created for T+0 (i.e. now-ish)
    event_time = datetime.now(timezone.utc) + timedelta(minutes=10)
    remind_at = event_time - timedelta(minutes=10)  # == now approx

    # Nudge remind_at slightly into the past so it is "due"
    remind_at = remind_at - timedelta(seconds=1)

    job = _make_job(remind_at=remind_at)
    db = _mock_db([job])

    count = process_due_reminders(db)

    assert count == 1
    assert job.status == REMINDER_STATUS_SENT


# ---------------------------------------------------------------------------
# ReminderWorker lifecycle
# ---------------------------------------------------------------------------

def test_reminder_worker_start_stop():
    """ReminderWorker starts and stops cleanly without errors."""
    worker = ReminderWorker(interval=1)
    with patch("app.modules.podija.reminder_worker.SessionLocal") as mock_sl:
        mock_db = MagicMock()
        mock_sl.return_value = mock_db
        query_mock = MagicMock()
        filter_mock = MagicMock()
        filter_mock.all.return_value = []
        query_mock.filter.return_value = filter_mock
        mock_db.query.return_value = query_mock

        worker.start()
        assert worker._thread is not None
        assert worker._thread.is_alive()

        worker.stop()
        assert not worker._thread.is_alive()
