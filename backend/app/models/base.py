"""
Base models for Cimeika entities
Defines the minimal entity contract according to UI specification
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from app.config.canon import CANON_BUNDLE_ID

Base = declarative_base()


class BaseEntity(Base):
    """
    Base entity model implementing minimal contract for Cimeika entities
    
    Required fields according to UI specification:
    - id: unique identifier
    - module: module name
    - time: timestamp
    - tags: list of tags
    - source_trace: source tracking information
    - canon_bundle_id: canonical bundle identifier
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String, nullable=False, index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    tags = Column(JSON, nullable=True, default=list)  # List of tag strings
    source_trace = Column(String, nullable=True)  # Source tracking
    canon_bundle_id = Column(String, nullable=False, default=CANON_BUNDLE_ID)
