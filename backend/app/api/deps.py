"""
FastAPI Route Dependencies and Security Injections.

Use Case:
- Provides dependency injection utilities for authentication, role verification, and database sessions:
  1. `get_current_user`: Validates JWT tokens from Authorization Bearer headers or secure HttpOnly cookies, and resolves active User entities.
  2. `get_current_active_admin`: Enforces that the authenticated user possesses the 'admin' role.
  3. `get_optional_current_user`: Safely retrieves user profile if token is provided, without failing on guest visits.
"""

from typing import Optional
from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository

# OAuth2 scheme for extracting Bearer tokens from the HTTP Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def get_current_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    FastAPI dependency validating the JWT token and returning the active authenticated User.

    Use Case:
    - Injected into protected routes (e.g. `/api/orders`, `/api/auth/me`).
    - Checks for JWT in:
      1. `Authorization: Bearer <token>` header - For programmatic API clients, tests, and Swagger.
      2. Secure `HttpOnly` cookie (`access_token`) - For secure browser sessions resistant to XSS.
    - Validates token signature, expiration, user existence, and active account status.

    Parameters:
    - request: Incoming FastAPI Request object (to access HttpOnly cookies).
    - token: Bearer token extracted from Authorization header if present.
    - db: Injected async database session.

    Returns:
    - Authenticated User entity.

    Raises:
    - UnauthorizedException: If token is missing, expired, invalid, or if user is deactivated.
    """
    # 1. Primary: Extract from explicit Authorization header if provided
    auth_token = token
    
    # 2. Fallback: Extract from secure HttpOnly cookie
    if not auth_token:
        auth_token = request.cookies.get("access_token")

    if not auth_token:
        raise UnauthorizedException("Authentication token is missing. Please log in.")
    
    payload = decode_access_token(auth_token)
    if not payload:
        raise UnauthorizedException("Session expired or token is invalid. Please log in again.")
    
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload.")
        
    user = await UserRepository.get_by_id(db, user_id)
    if not user:
        raise UnauthorizedException("User not found.")
    
    if not user.is_active:
        raise UnauthorizedException("User account is deactivated.")
        
    return user


async def get_current_active_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    FastAPI dependency ensuring the authenticated user has administrative privileges.

    Use Case:
    - Injected into all admin-only routes (e.g. `/api/admin/*`, menu item creation/deletion, availability toggling).

    Parameters:
    - current_user: User entity resolved from `get_current_user`.

    Returns:
    - Admin User entity.

    Raises:
    - ForbiddenException: If user role is not 'admin'.
    """
    if current_user.role != UserRole.ADMIN.value:
        raise ForbiddenException("Administrator privileges required for this action.")
    return current_user


async def get_optional_current_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    FastAPI dependency for endpoints accessible to both guests and authenticated users.

    Use Case:
    - Allows personalizing responses if an Authorization header or HttpOnly cookie is present, while allowing unauthenticated guest access.

    Parameters:
    - request: Incoming FastAPI Request object.
    - token: Optional bearer token.
    - db: Injected async database session.

    Returns:
    - User entity if token is valid, None otherwise.
    """
    auth_token = token or request.cookies.get("access_token")
    if not auth_token:
        return None
    try:
        payload = decode_access_token(auth_token)
        if not payload:
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None
        return await UserRepository.get_by_id(db, user_id)
    except Exception:
        return None
