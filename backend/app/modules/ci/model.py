"""
Ci module ORM models
Центральне ядро - оркестрація системи
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.config.database import Base
from app.config.canon import CANON_BUNDLE_ID


class CiEntity(Base):
    """
    Ci module entity - system orchestration data
    Зберігає глобальний контекст та координаційні дані
    """
    __tablename__ = "ci_entities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String, nullable=False, default='ci', index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Ci-specific fields
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    context_data = Column(JSON, nullable=True)  # Global context information
    orchestration_state = Column(String, nullable=True)  # Current orchestration state
    
    # Entity metadata
    tags = Column(JSON, nullable=True, default=list)
    source_trace = Column(String, nullable=True)
    canon_bundle_id = Column(String, nullable=False, default=CANON_BUNDLE_ID)
    
    def __repr__(self):
        return f"<CiEntity(id={self.id}, name='{self.name}', state='{self.orchestration_state}')>"
