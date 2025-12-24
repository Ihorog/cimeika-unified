# Cimeika Unified - AI Coding Agent Instructions

## Architecture Overview

**CIMEIKA** is a family life management platform built on **CANON v1.0.0** principles with 7 fixed modules. It's a bilingual (EN/UK) React+FastAPI monorepo following "reality first, action before explanation" design philosophy.

### Critical: Fixed Module System
The 7 modules are **immutable** - no additions/removals allowed:
- **Ci**: Central orchestration core (entry point: `ci.capture()`)
- **Kazkar**: Memory, stories, legends (night theme)
- **Podija**: Events, future scenarios
- **Nastrij**: Emotional states tracking
- **Malya**: Ideas, creativity, innovations
- **Gallery**: Visual archive, media
- **Calendar**: Time, rhythms, planning

All modules except Kazkar use **day theme** (deterministic, route-based theming).

## Backend (Python/FastAPI)

### Standard Module Structure
Each module in `backend/app/modules/{module}/` follows:
```
{module}/
  ├── api.py       # FastAPI routes ONLY (no logic)
  ├── service.py   # Business logic, implements ModuleInterface + ServiceInterface
  ├── model.py     # SQLAlchemy models (canon_bundle_id required)
  └── schema.py    # Pydantic v2 schemas (Base/Create/Update/Response)
```

### Service Layer Pattern
All services implement `ModuleInterface` and `ServiceInterface` from `backend/app/core/interfaces.py`:
- Must have `get_name()`, `get_status()`, `initialize()`, `shutdown()`
- CRUD operations: `create_*()`, `get_*()`, `get_*s()`, `update_*()`, `delete_*()`
- Services are registered in `backend/app/startup.py` via `registry.register()`

### API Routes
- Prefix: `/api/v1/{module}`
- All module routers aggregate in `backend/app/api/v1/router.py`
- Use FastAPI dependency injection with `get_db()` from `backend/app/config/database.py`
- Swagger docs auto-generate at `/api/docs`

### Database Conventions
- SQLAlchemy 2.0 with `backend/app/config/database.py` centralized config
- All models require `canon_bundle_id` (from `backend/app/config/canon.py`)
- Use JSON fields for flexible metadata
- Initialize DB with `backend/init_db.py`

### SEO Integration
**Critical**: The project has a 7×7 emotional-intent SEO matrix at `backend/app/config/seo/cimeikaseomatrix.yaml`:
- States: fatigue, tension, anxiety, joy, loss, anticipation, change
- Intents: understand, capture, calm, check, preserve, connect, prepare
- URL format: `/{lang}/{state}/{intent}` (e.g., `/en/fatigue/understand`)
- Access via `seo_service` singleton from `backend/app/config/seo/__init__.py`
- Ci module's `ci.capture()` uses SEO classification for routing

## Frontend (React 18 + TypeScript)

### Module Structure
Each module in `frontend/src/modules/{Module}/` follows:
```
{Module}/
  ├── views/       # UI orchestration (NO business logic)
  ├── components/  # Module-specific components
  ├── hooks/       # Custom React hooks (e.g., useCi)
  ├── service.ts   # API calls and data layer
  └── store.ts     # Zustand state management
```

### Theme System
**Deterministic** theme switching in `frontend/src/core/ThemeManager.jsx`:
- Route-based: Kazkar → night, all others → day
- Applied via `data-theme` attribute on document root
- NO manual theme toggles - themes are module-determined

### State Management
- Use **Zustand** (not Redux/Context API for module state)
- Global orchestrator in `frontend/src/core/orchestrator.ts`
- Example pattern: `useCiStore` in `frontend/src/modules/Ci/store.ts`

### Routing
- React Router v6 in `frontend/src/App.jsx`
- All routes under single `MainLayout` wrapper
- Root redirects to `/ci` (entry point per CANON)

## Development Workflows

### Local Development
```bash
# Full stack (recommended)
docker-compose up -d
# Backend: http://localhost:8000 | Frontend: http://localhost:3000

# Frontend only (no API calls will work)
cd frontend && npm install && npm run dev

# Backend only
cd backend && pip install -r requirements.txt && python main.py
```

### Testing
- Backend: `pytest` (tests in `backend/tests/`)
- SEO validation: `python backend/test_seo_service.py`
- No formal frontend tests currently (TBD)

### Database Migrations
- Run `python backend/init_db.py` to initialize all tables
- Alembic installed but not actively used yet (direct SQLAlchemy schema)

## Key Files to Reference

### CANON Specification
- `CIMEIKA_CANON_TZ_v1.yaml` - Foundational design principles
- `backend/app/config/canon.py` - Python implementation of CANON constants

### Architecture Documentation
- `docs/ARCHITECTURE.md` - Fixed structure rules
- `docs/MODULE_ORCHESTRATION.md` - Backend/frontend registry system
- `docs/SEO_INTEGRATION.md` - SEO matrix, URL routing, semantic research

### Configuration
- `docker-compose.yml` - PostgreSQL + backend + optional Redis/Celery
- `.env.template` - Required: `OPENAI_API_KEY`, `POSTGRES_*` credentials
- `backend/requirements.txt` - FastAPI 0.104, SQLAlchemy 2.0, Pydantic v2

## Project-Specific Conventions

### Naming
- **Ukrainian** is primary language for UI text (EN for docs/code)
- Module names: lowercase in backend (`ci`, `kazkar`), PascalCase in frontend (`Ci`, `Kazkar`)
- API prefixes match module names: `/api/v1/ci`, `/api/v1/kazkar`, etc.

### No-Gos
- ❌ Don't add/remove modules (7 is canonical)
- ❌ Don't create Flask code (archived in `/archive/flask/`)
- ❌ Don't add root-level directories (structure is fixed per `docs/ARCHITECTURE.md`)
- ❌ Don't put business logic in API routes (belongs in services)
- ❌ Don't use Redux/Context for module state (use Zustand)

### Entry Point Philosophy (CANON)
- Ci is THE action (`ci.capture()`)
- ≤5 seconds to first user action
- No login walls, onboarding, or menus on entry screen
- Stateless action that emits structured events

## SEO Matrix Usage
When working with emotional states or user intents:
1. Reference `backend/app/config/seo/cimeikaseomatrix.yaml`
2. Use `seo_service.get_entry(lang, state, intent)` for canonical titles
3. Build URLs with `seo_service.build_url(lang, state, intent)`
4. Check `seoresearchseeds.yaml` for semantic keyword patterns

## Integration Points
- **PostgreSQL** (primary data store): Models in `backend/app/models/`
- **OpenAI/Anthropic**: AI integrations via env keys (used in Ci orchestration)
- **Redis** (optional): Commented in docker-compose, use for Celery background tasks
- **Vercel**: Frontend deployment config in `vercel.json`, GitHub Actions in `.github/workflows/`

## Common Tasks

**Add new API endpoint to existing module**:
1. Add route function to `backend/app/modules/{module}/api.py`
2. Add service method to `backend/app/modules/{module}/service.py`
3. Update Pydantic schemas in `schema.py` if needed
4. No need to update router registration (already included)

**Add new database field**:
1. Update model in `backend/app/models/{module}_models.py`
2. Update Pydantic schemas in `backend/app/modules/{module}/schema.py`
3. Run `python backend/init_db.py` (drops and recreates tables - dev only!)

**Add new React component to module**:
1. Create in `frontend/src/modules/{Module}/components/`
2. Import in module's view file (`views/{Module}View.tsx`)
3. Theme will auto-apply based on route (see `ThemeManager.jsx`)

**Update SEO matrix entry**:
1. Edit `backend/app/config/seo/cimeikaseomatrix.yaml`
2. Restart backend (SEO service loads on startup)
3. Test with `python backend/test_seo_service.py`
