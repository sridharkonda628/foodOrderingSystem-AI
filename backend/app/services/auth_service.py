"""
Authentication Service.

Use Case:
- Handles user registration with email uniqueness validation and password hashing.
- Handles user login with password verification, active account status checks, and JWT token issuance.
- Provides profile retrieval by user ID.
"""

from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictException, UnauthorizedException, NotFoundException
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserOut


class AuthService:
    """
    Service encapsulating user registration, authentication, and session generation.
    """

    @staticmethod
    async def register(db: AsyncSession, data: UserRegister) -> Tuple[User, str]:
        """
        Registers a new user and generates an initial JWT access token.

        Use Case:
        - Called when a new customer or admin signs up via the `/api/auth/register` endpoint.
        - Enforces unique email constraint, hashes password with bcrypt, and creates database record.

        Parameters:
        - db: The active async database session.
        - data: Validated registration payload containing email, password, full name, and role.

        Returns:
        - Tuple of (User entity, JWT access token string).

        Raises:
        - ConflictException: If an account with the specified email already exists.
        """
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
        """
        Authenticates a user and issues a new JWT access token.

        Use Case:
        - Called when an existing user logs in via the `/api/auth/login` endpoint.
        - Verifies password hash and ensures account is active.

        Parameters:
        - db: The active async database session.
        - data: Validated login payload containing email and plain password.

        Returns:
        - Tuple of (User entity, JWT access token string).

        Raises:
        - UnauthorizedException: If credentials do not match or if account is deactivated.
        """
        user = await UserRepository.get_by_email(db, data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password.")
        
        if not user.is_active:
            raise UnauthorizedException("This user account is deactivated.")

        token = create_access_token(subject=user.id, role=user.role)
        return user, token

    @staticmethod
    async def get_current_user_profile(db: AsyncSession, user_id: str) -> User:
        """
        Fetches the user entity corresponding to the authenticated subject ID.

        Use Case:
        - Used by `/api/auth/me` to return current user session profile data.

        Parameters:
        - db: The active async database session.
        - user_id: User UUID string from token subject.

        Returns:
        - User entity.

        Raises:
        - NotFoundException: If user record no longer exists.
        """
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundException("User not found.")
        return user
