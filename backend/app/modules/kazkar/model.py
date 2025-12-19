"""
Kazkar module ORM models
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KazkarModel(Base):
    """Base model for Kazkar module"""
    __tablename__ = "kazkar_stories"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
