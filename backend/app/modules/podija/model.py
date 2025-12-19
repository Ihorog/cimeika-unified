"""
Podija module ORM models
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PodijaModel(Base):
    """Base model for Podija module"""
    __tablename__ = "podija_events"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    event_date = Column(DateTime)
