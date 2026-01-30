"""API Routers package."""

from .states import router as states_router
from .rankings import router as rankings_router
from .auth import router as auth_router
from .gap_analysis import router as gap_analysis_router
from .roadmaps import router as roadmaps_router
from .knowledge import router as knowledge_router

__all__ = ["states_router", "rankings_router", "auth_router", "gap_analysis_router", "roadmaps_router", "knowledge_router"]
