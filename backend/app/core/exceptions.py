"""
Custom Exception Classes and Global Error Handlers.

Use Case:
- Provides domain-specific, strongly typed exceptions that map cleanly to standard HTTP status codes.
- Ensures all API error responses follow a predictable, unified JSON format:
  `{"success": false, "error": {"code": "...", "message": "...", "details": {...}}}`.
"""

from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """
    Base application exception for all domain and operational errors.

    Use Case:
    - Extended by specialized error classes to capture structured error codes, messages, and details.
    """
    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(AppException):
    """
    Exception raised when a requested resource (e.g. menu item, order, user) does not exist.

    Use Case: Returns HTTP 404 with error code 'NOT_FOUND'.
    """
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND, details=details)


class UnauthorizedException(AppException):
    """
    Exception raised when authentication credentials are missing, invalid, or expired.

    Use Case: Returns HTTP 401 with error code 'UNAUTHORIZED'.
    """
    def __init__(self, message: str = "Invalid credentials or token expired", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="UNAUTHORIZED", status_code=status.HTTP_401_UNAUTHORIZED, details=details)


class ForbiddenException(AppException):
    """
    Exception raised when an authenticated user lacks permissions for an operation (e.g., non-admin accessing admin endpoints).

    Use Case: Returns HTTP 403 with error code 'FORBIDDEN'.
    """
    def __init__(self, message: str = "You do not have permission to access this resource", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="FORBIDDEN", status_code=status.HTTP_403_FORBIDDEN, details=details)


class BadRequestException(AppException):
    """
    Exception raised for invalid client inputs or business rule violations.

    Use Case: Returns HTTP 400 with error code 'BAD_REQUEST'.
    """
    def __init__(self, message: str = "Invalid request parameters", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST, details=details)


class ConflictException(AppException):
    """
    Exception raised when a unique constraint or duplicate record is encountered (e.g. duplicate email or slug).

    Use Case: Returns HTTP 409 with error code 'CONFLICT'.
    """
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="CONFLICT", status_code=status.HTTP_409_CONFLICT, details=details)


class ItemUnavailableException(AppException):
    """
    Exception raised when an order checkout is attempted with out-of-stock / unavailable items.

    Use Case: Returns HTTP 409 with error code 'ITEM_UNAVAILABLE' to trigger immediate cart UI warning.
    """
    def __init__(self, message: str = "One or more selected items are currently unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="ITEM_UNAVAILABLE", status_code=status.HTTP_409_CONFLICT, details=details)


class InvalidStateTransitionException(AppException):
    """
    Exception raised when an illegal order lifecycle transition is attempted (e.g. PLACED -> READY).

    Use Case: Returns HTTP 400 with error code 'INVALID_STATE_TRANSITION' to maintain strict order integrity.
    """
    def __init__(self, message: str = "Invalid order state transition", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="INVALID_STATE_TRANSITION", status_code=status.HTTP_400_BAD_REQUEST, details=details)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Global exception handler for all known application exceptions.

    Use Case:
    - Catches any raised `AppException` and transforms it into a standardized JSON error response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global catch-all exception handler for unexpected server errors.

    Use Case:
    - Logs full tracebacks on server side for debugging while masking internal error details from clients.
    - Returns HTTP 500 with a safe user-facing message.
    """
    import logging
    logging.getLogger("kpitech_food_order").exception(f"Unhandled Exception on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred. Please try again later.",
                "details": {}
            }
        }
    )
