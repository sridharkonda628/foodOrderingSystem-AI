"""
Authentication and User Profile Endpoints.

Use Case:
- Manages user onboarding and secure sessions:
  1. POST `/api/auth/register`: Customer or admin account registration (sets secure HttpOnly cookie & returns token).
  2. POST `/api/auth/login`: Credential validation, issues JWT, and sets secure HttpOnly cookie.
  3. POST `/api/auth/logout`: Clears the secure HttpOnly cookie to terminate the session.
  4. GET `/api/auth/me`: Authenticated user session profile verification.
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserOut
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _set_auth_cookie(response: Response, token: str) -> None:
    """
    Sets the secure HttpOnly cookie on the HTTP response.

    Security Benefits:
    - `httponly=True`: Prevents malicious JavaScript (XSS attacks) from accessing the JWT token.
    - `samesite="lax"`: Mitigates Cross-Site Request Forgery (CSRF).
    - `secure=not settings.DEBUG`: Ensures HTTPS transmission in production environments.
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=not settings.DEBUG,
        path="/"
    )


@router.post("/register", response_model=APIResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegister,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Registers a new user account, attaches a secure HttpOnly cookie, and returns token details.

    Use Case:
    - Customer sign up on frontend.

    Parameters:
    - data: Registration input payload.
    - response: FastAPI Response to attach HttpOnly cookie.
    - db: Async database session.

    Returns:
    - APIResponse containing JWT token and user profile.
    """
    user, token = await AuthService.register(db, data)
    _set_auth_cookie(response, token)
    user_out = UserOut.model_validate(user)
    return APIResponse(
        success=True,
        data=TokenResponse(access_token=token, token_type="bearer", user=user_out),
        message="Registration successful"
    )


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(
    data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticates user credentials, sets a secure HttpOnly cookie, and issues a JWT token.

    Use Case:
    - Customer and Admin login screen.

    Parameters:
    - data: Login payload containing email and password.
    - response: FastAPI Response to attach HttpOnly cookie.
    - db: Async database session.

    Returns:
    - APIResponse containing JWT token and user profile.
    """
    user, token = await AuthService.login(db, data)
    _set_auth_cookie(response, token)
    user_out = UserOut.model_validate(user)
    return APIResponse(
        success=True,
        data=TokenResponse(access_token=token, token_type="bearer", user=user_out),
        message="Login successful"
    )


@router.post("/logout", response_model=APIResponse[dict])
async def logout(response: Response):
    """
    Terminates the user session by clearing the secure HttpOnly cookie.

    Use Case:
    - Clears authentication credentials when the user clicks Logout.

    Parameters:
    - response: FastAPI Response to clear the cookie.

    Returns:
    - APIResponse with success confirmation.
    """
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax"
    )
    return APIResponse(
        success=True,
        data={},
        message="Logged out successfully"
    )


@router.get("/me", response_model=APIResponse[UserOut])
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves the profile of the currently authenticated user session.

    Use Case:
    - Validates active session on frontend app load and recovers user details.

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
