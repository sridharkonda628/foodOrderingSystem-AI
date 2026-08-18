from typing import Generic, Optional, TypeVar, Any, Dict
from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "Success"
    error: Optional[ErrorDetail] = None
