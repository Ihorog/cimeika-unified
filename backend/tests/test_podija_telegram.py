"""
Tests for the Podija MVP parser and extended PodijaService methods.
"""
import sys
import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["ENVIRONMENT"] = "test"
os.environ["LOG_LEVEL"] = "ERROR"
os.environ["POSTGRES_HOST"] = "localhost"

from app.modules.podija.parser import parse_add_args, parse_date, parse_time  # noqa: E402

# ---------------------------------------------------------------------------
# parse_date tests
# ---------------------------------------------------------------------------

_NOW = datetime(2026, 3, 10, 12, 0, 0)  # fixed reference


def test_parse_date_today():
    result = parse_date("сьогодні", now=_NOW)
    assert result == datetime(2026, 3, 10, 0, 0, 0)


def test_parse_date_tomorrow():
    result = parse_date("завтра", now=_NOW)
    assert result == datetime(2026, 3, 11, 0, 0, 0)


def test_parse_date_day_after_tomorrow():
    result = parse_date("послязавтра", now=_NOW)
    assert result == datetime(2026, 3, 12, 0, 0, 0)


def test_parse_date_iso():
    result = parse_date("2026-03-01", now=_NOW)
    assert result == datetime(2026, 3, 1, 0, 0, 0)


def test_parse_date_dot_format():
    result = parse_date("01.03.2026", now=_NOW)
    assert result == datetime(2026, 3, 1, 0, 0, 0)


def test_parse_date_invalid():
    assert parse_date("not-a-date", now=_NOW) is None
    assert parse_date("2026-13-01", now=_NOW) is None
    assert parse_date("32.01.2026", now=_NOW) is None


# ---------------------------------------------------------------------------
# parse_time tests
# ---------------------------------------------------------------------------

def test_parse_time_valid():
    assert parse_time("18:00") == (18, 0)
    assert parse_time("09:30") == (9, 30)
    assert parse_time("0:00") == (0, 0)
    assert parse_time("23:59") == (23, 59)


def test_parse_time_invalid():
    assert parse_time("25:00") is None
    assert parse_time("18:60") is None
    assert parse_time("abc") is None
    assert parse_time("") is None


# ---------------------------------------------------------------------------
# parse_add_args tests
# ---------------------------------------------------------------------------

def test_parse_add_args_basic():
    result = parse_add_args("завтра 18:00 зустріч", now=_NOW)
    assert result["error"] is None
    assert result["title"] == "зустріч"
    assert result["event_date"] == datetime(2026, 3, 11, 18, 0, 0)
    assert result["duration_minutes"] is None


def test_parse_add_args_with_duration():
    result = parse_add_args("2026-03-01 18:00 зустріч 60", now=_NOW)
    assert result["error"] is None
    assert result["title"] == "зустріч"
    assert result["event_date"] == datetime(2026, 3, 1, 18, 0, 0)
    assert result["duration_minutes"] == 60


def test_parse_add_args_multiword_title():
    result = parse_add_args("завтра 09:30 зустріч з командою", now=_NOW)
    assert result["error"] is None
    assert result["title"] == "зустріч з командою"
    assert result["duration_minutes"] is None


def test_parse_add_args_multiword_title_with_duration():
    result = parse_add_args("завтра 09:30 зустріч з командою 45", now=_NOW)
    assert result["error"] is None
    assert result["title"] == "зустріч з командою"
    assert result["duration_minutes"] == 45


def test_parse_add_args_too_few_args():
    result = parse_add_args("завтра 18:00", now=_NOW)
    assert result["error"] is not None


def test_parse_add_args_bad_date():
    result = parse_add_args("notadate 18:00 title", now=_NOW)
    assert result["error"] is not None
    assert "дату" in result["error"]


def test_parse_add_args_bad_time():
    result = parse_add_args("завтра 99:99 title", now=_NOW)
    assert result["error"] is not None
    assert "час" in result["error"]


def test_parse_add_args_empty():
    result = parse_add_args("", now=_NOW)
    assert result["error"] is not None


# ---------------------------------------------------------------------------
# PodijaService extended methods (unit tests with mocked DB)
# ---------------------------------------------------------------------------

from app.modules.podija.service import PodijaService  # noqa: E402
from app.modules.podija.model import PodijaEvent  # noqa: E402


def _make_event(id_: int, title: str, event_date: datetime, is_completed: bool = False):
    ev = PodijaEvent()
    ev.id = id_
    ev.title = title
    ev.event_date = event_date
    ev.is_completed = is_completed
    ev.status = 'planned'
    return ev


def test_mark_done_sets_completed():
    svc = PodijaService()
    svc.initialize()

    now = datetime.utcnow()
    event = _make_event(1, "test", now)

    db = MagicMock()
    # get_event will be called inside mark_done
    with patch.object(svc, "get_event", return_value=event):
        result = svc.mark_done(db, 1)

    assert result is not None
    assert result.is_completed is True
    db.commit.assert_called_once()


def test_mark_done_not_found():
    svc = PodijaService()
    svc.initialize()

    db = MagicMock()
    with patch.object(svc, "get_event", return_value=None):
        result = svc.mark_done(db, 999)

    assert result is None


def test_get_today_events_calls_db():
    svc = PodijaService()
    svc.initialize()

    db = MagicMock()
    mock_query = MagicMock()
    db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.all.return_value = []

    result = svc.get_today_events(db)

    assert result == []
    db.query.assert_called_once_with(PodijaEvent)


def test_get_week_events_calls_db():
    svc = PodijaService()
    svc.initialize()

    db = MagicMock()
    mock_query = MagicMock()
    db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.all.return_value = []

    result = svc.get_week_events(db)

    assert result == []
    db.query.assert_called_once_with(PodijaEvent)
