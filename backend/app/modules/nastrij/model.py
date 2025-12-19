"""
Nastrij module ORM models
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NastrijModel(Base):
    """Base model for Nastrij module"""
    __tablename__ = "nastrij_moods"
    
    id = Column(Integer, primary_key=True)
    mood = Column(String)
