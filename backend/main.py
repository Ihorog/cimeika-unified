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
from app.startup import setup_modules

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup: Initialize database and modules
    init_db()
    setup_modules()
    yield
    # Shutdown: cleanup if needed


# Create FastAPI application
app = FastAPI(
    title="CIMEIKA API",
    description="Центральна екосистема проєкту Cimeika - Family Management Platform",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "CIMEIKA Backend is running",
        "canon_bundle_id": CANON_BUNDLE_ID
    }


# Include API v1 router
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('BACKEND_PORT', 8000))
    host = os.getenv('BACKEND_HOST', '0.0.0.0')
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv('FASTAPI_RELOAD', '1') == '1'
    )
