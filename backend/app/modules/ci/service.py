"""
Ci module service layer
Business logic goes here
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.core.interfaces import ModuleInterface, ServiceInterface
from app.config.seo import seo_service
from app.modules.ci.model import CiEntity
from app.modules.ci.schema import CiEntityCreate, CiEntityUpdate


class CiService(ModuleInterface, ServiceInterface):
    """Service for Ci module operations - implements core interfaces"""
    
    def __init__(self):
        self._initialized = False
        self._name = "ci"
        self._seo_service = seo_service
    
    def get_name(self) -> str:
        """Get the module name"""
        return self._name
    
    def get_status(self) -> Dict[str, Any]:
        """Get module status"""
        return {
            "status": "active" if self._initialized else "inactive",
            "name": self._name,
            "initialized": self._initialized,
            "seo_enabled": True
        }
    
    def initialize(self) -> bool:
        """Initialize the Ci module"""
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the Ci module"""
        self._initialized = False
        return True
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the Ci module
        
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
    def create_entity(self, db: Session, entity_data: CiEntityCreate) -> CiEntity:
        """Create a new Ci entity"""
        db_entity = CiEntity(**entity_data.model_dump())
        db.add(db_entity)
        db.commit()
        db.refresh(db_entity)
        return db_entity
    
    def get_entity(self, db: Session, entity_id: int) -> Optional[CiEntity]:
        """Get a Ci entity by ID"""
        return db.query(CiEntity).filter(CiEntity.id == entity_id).first()
    
    def get_entities(self, db: Session, skip: int = 0, limit: int = 100) -> List[CiEntity]:
        """Get all Ci entities with pagination"""
        return db.query(CiEntity).offset(skip).limit(limit).all()
    
    def update_entity(self, db: Session, entity_id: int, entity_data: CiEntityUpdate) -> Optional[CiEntity]:
        """Update a Ci entity"""
        db_entity = self.get_entity(db, entity_id)
        if not db_entity:
            return None
        
        update_data = entity_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_entity, field, value)
        
        db.commit()
        db.refresh(db_entity)
        return db_entity
    
    def delete_entity(self, db: Session, entity_id: int) -> bool:
        """Delete a Ci entity"""
        db_entity = self.get_entity(db, entity_id)
        if not db_entity:
            return False
        
        db.delete(db_entity)
        db.commit()
        return True
    
    # SEO Operations
    def resolve_seo_entry(self, lang: str, state: str, intent: str) -> Dict[str, Any]:
        """
        Resolve SEO entry for given parameters
        
        Args:
            lang: Language code
            state: Emotional state
            intent: User intent
            
        Returns:
            Complete SEO entry or error
        """
        entry = self._seo_service.get_entry(lang, state, intent)
        if not entry:
            return {
                "error": "SEO entry not found",
                "lang": lang,
                "state": state,
                "intent": intent
            }
        return entry
    
    def get_module_mapping(self, state: str) -> Dict[str, Any]:
        """
        Get module mapping for a state
        
        Args:
            state: Emotional state
            
        Returns:
            Module and writes policy information
        """
        module = self._seo_service.get_module(state)
        writes_policy = self._seo_service.get_writes_policy(module)
        
        return {
            "state": state,
            "module": module,
            "writes_policy": writes_policy
        }

