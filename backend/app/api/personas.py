"""
Personas API - Endpoints for persona management and routing
Handles message routing, persona switching, and state updates
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.session import get_db
from app.modules.ci.coordinator import CiCoordinator
from app.modules.ci.state_manager import StateManager
from database.models import PersonaEnum

router = APIRouter(prefix="/api/v1/personas", tags=["Personas"])


class MessageRequest(BaseModel):
    user_id: str
    message: str


class PersonaSwitchRequest(BaseModel):
    user_id: str
    target_persona: PersonaEnum


class MoodUpdateRequest(BaseModel):
    user_id: str
    persona: PersonaEnum
    mood_score: int


@router.post("/route")
async def route_message(request: MessageRequest, db: Session = Depends(get_db)):
    """
    Analyze user message and route to appropriate persona
    """
    try:
        coordinator = CiCoordinator(db, request.user_id)
        result = await coordinator.route_message(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/switch")
async def switch_persona(request: PersonaSwitchRequest, db: Session = Depends(get_db)):
    """
    Manually switch to a specific persona
    """
    try:
        coordinator = CiCoordinator(db, request.user_id)
        result = await coordinator.switch_persona(request.target_persona)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mood")
async def update_mood(request: MoodUpdateRequest, db: Session = Depends(get_db)):
    """
    Update mood score for a persona
    """
    try:
        state_manager = StateManager(db, request.user_id)
        result = state_manager.update_mood(request.persona, request.mood_score)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active/{user_id}")
async def get_active_persona(user_id: str, db: Session = Depends(get_db)):
    """
    Get currently active persona for user
    """
    try:
        coordinator = CiCoordinator(db, user_id)
        return {"active_persona": coordinator.current_persona.value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
