"""
Kazkar module models
Data Transfer Objects for Kazkar (Memory/Stories) module
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class KazkarEntry(BaseModel):
    """Kazkar entry model"""
    id: Optional[str] = None
    title: str
    content: str
    type: str = Field(default="memory")  # story, memory, legend, fact
    timestamp: str  # ISO 8601 datetime when the memory occurred
    created_at: str  # ISO 8601 datetime when entry was created
    updated_at: str  # ISO 8601 datetime
    tags: Optional[List[str]] = None
    related_entries: Optional[List[str]] = None
    attachments: Optional[List[str]] = None


class CreateKazkarEntryRequest(BaseModel):
    """Request to create a Kazkar entry"""
    title: str
    content: str
    type: str = Field(default="memory")
    timestamp: str
    tags: Optional[List[str]] = None


class KazkarLibrary(BaseModel):
    """Kazkar library overview"""
    total_entries: int
    entries_by_type: dict
    recent_entries: List[KazkarEntry]


class KazkarEntriesResponse(BaseModel):
    """Response with Kazkar entries"""
    entries: List[KazkarEntry]
    count: int
