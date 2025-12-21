"""
Kazkar module service layer
Business logic goes here
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.core.interfaces import ModuleInterface, ServiceInterface
from app.modules.kazkar.model import KazkarStory
from app.modules.kazkar.schema import KazkarStoryCreate, KazkarStoryUpdate


class KazkarService(ModuleInterface, ServiceInterface):
    """Service for Kazkar module operations - implements core interfaces"""
    
    def __init__(self):
        self._initialized = False
        self._name = "kazkar"
    
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
        """Initialize the Kazkar module"""
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the Kazkar module"""
        self._initialized = False
        return True
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the Kazkar module
        
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
    def create_story(self, db: Session, story_data: KazkarStoryCreate) -> KazkarStory:
        """Create a new story"""
        db_story = KazkarStory(**story_data.model_dump())
        db.add(db_story)
        db.commit()
        db.refresh(db_story)
        return db_story
    
    def get_story(self, db: Session, story_id: int) -> Optional[KazkarStory]:
        """Get a story by ID"""
        return db.query(KazkarStory).filter(KazkarStory.id == story_id).first()
    
    def get_stories(self, db: Session, skip: int = 0, limit: int = 100) -> List[KazkarStory]:
        """Get all stories with pagination"""
        return db.query(KazkarStory).offset(skip).limit(limit).all()
    
    def update_story(self, db: Session, story_id: int, story_data: KazkarStoryUpdate) -> Optional[KazkarStory]:
        """Update a story"""
        db_story = self.get_story(db, story_id)
        if not db_story:
            return None
        
        update_data = story_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_story, field, value)
        
        db.commit()
        db.refresh(db_story)
        return db_story
    
    def delete_story(self, db: Session, story_id: int) -> bool:
        """Delete a story"""
        db_story = self.get_story(db, story_id)
        if not db_story:
            return False
        
        db.delete(db_story)
        db.commit()
        return True

