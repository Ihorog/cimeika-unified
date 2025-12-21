"""
Gallery module ORM models
Галерея - візуальний архів, медіа
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.config.database import Base
from app.config.canon import CANON_BUNDLE_ID


class GalleryItem(Base):
    """
    Gallery module entity - media items and visual archive
    Зберігає медіа файли та візуальний контент
    """
    __tablename__ = "gallery_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String, nullable=False, default='gallery', index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Gallery-specific fields
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    media_type = Column(String, nullable=False)  # image, video, audio, document
    url = Column(String, nullable=False)  # Storage URL or path
    thumbnail_url = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)  # Size in bytes
    mime_type = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional metadata (dimensions, duration, etc.)
    
    # Entity metadata
    tags = Column(JSON, nullable=True, default=list)
    source_trace = Column(String, nullable=True)
    canon_bundle_id = Column(String, nullable=False, default=CANON_BUNDLE_ID)
    
    def __repr__(self):
        return f"<GalleryItem(id={self.id}, title='{self.title}', type='{self.media_type}')>"
