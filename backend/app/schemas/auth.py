"""
Authentication and User Pydantic Schemas.

Use Case:
- Defines request validation schemas for user registration (`UserRegister`) and login (`UserLogin`).
- Defines response serialization schemas for user profiles (`UserOut`) and JWT tokens (`TokenResponse`).
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import UserRole


class UserRegister(BaseModel):
    """
    Request schema for new user registration.

    Use Case: Validates customer/admin registration inputs.
    """
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password with at least 6 characters")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: Optional[UserRole] = UserRole.CUSTOMER


class UserLogin(BaseModel):
    """
    Request schema for user authentication.

    Use Case: Validates email and password credentials during login.
    """
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """
    Response schema for public user profile.

    Use Case: Returns safe user details without exposing hashed passwords.
    """
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """
    Response schema returning JWT bearer token and authenticated user profile.

    Use Case: Returned on successful register and login actions.
    """
    access_token: str
    token_type: str = "bearer"
    user: UserOut
