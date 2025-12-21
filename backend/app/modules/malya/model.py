"""
Malya module ORM models
Маля - ідеї, творчість, інновації
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.config.database import Base
from app.config.canon import CANON_BUNDLE_ID


class MalyaIdea(Base):
    """
    Malya module entity - ideas and creative concepts
    Зберігає ідеї, творчі концепції та інновації
    """
    __tablename__ = "malya_ideas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String, nullable=False, default='malya', index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Malya-specific fields
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    idea_type = Column(String, nullable=True)  # concept, innovation, project, etc.
    status = Column(String, nullable=True)  # draft, in_progress, realized, archived
    related_ideas = Column(JSON, nullable=True)  # List of related idea IDs
    resources = Column(JSON, nullable=True)  # Resources needed or used
    
    # Entity metadata
    tags = Column(JSON, nullable=True, default=list)
    source_trace = Column(String, nullable=True)
    canon_bundle_id = Column(String, nullable=False, default=CANON_BUNDLE_ID)
    
    def __repr__(self):
        return f"<MalyaIdea(id={self.id}, title='{self.title}', status='{self.status}')>"
