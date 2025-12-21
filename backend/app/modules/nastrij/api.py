"""
Nastrij module API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.nastrij.schema import (
    NastrijEmotionSchema,
    NastrijEmotionCreate,
    NastrijEmotionUpdate
)
from app.modules.nastrij.service import NastrijService

router = APIRouter(prefix="/nastrij", tags=["nastrij"])
service = NastrijService()
service.initialize()


@router.get("/")
async def get_nastrij_status():
    """Get Nastrij module status"""
    return {
        "module": "nastrij",
        "name": "Настрій",
        "description": "Емоційні стани, контекст",
        "status": "active"
    }


@router.post("/emotions", response_model=NastrijEmotionSchema)
async def create_emotion(emotion: NastrijEmotionCreate, db: Session = Depends(get_db)):
    """Create a new emotion record"""
    return service.create_emotion(db, emotion)


@router.get("/emotions", response_model=List[NastrijEmotionSchema])
async def list_emotions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all emotions with pagination"""
    return service.get_emotions(db, skip=skip, limit=limit)


@router.get("/emotions/{emotion_id}", response_model=NastrijEmotionSchema)
async def get_emotion(emotion_id: int, db: Session = Depends(get_db)):
    """Get an emotion by ID"""
    emotion = service.get_emotion(db, emotion_id)
    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return emotion


@router.put("/emotions/{emotion_id}", response_model=NastrijEmotionSchema)
async def update_emotion(emotion_id: int, emotion: NastrijEmotionUpdate, db: Session = Depends(get_db)):
    """Update an emotion"""
    updated_emotion = service.update_emotion(db, emotion_id, emotion)
    if not updated_emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return updated_emotion


@router.delete("/emotions/{emotion_id}")
async def delete_emotion(emotion_id: int, db: Session = Depends(get_db)):
    """Delete an emotion"""
    success = service.delete_emotion(db, emotion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return {"message": "Emotion deleted successfully"}

