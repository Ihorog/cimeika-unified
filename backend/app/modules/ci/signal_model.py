"""
Ci module signal ORM model
ci_signals — Ci orchestration bus
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.config.database import Base


class CiSignal(Base):
    """
    Ci orchestration bus signal
    Carries events between modules through the Ci coordination layer
    """
    __tablename__ = "ci_signals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    signal_type = Column(String(64), nullable=False, index=True)
    source_module = Column(String(64), nullable=False)
    target_module = Column(String(64), nullable=True)
    payload = Column(JSON, nullable=True, default=dict)
    status = Column(String(32), nullable=False, default='pending', index=True)  # pending/processed/failed
    processed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)

    def __repr__(self):
        return f"<CiSignal(id={self.id}, type='{self.signal_type}', status='{self.status}')>"
