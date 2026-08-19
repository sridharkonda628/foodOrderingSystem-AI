"""
Common Response Wrapper Schemas.

Use Case:
- Provides a standard, generic response wrapper `APIResponse[T]` across all REST endpoints.
- Unifies success payloads, descriptive messages, and structured error details.
"""

from typing import Generic, Optional, TypeVar, Any, Dict
from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """
    Structured error detail schema.

    Use Case: Contains error code, descriptive message, and optional extra metadata.
    """
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class APIResponse(BaseModel, Generic[T]):
    """
    Generic API Response Envelope.

    Use Case:
    - Wraps all successful endpoint data (`data: T`) and error payloads.
    - Structure:
      {
        "success": bool,
        "data": Optional[T],
        "message": str,
        "error": Optional[ErrorDetail]
      }
    """
    success: bool = True
    data: Optional[T] = None
    message: str = "Success"
    error: Optional[ErrorDetail] = None
