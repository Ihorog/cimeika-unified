# Legacy Real-Time Data App Archive

## Source
Repository: `Ihorog/cimeika-real-time-data-app`  
Archived: 2026-02-04  
Reason: System consolidation into cimeika-unified

## Description
This directory contains archived documentation and specifications from the Cimeika real-time data application. This was an extensive prototype featuring FastAPI backend, Next.js frontend, and comprehensive audit documentation.

## Status
**DEPRECATED** - Extensive documentation preserved for reference. Real-time functionality has been integrated into cimeika-unified.

## Contents

### Architecture Documentation
- **ARCHITECTURE.md** - Complete system architecture overview
- **AGENTS.md** - Agent specifications and roles (Ci, ПоДія, Настрій, Маля, Казкар, Календар, Галерея)
- **cimeika_schema.json** - Module schema with endpoints and UI mappings
- **cimeika-api.yaml** - OpenAPI specification for orchestration API
- **swagger.json** - Complete Swagger/OpenAPI documentation

### Audit Reports
- **AUDIT_FINAL_REPORT.md** - Comprehensive final audit summary
- **AUDIT_BASELINE.md** - Baseline architectural state and risks
- **AUDIT_DEPENDENCIES.md** - npm and pip dependency audit
- **AUDIT_ECONOMIC.md** - Economic analysis and monetization strategies
- **AUDIT_INTEGRITY.md** - Code integrity and consistency checks
- **AUDIT_PERFORMANCE.md** - Performance optimization findings
- **AUDIT_SECURITY.md** - Security audit and vulnerability assessment
- **AUDIT_UX.md** - User experience improvements and changes

## Key System Components

### 7 Core Modules
1. **Ci (Ці)** - Central orchestration and coordination
2. **ПоДія (Podija)** - Events, scenarios, timelines
3. **Настрій (Nastiy)** - Mood tracking and advice
4. **Маля (Mala)** - Creative canvas and ideas
5. **Казкар (Kazkar)** - Story archive and narratives
6. **Календар (Calendar)** - Time nodes and schedules
7. **Галерея (Gallery)** - Images, memories, uploads

### Technology Stack
- **Frontend**: Next.js 16, Turbopack, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, Python
- **Node API**: Express.js v1
- **Deployment**: Hugging Face Space, GitHub Actions

## Audit Findings Summary

### Security
- API base URL validation implemented
- Path traversal protection in gallery
- Docker non-root user configuration
- Identified axios CVE requiring update

### Performance
- Unified API client with error handling
- Gallery caching (realpath/readdir with 5s TTL)
- TodayWidget non-blocking state updates
- Turbopack build optimization

### Dependencies
- Node.js 20.19.6 requirement
- FastAPI 0.124.0 upgrade recommended
- axios vulnerability (High) needs addressing

### UX Improvements
- Notification state management
- uk-UA localization consistency
- Tailwind directive ordering
- HTML entity cleanup

## Economic Model Insights

### Monetization Strategies
- Core subscription (B2C/B2B2C)
- API licensing for integrations
- Paid add-ons (stories, creative sessions, galleries)
- Content library (ciwiki pro)
- White-label solutions for partners

### Optimization Targets
- Bundle optimization: ≤2.5 MB
- Animation performance: ≥60 FPS
- Contrast ratio: ≥4.5:1 (WCAG AA)
- Response time reduction: -20%
- CPU/IOps reduction: -15%

## Architectural Patterns

### Orchestration Layer
- TaskOrchestrator for module coordination
- PriorityTaskScheduler for task management
- SimpleTaskExecutor for execution
- SenseNode for resonance scoring

### Connector Pattern
- HTTP bridges to upstream APIs
- Timeout and error handling
- Graceful fallbacks
- httpx-based implementation

### Module Integration
- Router-per-module architecture
- Shared design tokens
- Centralized API client
- Resonance metadata in responses

## Deployment Notes

### Hugging Face Space
- Dockerfile with non-root user
- Environment variable configuration
- Deploy script: `deploy_cimeika_api.sh`
- Required: `HF_TOKEN`, `OPENAI_API_KEY`

### Local Development
```bash
# Backend
uvicorn backend.main:app --reload --port 8000

# Frontend
npm run dev
```

## Migration to Unified

Key concepts integrated into cimeika-unified:
- 7-module structure
- Orchestration patterns
- API design principles
- Security best practices
- Performance optimizations
- Economic modeling

## Related Archives
- Core structure reference: See `abilities/dormant/realtime-core/`
- Legacy prototype: See `docs/archive/legacy-cimeika/`
- Template scaffold: See `docs/archive/legacy-cimejka/`

## Research Value

This archive provides valuable insights into:
- Real-time system architecture
- Module orchestration strategies
- Security audit methodologies
- Performance optimization techniques
- Economic modeling for AI platforms
- UX patterns for complex applications

---

*This extensive documentation serves as institutional knowledge for future development decisions.*
