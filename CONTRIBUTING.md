# Contributing to CIMEIKA UNIFIED

Welcome to the CIMEIKA project! We're building a bilingual (EN/UK) family life management platform based on the **CANON v1.0.0** principles with 7 fixed modules.

## 🎯 Mission & Context

CIMEIKA follows the "reality first, action before explanation" design philosophy with a fixed architecture of 7 immutable modules (Ci, Kazkar, Podija, Nastrij, Malya, Gallery, Calendar). This project is currently in **MVP phase** with a focus on establishing core functionality.

## 📋 PR Submission Rules

### Before Submitting

1. **Read the architecture docs**: Familiarize yourself with `docs/ARCHITECTURE.md` and `CIMEIKA_CANON_TZ_v1.yaml`
2. **Check existing issues**: Ensure your change aligns with planned work
3. **Test locally**: Verify all checks pass before submitting
4. **Keep it minimal**: Make the smallest possible changes to achieve the goal

### PR Requirements

- **Clear title**: Use format `[Module] Brief description` (e.g., `[Ci] Add capture validation`)
- **Detailed description**: 
  - What problem does this solve?
  - What changes were made?
  - How was it tested?
- **Link issues**: Reference related issues with `Fixes #123` or `Relates to #456`
- **Clean commits**: Follow conventional commit format (see below)
- **Passing CI**: All automated checks must pass (lint, build, tests)

## 💻 Code Style Guidelines

### Frontend (React + TypeScript)

- **Indentation**: 2 spaces
- **Linter**: ESLint (run `npm run lint` in `frontend/`)
- **Naming conventions**:
  - Components: PascalCase (`CiOverlay.jsx`)
  - Hooks: camelCase with `use` prefix (`useCiStore`)
  - Files: Match component name
- **Module structure**: Follow existing pattern in `frontend/src/modules/`
- **No business logic in views**: Keep logic in services/hooks
- **Theme system**: Deterministic route-based (Kazkar=night, others=day)
- **ESLint warnings**: Up to 10 warnings allowed (for React hooks exhaustive-deps - adding suggested dependencies can cause infinite loops)

### Backend (Python + FastAPI)

- **Indentation**: 4 spaces
- **Linter**: flake8 or ruff (CI will run both)
- **Naming conventions**:
  - Modules: lowercase (`ci`, `kazkar`)
  - Classes: PascalCase (`ModuleInterface`)
  - Functions: snake_case (`get_status()`)
- **Module structure**: Follow pattern in `backend/app/modules/{module}/`
  - `api.py` - Routes only (no business logic)
  - `service.py` - Business logic (implements ModuleInterface)
  - `model.py` - SQLAlchemy models (require `canon_bundle_id`)
  - `schema.py` - Pydantic v2 schemas
- **Type hints**: Use them consistently
- **Docstrings**: Required for public functions

### General Conventions

- **Language**: Ukrainian for UI text, English for code/docs
- **Line length**: Max 100 characters (soft limit)
- **Imports**: Group by stdlib, third-party, local
- **Comments**: Only when necessary to explain "why", not "what"

## 📝 Commit Message Conventions

We follow **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code restructuring (no feature/bug change)
- `test`: Adding/updating tests
- `chore`: Build process, dependencies, tooling

### Examples

```
feat(ci): add voice input capture
fix(kazkar): correct legend date parsing
docs: update SEO integration guide
chore: upgrade FastAPI to 0.104.1
```

### Scope

Use module names when applicable: `ci`, `kazkar`, `podija`, `nastrij`, `malya`, `gallery`, `calendar`, `backend`, `frontend`, `infra`

## 🔍 Review Process

### What Reviewers Look For

1. **Alignment with CANON principles**: Does it follow the fixed architecture?
2. **Minimal changes**: Are changes surgical and necessary?
3. **Code quality**: Proper style, naming, structure
4. **Testing**: Are changes validated with tests?
5. **Documentation**: Are relevant docs updated?
6. **No breaking changes**: Unless explicitly planned

### Response Time Expectations

- Initial review: Within 2-3 business days
- Follow-up reviews: Within 1 business day
- Maintainer: @Ihorog

### Addressing Feedback

- Respond to all comments (even if just acknowledging)
- Make requested changes in new commits (don't force-push)
- Mark conversations as resolved when addressed
- Request re-review when ready

## 🧪 Testing Requirements

### Frontend Tests

Currently minimal - focus on manual testing:
1. Run dev server: `cd frontend && npm run dev`
2. Test affected modules manually
3. Verify theme switching works
4. Check responsive behavior

### Backend Tests

Required for all service changes:
1. Add tests in `backend/tests/`
2. Follow existing pattern (see `test_kazkar_legend.py`)
3. Use pytest fixtures for database setup
4. Run tests: `pytest backend/tests/ -v`

### Integration Testing

- Test with full stack via `docker-compose up`
- Verify API endpoints with `/api/docs` (Swagger)
- Check database migrations with `python backend/init_db.py`

## ✅ Definition of Done

Before marking PR as ready for review, ensure:

- [ ] Code follows style guidelines (lint passes)
- [ ] All CI checks pass (build, lint, tests)
- [ ] Changes are minimal and focused
- [ ] Relevant documentation updated
- [ ] Manual testing completed
- [ ] No console errors or warnings
- [ ] Database schema changes are reflected in models
- [ ] API changes are documented in Swagger (auto-generated)
- [ ] Commit messages follow conventions
- [ ] PR description is complete and clear

## 🚫 What Not to Do

- ❌ Don't add/remove modules (7 is canonical)
- ❌ Don't create Flask code (archived in `/archive/flask/`)
- ❌ Don't add root-level directories (structure is fixed)
- ❌ Don't put business logic in API routes (belongs in services)
- ❌ Don't use Redux/Context for module state (use Zustand)
- ❌ Don't add manual theme toggles (themes are route-determined)
- ❌ Don't modify CANON principles without discussion

## 🛠️ Development Workflow

### Local Setup

```bash
# 1. Clone and setup
git clone https://github.com/Ihorog/cimeika-unified.git
cd cimeika-unified
cp .env.template .env
# Edit .env with your API keys

# 2. Full stack (recommended)
docker-compose up -d

# 3. Or run separately:
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

### Making Changes

1. **Create branch**: `git checkout -b feature/your-feature-name`
2. **Make changes**: Follow the guidelines above
3. **Test locally**: Run lint, build, and tests
4. **Commit**: Use conventional commit format
5. **Push**: `git push origin feature/your-feature-name`
6. **Open PR**: Use PR template, fill all sections

### Running Quality Checks

```bash
# Frontend checks
cd frontend
npm install
npm run lint
npm run build

# Backend checks
cd backend
pip install -r requirements.txt
flake8 app/ --max-line-length=100 --extend-ignore=E203,W503
pytest tests/ -v
```

## 📚 Key Resources

- **Architecture**: `docs/ARCHITECTURE.md`
- **CANON Spec**: `CIMEIKA_CANON_TZ_v1.yaml`
- **Module Orchestration**: `docs/MODULE_ORCHESTRATION.md`
- **SEO Integration**: `docs/SEO_INTEGRATION.md`
- **Android Integration**: `docs/ANDROID_WEBVIEW_INTEGRATION.md`
- **Quick Start**: `QUICKSTART_DEV.md`

## 🤝 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open an issue with detailed reproduction steps
- **Feature requests**: Open an issue with clear use case
- **Urgent**: Contact @Ihorog directly

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to CIMEIKA! 🚀
