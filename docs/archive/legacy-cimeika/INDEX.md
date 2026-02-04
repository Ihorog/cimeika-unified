# Legacy Cimeika Archive

## Source
Repository: `Ihorog/cimeika`  
Archived: 2026-02-04  
Reason: System consolidation into cimeika-unified

## Description
This directory contains archived assets from the legacy Cimeika prototype repository. The repository was a mixed HTML/Next.js/Gradle hybrid that served as an early prototype for the Cimeika ecosystem.

## Status
**DEPRECATED** - No active development. Preserved for historical reference and intellectual asset retention.

## Contents

### Documentation Files
- **TECH_SPEC.md** - Technical specification and optimization requirements (Ukrainian)
- **cimeika_project.md** - Project documentation describing the Cimeika system concept and Ci agent
- **cimeika.config.yaml** - Centralized configuration for API keys and environment modes
- **cimeika-api.yaml** - OpenAPI specification for the Cimeika API
- **README_quickstart.md** - Quick start guide for local development and Hugging Face deployment
- **requirements.txt** - Python dependencies (Flask, requests, gunicorn, python-dotenv)

### Key Features Documented
1. **API Structure**: Base URL, endpoints for story/scene, gallery/feed, weights/recompute, events/notify, telemetry
2. **Frontend Requirements**: React/Vite/Tailwind, bundle optimization ≤2.5 MB, Framer Motion animations ≥60 FPS
3. **Backend Requirements**: Modular routes, daily pipelines, JSON logging, Telegram/Email notifications
4. **CI/CD**: GitHub Actions with linting, testing, and Hugging Face Space deployment
5. **Acceptance Criteria**: Performance targets, accessibility (WCAG AA), weight thresholds

## Architecture Notes
- Mixed technology stack (HTML + Next.js + Gradle)
- Targeted Hugging Face Space for deployment
- Emphasis on mobile optimization and performance
- Integration with OpenAI, OpenWeather, Telegram, and GitHub APIs

## Related Archives
- Orchestra scripts: See `abilities/dormant/orchestra/`
- Real-time implementation: See `docs/archive/legacy-realtime/`

## Migration Notes
Assets from this repository have been preserved to maintain institutional knowledge about:
- Early system architecture decisions
- API design patterns
- Configuration management approaches
- Deployment strategies for Hugging Face Spaces

---

*For current active development, see the main cimeika-unified repository structure.*
