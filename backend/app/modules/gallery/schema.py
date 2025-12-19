"""
Gallery module Pydantic schemas
"""
from pydantic import BaseModel


class GallerySchema(BaseModel):
    """Base schema for Gallery module"""
    id: int
    title: str
    url: str
    
    class Config:
        from_attributes = True
