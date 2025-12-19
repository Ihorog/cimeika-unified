"""
Kazkar module Pydantic schemas
"""
from pydantic import BaseModel


class KazkarSchema(BaseModel):
    """Base schema for Kazkar module"""
    id: int
    title: str
    content: str
    
    class Config:
        from_attributes = True
