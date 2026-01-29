"""API Routers package."""

from .states import router as states_router
from .rankings import router as rankings_router
from .auth import router as auth_router

__all__ = ["states_router", "rankings_router", "auth_router"]
