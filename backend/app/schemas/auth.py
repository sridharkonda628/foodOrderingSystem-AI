from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password with at least 6 characters")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: Optional[UserRole] = UserRole.CUSTOMER


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
