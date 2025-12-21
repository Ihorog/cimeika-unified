"""
Podija module ORM models
Події - майбутнє, сценарії
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from datetime import datetime
from app.config.database import Base
from app.config.canon import CANON_BUNDLE_ID


class PodijaEvent(Base):
    """
    Podija module entity - events and scenarios
    Зберігає події, плани та можливі сценарії
    """
    __tablename__ = "podija_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String, nullable=False, default='podija', index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Podija-specific fields
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(DateTime, nullable=True)  # When the event is/was scheduled
    event_type = Column(String, nullable=True)  # past, future, planned, scenario
    is_completed = Column(Boolean, default=False)
    participants = Column(JSON, nullable=True)  # List of participants
    location = Column(String, nullable=True)
    
    # Entity metadata
    tags = Column(JSON, nullable=True, default=list)
    source_trace = Column(String, nullable=True)
    canon_bundle_id = Column(String, nullable=False, default=CANON_BUNDLE_ID)
    
    def __repr__(self):
        return f"<PodijaEvent(id={self.id}, title='{self.title}', date='{self.event_date}')>"
