"""
Gallery module service
Business logic for Gallery module
"""
from datetime import datetime
from typing import List
from ..models.gallery_models import GalleryItem, CreateGalleryItemRequest, GalleryItemsResponse
import uuid


class GalleryService:
    """Service for Gallery module"""

    def __init__(self):
        # In-memory storage (stub)
        self.items: List[GalleryItem] = []

    def get_items(self) -> GalleryItemsResponse:
        """Get all gallery items"""
        return GalleryItemsResponse(
            items=self.items,
            count=len(self.items)
        )

    def create_item(self, request: CreateGalleryItemRequest) -> GalleryItem:
        """Create a new gallery item"""
        now = datetime.utcnow().isoformat()
        item = GalleryItem(
            id=str(uuid.uuid4()),
            title=request.title,
            description=request.description,
            type=request.type,
            url=request.url,
            thumbnail_url=None,
            tags=request.tags,
            created_at=now,
            updated_at=now,
            metadata={}
        )
        self.items.append(item)
        return item

    def get_item(self, item_id: str) -> GalleryItem:
        """Get item by ID"""
        for item in self.items:
            if item.id == item_id:
                return item
        raise ValueError(f"Item {item_id} not found")

    def delete_item(self, item_id: str) -> None:
        """Delete an item"""
        self.items = [i for i in self.items if i.id != item_id]


# Singleton instance
gallery_service = GalleryService()
