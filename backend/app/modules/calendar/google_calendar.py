"""
Google Calendar integration service for CIMEIKA Calendar module.
Uses a Google service account to create and delete Calendar events.

Required ENV:
    GOOGLE_CLIENT_EMAIL  - service account email
    GOOGLE_PRIVATE_KEY   - service account private key (PEM, newlines as \\n)
    GOOGLE_CALENDAR_ID   - target Google Calendar id
"""
import os
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


def _build_service():
    """Build and return an authenticated Google Calendar API service."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise RuntimeError(
            "google-api-python-client and google-auth are required. "
            "Install them via: pip install google-api-python-client google-auth"
        ) from exc

    client_email = os.environ.get("GOOGLE_CLIENT_EMAIL", "")
    private_key = os.environ.get("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n")

    if not client_email or not private_key:
        raise ValueError(
            "GOOGLE_CLIENT_EMAIL and GOOGLE_PRIVATE_KEY must be set in the environment."
        )

    credentials = service_account.Credentials.from_service_account_info(
        {
            "type": "service_account",
            "client_email": client_email,
            "private_key": private_key,
            "token_uri": "https://oauth2.googleapis.com/token",
        },
        scopes=["https://www.googleapis.com/auth/calendar"],
    )
    return build("calendar", "v3", credentials=credentials, cache_discovery=False)


def _calendar_id() -> str:
    cal_id = os.environ.get("GOOGLE_CALENDAR_ID", "")
    if not cal_id:
        raise ValueError("GOOGLE_CALENDAR_ID must be set in the environment.")
    return cal_id


def _to_rfc3339(dt: datetime) -> str:
    """Return RFC 3339 string; add UTC timezone if naive."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def create_google_event(
    title: str,
    scheduled_at: datetime,
    end_time: Optional[datetime] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
) -> str:
    """
    Create a Google Calendar event via service account.

    Returns the created event's Google Calendar event id (external_id).
    """
    service = _build_service()
    cal_id = _calendar_id()

    start = _to_rfc3339(scheduled_at)
    # Default duration: 1 hour if end_time not provided
    if end_time is None:
        from datetime import timedelta
        end_time = scheduled_at + timedelta(hours=1)
    end = _to_rfc3339(end_time)

    body = {
        "summary": title,
        "start": {"dateTime": start},
        "end": {"dateTime": end},
    }
    if description:
        body["description"] = description
    if location:
        body["location"] = location

    event = service.events().insert(calendarId=cal_id, body=body).execute()
    event_id: str = event["id"]
    logger.info("Created Google Calendar event id=%s for title='%s'", event_id, title)
    return event_id


def delete_google_event(external_id: str) -> None:
    """
    Delete a Google Calendar event by its external_id.
    Silently ignores 404 (already deleted / not found).
    """
    from googleapiclient.errors import HttpError

    service = _build_service()
    cal_id = _calendar_id()

    try:
        service.events().delete(calendarId=cal_id, eventId=external_id).execute()
        logger.info("Deleted Google Calendar event id=%s", external_id)
    except HttpError as exc:
        if exc.resp.status == 404:
            logger.warning(
                "Google Calendar event id=%s not found (already deleted?)", external_id
            )
        else:
            raise
