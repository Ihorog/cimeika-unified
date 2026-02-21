"""
Calendar sync worker for CIMEIKA.

Picks up calendar_entries with sync_status='pending' and pushes them
to Google Calendar via a service account.

Flow:
    pending  →  create Google event  →  external_id set, sync_status='synced'
    pending  →  error                →  sync_status='failed', last_error set
    cancelled (podija_events) → delete Google event (MVP)

Usage (run once / on a schedule):
    from app.modules.calendar.worker import run_sync
    run_sync(db)
"""
import logging
from sqlalchemy.orm import Session

from app.modules.calendar.model import CalendarEntry
from app.modules.calendar.google_calendar import create_google_event, delete_google_event

logger = logging.getLogger(__name__)

SYNC_STATUS_PENDING = "pending"
SYNC_STATUS_SYNCED = "synced"
SYNC_STATUS_FAILED = "failed"
SYNC_STATUS_CANCELLED = "cancelled"


def sync_pending_entries(db: Session) -> dict:
    """
    Process all calendar_entries with sync_status='pending'.

    For each pending entry:
      - Creates a Google Calendar event.
      - On success: sets external_id + sync_status='synced'.
      - On failure: sets sync_status='failed' + last_error.

    Returns a summary dict with counts of synced and failed entries.
    """
    pending = (
        db.query(CalendarEntry)
        .filter(CalendarEntry.sync_status == SYNC_STATUS_PENDING)
        .all()
    )

    synced_count = 0
    failed_count = 0

    for entry in pending:
        try:
            external_id = create_google_event(
                title=entry.title,
                scheduled_at=entry.scheduled_at,
                end_time=entry.end_time,
                description=entry.description,
                location=entry.location,
            )
            entry.external_id = external_id
            entry.sync_status = SYNC_STATUS_SYNCED
            entry.last_error = None
            db.commit()
            synced_count += 1
            logger.info(
                "Synced calendar_entry id=%d to Google event id=%s",
                entry.id,
                external_id,
            )
        except Exception as exc:
            db.rollback()
            error_msg = str(exc)
            entry.sync_status = SYNC_STATUS_FAILED
            entry.last_error = error_msg
            db.commit()
            failed_count += 1
            logger.error(
                "Failed to sync calendar_entry id=%d: %s", entry.id, error_msg
            )

    return {"synced": synced_count, "failed": failed_count}


def cancel_entry(db: Session, entry: CalendarEntry) -> None:
    """
    Cancel a calendar entry (MVP: delete associated Google Calendar event).

    Sets sync_status='cancelled'. If an external_id exists, the corresponding
    Google Calendar event is deleted first.
    """
    if entry.external_id:
        try:
            delete_google_event(entry.external_id)
        except Exception as exc:
            logger.error(
                "Failed to delete Google event id=%s for calendar_entry id=%d: %s",
                entry.external_id,
                entry.id,
                exc,
            )

    entry.sync_status = SYNC_STATUS_CANCELLED
    db.commit()
    logger.info("Cancelled calendar_entry id=%d", entry.id)


def run_sync(db: Session) -> dict:
    """
    Main entry point for the sync worker.

    Processes all pending calendar_entries and returns a summary.
    """
    logger.info("Starting calendar sync worker run")
    result = sync_pending_entries(db)
    logger.info(
        "Calendar sync worker finished: synced=%d, failed=%d",
        result["synced"],
        result["failed"],
    )
    return result
