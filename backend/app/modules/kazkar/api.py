"""
Kazkar module API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.kazkar.schema import (
    KazkarStorySchema,
    KazkarStoryCreate,
    KazkarStoryUpdate
)
from app.modules.kazkar.service import KazkarService
from app.modules.kazkar.websocket import kazkar_ws_manager, broadcast_legend_event

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
        
        # Broadcast update event
        await broadcast_legend_event(
            event_type="legend_updated",
            legend_id=updated_story.id,
            data={"title": updated_story.title, "action": "updated"}
        )
        
        return updated_story
    
    # Create new story
    new_story = service.create_story(db, story)
    
    # Broadcast creation event
    await broadcast_legend_event(
        event_type="legend_created",
        legend_id=new_story.id,
        data={"title": new_story.title, "action": "created"}
    )
    
    return new_story


@router.post("/broadcast")
async def broadcast_event(event: dict):
    """
    Broadcast a custom event to all connected WebSocket clients
    Used for testing or manual event triggers
    """
    await kazkar_ws_manager.broadcast(event)
    return {"status": "success", "message": "Event broadcasted to all clients"}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time Kazkar updates
    
    Clients can connect to receive live events such as:
    - legend_sense_activated: When a sense node is activated
    - legend_created: When a new legend is added
    - legend_updated: When a legend is modified
    - legends_synced: When batch sync completes
    """
    await kazkar_ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            # Echo back for now (can be extended for client -> server events)
            await websocket.send_json({
                "event": "echo",
                "received": data,
                "timestamp": int(__import__('datetime').datetime.now().timestamp())
            })
    except WebSocketDisconnect:
        kazkar_ws_manager.disconnect(websocket)


