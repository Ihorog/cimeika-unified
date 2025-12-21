"""
Kazkar module ORM models
Пам'ять - історії, спогади, легенди
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.config.database import Base
from app.config.canon import CANON_BUNDLE_ID


class KazkarStory(Base):
    """
    Kazkar module entity - stories and memories
    Зберігає історії, спогади та легенди
    """
    __tablename__ = "kazkar_stories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String, nullable=False, default='kazkar', index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Kazkar-specific fields
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    story_type = Column(String, nullable=True)  # memory, legend, story, etc.
    participants = Column(JSON, nullable=True)  # List of people involved
    location = Column(String, nullable=True)  # Where it happened
    
    # Entity metadata
    tags = Column(JSON, nullable=True, default=list)
    source_trace = Column(String, nullable=True)
    canon_bundle_id = Column(String, nullable=False, default=CANON_BUNDLE_ID)
    
    def __repr__(self):
        return f"<KazkarStory(id={self.id}, title='{self.title}', type='{self.story_type}')>"
