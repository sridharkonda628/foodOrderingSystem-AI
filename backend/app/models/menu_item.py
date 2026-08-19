"""
Menu Item Database Model.

Use Case:
- Defines the `menu_items` table storing individual culinary dishes.
- Contains rich metadata for AI hybrid search and filtering: pricing, vegetarian flag,
  spiciness flag, JSON dietary tags, live availability status, and popularity score.
"""

import uuid
from datetime import datetime, timezone
from typing import List
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class MenuItem(Base):
    """
    MenuItem ORM Entity.

    Use Case:
    - Represents a dish on the restaurant menu.
    - Queried by customers browsing categories, searched by AI NLP engine, and added to orders.
    """
    __tablename__ = "menu_items"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=""
    )
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    is_vegetarian: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True
    )
    is_spicy: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )
    dietary_tags: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True
    )
    popularity_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
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

    # Relationships
    category = relationship("Category", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")
