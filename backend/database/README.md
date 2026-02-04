# Database Layer Documentation

## Overview

This directory contains the PostgreSQL database layer implementation for the CIMEIKA ecosystem with pgvector extension for semantic search.

## Structure

```
database/
├── __init__.py         # Package exports for clean imports
├── models.py           # SQLAlchemy models (User, Persona, MemoryEntry, SystemState)
├── session.py          # Database session management and connection pooling
├── schema.sql          # Raw SQL schema for Docker initialization
└── README.md           # This file
```

## Quick Start

### Import Models

```python
from database import (
    Base,
    PersonaEnum,
    User,
    Persona,
    MemoryEntry,
    SystemState,
    get_db,
)
```

### Use in FastAPI

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db, User

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### Run Migrations

```bash
# Apply all migrations
cd backend
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"

# Rollback one migration
alembic downgrade -1
```

## Models

### User
- UUID primary key with server-side generation
- Unique username and email
- Timestamps (created_at, updated_at)
- Relationships: memory_entries, system_states

### Persona
- 7 predefined personas (Ci, Kazkar, Nastrij, Podija, Malya, Gallery, Calendar)
- Ukrainian base prompts
- English descriptions
- Relationship: system_states

### MemoryEntry
- Vector embeddings (1536 dimensions) for semantic search
- Belongs to a user
- JSONB metadata (accessed as `meta_data` in Python)
- IVFFlat index for fast similarity search

### SystemState
- Tracks mood (1-10) and energy level per user-persona combination
- Foreign keys to users and personas
- JSONB context data

## Configuration

Set these environment variables:

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cimeika
POSTGRES_USER=cimeika_user
POSTGRES_PASSWORD=your_secure_password
```

## Connection Pooling

- Pool size: 10
- Max overflow: 20
- Pre-ping enabled for connection health
- Connections recycled after 1 hour

## Key Features

1. **UUID Primary Keys**: Better security and scalability
2. **Vector Embeddings**: Semantic search with pgvector
3. **Cascade Deletes**: Referential integrity maintained
4. **Automatic Timestamps**: Server-side triggers for updated_at
5. **Seed Data**: 7 personas pre-populated

## Dependencies

```
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.0
pgvector==0.2.4
```

## Testing

Run integration tests:

```bash
cd backend
python -m pytest tests/test_database.py -v
```

## Documentation

See `docs/DATABASE_SCHEMA.md` for:
- ER diagram
- Detailed table descriptions
- Vector search examples
- Performance considerations

## Notes

- The `metadata` column in MemoryEntry is accessed as `meta_data` in Python to avoid conflicts with SQLAlchemy's reserved attribute
- All timestamps are timezone-aware
- PostgreSQL extensions (uuid-ossp, vector) must be enabled
