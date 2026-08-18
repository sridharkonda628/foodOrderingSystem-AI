from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Category(Base):
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

    # Relationships
    menu_items = relationship("MenuItem", back_populates="category", cascade="all, delete-orphan")
