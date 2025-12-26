# CIMEIKA Backend

FastAPI backend для CIMEIKA екосистеми - Family Management Platform.

## Architecture

CIMEIKA backend follows the **MVP Production Backbone** architecture with 7 fixed modules:
- **Ci** - Central orchestration core
- **Kazkar** - Memory, stories, legends
- **Podija** - Events, future scenarios
- **Nastrij** - Emotional states tracking
- **Malya** - Ideas, creativity, innovations
- **Gallery** - Visual archive, media
- **Calendar** - Time, rhythms, planning

## Structure

```
backend/
├── app/                    # Main application code
│   ├── api/               # REST API endpoints
│   │   └── v1/           # API version 1
│   │       ├── router.py      # Main API router
│   │       ├── health.py      # Health check endpoints
│   │       └── modules.py     # Module management endpoints
│   ├── core/              # Core functionality
│   │   ├── config.py          # Configuration management
│   │   ├── logging.py         # Structured logging
│   │   ├── interfaces.py      # Module interfaces
│   │   └── orchestrator.py    # Module registry
│   ├── modules/           # 7 CIMEIKA modules
│   │   ├── ci/           # Central orchestration
│   │   ├── kazkar/       # Memory & stories
│   │   ├── podija/       # Events
│   │   ├── nastrij/      # Emotional states
│   │   ├── malya/        # Ideas
│   │   ├── gallery/      # Media
│   │   └── calendar/     # Time management
│   ├── config/            # Configuration files
│   │   ├── canon.py          # CANON constants
│   │   ├── database.py       # Database setup
│   │   └── seo/             # SEO configuration
│   └── models/            # Database models
├── tests/                 # Test suite
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── Dockerfile           # Docker configuration
```

## Development

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- pip or poetry

### Local Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   # Copy template and edit
   cp ../.env.template ../.env
   
   # Required variables:
   # ENVIRONMENT=development
   # LOG_LEVEL=INFO
   # POSTGRES_HOST=localhost
   # POSTGRES_DB=cimeika
   # POSTGRES_USER=cimeika_user
   # POSTGRES_PASSWORD=your_password
   ```

4. **Initialize database:**
   ```bash
   python init_db.py
   ```

5. **Run development server:**
   ```bash
   python main.py
   ```

Backend will be available at http://localhost:8000

### API Documentation

When the server is running, interactive API documentation is available at:
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

### API Endpoints

#### Health & Status
- `GET /health` - Basic health check
- `GET /ready` - Readiness check with environment validation
- `GET /` - API information and module list

#### Modules (v1)
- `GET /api/v1/modules/` - List all 7 modules
- `GET /api/v1/modules/status` - Get status of all modules
- `GET /api/v1/modules/{module}/status` - Get status of specific module

#### Module-Specific Endpoints
Each module has its own set of CRUD endpoints under `/api/v1/{module}/`

### Configuration

Configuration is managed through environment variables (see `app/core/config.py`):

**Required:**
- `ENVIRONMENT` - Environment name (development, production)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

**Optional:**
- `SENTRY_DSN` - Sentry monitoring URL
- `OPENAI_API_KEY` - OpenAI API key for AI features
- `ANTHROPIC_API_KEY` - Anthropic API key for Claude
- `CORS_ORIGINS` - Comma-separated list of allowed origins

### Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_health.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Linting & Formatting

```bash
# Check for critical errors
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Full lint check
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

# Format code
black .

# Check formatting without changes
black --check .
```

## Docker Development

Run backend with Docker Compose (includes PostgreSQL):

```bash
# From project root
docker compose up -d backend

# View logs
docker compose logs -f backend

# Stop
docker compose down
```

## Technologies

- **FastAPI** - Modern, high-performance web framework
- **Pydantic v2** - Data validation using Python type hints
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **PostgreSQL 15** - Primary database
- **Uvicorn** - ASGI server
- **pytest** - Testing framework
- **flake8** - Linting
- **black** - Code formatting

### Optional Integrations
- **Sentry** - Error tracking and monitoring
- **OpenAI** - GPT integration for Ci module
- **Anthropic** - Claude integration for advanced AI
- **Redis** - Caching and rate limiting (future)
- **Celery** - Background task processing (future)

## Project Conventions

### Code Style
- Follow PEP 8
- Max line length: 127 characters
- Use type hints
- Docstrings for public APIs
- Format with `black`

### Module Structure
Each module follows a standard pattern:
```
module/
├── api.py       # FastAPI routes (no logic)
├── service.py   # Business logic
├── model.py     # Database models
└── schema.py    # Pydantic schemas
```

### Service Interface
All services implement `ModuleInterface` and `ServiceInterface`:
- `get_name()`, `get_status()`
- `initialize()`, `shutdown()`
- CRUD operations: `create_*()`, `get_*()`, `update_*()`, `delete_*()`

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | No | `development` | Environment name |
| `DEBUG` | No | `true` | Debug mode |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `BACKEND_HOST` | No | `0.0.0.0` | Server host |
| `BACKEND_PORT` | No | `8000` | Server port |
| `CORS_ORIGINS` | No | `localhost:3000,localhost:5173` | Allowed CORS origins |
| `POSTGRES_HOST` | No | `localhost` | PostgreSQL host |
| `POSTGRES_PORT` | No | `5432` | PostgreSQL port |
| `POSTGRES_DB` | No | `cimeika` | Database name |
| `POSTGRES_USER` | No | `cimeika_user` | Database user |
| `POSTGRES_PASSWORD` | No | `change_me_in_production` | Database password |
| `SECRET_KEY` | No | `change_me_in_production` | Secret key for sessions |
| `SENTRY_DSN` | No | None | Sentry monitoring URL |
| `OPENAI_API_KEY` | No | None | OpenAI API key |
| `ANTHROPIC_API_KEY` | No | None | Anthropic API key |

## Production Deployment

See `docs/production-checklist.md` (created in PR-06) for production deployment guidelines.

## Contributing

See `CONTRIBUTING.md` in the project root for contribution guidelines.

## License

See LICENSE file in project root.
