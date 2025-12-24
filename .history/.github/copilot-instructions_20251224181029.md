# GitHub Copilot Instructions — Cimeika Unified

**Cimeika** is a family memory & planning hub with a fixed 7-module architecture. This is a production system with deterministic structure — **do not modify architecture without explicit direction**.

---

## Project Architecture

### Root Structure (FIXED — Do Not Change)
```
cimeika-unified/
├─ backend/          # FastAPI + SQLAlchemy
├─ frontend/         # React 18 + Vite
├─ docs/            # Architecture docs
├─ infra/           # Docker configs
├─ scripts/         # Utility scripts
└─ .github/         # CI/CD + instructions
```

### The 7 Fixed Modules (Core to the Product)
1. **Ci** — Central orchestration core, entry point action `ci.capture()`
2. **Kazkar** — Memory, stories, legends (night theme)
3. **Podija** — Events, future, scenarios
4. **Nastrij** — Emotional states, context
5. **Malya** — Ideas, creativity, innovations
6. **Gallery** — Visual archive, media, print
7. **Calendar** — Time, rhythms, planning

**CANON**: See `CIMEIKA_CANON_TZ_v1.yaml` — the single entry action is `ci.capture()` which classifies and routes to appropriate modules.

---

## Backend (Python 3.11+)

### Stack
- **FastAPI** (main framework, not Flask)
- **SQLAlchemy 2.0** (ORM)
- **Pydantic v2** (schemas)
- **PostgreSQL** (database)

### Module Standard Structure
```
backend/app/modules/<module>/
├─ api.py        # FastAPI routes ONLY (no business logic)
├─ service.py    # Business logic + implements ModuleInterface
├─ model.py      # SQLAlchemy ORM models
├─ schema.py     # Pydantic request/response schemas
└─ __init__.py
```

### Module Interface Pattern (CRITICAL)
All services MUST implement `ModuleInterface` from `app.core.interfaces`:

```python
from app.core.interfaces import ModuleInterface

class MyModuleService(ModuleInterface):
    def get_name(self) -> str:
        return "my_module"
    
    def get_status(self) -> Dict[str, Any]:
        return {"status": "active", "initialized": self._initialized}
    
    def initialize(self) -> bool:
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        # cleanup logic
        return True
```

### Module Registration
Modules are registered in `backend/app/startup.py` using the `registry` singleton from `app.core.orchestrator`:

```python
from app.core import registry
from app.modules.ci.service import CiService

ci_service = CiService()
registry.register('ci', ci_service)
```

**Rule**: Services instantiate ONCE globally in `startup.py`, then registered. Never create multiple instances.

### API Routing
- All routes through `backend/app/api/v1/router.py`
- Module routes: `/api/v1/{module}/...`
- Module APIs register via: `router.include_router(module_router)`
- See live docs at `http://localhost:8000/api/docs`

### SEO Matrix System
Specialized content system at `.governance/seo/cimeika_seo_matrix.yaml`:
- 7 modules × 7 traffic categories = 49 content patterns
- Service: `app.config.seo.seo_matrix_service.SeoMatrixService`
- URL format: `/{lang}/{module}/{category}[/page]`
- Example: `/en/ci/use_cases`, `/ua/kazkar/examples`

---

## Frontend (React 18)

### Stack
- **React 18** (hooks, no class components)
- **Vite** (dev server + build)
- **React Router** (routing)
- **No TypeScript** (uses `.jsx` not `.ts`)
- **No Zustand yet** (mentioned in old docs but not implemented)

### Module Standard Structure
```
frontend/src/modules/<module>/
├─ <Module>View.jsx   # Main view component
├─ components/        # Module-specific components
└─ index.js          # Exports
```

**Note**: Frontend uses lowercase module names in paths but PascalCase for components (`kazkar` → `KazkarView`).

### Deterministic Theme System
Theme is determined by route, not state. See `frontend/src/core/ThemeManager.jsx`:

```jsx
const THEME_MAP = {
  '/kazkar': 'night',  // ONLY Kazkar gets night theme
  // All others: 'day'
};
```

**Rule**: Theme changes are automatic on navigation. Do NOT add theme toggles or user preferences — theme follows module identity.

### Global Components
- **CiOverlay** (`frontend/src/components/CiOverlay.jsx`) — Global assistant, available everywhere
- **MainLayout** (`frontend/src/layouts/MainLayout.jsx`) — Root layout with navigation

### Routing
Routes defined in `frontend/src/App.jsx`:
```jsx
<Route path="ci" element={<CiView />} />
<Route path="kazkar" element={<KazkarView />} />
// etc.
```

Default route redirects to `/ci` (entry point).

---

## Development Workflows

### Local Development (Docker)
```bash
# 1. Setup environment
cp .env.template .env
# Edit .env with your keys (OPENAI_API_KEY required for chat)

# 2. Start everything
docker-compose up -d

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Frontend Only (No Backend)
```bash
cd frontend
npm install
npm run dev
# http://localhost:5173 (Vite default) or http://localhost:3000
```
Works for UI development but API calls will fail (ERR_CONNECTION_REFUSED is expected).

### Backend Database Init
```bash
cd backend
python init_db.py  # Creates tables from SQLAlchemy models
```

### Testing SEO Matrix
```bash
cd backend
python test_seo_matrix_service.py  # Unit tests for SEO system
```

---

## Key Patterns & Conventions

### No Circular Imports
- Core (`backend/app/core/`) orchestrates modules via interfaces
- Core NEVER imports from modules directly
- Modules MAY import from core (interfaces, orchestrator)
- Modules NEVER import from each other

### API First Development
1. Define Pydantic schema in `schema.py`
2. Create route in `api.py` with type hints
3. Implement business logic in `service.py`
4. OpenAPI docs generate automatically

### Stateless Entry Point (CANON)
The `ci.capture()` action is stateless:
- No login required
- Receives raw event (text/voice/image)
- Classifies to appropriate module
- Returns structured event + context
- Goal: action in ≤5 seconds

### Commit Style
```
feat(module): add new feature
fix(module): resolve bug
docs: update documentation
refactor(module): restructure without behavior change
chore: dependency updates, configs
```

---

## Critical Files to Know

| File | Purpose |
|------|---------|
| `CIMEIKA_CANON_TZ_v1.yaml` | Product principles & entry action spec |
| `docs/ARCHITECTURE.md` | Full architecture reference |
| `docker-compose.yml` | Service orchestration (postgres, backend, frontend) |
| `backend/app/startup.py` | Module registration & initialization |
| `backend/app/core/orchestrator.py` | Module registry implementation |
| `backend/app/api/v1/router.py` | API route aggregation |
| `frontend/src/App.jsx` | React routing & module navigation |
| `frontend/src/core/ThemeManager.jsx` | Deterministic theme system |
| `.governance/seo/cimeika_seo_matrix.yaml` | SEO content strategy |

---

## When You're Unsure

1. **Check docs first**: `docs/ARCHITECTURE.md`, `docs/MODULE_ORCHESTRATION.md`
2. **Find examples**: Look at existing module (e.g., `kazkar` or `ci`)
3. **Ask, don't guess**: This is a production system with intentional structure
4. **Read CANON**: `CIMEIKA_CANON_TZ_v1.yaml` defines core behavior

**Never**: Create new root directories, add state management not in pattern, bypass module orchestration, change theme logic.

---

## Questions to Iterate On

- Are there specific module interaction patterns I should document?
- Should I detail the CI Legends subsystem (ciwiki integration)?
- Any database migration patterns I should cover?
- Should I document the Vercel deployment workflow?
