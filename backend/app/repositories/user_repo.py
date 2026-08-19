"""
User Repository.

Use Case:
- Provides database access methods for User entities (lookup by ID, lookup by email, and account creation).
- Used by `AuthService` and authentication dependency resolvers.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserRepository:
    """
    Repository handling persistence and queries for Users.
    """

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """
        Retrieves a user by unique primary key UUID.

        Use Case:
        - Used during JWT token validation (`get_current_user`) to verify user existence and active status.

        Parameters:
        - db: The active async database session.
        - user_id: User UUID string.

        Returns:
        - User entity if found, None otherwise.
        """
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Retrieves a user by lowercase trimmed email address.

        Use Case:
        - Used during login to look up account credentials and during registration to check for existing accounts.

        Parameters:
        - db: The active async database session.
        - email: Case-insensitive email string.

        Returns:
        - User entity if found, None otherwise.
        """
        stmt = select(User).where(User.email == email.lower().strip())
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user: User) -> User:
        """
        Inserts and commits a new User entity.

        Use Case:
        - Registers a new customer or admin user in the system.

        Parameters:
        - db: The active async database session.
        - user: Unpersisted User model instance.

        Returns:
        - Persisted User entity with assigned ID and timestamps.
        """
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
