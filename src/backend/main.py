"""
SISStateReportingManager - Backend API

FastAPI application for state expansion planning tool.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db, close_db
from .routers import states_router, rankings_router, auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="SISStateReportingManager API",
    description="AI-powered state expansion planning tool for SIS vendors",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(states_router)
app.include_router(rankings_router)
app.include_router(auth_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "SISStateReportingManager API",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "states": "/api/states",
            "rankings": "/api/rankings",
            "auth": "/api/auth",
        },
    }
