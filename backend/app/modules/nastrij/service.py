"""
Nastrij module service layer
Business logic goes here
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.core.interfaces import ModuleInterface, ServiceInterface
from app.modules.nastrij.model import NastrijEmotion
from app.modules.nastrij.schema import NastrijEmotionCreate, NastrijEmotionUpdate


class NastrijService(ModuleInterface, ServiceInterface):
    """Service for Nastrij module operations - implements core interfaces"""
    
    def __init__(self):
        self._initialized = False
        self._name = "nastrij"
    
    def get_name(self) -> str:
        """Get the module name"""
        return self._name
    
    def get_status(self) -> Dict[str, Any]:
        """Get module status"""
        return {
            "status": "active" if self._initialized else "inactive",
            "name": self._name,
            "initialized": self._initialized
        }
    
    def initialize(self) -> bool:
        """Initialize the Nastrij module"""
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the Nastrij module"""
        self._initialized = False
        return True
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the Nastrij module
        
        Args:
            data: Input data to process
            
        Returns:
            Dict: Processed result
        """
        if not self._initialized:
            return {"error": "Module not initialized"}
        
        return {
            "status": "success",
            "module": self._name,
            "processed": True,
            "data": data
        }
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate input data"""
        return isinstance(data, dict)
    
    # CRUD Operations
    def create_emotion(self, db: Session, emotion_data: NastrijEmotionCreate) -> NastrijEmotion:
        """Create a new emotion record"""
        db_emotion = NastrijEmotion(**emotion_data.model_dump())
        db.add(db_emotion)
        db.commit()
        db.refresh(db_emotion)
        return db_emotion
    
    def get_emotion(self, db: Session, emotion_id: int) -> Optional[NastrijEmotion]:
        """Get an emotion by ID"""
        return db.query(NastrijEmotion).filter(NastrijEmotion.id == emotion_id).first()
    
    def get_emotions(self, db: Session, skip: int = 0, limit: int = 100) -> List[NastrijEmotion]:
        """Get all emotions with pagination"""
        return db.query(NastrijEmotion).offset(skip).limit(limit).all()
    
    def update_emotion(self, db: Session, emotion_id: int, emotion_data: NastrijEmotionUpdate) -> Optional[NastrijEmotion]:
        """Update an emotion"""
        db_emotion = self.get_emotion(db, emotion_id)
        if not db_emotion:
            return None
        
        update_data = emotion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_emotion, field, value)
        
        db.commit()
        db.refresh(db_emotion)
        return db_emotion
    
    def delete_emotion(self, db: Session, emotion_id: int) -> bool:
        """Delete an emotion"""
        db_emotion = self.get_emotion(db, emotion_id)
        if not db_emotion:
            return False
        
        db.delete(db_emotion)
        db.commit()
        return True

