"""
Gallery module API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.gallery.schema import (
    GalleryItemSchema,
    GalleryItemCreate,
    GalleryItemUpdate
)
from app.modules.gallery.service import GalleryService

router = APIRouter(prefix="/gallery", tags=["gallery"])
service = GalleryService()
service.initialize()


@router.get("/")
async def get_gallery_status():
    """Get Gallery module status"""
    return {
        "module": "gallery",
        "name": "Галерея",
        "description": "Візуальний архів, медіа",
        "status": "active"
    }


@router.post("/items", response_model=GalleryItemSchema)
async def create_item(item: GalleryItemCreate, db: Session = Depends(get_db)):
    """Create a new gallery item"""
    return service.create_item(db, item)


@router.get("/items", response_model=List[GalleryItemSchema])
async def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all gallery items with pagination"""
    return service.get_items(db, skip=skip, limit=limit)


@router.get("/items/{item_id}", response_model=GalleryItemSchema)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a gallery item by ID"""
    item = service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/items/{item_id}", response_model=GalleryItemSchema)
async def update_item(item_id: int, item: GalleryItemUpdate, db: Session = Depends(get_db)):
    """Update a gallery item"""
    updated_item = service.update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a gallery item"""
    success = service.delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

