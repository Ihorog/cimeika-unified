"""
Malya module service layer
Business logic goes here
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.core.interfaces import ModuleInterface, ServiceInterface
from app.modules.malya.model import MalyaIdea
from app.modules.malya.schema import MalyaIdeaCreate, MalyaIdeaUpdate


class MalyaService(ModuleInterface, ServiceInterface):
    """Service for Malya module operations - implements core interfaces"""
    
    def __init__(self):
        self._initialized = False
        self._name = "malya"
    
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
        """Initialize the Malya module"""
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the Malya module"""
        self._initialized = False
        return True
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the Malya module
        
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
    def create_idea(self, db: Session, idea_data: MalyaIdeaCreate) -> MalyaIdea:
        """Create a new idea"""
        db_idea = MalyaIdea(**idea_data.model_dump())
        db.add(db_idea)
        db.commit()
        db.refresh(db_idea)
        return db_idea
    
    def get_idea(self, db: Session, idea_id: int) -> Optional[MalyaIdea]:
        """Get an idea by ID"""
        return db.query(MalyaIdea).filter(MalyaIdea.id == idea_id).first()
    
    def get_ideas(self, db: Session, skip: int = 0, limit: int = 100) -> List[MalyaIdea]:
        """Get all ideas with pagination"""
        return db.query(MalyaIdea).offset(skip).limit(limit).all()
    
    def update_idea(self, db: Session, idea_id: int, idea_data: MalyaIdeaUpdate) -> Optional[MalyaIdea]:
        """Update an idea"""
        db_idea = self.get_idea(db, idea_id)
        if not db_idea:
            return None
        
        update_data = idea_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_idea, field, value)
        
        db.commit()
        db.refresh(db_idea)
        return db_idea
    
    def delete_idea(self, db: Session, idea_id: int) -> bool:
        """Delete an idea"""
        db_idea = self.get_idea(db, idea_id)
        if not db_idea:
            return False
        
        db.delete(db_idea)
        db.commit()
        return True

