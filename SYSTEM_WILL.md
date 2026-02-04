# Cimeika System Will — Guidance for AI Agents

---

## PURPOSE

This document explains to AI agents how to work effectively within the Cimeika ecosystem. It defines the system's philosophy, architecture principles, and operational guidelines that all AI agents must follow when contributing to the codebase.

**Target Audience:** GitHub Copilot, Claude, GPT, and other AI coding assistants

---

## CORE PHILOSOPHY

### The Cimeika Way

Cimeika is an integrated life management platform built around **7 specialized modules** coordinated by a **central Ci core**. The system follows these fundamental principles:

1. **Modularity** — Each module is self-contained but interconnected
2. **Orchestration** — Ci core coordinates all module interactions
3. **Self-Improvement** — The system detects gaps and suggests enhancements
4. **Documentation First** — All behavior must be documented before implementation
5. **Anti-Repeat Principle** — Eliminate all repeated actions permanently

---

## REPOSITORY STRUCTURE

```
cimeika-unified/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── core/              # Core system components
│   │   │   ├── manifest.json         # Tool registry (SOURCE OF TRUTH)
│   │   │   ├── self_improvement.py   # Auto-improvement mechanism
│   │   │   ├── config.py             # Configuration management
│   │   │   └── orchestrator.py       # Module coordination
│   │   ├── modules/           # 7 specialized modules
│   │   │   ├── ci/           # Central orchestration
│   │   │   ├── kazkar/       # Memory & legends
│   │   │   ├── podija/       # Events & futures
│   │   │   ├── nastrij/      # Emotional states
│   │   │   ├── malya/        # Ideas & creativity
│   │   │   ├── gallery/      # Visual media
│   │   │   └── calendar/     # Time management
│   │   ├── api/              # API routes
│   │   └── models/           # Database models
│   └── main.py               # Application entry point
├── frontend/                  # React + Vite frontend
│   └── src/
│       ├── modules/          # UI for each backend module
│       └── components/       # Shared components
├── docs/                     # Documentation
├── .github/                  # CI/CD and Copilot instructions
│   └── copilot-instructions.md    # Global rules (canonical)
└── SYSTEM_WILL.md           # This file — AI guidance

```

---

## THE 7 MODULES

Each module represents a distinct aspect of life management:

| Module | Ukrainian | Purpose | Color Theme |
|--------|-----------|---------|-------------|
| **Ci** | Ці | Central orchestration, coordination | Day |
| **Kazkar** | Казкар | Memory, stories, legends | Night |
| **Podija** | Подія | Events, future scenarios | Day |
| **Nastrij** | Настрій | Emotional states, moods | Day |
| **Malya** | Маля | Ideas, creativity, innovation | Day |
| **Gallery** | Галерея | Visual archive, media | Day |
| **Calendar** | Календар | Time, rhythms, planning | Day |

### Module Communication

- All inter-module communication goes through **Ci Core**
- Modules never call each other directly
- Use orchestrator pattern defined in `backend/app/core/orchestrator.py`

---

## SELF-IMPROVEMENT MECHANISM

### What It Is

The self-improvement mechanism (`backend/app/core/self_improvement.py`) automatically:
1. Detects missing or inactive tools in the manifest
2. Generates detailed GitHub Issue descriptions
3. Suggests implementation steps
4. Maintains tool registry consistency

### How It Works

1. **Tool Registry** — `manifest.json` is the source of truth for all tools
2. **Validation** — Regularly checks if required tools are present and active
3. **Issue Generation** — Creates comprehensive GitHub Issues for missing tools
4. **Auto-Documentation** — Each generated issue includes implementation guidance

### Using the Mechanism

```bash
# Validate all tools
python -m app.core.self_improvement validate

# Generate issue for specific tool
python -m app.core.self_improvement generate-issue <tool_id> <reason>

# Full report with all issues
python -m app.core.self_improvement report
```

### When to Use

**AI agents should run validation:**
- Before starting major feature work
- After adding new modules or tools
- When encountering "tool not found" errors
- As part of PR checklist

---

## MANIFEST.JSON — Tool Registry

**Location:** `backend/app/core/manifest.json`

**Purpose:** Single source of truth for all tools, modules, and integrations

### Tool Schema

```json
{
  "id": "unique_tool_id",
  "name": "Human Readable Name",
  "description": "What this tool does",
  "status": "active|inactive|deprecated",
  "category": "core|module|service|integration",
  "endpoints": ["/api/v1/tool/endpoint"],
  "dependencies": ["ci_core"],
  "external_dependencies": ["ENV_VAR_NAME"]
}
```

### Tool Categories

- **core** — Essential system components (e.g., ci_core, orchestrator)
- **module** — One of the 7 main modules (kazkar, podija, etc.)
- **service** — Supporting services (SEO, analytics, etc.)
- **integration** — External API integrations (OpenAI, etc.)

### Adding New Tools

1. Define tool in `manifest.json` following the schema
2. Implement functionality in appropriate directory
3. Register endpoints in FastAPI router
4. Update this documentation
5. Run validation: `python -m app.core.self_improvement validate`

---

## WORKFLOW FOR AI AGENTS

### Standard Development Flow

Follow this sequence for ALL changes:

```
1. Plan
   ↓
2. Document (update docs if needed)
   ↓
3. Implement in feature branch
   ↓
4. Test & Validate
   ↓
5. Run self-improvement validation
   ↓
6. Create Pull Request
   ↓
7. Wait for human approval
   ↓
8. Merge
```

### Pre-Implementation Checklist

Before making changes, AI agents must:

- [ ] Read `SYSTEM_WILL.md` (this file)
- [ ] Check `.github/copilot-instructions.md` for global rules
- [ ] Validate current tool manifest: `python -m app.core.self_improvement validate`
- [ ] Review relevant module documentation in `docs/`
- [ ] Understand dependencies in `manifest.json`
- [ ] Check for existing similar implementations

### Implementation Checklist

When implementing features:

- [ ] Make minimal, surgical changes only
- [ ] Follow existing code patterns and structure
- [ ] Update `manifest.json` if adding new tools
- [ ] Document all changes in relevant docs
- [ ] Add/update tests for new functionality
- [ ] Run linters and tests
- [ ] Validate with self-improvement mechanism
- [ ] Create comprehensive PR description

### Post-Implementation Checklist

After implementation:

- [ ] All tests pass
- [ ] Linting passes
- [ ] Self-improvement validation passes
- [ ] Documentation is updated
- [ ] PR description explains what, why, and how
- [ ] Security considerations addressed
- [ ] No secrets in code
- [ ] Rollback plan documented

---

## ANTI-REPEAT PRINCIPLE

**Core Rule:** Any repeated action is a system failure.

### What Counts as a Repeat?

- Running the same manual command twice
- Encountering the same error twice
- Following the same manual steps for standard tasks
- Copy-pasting similar code without abstraction

### How to Eliminate Repeats

When you detect a repeat:

1. **Identify root cause** — Why did this repeat happen?
2. **Create automation** — Script, function, or tool to prevent it
3. **Update manifest** — Add new tool to `manifest.json`
4. **Document** — Explain the automation in relevant docs
5. **Test** — Ensure the issue cannot reoccur

### Examples

❌ **Bad:** Manually running database migrations every time
✅ **Good:** Add migration script to `Makefile`, document in README

❌ **Bad:** Copying the same endpoint pattern for each module
✅ **Good:** Create endpoint generator or base class

❌ **Bad:** Manually validating tool availability each PR
✅ **Good:** Self-improvement mechanism auto-validates (already implemented!)

---

## FROZEN REPOSITORIES

**CRITICAL:** Some repositories are read-only for AI agents.

### cit_versel

- **Status:** STRICTLY FROZEN
- **Actions:** NO changes, NO deployment, NO workflows
- **Reason:** Production stability and safety

**Do NOT:**
- Modify any files in `cit_versel`
- Create PRs against `cit_versel`
- Run any commands affecting `cit_versel`
- Suggest changes to `cit_versel`

**If changes are needed:**
- Discuss with human maintainer first
- Human will decide if/how to proceed

---

## CODING STANDARDS

### Python (Backend)

```python
# File structure
"""Module docstring explaining purpose"""

from typing import Dict, List, Optional
import standard_libs
import third_party_libs
from app.module import local_imports

class MyClass:
    """Class docstring"""
    
    def method(self, param: str) -> Dict:
        """Method docstring with types"""
        pass
```

**Standards:**
- Type hints for all function signatures
- Docstrings for modules, classes, and public methods
- Follow PEP 8 style guide
- Use `black` formatter
- Use `pylint` for linting

### TypeScript (Frontend)

```typescript
// Component structure
import React from 'react';
import { useState } from 'react';
import type { MyType } from './types';

interface Props {
  title: string;
  onAction?: () => void;
}

export const MyComponent: React.FC<Props> = ({ title, onAction }) => {
  // Implementation
};
```

**Standards:**
- TypeScript strict mode
- Props interfaces for all components
- Use functional components with hooks
- ESLint configuration from `.eslintrc.cjs`

### General

- **English** — Code and comments in English
- **Ukrainian** — User-facing text and documentation in Ukrainian
- **Minimal Changes** — Change only what's necessary
- **No Secrets** — Never commit credentials or API keys

---

## ERROR HANDLING

### When You Encounter Errors

1. **Check manifest** — Is the tool registered and active?
2. **Check dependencies** — Are all dependencies available?
3. **Check logs** — What does the error actually say?
4. **Check docs** — Is there guidance for this scenario?
5. **Use self-improvement** — Run validation to detect issues

### Common Issues

| Error | Check | Solution |
|-------|-------|----------|
| Tool not found | `manifest.json` | Add tool definition |
| Import error | Dependencies | Check `requirements.txt` |
| API endpoint 404 | Route registration | Register in router |
| Module missing | Structure | Create module directory |

---

## TESTING REQUIREMENTS

### Backend Tests

```bash
# Run all tests
cd backend
pytest

# Run specific test
pytest tests/test_module.py

# Run with coverage
pytest --cov=app
```

### Frontend Tests

```bash
# Run all tests
cd frontend
npm test

# Run linting
npm run lint
```

### Integration Tests

- Test full user flows
- Verify module orchestration
- Check API endpoints
- Validate database operations

---

## SECURITY GUIDELINES

### Never Commit

- API keys or secrets
- Database credentials
- User data
- Private keys or certificates

### Always Use

- Environment variables for secrets
- `.env` files (gitignored)
- GitHub Secrets for CI/CD
- Proper authentication/authorization

### Validate

- All user input
- All external data
- All API responses
- All file uploads

---

## DOCUMENTATION HIERARCHY

When uncertain, consult in this order:

1. **`.github/copilot-instructions.md`** — Global rules (HIGHEST AUTHORITY)
2. **`SYSTEM_WILL.md`** — This file (system guidance)
3. **`docs/ARCHITECTURE.md`** — System architecture
4. **`README.md`** — Project overview
5. **Module-specific docs** — In `docs/` directory
6. **Code comments** — Inline documentation

### When Documentation Is Missing

1. **STOP** — Don't guess or proceed blindly
2. **ASK** — Request clarification from human
3. **DOCUMENT** — Add missing documentation first
4. **IMPLEMENT** — Only after docs are clear

---

## COMMON TASKS

### Adding a New Module

1. Check if module is in `manifest.json` — if not, add it
2. Create module directory: `backend/app/modules/<module_name>/`
3. Create required files:
   - `__init__.py`
   - `routes.py` — API endpoints
   - `service.py` — Business logic
   - `models.py` — Database models
4. Register routes in main router
5. Add tests: `backend/tests/test_<module_name>.py`
6. Update documentation
7. Run validation

### Adding an API Endpoint

1. Define in appropriate `routes.py`
2. Add endpoint to `manifest.json`
3. Implement handler function
4. Add request/response models
5. Add tests
6. Update API documentation

### Fixing a Bug

1. Reproduce the bug
2. Write a failing test
3. Fix the bug (minimal change)
4. Verify test passes
5. Check for similar bugs elsewhere
6. Document the fix
7. Consider: does this prevent repeats?

### Refactoring

1. **DON'T** refactor without explicit permission
2. If approved:
   - Preserve all functionality
   - Add tests first
   - Refactor incrementally
   - Verify nothing breaks
   - Update documentation

---

## ENVIRONMENT SETUP

### Required Environment Variables

Check `.env.example` for full list. Critical ones:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/cimeika

# API Keys
OPENAI_API_KEY=sk-...  # For AI chat

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Setup Commands

```bash
# First-time setup
make setup

# Start development
make dev

# Run tests
make test

# Run linters
make lint

# Database init
make db-init
```

---

## VERSION CONTROL

### Branch Naming

```
feature/<feature-name>
fix/<bug-name>
docs/<doc-update>
refactor/<component-name>
```

### Commit Messages

```
<type>: <short description>

<optional longer description>

<optional footer>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Requests

**Title:** Clear, concise description

**Body must include:**
- What changed
- Why it changed
- How it was tested
- Related issues
- Risk assessment
- Rollback plan

---

## INTEGRATION WITH OTHER TOOLS

### GitHub Actions

CI/CD pipelines run automatically:
- Linting
- Testing
- Type checking
- Security scanning

**Never skip CI checks**

### Docker

Local development uses Docker Compose:

```bash
docker-compose up -d      # Start all services
docker-compose logs -f    # View logs
docker-compose down       # Stop services
```

### Vercel

Frontend deployment:
- Auto-deploys from `main` branch
- Preview deployments for PRs
- Environment variables in Vercel dashboard

---

## PERFORMANCE CONSIDERATIONS

### Backend

- Use async/await for I/O operations
- Implement caching where appropriate
- Optimize database queries
- Use pagination for large datasets

### Frontend

- Lazy load components
- Optimize images
- Minimize bundle size
- Use React.memo for expensive renders

---

## MONITORING & OBSERVABILITY

### Logging

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)
```

### Health Checks

- `/health` — Basic health check
- `/ready` — Readiness check (DB, external services)
- Monitor these in production

---

## WHEN TO ASK FOR HELP

AI agents should request human guidance when:

- Documentation is unclear or contradictory
- Changes would affect multiple modules
- Security implications are uncertain
- Breaking changes might be needed
- Architectural decisions are required
- Frozen repositories need changes
- Task is outside defined scope

**It's better to ask than to guess wrong.**

---

## QUALITY STANDARDS

Before submitting any PR:

✅ Code follows style guide
✅ All tests pass
✅ Linting passes
✅ Documentation is updated
✅ No secrets committed
✅ Self-improvement validation passes
✅ PR description is complete
✅ Changes are minimal and focused

---

## CONTINUOUS IMPROVEMENT

This document should evolve. When you:

- Discover a gap in documentation
- Find a repeated pattern
- Identify a common mistake
- Learn something important

**→ Update this document**

File format: Markdown
Location: Repository root
Maintenance: Continuous

---

## EMERGENCY PROCEDURES

### If Production Breaks

1. **DON'T PANIC** — Human will handle
2. **DON'T PUSH FIXES** — Frozen deployment
3. **DO DOCUMENT** — What went wrong
4. **DO ASSIST** — Help diagnose if asked

### If Tests Fail

1. Check if issue is related to your changes
2. If yes: fix it
3. If no: report to human maintainer
4. Don't suppress or skip failing tests

### If Security Issue Found

1. **STOP** — Don't commit or push
2. **NOTIFY** — Alert human immediately
3. **DOCUMENT** — Record what you found
4. **WAIT** — For guidance on resolution

---

## PHILOSOPHICAL GUIDELINES

### Think Like Cimeika

- **Harmony** — All parts work together
- **Clarity** — Clear > clever
- **Sustainability** — Build for maintenance
- **Reliability** — Predictable behavior
- **Growth** — Self-improvement built-in

### Decision Framework

When making decisions:

1. **Does it follow global instructions?**
2. **Does it eliminate repeats?**
3. **Is it minimal and surgical?**
4. **Is it documented?**
5. **Is it testable?**

If all yes → proceed
If any no → reconsider

---

## FINAL REMINDERS

1. **Read global instructions first** — `.github/copilot-instructions.md`
2. **Update manifest when adding tools** — `manifest.json`
3. **Run self-improvement validation** — Before every PR
4. **Document everything** — Code, decisions, rationale
5. **Make minimal changes** — Touch only what's needed
6. **Test thoroughly** — No untested code
7. **Ask when uncertain** — Better than guessing
8. **Never commit secrets** — Use environment variables
9. **Respect frozen repos** — `cit_versel` is off-limits
10. **Human approval required** — Always wait for merge approval

---

## RESOURCES

### Documentation
- Global Rules: `.github/copilot-instructions.md`
- Architecture: `docs/ARCHITECTURE.md`
- API Reference: `API_REFERENCE.md`
- Quick Start: `QUICKSTART_DEV.md`

### Tools
- Self-Improvement: `backend/app/core/self_improvement.py`
- Manifest: `backend/app/core/manifest.json`
- Orchestrator: `backend/app/core/orchestrator.py`

### External
- GitHub Repository: https://github.com/Ihorog/cimeika-unified
- Wiki: https://github.com/Ihorog/ciwiki

---

**VERSION:** 1.0.0  
**LAST UPDATED:** 2026-01-25  
**MAINTAINED BY:** Cimeika Core Team  
**FOR:** AI Agents (GitHub Copilot, Claude, GPT, etc.)

---

*"Copilot prepares. Human decides."*

END OF SYSTEM_WILL.md
