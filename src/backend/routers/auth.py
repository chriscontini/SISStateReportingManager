"""
Authentication API router.

Simple password-based authentication for internal tool.
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)

# Simple in-memory session store
# In production, use Redis or database
_sessions: dict[str, datetime] = {}

# Session duration
SESSION_DURATION_HOURS = 24

# Password from environment (default for development)
APP_PASSWORD = os.environ.get("APP_PASSWORD", "oncourse2026")


class LoginRequest(BaseModel):
    """Login request schema."""
    password: str


class LoginResponse(BaseModel):
    """Login response schema."""
    token: str
    expires_at: datetime


class AuthStatusResponse(BaseModel):
    """Auth status response schema."""
    authenticated: bool
    expires_at: Optional[datetime] = None


def verify_token(token: str) -> bool:
    """Verify if a token is valid and not expired."""
    if token not in _sessions:
        return False

    expires_at = _sessions[token]
    if datetime.utcnow() > expires_at:
        # Token expired, remove it
        del _sessions[token]
        return False

    return True


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> bool:
    """
    Dependency to verify authentication.

    Returns True if authenticated, raises HTTPException otherwise.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    if not verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return True


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate with password and receive a session token.

    The password is configured via APP_PASSWORD environment variable.
    Default for development: "oncourse2026"
    """
    if request.password != APP_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    # Generate secure token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=SESSION_DURATION_HOURS)

    # Store session
    _sessions[token] = expires_at

    return LoginResponse(token=token, expires_at=expires_at)


@router.post("/logout")
async def logout(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
):
    """
    Logout and invalidate the current session token.
    """
    if credentials and credentials.credentials in _sessions:
        del _sessions[credentials.credentials]

    return {"message": "Logged out successfully"}


@router.get("/status", response_model=AuthStatusResponse)
async def auth_status(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
):
    """
    Check current authentication status.
    """
    if credentials is None:
        return AuthStatusResponse(authenticated=False)

    token = credentials.credentials
    if token in _sessions:
        expires_at = _sessions[token]
        if datetime.utcnow() < expires_at:
            return AuthStatusResponse(authenticated=True, expires_at=expires_at)

    return AuthStatusResponse(authenticated=False)
