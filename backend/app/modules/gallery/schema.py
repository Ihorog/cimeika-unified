"""
Gallery module Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict


class GallerySchema(BaseModel):
    """Base schema for Gallery module"""
    id: int
    title: str
    url: str
    
    model_config = ConfigDict(from_attributes=True)
