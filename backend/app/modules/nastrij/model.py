"""
Nastrij module ORM models
Настрій - емоційні стани, контекст
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from datetime import datetime
from app.config.database import Base
from app.config.canon import CANON_BUNDLE_ID


class NastrijEmotion(Base):
    """
    Nastrij module entity - emotional states and context
    Зберігає емоційні стани та контекстуальну інформацію
    """
    __tablename__ = "nastrij_emotions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String, nullable=False, default='nastrij', index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Nastrij-specific fields
    emotion_state = Column(String, nullable=False)  # Current emotional state
    intensity = Column(Float, nullable=True)  # Intensity level (0-10)
    context = Column(Text, nullable=True)  # Context description
    triggers = Column(JSON, nullable=True)  # What triggered this state
    notes = Column(Text, nullable=True)
    
    # Entity metadata
    tags = Column(JSON, nullable=True, default=list)
    source_trace = Column(String, nullable=True)
    canon_bundle_id = Column(String, nullable=False, default=CANON_BUNDLE_ID)
    
    def __repr__(self):
        return f"<NastrijEmotion(id={self.id}, state='{self.emotion_state}', intensity={self.intensity})>"
