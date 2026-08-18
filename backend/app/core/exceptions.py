from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
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
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND, details=details)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Invalid credentials or token expired", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="UNAUTHORIZED", status_code=status.HTTP_401_UNAUTHORIZED, details=details)


class ForbiddenException(AppException):
    def __init__(self, message: str = "You do not have permission to access this resource", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="FORBIDDEN", status_code=status.HTTP_403_FORBIDDEN, details=details)


class BadRequestException(AppException):
    def __init__(self, message: str = "Invalid request parameters", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST, details=details)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="CONFLICT", status_code=status.HTTP_409_CONFLICT, details=details)


class ItemUnavailableException(AppException):
    def __init__(self, message: str = "One or more selected items are currently unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="ITEM_UNAVAILABLE", status_code=status.HTTP_409_CONFLICT, details=details)


class InvalidStateTransitionException(AppException):
    def __init__(self, message: str = "Invalid order state transition", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="INVALID_STATE_TRANSITION", status_code=status.HTTP_400_BAD_REQUEST, details=details)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
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
