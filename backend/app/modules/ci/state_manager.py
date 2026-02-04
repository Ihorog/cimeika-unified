"""
State Manager - Handles persona state persistence
Manages mood, energy levels, and context data for personas
"""
from sqlalchemy.orm import Session
from database.models import SystemState, PersonaEnum, Persona
from typing import Optional, Dict


class StateManager:
    """Управління станами персон для користувача"""
    
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id
    
    def update_mood(self, persona: PersonaEnum, mood_score: int) -> Dict:
        """Update mood score (1-10)"""
        if not 1 <= mood_score <= 10:
            raise ValueError("Mood score must be between 1 and 10")
        
        state = self._get_or_create_state(persona)
        state.mood_score = mood_score
        self.db.commit()
        
        return {"persona": persona.value, "mood_score": mood_score}
    
    def update_energy(self, persona: PersonaEnum, energy_level: int) -> Dict:
        """Update energy level (1-10)"""
        if not 1 <= energy_level <= 10:
            raise ValueError("Energy level must be between 1 and 10")
        
        state = self._get_or_create_state(persona)
        state.energy_level = energy_level
        self.db.commit()
        
        return {"persona": persona.value, "energy_level": energy_level}
    
    def get_state(self, persona: PersonaEnum) -> Optional[Dict]:
        """Get current state for a persona"""
        state = self._get_or_create_state(persona)
        return {
            "mood_score": state.mood_score,
            "energy_level": state.energy_level,
            "context_data": state.context_data
        }
    
    def _get_or_create_state(self, persona: PersonaEnum) -> SystemState:
        """Internal: get or create state record"""
        persona_obj = self.db.query(Persona).filter(
            Persona.name == persona
        ).first()
        
        if not persona_obj:
            raise ValueError(f"Persona {persona} not found in database")
        
        state = self.db.query(SystemState).filter(
            SystemState.user_id == self.user_id,
            SystemState.persona_id == persona_obj.id
        ).first()
        
        if not state:
            state = SystemState(
                user_id=self.user_id,
                persona_id=persona_obj.id,
                mood_score=5,
                energy_level=5
            )
            self.db.add(state)
            self.db.commit()
        
        return state
