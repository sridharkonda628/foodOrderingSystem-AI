"""
Category Database Model.

Use Case:
- Defines the `categories` table representing restaurant menu sections (e.g. Starters, Main Course, Biryani).
- Supports display ordering, active status toggling, and one-to-many relationship with `MenuItem`.
"""

from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Category(Base):
    """
    Category ORM Entity.

    Use Case:
    - Organizes food items into logical customer-facing sections with display priority.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
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

    # Relationships: One Category has many MenuItems (cascade deletes orphaned items)
    menu_items = relationship("MenuItem", back_populates="category", cascade="all, delete-orphan")
