"""
Malya module API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.malya.schema import (
    MalyaIdeaSchema,
    MalyaIdeaCreate,
    MalyaIdeaUpdate
)
from app.modules.malya.service import MalyaService

router = APIRouter(prefix="/malya", tags=["malya"])
service = MalyaService()
service.initialize()


@router.get("/")
async def get_malya_status():
    """Get Malya module status"""
    return {
        "module": "malya",
        "name": "Маля",
        "description": "Ідеї, творчість, інновації",
        "status": "active"
    }


@router.post("/ideas", response_model=MalyaIdeaSchema)
async def create_idea(idea: MalyaIdeaCreate, db: Session = Depends(get_db)):
    """Create a new idea"""
    return service.create_idea(db, idea)


@router.get("/ideas", response_model=List[MalyaIdeaSchema])
async def list_ideas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all ideas with pagination"""
    return service.get_ideas(db, skip=skip, limit=limit)


@router.get("/ideas/{idea_id}", response_model=MalyaIdeaSchema)
async def get_idea(idea_id: int, db: Session = Depends(get_db)):
    """Get an idea by ID"""
    idea = service.get_idea(db, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea


@router.put("/ideas/{idea_id}", response_model=MalyaIdeaSchema)
async def update_idea(idea_id: int, idea: MalyaIdeaUpdate, db: Session = Depends(get_db)):
    """Update an idea"""
    updated_idea = service.update_idea(db, idea_id, idea)
    if not updated_idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return updated_idea


@router.delete("/ideas/{idea_id}")
async def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    """Delete an idea"""
    success = service.delete_idea(db, idea_id)
    if not success:
        raise HTTPException(status_code=404, detail="Idea not found")
    return {"message": "Idea deleted successfully"}

