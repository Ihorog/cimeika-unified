"""
Malya module Pydantic schemas
"""
from pydantic import BaseModel


class MalyaSchema(BaseModel):
    """Base schema for Malya module"""
    id: int
    title: str
    description: str
    
    class Config:
        from_attributes = True
