"""
ReminderWorker: polls reminder_jobs every 30s and sends Telegram notifications.
"""
import logging
import os
import threading
import time
from datetime import datetime, timezone

import requests
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.modules.podija.reminder_model import (
    ReminderJob,
    REMINDER_MAX_ATTEMPTS,
    REMINDER_STATUS_FAILED,
    REMINDER_STATUS_PENDING,
    REMINDER_STATUS_SENT,
)

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 30


def send_telegram(chat_id: str, text: str, bot_token: str) -> None:
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    resp = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
    resp.raise_for_status()


def process_due_reminders(db: Session) -> int:
    """
    Fetch pending reminders whose remind_at <= now(), attempt delivery.
    Returns the number of reminders processed.
    """
    now = datetime.now(timezone.utc)
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")

    due = (
        db.query(ReminderJob)
        .filter(
            ReminderJob.status == REMINDER_STATUS_PENDING,
            ReminderJob.remind_at <= now,
        )
        .all()
    )

    for job in due:
        chat_id = os.getenv("TELEGRAM_CHAT_ID", str(job.user_id))
        message = (
            f"\U000023F0 Reminder: event #{job.event_id} starts in ~10 minutes!"
        )
        try:
            if bot_token:
                send_telegram(chat_id, message, bot_token)
            job.status = REMINDER_STATUS_SENT
            job.updated_at = datetime.now(timezone.utc)
            logger.info("Reminder %s sent (event_id=%s)", job.id, job.event_id)
        except Exception as exc:  # noqa: BLE001
            job.attempts += 1
            job.last_error = str(exc)
            job.updated_at = datetime.now(timezone.utc)
            if job.attempts >= REMINDER_MAX_ATTEMPTS:
                job.status = REMINDER_STATUS_FAILED
                logger.error(
                    "Reminder %s failed permanently after %d attempts: %s",
                    job.id,
                    job.attempts,
                    exc,
                )
            else:
                logger.warning(
                    "Reminder %s attempt %d failed: %s", job.id, job.attempts, exc
                )
        db.commit()

    return len(due)


class ReminderWorker:
    """Background thread that polls reminder_jobs every POLL_INTERVAL_SECONDS."""

    def __init__(self, interval: int = POLL_INTERVAL_SECONDS):
        self._interval = interval
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the background polling thread."""
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run, name="ReminderWorker", daemon=True
        )
        self._thread.start()
        logger.info("ReminderWorker started (interval=%ds)", self._interval)

    def stop(self) -> None:
        """Signal the worker to stop and wait for the thread to finish."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=self._interval + 5)
        logger.info("ReminderWorker stopped")

    def _run(self) -> None:
        """Main polling loop."""
        while not self._stop_event.is_set():
            try:
                db: Session = SessionLocal()
                try:
                    count = process_due_reminders(db)
                    if count:
                        logger.info("Processed %d reminder(s)", count)
                finally:
                    db.close()
            except Exception as exc:  # noqa: BLE001
                logger.error("ReminderWorker error: %s", exc, exc_info=True)
            self._stop_event.wait(self._interval)
