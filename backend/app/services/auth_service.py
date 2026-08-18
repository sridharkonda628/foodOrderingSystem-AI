from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictException, UnauthorizedException, NotFoundException
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserOut


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, data: UserRegister) -> Tuple[User, str]:
        existing_user = await UserRepository.get_by_email(db, data.email)
        if existing_user:
            raise ConflictException(f"An account with email '{data.email}' already exists.")

        user = User(
            email=data.email.lower().strip(),
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name.strip(),
            role=data.role.value if data.role else UserRole.CUSTOMER.value,
            is_active=True
        )
        created_user = await UserRepository.create(db, user)
        token = create_access_token(subject=created_user.id, role=created_user.role)
        return created_user, token

    @staticmethod
    async def login(db: AsyncSession, data: UserLogin) -> Tuple[User, str]:
        user = await UserRepository.get_by_email(db, data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password.")
        
        if not user.is_active:
            raise UnauthorizedException("This user account is deactivated.")

        token = create_access_token(subject=user.id, role=user.role)
        return user, token

    @staticmethod
    async def get_current_user_profile(db: AsyncSession, user_id: str) -> User:
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundException("User not found.")
        return user
