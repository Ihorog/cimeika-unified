"""
CIMEIKA FastAPI Application
Main FastAPI server with all module integrations
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.config.database import init_db
from app.config.canon import CANON_BUNDLE_ID
from app.api.v1.router import api_router
from app.api.v1 import health
from app.startup import setup_modules
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.rate_limit import RateLimitMiddleware

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting CIMEIKA Backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Log Level: {settings.LOG_LEVEL}")
    
    # Validate configuration
    validation = settings.validate()
    if not validation["valid"]:
        for error in validation["errors"]:
            logger.error(f"Configuration error: {error}")
    for warning in validation["warnings"]:
        logger.warning(f"Configuration warning: {warning}")
    
    # Startup: Initialize database and modules
    try:
        init_db()
        logger.info("Database initialized")
        setup_modules()
        logger.info("Modules initialized")
    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)
        raise
    
    logger.info("CIMEIKA Backend started successfully")
    yield
    
    # Shutdown: cleanup if needed
    logger.info("Shutting down CIMEIKA Backend...")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Configure CORS
logger.info(f"CORS configured with origins: {settings.CORS_ORIGINS}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=60,
    requests_per_hour=1000,
    exclude_paths=["/health", "/ready", "/", "/api/docs", "/api/redoc", "/api/openapi.json"]
)


@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "status": "success",
        "message": "CIMEIKA FastAPI Backend",
        "version": "0.1.0",
        "canon_bundle_id": CANON_BUNDLE_ID,
        "docs": "/api/docs",
        "modules": [
            "Ci - Центральне ядро",
            "Казкар - Пам'ять",
            "Подія - Події",
            "Настрій - Емоції",
            "Маля - Ідеї",
            "Галерея - Медіа",
            "Календар - Час"
        ]
    }


# Include health check router (at root level)
app.include_router(health.router)

# Include API v1 router
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting uvicorn server on {settings.BACKEND_HOST}:{settings.BACKEND_PORT}")
    
    # Use string reference for reload support, direct app object otherwise
    uvicorn.run(
        "main:app" if settings.FASTAPI_RELOAD else app,
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.FASTAPI_RELOAD
    )
