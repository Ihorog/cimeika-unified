"""
Ci module Pydantic schemas
"""
from pydantic import BaseModel


class CiSchema(BaseModel):
    """Base schema for Ci module"""
    id: int
    name: str
    
    class Config:
        from_attributes = True
