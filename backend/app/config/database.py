"""
Централізована конфігурація бази даних
Database configuration and session management
"""
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL configuration
POSTGRES_USER = os.getenv('POSTGRES_USER', 'cimeika_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'change_me')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'cimeika')

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20,
    echo=os.getenv('SQLALCHEMY_ECHO', '0') == '1'  # Enable SQL logging in debug
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session
    Use with FastAPI Depends()
    
    Example:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    Should be called on application startup
    """
    # Import all models here to ensure they're registered
    from app.modules.ci.model import CiEntity
    from app.modules.kazkar.model import KazkarStory
    from app.modules.podija.model import PodijaEvent
    from app.modules.nastrij.model import NastrijEmotion
    from app.modules.malya.model import MalyaIdea
    from app.modules.gallery.model import GalleryItem
    from app.modules.calendar.model import CalendarEntry
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
