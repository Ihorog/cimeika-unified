"""
Ci Coordinator - Central orchestrator for the CIMEIKA ecosystem
Handles intent analysis, persona routing, and state management
"""
from typing import Dict, Optional
from sqlalchemy.orm import Session
from database.models import Persona, SystemState, PersonaEnum, User
from datetime import datetime, timezone


class CiCoordinator:
    """
    Ці — центральний координатор екосистеми Cimeika
    Відповідає за:
    - Аналіз наміру користувача (intent recognition)
    - Маршрутизацію до відповідної персони
    - Управління станом системи
    """
    
    INTENT_KEYWORDS = {
        PersonaEnum.KAZKAR: ["історія", "спогад", "минуле", "пам'ять", "згадка"],
        PersonaEnum.PODIJA: ["подія", "план", "майбутнє", "захід", "зустріч", "заплануй"],
        PersonaEnum.NASTRIJ: ["настрій", "емоція", "почуття", "відчуття", "як ти"],
        PersonaEnum.MALYA: ["ідея", "творчість", "креатив", "створи", "малюнок", "дизайн"],
        PersonaEnum.GALLERY: ["фото", "зображення", "картинка", "галерея", "медіа"],
        PersonaEnum.CALENDAR: ["час", "календар", "дата", "коли", "розклад", "термін"]
    }
    
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id
        self.current_persona = self._get_active_persona()
    
    def _get_active_persona(self) -> PersonaEnum:
        """Отримати активну персону з БД"""
        state = self.db.query(SystemState).filter(
            SystemState.user_id == self.user_id
        ).order_by(SystemState.updated_at.desc()).first()
        
        if state and state.persona:
            return state.persona.name
        return PersonaEnum.CI  # Default
    
    async def analyze_intent(self, message: str) -> PersonaEnum:
        """
        Аналіз наміру користувача на основі ключових слів
        Returns: PersonaEnum
        """
        message_lower = message.lower()
        
        # Score each persona based on keyword matches
        scores = {}
        for persona, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in message_lower)
            if score > 0:
                scores[persona] = score
        
        # Return persona with highest score, or keep current if no match
        if scores:
            return max(scores, key=scores.get)
        return self.current_persona
    
    async def switch_persona(self, target_persona: PersonaEnum) -> Dict:
        """
        Перемикання на нову персону
        Updates SystemState in database
        """
        # Get persona from DB
        persona_obj = self.db.query(Persona).filter(
            Persona.name == target_persona
        ).first()
        
        if not persona_obj:
            raise ValueError(f"Persona {target_persona} not found")
        
        # Update or create system state
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
        
        # Update timestamp
        state.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        
        self.current_persona = target_persona
        
        return {
            "persona": target_persona.value,
            "base_prompt": persona_obj.base_prompt,
            "mood_score": state.mood_score,
            "energy_level": state.energy_level
        }
    
    async def route_message(self, message: str) -> Dict:
        """
        Main entry point: analyze and route message
        Returns full context for the active persona
        """
        detected_persona = await self.analyze_intent(message)
        
        # Switch if needed
        if detected_persona != self.current_persona:
            context = await self.switch_persona(detected_persona)
            context["switched"] = True
        else:
            persona_obj = self.db.query(Persona).filter(
                Persona.name == self.current_persona
            ).first()
            state = self.db.query(SystemState).filter(
                SystemState.user_id == self.user_id
            ).order_by(SystemState.updated_at.desc()).first()
            
            context = {
                "persona": self.current_persona.value,
                "base_prompt": persona_obj.base_prompt if persona_obj else "",
                "mood_score": state.mood_score if state else 5,
                "energy_level": state.energy_level if state else 5,
                "switched": False
            }
        
        return {
            **context,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
