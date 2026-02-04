---
source: Ihorog/cimeika-real-time-data-app
archived: 2026-02-04
reason: System consolidation - architectural reference only
---

# Real-Time Core Structure Reference

This document provides an architectural overview of the backend/ and core/ directories from the cimeika-real-time-data-app repository.

## Backend Structure

The backend directory contained a FastAPI application with the following organization:

```
backend/
├── main.py                    # Main FastAPI application entry point
├── routers/                   # Module-specific route handlers
│   ├── ci.py                 # Central orchestration endpoints
│   ├── podia.py              # Event management endpoints
│   ├── nastiy.py             # Mood tracking endpoints
│   ├── mala.py               # Creative endpoints
│   ├── kazkar.py             # Story endpoints
│   ├── calendar.py           # Calendar endpoints
│   └── gallery.py            # Gallery endpoints
├── utils/                     # Utility modules
│   ├── connectors.py         # HTTP connectors to upstream APIs
│   ├── orchestrator.py       # Task orchestration utilities
│   └── sense_engine.py       # Resonance scoring system
├── config.py                  # Configuration management
└── tests/                     # Test suite
```

## Core Structure

The core directory provided orchestration and sense utilities:

```
core/
├── orchestrator.py            # TaskOrchestrator, PriorityTaskScheduler
├── sense_node.py              # SenseNode resonance helpers
└── visual_axis_manifest.json # PLUS/MINUS axis definitions
```

## Key Architectural Patterns

### 1. Module-Based Routing
Each Cimeika module (Ci, ПоДія, Настрій, Маля, Казкар, Календар, Галерея) had dedicated routers that exposed REST endpoints.

### 2. Connector Pattern
The `connectors.py` module provided HTTP bridges to upstream APIs, with timeout/error handling and graceful fallbacks.

### 3. Orchestration Layer
The orchestrator utilities enabled:
- Task priority scheduling
- Module coordination
- Event dispatching

### 4. Sense Engine
Implemented resonance scoring based on visual axis manifests (PLUS/MINUS balance).

## Integration Points

- Frontend called FastAPI endpoints at `http://localhost:8000`
- Routers delegated to orchestrator helpers
- Connectors proxied to upstream Cimeika API
- Sense engine provided resonance metadata

## Deployment Context

- Designed for Hugging Face Space deployment
- Used Docker with non-root user
- GitHub Actions for CI/CD
- Environment variables for configuration

---

**Note**: This is a structural reference only. The actual implementation resides in the archived repository. For full code details, see the original repository or archived documentation.
