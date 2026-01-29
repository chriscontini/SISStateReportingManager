"""
SISStateReportingManager - Backend API

FastAPI application for state expansion planning tool.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SISStateReportingManager API",
    description="AI-powered state expansion planning tool for SIS vendors",
    version="0.1.0",
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    }
