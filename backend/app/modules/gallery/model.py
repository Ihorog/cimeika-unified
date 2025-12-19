"""
Gallery module ORM models
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GalleryModel(Base):
    """Base model for Gallery module"""
    __tablename__ = "gallery_media"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
