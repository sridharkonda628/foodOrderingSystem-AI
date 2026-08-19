"""
SQLAlchemy Declarative Base.

Use Case:
- Serves as the base class from which all ORM models (User, Category, MenuItem, Order, OrderItem) inherit.
- Enables SQLAlchemy metadata collection and schema migrations.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy declarative database models.
    """
    pass
