"""
Kazkar module API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.kazkar.schema import (
    KazkarStorySchema,
    KazkarStoryCreate,
    KazkarStoryUpdate
)
from app.modules.kazkar.service import KazkarService

router = APIRouter(prefix="/kazkar", tags=["kazkar"])
service = KazkarService()
service.initialize()


@router.get("/")
async def get_kazkar_status():
    """Get Kazkar module status"""
    return {
        "module": "kazkar",
        "name": "Казкар",
        "description": "Пам'ять, історії, легенди",
        "status": "active"
    }


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about stories by type"""
    counts = service.get_stories_count_by_type(db)
    total = sum(counts.values())
    return {
        "total_stories": total,
        "by_type": counts
    }


@router.post("/stories", response_model=KazkarStorySchema)
async def create_story(story: KazkarStoryCreate, db: Session = Depends(get_db)):
    """Create a new story"""
    return service.create_story(db, story)


@router.get("/stories", response_model=List[KazkarStorySchema])
async def list_stories(skip: int = 0, limit: int = 100, story_type: str = None, db: Session = Depends(get_db)):
    """Get all stories with pagination and optional type filter"""
    return service.get_stories(db, skip=skip, limit=limit, story_type=story_type)


@router.get("/legends", response_model=List[KazkarStorySchema])
async def list_legends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get only legends"""
    return service.get_legends(db, skip=skip, limit=limit)


@router.get("/stories/{story_id}", response_model=KazkarStorySchema)
async def get_story(story_id: int, db: Session = Depends(get_db)):
    """Get a story by ID"""
    story = service.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.put("/stories/{story_id}", response_model=KazkarStorySchema)
async def update_story(story_id: int, story: KazkarStoryUpdate, db: Session = Depends(get_db)):
    """Update a story"""
    updated_story = service.update_story(db, story_id, story)
    if not updated_story:
        raise HTTPException(status_code=404, detail="Story not found")
    return updated_story


@router.delete("/stories/{story_id}")
async def delete_story(story_id: int, db: Session = Depends(get_db)):
    """Delete a story"""
    success = service.delete_story(db, story_id)
    if not success:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"message": "Story deleted successfully"}


@router.post("/import", response_model=KazkarStorySchema)
async def import_legend(story: KazkarStoryCreate, db: Session = Depends(get_db)):
    """
    Import a legend from external source (e.g., GitHub sync script)
    This endpoint is used by the legends sync pipeline to automatically
    import markdown legends into the database.
    """
    # Check if a story with the same title and source_trace already exists
    existing = service.get_story_by_source(db, story.source_trace)
    if existing:
        # Update existing story instead of creating duplicate
        update_data = KazkarStoryUpdate(**story.model_dump())
        updated_story = service.update_story(db, existing.id, update_data)
        return updated_story
    
    # Create new story
    return service.create_story(db, story)

