"""
Podija MVP date/time parser
Parses command arguments for /add: <date> <time> <title> [duration_minutes]

Supported date formats:
  - Ukrainian words: сьогодні, сегодня, завтра, послязавтра
  - ISO date: YYYY-MM-DD
  - DD.MM.YYYY

Supported time format: HH:MM
"""
import re
from datetime import datetime, timedelta
from typing import Optional, Tuple


UKRAINIAN_DATES = {
    "сьогодні": 0,
    "сегодня": 0,
    "завтра": 1,
    "послязавтра": 2,
}


def parse_date(token: str, now: Optional[datetime] = None) -> Optional[datetime]:
    """
    Parse a date token.

    Returns a date-only datetime (time set to 00:00).
    Returns None if the token cannot be parsed.
    """
    if now is None:
        now = datetime.utcnow()

    token_lower = token.lower().strip()

    # Ukrainian / natural language
    if token_lower in UKRAINIAN_DATES:
        return (now + timedelta(days=UKRAINIAN_DATES[token_lower])).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    # ISO format: YYYY-MM-DD
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", token_lower)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None

    # DD.MM.YYYY
    m = re.fullmatch(r"(\d{2})\.(\d{2})\.(\d{4})", token_lower)
    if m:
        try:
            return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            return None

    return None


def parse_time(token: str) -> Optional[Tuple[int, int]]:
    """
    Parse a time token in HH:MM format.

    Returns (hour, minute) tuple or None.
    """
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", token.strip())
    if m:
        hour, minute = int(m.group(1)), int(m.group(2))
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return hour, minute
    return None


def parse_add_args(args: str, now: Optional[datetime] = None) -> dict:
    """
    Parse arguments for the /add command.

    Expected format:
        <date> <time> <title> [duration_minutes]

    Examples:
        завтра 18:00 зустріч
        2026-03-01 18:00 зустріч 60
        сьогодні 09:30 standup 15

    Returns a dict with keys:
        event_date (datetime), title (str), duration_minutes (int|None),
        error (str|None)
    """
    if now is None:
        now = datetime.utcnow()

    tokens = args.strip().split(None, 2)  # date, time, rest (title + optional duration)
    if len(tokens) < 3:
        return {
            "event_date": None,
            "title": None,
            "duration_minutes": None,
            "error": (
                "Недостатньо аргументів. "
                "Формат: /add <дата> <час> <назва> [тривалість_хв]\n"
                "Приклад: /add завтра 18:00 зустріч 60"
            ),
        }

    date_token, time_token = tokens[0], tokens[1]
    rest = tokens[2]  # title + optional duration

    date = parse_date(date_token, now)
    if date is None:
        return {
            "event_date": None,
            "title": None,
            "duration_minutes": None,
            "error": f"Не вдалося розпізнати дату: «{date_token}»",
        }

    time_parts = parse_time(time_token)
    if time_parts is None:
        return {
            "event_date": None,
            "title": None,
            "duration_minutes": None,
            "error": f"Не вдалося розпізнати час: «{time_token}» (очікується ГГ:ХХ)",
        }

    event_dt = date.replace(hour=time_parts[0], minute=time_parts[1], second=0, microsecond=0)

    # Split rest into title and optional trailing integer (duration)
    rest_tokens = rest.rsplit(None, 1)
    duration_minutes = None
    if len(rest_tokens) == 2 and rest_tokens[1].isdigit():
        duration_minutes = int(rest_tokens[1])
        title = rest_tokens[0].strip()
    else:
        title = rest.strip()

    if not title:
        return {
            "event_date": None,
            "title": None,
            "duration_minutes": None,
            "error": "Назва події не може бути порожньою.",
        }

    return {
        "event_date": event_dt,
        "title": title,
        "duration_minutes": duration_minutes,
        "error": None,
    }
