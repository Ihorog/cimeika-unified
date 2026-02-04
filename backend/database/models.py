"""
SQLAlchemy models for CIMEIKA database with pgvector support
Implements the 7 personas architecture with vector embeddings
"""

import enum
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class PersonaEnum(str, enum.Enum):
    """7 Personas of the CIMEIKA ecosystem"""

    CI = "Ci"
    KAZKAR = "Kazkar"
    NASTRIJ = "Nastrij"
    PODIJA = "Podija"
    MALYA = "Malya"
    GALLERY = "Gallery"
    CALENDAR = "Calendar"


class User(Base):
    """User model with UUID primary key"""

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    memory_entries = relationship(
        "MemoryEntry", back_populates="user", cascade="all, delete-orphan"
    )
    system_states = relationship(
        "SystemState", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Persona(Base):
    """Persona model representing one of the 7 CIMEIKA personas"""

    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(SQLEnum(PersonaEnum), unique=True, nullable=False, index=True)
    base_prompt = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    system_states = relationship(
        "SystemState", back_populates="persona", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Persona(id={self.id}, name={self.name.value})>"


class MemoryEntry(Base):
    """Memory entry with vector embedding for semantic search"""

    __tablename__ = "memory_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content = Column(Text, nullable=False)
    embedding = Column(
        Vector(1536), nullable=True
    )  # OpenAI ada-002 embedding dimension
    meta_data = Column(
        "metadata", JSON, nullable=True, default=dict
    )  # Use meta_data in Python, metadata in DB
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user = relationship("User", back_populates="memory_entries")

    def __repr__(self):
        return f"<MemoryEntry(id={self.id}, user_id={self.user_id})>"


class SystemState(Base):
    """System state tracking persona mood and energy levels"""

    __tablename__ = "system_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    persona_id = Column(
        Integer,
        ForeignKey("personas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    mood_score = Column(Integer, nullable=False)  # 1-10 scale
    energy_level = Column(Float, nullable=False)  # Float for more precision
    context_data = Column(JSON, nullable=True, default=dict)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user = relationship("User", back_populates="system_states")
    persona = relationship("Persona", back_populates="system_states")

    def __repr__(self):
        return f"<SystemState(id={self.id}, user_id={self.user_id}, persona_id={self.persona_id})>"
