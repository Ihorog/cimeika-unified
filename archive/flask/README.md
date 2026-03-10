# Flask Backend Archive

This code was archived during architecture normalization (2025-12-23).
FastAPI is now the single backend framework.

## Archived Content

### `/api/` - Original Flask API modules
- Legacy Flask-based API endpoints for all 7 modules
- Archived: 2025-12-23

### `/server/` - Flask servers and utilities
- `cit_server.py` - Original Flask server with UI routes and registry
- `cit_ui_pwa.py` - PWA UI server
- `jobs.py`, `job_store.py` - Job management utilities
- `openai_client.py` - OpenAI integration
- Archived: 2026-03-10

### `/ci/server/` - CI fallback Flask API
- `fallback_api.py` - Simple Flask echo API
- `cit_ui_pwa.py` - PWA UI server
- Multiple backup files from various iterations
- Archived: 2026-03-10

## Migration Note

All functionality has been reimplemented in FastAPI backend (`/backend/main.py`).

Archived for reference and potential rollback only.
