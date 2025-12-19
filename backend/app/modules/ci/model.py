"""
Ci module ORM models
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CiModel(Base):
    """Base model for Ci module"""
    __tablename__ = "ci_data"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
