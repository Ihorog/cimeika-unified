"""
Calendar module ORM models
Календар - час, ритми, планування
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from datetime import datetime
from app.config.database import Base
from app.config.canon import CANON_BUNDLE_ID


class CalendarEntry(Base):
    """
    Calendar module entity - time management and planning
    Зберігає календарні події, плани та ритми
    """
    __tablename__ = "calendar_entries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String, nullable=False, default='calendar', index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Calendar-specific fields
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    scheduled_at = Column(DateTime, nullable=False)  # When it's scheduled
    end_time = Column(DateTime, nullable=True)
    entry_type = Column(String, nullable=True)  # event, reminder, routine, rhythm
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(JSON, nullable=True)  # Pattern for recurring events
    location = Column(String, nullable=True)
    participants = Column(JSON, nullable=True)
    reminder_settings = Column(JSON, nullable=True)
    
    # Entity metadata
    tags = Column(JSON, nullable=True, default=list)
    source_trace = Column(String, nullable=True)
    canon_bundle_id = Column(String, nullable=False, default=CANON_BUNDLE_ID)
    
    def __repr__(self):
        return f"<CalendarEntry(id={self.id}, title='{self.title}', scheduled='{self.scheduled_at}')>"
