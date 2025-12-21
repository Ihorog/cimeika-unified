# CIMEIKA API Documentation

## Overview

CIMEIKA API provides RESTful endpoints for managing family life through 7 interconnected modules.

## Base URL

- **Development**: `http://localhost:5000` (Flask) or `http://localhost:8000` (FastAPI)
- **API v1**: `/api/v1`

## FastAPI vs Flask

The project includes both Flask and FastAPI implementations:

- **Flask** (`main.py`): Legacy implementation, SEO-focused endpoints
- **FastAPI** (`fastapi_app.py`): Modern implementation with full CRUD operations, OpenAPI docs

### Running FastAPI

```bash
cd backend
python fastapi_app.py
```

Or using uvicorn directly:
```bash
uvicorn fastapi_app:app --reload --port 8000
```

Access interactive API documentation at:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Modules and Endpoints

### 1. Ci (Центральне ядро) - Core Orchestration

**Endpoints:**
- `GET /api/v1/ci/` - Get module status
- `GET /api/v1/ci/seo/*` - SEO-related endpoints (inherited from Flask)

### 2. Kazkar (Пам'ять) - Memory & Stories

**Endpoints:**
- `GET /api/v1/kazkar/` - Get module status
- `POST /api/v1/kazkar/stories` - Create new story
- `GET /api/v1/kazkar/stories` - List all stories
- `GET /api/v1/kazkar/stories/{id}` - Get story by ID
- `PUT /api/v1/kazkar/stories/{id}` - Update story
- `DELETE /api/v1/kazkar/stories/{id}` - Delete story

**Story Schema:**
```json
{
  "title": "string",
  "content": "string",
  "story_type": "string (optional)",
  "participants": ["string"],
  "location": "string (optional)",
  "tags": ["string"]
}
```

### 3. Podija (Події) - Events

**Endpoints:**
- `GET /api/v1/podija/` - Get module status
- `POST /api/v1/podija/events` - Create new event
- `GET /api/v1/podija/events` - List all events
- `GET /api/v1/podija/events/{id}` - Get event by ID
- `PUT /api/v1/podija/events/{id}` - Update event
- `DELETE /api/v1/podija/events/{id}` - Delete event

**Event Schema:**
```json
{
  "title": "string",
  "description": "string (optional)",
  "event_date": "datetime (optional)",
  "event_type": "string (optional)",
  "is_completed": "boolean",
  "participants": ["string"],
  "location": "string (optional)",
  "tags": ["string"]
}
```

### 4. Nastrij (Настрій) - Emotional States

**Endpoints:**
- `GET /api/v1/nastrij/` - Get module status
- `POST /api/v1/nastrij/emotions` - Create emotion record
- `GET /api/v1/nastrij/emotions` - List all emotions
- `GET /api/v1/nastrij/emotions/{id}` - Get emotion by ID
- `PUT /api/v1/nastrij/emotions/{id}` - Update emotion
- `DELETE /api/v1/nastrij/emotions/{id}` - Delete emotion

**Emotion Schema:**
```json
{
  "emotion_state": "string",
  "intensity": "float (0-10, optional)",
  "context": "string (optional)",
  "triggers": ["string"],
  "notes": "string (optional)",
  "tags": ["string"]
}
```

### 5. Malya (Маля) - Ideas & Creativity

**Endpoints:**
- `GET /api/v1/malya/` - Get module status
- `POST /api/v1/malya/ideas` - Create new idea
- `GET /api/v1/malya/ideas` - List all ideas
- `GET /api/v1/malya/ideas/{id}` - Get idea by ID
- `PUT /api/v1/malya/ideas/{id}` - Update idea
- `DELETE /api/v1/malya/ideas/{id}` - Delete idea

**Idea Schema:**
```json
{
  "title": "string",
  "description": "string",
  "idea_type": "string (optional)",
  "status": "string (optional)",
  "related_ideas": [1, 2, 3],
  "resources": ["string"],
  "tags": ["string"]
}
```

### 6. Gallery (Галерея) - Media Archive

**Endpoints:**
- `GET /api/v1/gallery/` - Get module status
- `POST /api/v1/gallery/items` - Create new gallery item
- `GET /api/v1/gallery/items` - List all items
- `GET /api/v1/gallery/items/{id}` - Get item by ID
- `PUT /api/v1/gallery/items/{id}` - Update item
- `DELETE /api/v1/gallery/items/{id}` - Delete item

**Gallery Item Schema:**
```json
{
  "title": "string",
  "description": "string (optional)",
  "media_type": "string (image|video|audio|document)",
  "url": "string",
  "thumbnail_url": "string (optional)",
  "file_size": "integer (optional)",
  "mime_type": "string (optional)",
  "metadata": {},
  "tags": ["string"]
}
```

### 7. Calendar (Календар) - Time Management

**Endpoints:**
- `GET /api/v1/calendar/` - Get module status
- `POST /api/v1/calendar/entries` - Create new entry
- `GET /api/v1/calendar/entries` - List all entries
- `GET /api/v1/calendar/entries/{id}` - Get entry by ID
- `PUT /api/v1/calendar/entries/{id}` - Update entry
- `DELETE /api/v1/calendar/entries/{id}` - Delete entry

**Calendar Entry Schema:**
```json
{
  "title": "string",
  "description": "string (optional)",
  "scheduled_at": "datetime",
  "end_time": "datetime (optional)",
  "entry_type": "string (optional)",
  "is_recurring": "boolean",
  "recurrence_pattern": {},
  "location": "string (optional)",
  "participants": ["string"],
  "reminder_settings": {},
  "tags": ["string"]
}
```

## Common Fields

All entities include these metadata fields:
- `id` - Unique identifier (auto-generated)
- `module` - Module name (auto-set)
- `time` - Creation timestamp (auto-generated)
- `canon_bundle_id` - Canonical bundle identifier (auto-set)
- `source_trace` - Source tracking information (optional)

## Pagination

List endpoints support pagination:
- `skip` - Number of items to skip (default: 0)
- `limit` - Maximum items to return (default: 100, max: 100)

Example: `GET /api/v1/kazkar/stories?skip=10&limit=20`

## Error Responses

Standard error format:
```json
{
  "detail": "Error message"
}
```

HTTP Status Codes:
- `200` - Success
- `201` - Created
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Database Setup

Initialize the database:
```bash
cd backend
python init_db.py
```

This creates all necessary tables for the 7 modules.

## Testing with curl

### Create a story:
```bash
curl -X POST http://localhost:8000/api/v1/kazkar/stories \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Перша історія",
    "content": "Це тестова історія про сім'ю",
    "story_type": "memory",
    "tags": ["test", "family"]
  }'
```

### List stories:
```bash
curl http://localhost:8000/api/v1/kazkar/stories
```

### Get specific story:
```bash
curl http://localhost:8000/api/v1/kazkar/stories/1
```

## Docker Deployment

Run full stack with Docker Compose:
```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend (port 5000)
- Frontend (port 3000)
- Celery Worker

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python fastapi_app.py
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## Next Steps

1. Implement authentication & authorization
2. Add file upload support for Gallery
3. Implement advanced search and filtering
4. Add WebSocket support for real-time updates
5. Integrate AI features (OpenAI, Claude)
6. Add comprehensive tests
7. Set up CI/CD pipeline
