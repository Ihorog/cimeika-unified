"""
Нагадування для подій (T-10m Telegram reminders)
"""
import uuid
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.config.database import Base


REMINDER_STATUS_PENDING = "pending"
REMINDER_STATUS_SENT = "sent"
REMINDER_STATUS_FAILED = "failed"

REMINDER_CHANNEL_TELEGRAM = "telegram"

# Maximum delivery attempts before marking as failed
REMINDER_MAX_ATTEMPTS = 3


class ReminderJob(Base):
    """
    Scheduled reminder job for a podija event.
    Worker polls every 30s and sends via Telegram.
    """
    __tablename__ = "reminder_jobs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    event_id = Column(
        Integer,
        ForeignKey("podija_events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    remind_at = Column(DateTime(timezone=True), nullable=False, index=True)
    channel = Column(String(64), nullable=False, default=REMINDER_CHANNEL_TELEGRAM)
    status = Column(String(32), nullable=False, default=REMINDER_STATUS_PENDING, index=True)
    attempts = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return (
            f"<ReminderJob(id={self.id}, event_id={self.event_id}, "
            f"status={self.status}, remind_at={self.remind_at})>"
        )
