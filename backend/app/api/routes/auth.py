"""
Authentication and User Profile Endpoints.

Use Case:
- Manages user onboarding and security sessions:
  1. POST `/api/auth/register`: Customer or admin account registration.
  2. POST `/api/auth/login`: Credential validation and JWT token issuance.
  3. GET `/api/auth/me`: Authenticated user session profile verification.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserOut
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=APIResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Registers a new user account and returns an authentication bearer token.

    Use Case:
    - Customer sign up on frontend.

    Parameters:
    - data: Registration input payload.
    - db: Async database session.

    Returns:
    - APIResponse containing JWT token and user profile.
    """
    user, token = await AuthService.register(db, data)
    user_out = UserOut.model_validate(user)
    return APIResponse(
        success=True,
        data=TokenResponse(access_token=token, token_type="bearer", user=user_out),
        message="Registration successful"
    )


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(
    data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticates user credentials and issues a JWT bearer token.

    Use Case:
    - Customer and Admin login screen.

    Parameters:
    - data: Login payload containing email and password.
    - db: Async database session.

    Returns:
    - APIResponse containing JWT token and user profile.
    """
    user, token = await AuthService.login(db, data)
    user_out = UserOut.model_validate(user)
    return APIResponse(
        success=True,
        data=TokenResponse(access_token=token, token_type="bearer", user=user_out),
        message="Login successful"
    )


@router.get("/me", response_model=APIResponse[UserOut])
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves the profile of the currently authenticated user session.

    Use Case:
    - Validates stored token on frontend app load and recovers current user role and details.

    Parameters:
    - current_user: Resolved authenticated User entity.

    Returns:
    - APIResponse containing `UserOut`.
    """
    user_out = UserOut.model_validate(current_user)
    return APIResponse(
        success=True,
        data=user_out,
        message="User profile retrieved"
    )
