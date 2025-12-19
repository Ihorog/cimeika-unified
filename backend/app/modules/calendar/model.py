"""
Calendar module ORM models
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CalendarModel(Base):
    """Base model for Calendar module"""
    __tablename__ = "calendar_events"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    scheduled_at = Column(DateTime)
