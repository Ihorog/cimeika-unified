# Database Schema Documentation

## Overview

The CIMEIKA database layer uses PostgreSQL with the pgvector extension to support vector embeddings for semantic search. The schema implements a 7-persona architecture with proper relationships and cascade deletes.

## Entity Relationship Diagram

```mermaid
erDiagram
    users ||--o{ memory_entries : has
    users ||--o{ system_states : has
    personas ||--o{ system_states : tracks
    
    users {
        uuid id PK
        varchar username UK
        varchar email UK
        timestamp created_at
        timestamp updated_at
    }
    
    personas {
        serial id PK
        persona_type name UK
        text base_prompt
        text description
        timestamp created_at
        timestamp updated_at
    }
    
    memory_entries {
        serial id PK
        uuid user_id FK
        text content
        vector_1536 embedding
        jsonb metadata
        timestamp created_at
        timestamp updated_at
    }
    
    system_states {
        serial id PK
        uuid user_id FK
        integer persona_id FK
        integer mood_score
        float energy_level
        jsonb context_data
        timestamp created_at
        timestamp updated_at
    }
```

## Table Descriptions

### Users
Stores user accounts with UUID primary keys for better scalability and security.

**Columns:**
- `id` (UUID): Primary key, auto-generated using `uuid_generate_v4()`
- `username` (VARCHAR): Unique username, indexed
- `email` (VARCHAR): Unique email address, indexed
- `created_at` (TIMESTAMP): Account creation timestamp
- `updated_at` (TIMESTAMP): Last modification timestamp

**Relationships:**
- One-to-many with `memory_entries`
- One-to-many with `system_states`

**Cascade Behavior:**
- Deleting a user deletes all associated memory entries and system states

### Personas
The 7 CIMEIKA personas with their base prompts and descriptions.

**Columns:**
- `id` (SERIAL): Primary key
- `name` (persona_type ENUM): One of the 7 persona names, unique
- `base_prompt` (TEXT): Ukrainian prompt defining persona behavior
- `description` (TEXT): English description of the persona's role
- `created_at` (TIMESTAMP): Creation timestamp
- `updated_at` (TIMESTAMP): Last modification timestamp

**Persona Values:**
- `Ci` - Central orchestration coordinator
- `Kazkar` - Memory and legend keeper
- `Nastrij` - Emotional state analyzer
- `Podija` - Event and scenario master
- `Malya` - Creativity and idea engine
- `Gallery` - Visual archivist
- `Calendar` - Time and rhythm controller

**Relationships:**
- One-to-many with `system_states`

### Memory Entries
Stores user memories with vector embeddings for semantic search using pgvector.

**Columns:**
- `id` (SERIAL): Primary key
- `user_id` (UUID): Foreign key to users, indexed
- `content` (TEXT): Memory content
- `embedding` (vector(1536)): OpenAI ada-002 embedding for semantic search
- `metadata` (JSONB): Additional metadata (tags, source, etc.)
- `created_at` (TIMESTAMP): Creation timestamp
- `updated_at` (TIMESTAMP): Last modification timestamp

**Indexes:**
- IVFFlat index on `embedding` for fast vector similarity search using cosine distance

**Relationships:**
- Many-to-one with `users`

### System States
Tracks the current mood and energy level for each user-persona combination.

**Columns:**
- `id` (SERIAL): Primary key
- `user_id` (UUID): Foreign key to users, indexed
- `persona_id` (INTEGER): Foreign key to personas, indexed
- `mood_score` (INTEGER): Mood score from 1-10, constrained
- `energy_level` (FLOAT): Energy level (precision float)
- `context_data` (JSONB): Additional context information
- `created_at` (TIMESTAMP): Creation timestamp
- `updated_at` (TIMESTAMP): Last modification timestamp

**Relationships:**
- Many-to-one with `users`
- Many-to-one with `personas`

## Database Extensions

### uuid-ossp
Provides UUID generation functions for user IDs.

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### pgvector
Enables vector similarity search for memory embeddings.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## Migration Commands

### Initialize Alembic
```bash
cd backend
alembic init alembic
```

### Create Initial Migration
```bash
cd backend
alembic revision --autogenerate -m "Initial schema with pgvector"
```

### Apply Migrations
```bash
cd backend
alembic upgrade head
```

### Rollback Migration
```bash
cd backend
alembic downgrade -1
```

### View Migration History
```bash
cd backend
alembic history
```

### View Current Version
```bash
cd backend
alembic current
```

## Vector Search Examples

### Semantic Memory Search
Find memories similar to a query using cosine similarity:

```python
from sqlalchemy import select
from database import MemoryEntry, get_db
from pgvector.sqlalchemy import Vector

# Assume we have a query embedding from OpenAI
query_embedding = [0.1, 0.2, ..., 0.9]  # 1536 dimensions

# Find top 5 most similar memories
db = next(get_db())
results = db.execute(
    select(MemoryEntry)
    .order_by(MemoryEntry.embedding.cosine_distance(query_embedding))
    .limit(5)
).scalars().all()
```

### Add Memory with Embedding
```python
from database import MemoryEntry, get_db
import openai

# Generate embedding using OpenAI
response = openai.Embedding.create(
    input="My important memory",
    model="text-embedding-ada-002"
)
embedding = response['data'][0]['embedding']

# Store in database
db = next(get_db())
memory = MemoryEntry(
    user_id=user_id,
    content="My important memory",
    embedding=embedding,
    metadata={"source": "user_input", "tags": ["important"]}
)
db.add(memory)
db.commit()
```

### Filter by Persona State
```python
from database import SystemState, Persona, PersonaEnum, get_db

db = next(get_db())
# Get all high-energy states for Kazkar persona
kazkar_states = (
    db.query(SystemState)
    .join(Persona)
    .filter(Persona.name == PersonaEnum.KAZKAR)
    .filter(SystemState.energy_level > 0.7)
    .all()
)
```

## Configuration

### Environment Variables
Required environment variables for database connection:

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cimeika
POSTGRES_USER=cimeika_user
POSTGRES_PASSWORD=your_secure_password
```

### Connection String
The database URL is automatically constructed from environment variables:

```
postgresql://cimeika_user:password@localhost:5432/cimeika
```

### Connection Pool Settings
- Pool size: 10
- Max overflow: 20
- Pool pre-ping: Enabled (verifies connections before use)
- Pool recycle: 3600 seconds (1 hour)

## Performance Considerations

### Vector Indexing
The IVFFlat index on embeddings provides fast approximate nearest neighbor search:
- Build time: O(n) where n is number of vectors
- Query time: Sub-linear for approximate search
- Trade-off between speed and accuracy

### Best Practices
1. Create vector index after bulk inserting embeddings
2. Use batch operations for inserting multiple memories
3. Consider partitioning `memory_entries` table for large datasets
4. Monitor connection pool usage in production
5. Use prepared statements for repeated queries

## Seed Data

The database includes seed data for all 7 personas with their Ukrainian base prompts:

```sql
INSERT INTO personas (name, base_prompt, description) VALUES
    ('Ci', 'Ти Ці — центральний координатор екосистеми Cimeika.', 'Central orchestration and coordination module'),
    ('Kazkar', 'Ти Казкар — хранитель спогадів і історій.', 'Memory and story keeper, guardian of legends'),
    ('Nastrij', 'Ті Настрій — емоційний аналітик.', 'Emotional state analyzer and mood tracker'),
    ('Podija', 'Ти Подія — майстер подій і майбутніх сценаріїв.', 'Event master and future scenario planner'),
    ('Malya', 'Ти Маля — двигун творчості та ідей.', 'Creativity engine and idea generator'),
    ('Gallery', 'Ти Галерея — візуальний архівіст.', 'Visual archivist and media manager'),
    ('Calendar', 'Ті Календар — контролер ритмів і часу.', 'Time rhythm controller and schedule manager');
```

## Security Considerations

1. **UUID Primary Keys**: Prevents enumeration attacks
2. **Cascade Deletes**: Ensures data integrity when users are deleted
3. **Indexed Foreign Keys**: Improves query performance and enforces referential integrity
4. **Parameterized Queries**: SQLAlchemy ORM prevents SQL injection
5. **Connection Pooling**: Limits database connections and prevents resource exhaustion

## Troubleshooting

### Extension Not Found
If pgvector extension is not available:
```bash
# Install pgvector on Ubuntu/Debian
sudo apt-get install postgresql-15-pgvector

# Or use Docker image with pgvector pre-installed
docker pull ankane/pgvector
```

### Migration Conflicts
If migrations conflict or fail:
```bash
# Reset migrations (development only!)
alembic downgrade base
alembic upgrade head
```

### Connection Issues
Check database connectivity:
```bash
psql -h localhost -U cimeika_user -d cimeika
```

For more information, see:
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
