# Contributing to CIMEIKA Unified

Thank you for your interest in contributing to CIMEIKA! This document outlines the process and rules for contributing to this project.

## 🎯 Philosophy

CIMEIKA follows the **"MVP Production Backbone"** approach:
- **NO fake integrations** - Real implementations only
- **NO secrets in repo** - Use environment variables
- **Minimal diffs, maximum value** - Surgical changes only
- **No mass refactors** - Incremental improvements

## 📋 PR Requirements

Every Pull Request MUST include:

1. **Summary** - Clear description of what and why
2. **Changed files list** - Enumerate all modified files
3. **Local verification steps** - How to test locally
4. **Acceptance Criteria** - Explicit definition of done

### PR Template

```markdown
## Summary
[Brief description of the change]

## Changed Files
- `path/to/file1.py` - [description]
- `path/to/file2.js` - [description]

## Local Verification Steps
1. Step 1
2. Step 2
3. Expected result

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] CI passes
```

## 🔄 Development Workflow

### 1. Branch Naming
```bash
# Feature branches
feature/short-description

# Bug fixes
fix/short-description

# Hotfixes
hotfix/critical-issue

# MVP PR series (special)
mvp/pr-01-governance
mvp/pr-02-backend-bootstrap
```

### 2. Commit Messages
Use conventional commits format:
```
type(scope): subject

body (optional)
footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(backend): add rate limiting middleware"
git commit -m "fix(frontend): resolve theme switching bug in Kazkar"
git commit -m "docs: update production checklist"
```

### 3. Before Submitting PR

**Backend:**
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run linter
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Format code
black .

# Run tests
pytest tests/ -v
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm ci

# Run linter
npm run lint

# Build
npm run build
```

**Docker Compose:**
```bash
# Full stack test
docker compose up -d
curl http://localhost:8000/health
curl http://localhost:3000
```

## 🚫 What NOT to Do

1. **Don't commit secrets** - Use `.env` files (gitignored)
2. **Don't add fake integrations** - Real or nothing
3. **Don't mass refactor** - Small, focused changes
4. **Don't break existing tests** - Fix or justify
5. **Don't add unnecessary dependencies** - Justify each new package
6. **Don't bypass CI** - All PRs must pass CI

## ✅ Definition of Done

A PR is considered complete when:

- [ ] Code changes are minimal and focused
- [ ] All CI checks pass (lint, build, tests)
- [ ] Local verification steps documented and tested
- [ ] No secrets or credentials committed
- [ ] Documentation updated (if applicable)
- [ ] Tests added/updated (if applicable)
- [ ] Code review approved by @Ihorog

## 🔐 Security

- Use environment variables for all secrets
- Follow OWASP security best practices
- Report security vulnerabilities privately to @Ihorog
- Never commit API keys, passwords, or tokens

## 📚 Code Style

### Python (Backend)
- Follow PEP 8
- Use `black` for formatting (line length: 127)
- Use `flake8` for linting
- Type hints encouraged
- Docstrings for public APIs

### JavaScript/JSX (Frontend)
- Follow ESLint configuration
- Use Prettier for formatting
- Functional components with hooks
- PropTypes or TypeScript types

### File Structure
- Follow the existing module structure (7 fixed modules)
- Keep module-specific code in module directories
- Shared utilities in `core/` or `utils/`

## 🧪 Testing

### Backend Tests
```python
# tests/test_*.py
import pytest

def test_health_endpoint():
    # Test implementation
    assert response.status_code == 200
```

### Frontend Tests
```javascript
// Currently using manual testing
// Automated tests TBD
```

## 📖 Documentation

Update documentation when:
- Adding new features
- Changing APIs or interfaces
- Updating configuration
- Modifying development workflow

Documentation lives in:
- `/docs/` - Architecture and design docs
- `README.md` - Quick start and overview
- `CONTRIBUTING.md` - This file
- Inline code comments (when necessary)

## 🙋 Getting Help

- Open an issue for bugs or feature requests
- Tag @Ihorog for code review
- Check existing documentation in `/docs/`

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to CIMEIKA! 🚀
