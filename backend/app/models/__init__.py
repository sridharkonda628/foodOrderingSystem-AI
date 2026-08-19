"""
Database ORM Models Package.

Use Case:
- Exports all SQLAlchemy ORM models (User, Category, MenuItem, Order, OrderItem)
  so that table relationships are properly configured and discoverable.
"""

from app.models.user import User, UserRole
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem, OrderStatus

__all__ = [
    "User",
    "UserRole",
    "Category",
    "MenuItem",
    "Order",
    "OrderItem",
    "OrderStatus",
]
