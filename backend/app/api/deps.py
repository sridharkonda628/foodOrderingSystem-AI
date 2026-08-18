from typing import Optional
from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not token:
        raise UnauthorizedException("Authentication token is missing. Please log in.")
    
    payload = decode_access_token(token)
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
    if current_user.role != UserRole.ADMIN.value:
        raise ForbiddenException("Administrator privileges required for this action.")
    return current_user


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        if not payload:
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None
        return await UserRepository.get_by_id(db, user_id)
    except Exception:
        return None
