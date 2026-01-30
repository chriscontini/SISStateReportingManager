"""
SISStateReportingManager - Backend API

FastAPI application for state expansion planning tool.
"""

import time
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import init_db, close_db, get_db
from .routers import states_router, rankings_router, auth_router, gap_analysis_router, roadmaps_router, knowledge_router, chat_router, competitors_router
from .models import State, StateScore, StateAnalysis, GapAnalysis, Roadmap, KnowledgeArticle, ChatSession, Competitor
from .middleware import setup_error_handlers, RequestLoggingMiddleware

# Track application start time
APP_START_TIME = datetime.utcnow()


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

# Setup error handlers
setup_error_handlers(app)

# Request logging middleware
app.add_middleware(RequestLoggingMiddleware)

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
app.include_router(gap_analysis_router)
app.include_router(roadmaps_router)
app.include_router(knowledge_router)
app.include_router(chat_router)
app.include_router(competitors_router)


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Enhanced health check endpoint with database connectivity."""
    health = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "uptime_seconds": (datetime.utcnow() - APP_START_TIME).total_seconds(),
    }

    # Check database connectivity
    try:
        start = time.time()
        await db.execute(text("SELECT 1"))
        db_latency = (time.time() - start) * 1000
        health["database"] = {
            "status": "connected",
            "latency_ms": round(db_latency, 2),
        }
    except Exception as e:
        health["status"] = "degraded"
        health["database"] = {
            "status": "disconnected",
            "error": str(e),
        }

    return health


@app.get("/api/admin/stats")
async def admin_stats(db: AsyncSession = Depends(get_db)):
    """Admin statistics endpoint for monitoring."""
    stats = {
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": (datetime.utcnow() - APP_START_TIME).total_seconds(),
        "counts": {},
        "recent_activity": {},
    }

    # Get record counts
    models = [
        ("states", State),
        ("state_scores", StateScore),
        ("state_analyses", StateAnalysis),
        ("gap_analyses", GapAnalysis),
        ("roadmaps", Roadmap),
        ("knowledge_articles", KnowledgeArticle),
        ("chat_sessions", ChatSession),
        ("competitors", Competitor),
    ]

    for name, model in models:
        try:
            result = await db.execute(select(func.count()).select_from(model))
            stats["counts"][name] = result.scalar() or 0
        except Exception:
            stats["counts"][name] = -1

    # Get states with scores
    try:
        result = await db.execute(
            select(func.count()).select_from(StateScore).where(StateScore.total_score > 0)
        )
        stats["counts"]["states_with_scores"] = result.scalar() or 0
    except Exception:
        stats["counts"]["states_with_scores"] = -1

    return stats


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "SISStateReportingManager API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "admin_stats": "/api/admin/stats",
        "endpoints": {
            "states": "/api/states",
            "rankings": "/api/rankings",
            "auth": "/api/auth",
            "gap_analysis": "/api/gap-analysis",
            "roadmaps": "/api/roadmaps",
            "knowledge": "/api/knowledge",
            "chat": "/api/chat",
            "competitors": "/api/competitors",
        },
    }
