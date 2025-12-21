"""
CI module models
Data Transfer Objects for Ci module
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ModuleInfo(BaseModel):
    """Module information"""
    id: str
    name: str
    description: str
    status: str = Field(default="in_development")


class HealthStatus(BaseModel):
    """System health status"""
    status: str
    message: str
    timestamp: str
    version: Optional[str] = None
    canon_bundle_id: Optional[str] = None


class CiState(BaseModel):
    """Ci module state"""
    status: str = Field(default="idle")
    modules: List[ModuleInfo] = Field(default_factory=list)
    health: Optional[HealthStatus] = None


class CiChatMessage(BaseModel):
    """Chat message to Ci"""
    message: str
    context: Optional[Dict[str, Any]] = None


class CiChatResponse(BaseModel):
    """Chat response from Ci"""
    reply: str
    timestamp: str
    context: Optional[Dict[str, Any]] = None
