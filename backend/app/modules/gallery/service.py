"""
Gallery module service layer
Business logic goes here
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.core.interfaces import ModuleInterface, ServiceInterface
from app.modules.gallery.model import GalleryItem
from app.modules.gallery.schema import GalleryItemCreate, GalleryItemUpdate


class GalleryService(ModuleInterface, ServiceInterface):
    """Service for Gallery module operations - implements core interfaces"""
    
    def __init__(self):
        self._initialized = False
        self._name = "gallery"
    
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
        """Initialize the Gallery module"""
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the Gallery module"""
        self._initialized = False
        return True
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the Gallery module
        
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
    def create_item(self, db: Session, item_data: GalleryItemCreate) -> GalleryItem:
        """Create a new gallery item"""
        db_item = GalleryItem(**item_data.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def get_item(self, db: Session, item_id: int) -> Optional[GalleryItem]:
        """Get a gallery item by ID"""
        return db.query(GalleryItem).filter(GalleryItem.id == item_id).first()
    
    def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> List[GalleryItem]:
        """Get all gallery items with pagination"""
        return db.query(GalleryItem).offset(skip).limit(limit).all()
    
    def update_item(self, db: Session, item_id: int, item_data: GalleryItemUpdate) -> Optional[GalleryItem]:
        """Update a gallery item"""
        db_item = self.get_item(db, item_id)
        if not db_item:
            return None
        
        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def delete_item(self, db: Session, item_id: int) -> bool:
        """Delete a gallery item"""
        db_item = self.get_item(db, item_id)
        if not db_item:
            return False
        
        db.delete(db_item)
        db.commit()
        return True

