"""
User Database Model and UserRole Enum.

Use Case:
- Defines the `users` table for system authentication and authorization.
- Supports Role-Based Access Control (RBAC) separating 'admin' (restaurant manager)
  from 'customer' (ordering patrons).
"""

import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class UserRole(str, Enum):
    """
    Role-Based Access Control (RBAC) Roles.

    Use Case:
    - ADMIN: Access to analytics dashboard, menu item CRUD, and order status updates.
    - CUSTOMER: Access to browsing menu, searching dishes, placing orders, and order history.
    """
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(Base):
    """
    User ORM Entity.

    Use Case:
    - Stores account credentials (email, bcrypt password hash), profile name, active flag,
      and assigned user role.
    """
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(50),
        default=UserRole.CUSTOMER.value,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships: One customer has many placed orders
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
