"""
Reminder jobs ORM model
reminder_jobs — scheduled T-10m (and custom) reminders
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.config.database import Base


class ReminderJob(Base):
    """
    Scheduled reminder delivery job
    Fires at remind_at UTC time for a linked entity (podija_event / calendar_entry)
    """
    __tablename__ = "reminder_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_type = Column(String(64), nullable=False)   # podija_event | calendar_entry
    entity_id = Column(Integer, nullable=False)
    remind_at = Column(DateTime, nullable=False, index=True)   # exact UTC fire time
    offset_minutes = Column(Integer, nullable=False, default=10)
    channel = Column(String(32), nullable=False, default='telegram')  # telegram/web/both
    status = Column(String(32), nullable=False, default='pending', index=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    payload = Column(JSON, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self):
        return (
            f"<ReminderJob(id={self.id}, entity={self.entity_type}:{self.entity_id}, "
            f"remind_at='{self.remind_at}', status='{self.status}')>"
        )
