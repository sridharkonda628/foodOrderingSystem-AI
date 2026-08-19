"""
Order and Order Item Database Models and Status Enum.

Use Case:
- Defines the `orders` and `order_items` tables.
- Implements price snapshotting (storing `unit_price` and `subtotal` at checkout time)
  to preserve financial integrity regardless of future menu price modifications.
- Implements standard order lifecycle statuses via `OrderStatus`.
"""

import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class OrderStatus(str, Enum):
    """
    Enumeration of allowed order lifecycle states.

    Use Case:
    - Enforces state consistency across database records, API schemas, and state machine transitions.
    """
    PLACED = "placed"          # Customer submitted order
    CONFIRMED = "confirmed"    # Restaurant acknowledged and accepted order
    PREPARING = "preparing"    # Kitchen actively preparing the dishes
    READY = "ready"            # Food packaged and awaiting delivery/pickup
    PICKED_UP = "picked_up"    # Delivered or collected by customer (terminal success state)
    CANCELLED = "cancelled"    # Cancelled by customer or admin (terminal abort state)


class Order(Base):
    """
    Order ORM Entity.

    Use Case:
    - Represents the header of a customer order transaction, tracking status, customer ID,
      calculated total amount, and delivery notes.
    """
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
    """
    OrderItem ORM Entity.

    Use Case:
    - Represents individual line items in an order.
    - Stores `unit_price` and `subtotal` snapshots at time of purchase.
    """
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
