"""
Centralized error handling middleware for the API.

Provides consistent error response format and logging for all exceptions.
"""

import logging
import traceback
from datetime import datetime
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: bool = True
    code: str
    message: str
    detail: str | None = None
    timestamp: str
    path: str


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        message: str,
        code: str = "API_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class NotFoundError(APIError):
    """Resource not found error."""

    def __init__(self, resource: str, identifier: str | int | None = None):
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} with ID '{identifier}' not found"
        super().__init__(
            message=f"{resource} not found",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ValidationError(APIError):
    """Validation error."""

    def __init__(self, message: str, detail: str | None = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class AuthenticationError(APIError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(APIError):
    """Authorization error."""

    def __init__(self, message: str = "Not authorized"):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class DatabaseError(APIError):
    """Database error."""

    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class ExternalServiceError(APIError):
    """External service error (e.g., AI API failure)."""

    def __init__(self, service: str, message: str | None = None):
        super().__init__(
            message=f"External service error: {service}",
            code="EXTERNAL_SERVICE_ERROR",
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=message,
        )


def create_error_response(
    request: Request,
    code: str,
    message: str,
    detail: str | None = None,
) -> dict:
    """Create a standardized error response dictionary."""
    return {
        "error": True,
        "code": code,
        "message": message,
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat(),
        "path": str(request.url.path),
    }


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle custom API errors."""
    logger.warning(
        f"API Error: {exc.code} - {exc.message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "code": exc.code,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            request=request,
            code=exc.code,
            message=exc.message,
            detail=exc.detail,
        ),
    )


async def sqlalchemy_error_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Handle SQLAlchemy database errors."""
    logger.error(
        f"Database Error: {str(exc)}",
        extra={"path": request.url.path, "method": request.method},
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            request=request,
            code="DATABASE_ERROR",
            message="A database error occurred",
            detail="Please try again later" if not logger.isEnabledFor(logging.DEBUG) else str(exc),
        ),
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all unhandled exceptions."""
    logger.error(
        f"Unhandled Exception: {type(exc).__name__}: {str(exc)}",
        extra={"path": request.url.path, "method": request.method},
        exc_info=True,
    )

    # Don't expose internal error details in production
    detail = None
    if logger.isEnabledFor(logging.DEBUG):
        detail = traceback.format_exc()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            request=request,
            code="INTERNAL_ERROR",
            message="An internal server error occurred",
            detail=detail,
        ),
    )


def setup_error_handlers(app: FastAPI) -> None:
    """Register error handlers with the FastAPI application."""
    app.add_exception_handler(APIError, api_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)


class RequestLoggingMiddleware:
    """Middleware for logging requests and responses."""

    def __init__(self, app: Callable):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = datetime.utcnow()

        # Capture response status
        response_status = None

        async def send_wrapper(message):
            nonlocal response_status
            if message["type"] == "http.response.start":
                response_status = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # Log the request
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            path = scope.get("path", "")
            method = scope.get("method", "")

            logger.info(
                f"{method} {path} - {response_status} - {duration:.2f}ms",
                extra={
                    "method": method,
                    "path": path,
                    "status": response_status,
                    "duration_ms": duration,
                },
            )
