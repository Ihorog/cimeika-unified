# Cimeika Modules Overview

This document provides an overview of all 7 modules in the Cimeika Unified system.

## Module Architecture

Cimeika is organized into 7 core modules, each with a specific domain responsibility:

1. **Ci** — Central orchestration core
2. **PoDija** — Events and timeline
3. **Nastrij** — Emotional states and mood tracking
4. **Malya** — Ideas and creativity
5. **Kazkar** — Memory and stories
6. **Calendar** — Time management and planning
7. **Gallery** — Media content

## Structure

### Frontend Structure

Each module follows a consistent structure in `frontend/src/modules/<ModuleName>/`:

```
ModuleName/
├── index.ts          # Module exports
├── page.tsx          # Alternative entry point
├── types.ts          # TypeScript type definitions
├── api.ts            # API client functions
├── ui.tsx            # Reusable UI components
├── service.ts        # Legacy service (maintained for compatibility)
├── store.ts          # Zustand state management
├── hooks/            # React hooks
│   └── useModuleName.ts
└── views/            # View components
    └── ModuleNameView.tsx
```

### Backend Structure

Each module has corresponding backend components:

```
backend/
├── api/
│   └── modulename.py      # REST API endpoints
├── models/
│   └── modulename_models.py   # Pydantic DTOs
└── services/
    └── modulename_service.py  # Business logic
```

## Routing

All modules are accessible through clean URLs:

- `/` — Ci Entry Screen (default)
- `/ci` — Ci module
- `/podija` — PoDija module
- `/nastrij` — Nastrij module
- `/malya` — Malya module
- `/kazkar` — Kazkar module
- `/calendar` — Calendar module
- `/gallery` — Gallery module

## Global Navigation

The **Ci FAB (Floating Action Button)** provides global access to:

- Navigation to all 7 modules
- Quick search functionality
- System health status
- Quick actions

The Ci FAB is present on every screen and accessible via a floating button in the bottom-right corner.

## API Prefixes

Each module has its own API prefix:

- `/api/ci/*` — Ci module endpoints
- `/api/podija/*` — PoDija module endpoints
- `/api/nastrij/*` — Nastrij module endpoints
- `/api/malya/*` — Malya module endpoints
- `/api/kazkar/*` — Kazkar module endpoints
- `/api/calendar/*` — Calendar module endpoints
- `/api/gallery/*` — Gallery module endpoints

## Key Endpoints

### Health Check
- `GET /health` — System health status

### Ci Module
- `GET /api/ci/state` — Get Ci state
- `POST /api/ci/chat` — Chat with Ci

### Calendar Module
- `GET /api/calendar/events` — Get all events
- `POST /api/calendar/events` — Create event

### Gallery Module
- `GET /api/gallery/items` — Get all items
- `POST /api/gallery/items` — Create item

### PoDija Module
- `GET /api/podija/timeline` — Get timeline nodes
- `POST /api/podija/timeline` — Create timeline node

### Nastrij Module
- `GET /api/nastrij/state` — Get Nastrij state
- `POST /api/nastrij/mood` — Create mood entry

### Kazkar Module
- `GET /api/kazkar/library` — Get library overview
- `GET /api/kazkar/stories` — Get all stories (formerly entries)
- `GET /api/kazkar/legends` — Get all legends (including Ci legends)
- `POST /api/kazkar/stories` — Create story or legend

> **Note**: Kazkar is the official repository (аптека) for the **Ci Legends Library**. All Ci system legends are stored here with `story_type: "legend"` and tag `"ci"`. See [CI_LEGENDS_PLACEMENT.md](../CI_LEGENDS_PLACEMENT.md) for details.

### Malya Module
- `GET /api/malya/ideas` — Get all ideas
- `POST /api/malya/ideas` — Create idea

## Data Models (DTOs)

### Frontend (TypeScript)
- `CiState`, `CiChatMessage`, `HealthStatus`
- `CalendarEvent`, `CreateEventRequest`
- `GalleryItem`, `CreateGalleryItemRequest`
- `TimelineNode`, `CreateTimelineNodeRequest`
- `NastrijState`, `MoodEntry`, `MoodAnalytics`
- `KazkarEntry`, `KazkarLibrary`
- `MalyaIdea`, `CreateIdeaRequest`

### Backend (Python/Pydantic)
All backend models mirror frontend types with Pydantic validation:
- Located in `backend/models/*_models.py`
- Full validation and serialization support
- Consistent field naming with frontend

## Module Interactions

Modules interact through:

1. **Ci Orchestration** — Central coordination
2. **Shared Context** — Global state management
3. **API Integration** — REST API communication
4. **Event System** — Module-to-module events

## Development Guidelines

### Adding New Features to a Module

1. Define types in `types.ts`
2. Add API functions in `api.ts`
3. Update backend models in `models/`
4. Implement service logic in `services/`
5. Add API endpoints in `api/`
6. Update module documentation in `docs/modules/`

### Module Independence

- Each module is self-contained
- Modules don't import directly from other modules
- Communication through Ci or API only
- No circular dependencies

## Documentation

Detailed documentation for each module is available in `docs/modules/`:

- [Ci Module Documentation](./ci.md)
- [PoDija Module Documentation](./podija.md)
- [Nastrij Module Documentation](./nastrij.md)
- [Malya Module Documentation](./malya.md)
- [Kazkar Module Documentation](./kazkar.md)
- [Calendar Module Documentation](./calendar.md)
- [Gallery Module Documentation](./gallery.md)

## Status

All 7 modules are currently in development status with:

✅ Frontend module structure
✅ Backend API structure
✅ DTO models (frontend & backend)
✅ Service layer (stub implementations)
✅ API endpoints (minimal implementations)
✅ Documentation
✅ Routing
✅ Global Ci FAB navigation

## Next Steps

1. Implement full business logic in services
2. Add database persistence
3. Enhance UI components
4. Add comprehensive testing
5. Implement inter-module communication
6. Add real-time features with WebSockets
7. Deploy to production environment
