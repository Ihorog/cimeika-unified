"""
Kazkar module service
Business logic for Kazkar (Memory/Stories) module
"""
from datetime import datetime
from typing import List
from ..models.kazkar_models import (
    KazkarEntry, CreateKazkarEntryRequest, KazkarLibrary, KazkarEntriesResponse
)
import uuid


class KazkarService:
    """Service for Kazkar module"""

    def __init__(self):
        # In-memory storage (stub)
        self.entries: List[KazkarEntry] = []

    def get_library(self) -> KazkarLibrary:
        """Get library overview"""
        entries_by_type = {}
        for entry in self.entries:
            entries_by_type[entry.type] = entries_by_type.get(entry.type, 0) + 1

        recent = sorted(self.entries, key=lambda e: e.created_at, reverse=True)[:10]

        return KazkarLibrary(
            total_entries=len(self.entries),
            entries_by_type=entries_by_type,
            recent_entries=recent
        )

    def get_entries(self) -> KazkarEntriesResponse:
        """Get all entries"""
        return KazkarEntriesResponse(
            entries=self.entries,
            count=len(self.entries)
        )

    def create_entry(self, request: CreateKazkarEntryRequest) -> KazkarEntry:
        """Create a new entry"""
        now = datetime.utcnow().isoformat()
        entry = KazkarEntry(
            id=str(uuid.uuid4()),
            title=request.title,
            content=request.content,
            type=request.type,
            timestamp=request.timestamp,
            created_at=now,
            updated_at=now,
            tags=request.tags,
            related_entries=[],
            attachments=[]
        )
        self.entries.append(entry)
        return entry

    def get_entry(self, entry_id: str) -> KazkarEntry:
        """Get entry by ID"""
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        raise ValueError(f"Entry {entry_id} not found")

    def update_entry(self, entry_id: str, updates: dict) -> KazkarEntry:
        """Update an entry"""
        for i, entry in enumerate(self.entries):
            if entry.id == entry_id:
                updates['updated_at'] = datetime.utcnow().isoformat()
                updated_entry = entry.copy(update=updates)
                self.entries[i] = updated_entry
                return updated_entry
        raise ValueError(f"Entry {entry_id} not found")

    def delete_entry(self, entry_id: str) -> None:
        """Delete an entry"""
        self.entries = [e for e in self.entries if e.id != entry_id]


# Singleton instance
kazkar_service = KazkarService()
