# Cimeika Unified Architecture

This document describes the fixed architecture structure of the Cimeika Unified project.

## Root Structure

```
cimeika-unified/
├─ backend/          # Python backend (FastAPI + Flask)
├─ frontend/         # React frontend (TypeScript + Vite)
├─ docs/             # Documentation
├─ infra/            # Infrastructure configuration
├─ scripts/          # Utility scripts
└─ .github/          # GitHub configuration and Copilot instructions
```

**Note:** This structure is fixed. No additional root-level directories should be created.

## Backend Structure

```
backend/app/
├─ core/             # Core orchestration and module coordination
├─ modules/          # 7 fixed modules
│  ├─ ci/           # Central orchestration core
│  ├─ kazkar/       # Memory, stories, legends
│  ├─ podija/       # Events, future, scenarios
│  ├─ nastrij/      # Emotional states, context
│  ├─ malya/        # Ideas, creativity, innovations
│  ├─ gallery/      # Visual archive, media
│  └─ calendar/     # Time, rhythms, planning
├─ api/             # API layer (v1)
├─ models/          # Database models (shared)
├─ services/        # Business services (shared)
├─ config/          # Configuration
└─ utils/           # Utility functions
```

### Module Standard Structure

Each module follows this structure:
```
module/
├─ __init__.py
├─ api.py           # API routes only
├─ service.py       # Business logic
├─ model.py         # ORM models
├─ schema.py        # Pydantic schemas
└─ config.py        # Module configuration
```

## Frontend Structure

```
frontend/src/
├─ app/             # App-level components and configuration
├─ components/      # Shared components
├─ modules/         # 7 fixed modules (mirror backend)
│  ├─ Ci/          # Central orchestration core
│  ├─ Kazkar/      # Memory, stories, legends
│  ├─ Podija/      # Events, future, scenarios
│  ├─ Nastrij/     # Emotional states, context
│  ├─ Malya/       # Ideas, creativity, innovations
│  ├─ Gallery/     # Visual archive, media
│  └─ Calendar/    # Time, rhythms, planning
├─ stores/         # Global state management
├─ services/       # Shared services
├─ styles/         # Global styles
└─ assets/         # Static assets
```

### Module Standard Structure

Each module follows this structure:
```
Module/
├─ views/          # UI orchestration (no business logic)
├─ components/     # Module-specific components
├─ hooks/          # Custom React hooks
├─ service.ts      # API and data layer
├─ store.ts        # State management (Zustand)
└─ index.ts        # Module exports
```

## Technology Stack

### Backend
- Python ≥ 3.11
- FastAPI (primary API framework)
- SQLAlchemy 2.0 (ORM)
- Pydantic v2 (schemas)
- PostgreSQL (database)
- Redis (cache)

### Frontend
- React 18
- TypeScript (strict mode enabled)
- Zustand (state management)
- Vite (build tool)
- Tailwind CSS (styling)

## Rules

1. **No structural changes** without explicit instruction
2. **Module names are fixed** - cannot be changed
3. **One file, one responsibility**
4. **No circular imports**
5. **Core does not contain domain logic**
6. **Views do not contain business logic**
7. **No direct imports between modules** (use core/API)

## Module Registry

The core orchestrator maintains a registry of all modules. Modules communicate through this registry, not directly.

---

For detailed instructions, see `.github/copilot-instructions.md`
