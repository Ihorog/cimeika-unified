"""
Malya module ORM models
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MalyaModel(Base):
    """Base model for Malya module"""
    __tablename__ = "malya_ideas"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
