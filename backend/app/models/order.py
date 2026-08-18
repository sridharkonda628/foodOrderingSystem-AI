import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class OrderStatus(str, Enum):
    PLACED = "placed"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    PICKED_UP = "picked_up"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    customer_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default=OrderStatus.PLACED.value,
        nullable=False,
        index=True
    )
    total_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )
    delivery_notes: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=""
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    customer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    order_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    menu_item_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("menu_items.id", ondelete="RESTRICT"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )
    unit_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    subtotal: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")
