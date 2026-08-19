"""
Order Repository and Analytics Aggregation.

Use Case:
- Manages order creation, retrieval, and status updates in the database.
- Implements high-performance SQL aggregation queries for the Real-time Restaurant Manager Dashboard
  (calculates today's total orders, gross revenue, average order value, active kitchen orders,
  status distribution, and top 5 best-selling items).
"""

from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order, OrderItem, OrderStatus
from app.models.user import User
from app.models.menu_item import MenuItem
from app.models.category import Category


class OrderRepository:
    """
    Repository handling persistence, status lifecycle, and analytics aggregation for Orders.
    """

    @staticmethod
    async def create_order(
        db: AsyncSession,
        order: Order,
        items: List[OrderItem]
    ) -> Order:
        """
        Persists a new Order and its line items inside an atomic database transaction.

        Use Case:
        - Called by `OrderService.create_order` during customer checkout.
        - Refreshes and loads customer and dish relationships for the returned model.

        Parameters:
        - db: The active async database session.
        - order: The parent Order instance.
        - items: The list of associated OrderItem instances.

        Returns:
        - Fully populated Order entity with items and customer relationship.
        """
        db.add(order)
        for item in items:
            db.add(item)
        await db.commit()
        
        # Reload with items and customer
        stmt = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(OrderItem.menu_item)
            )
            .where(Order.id == order.id)
        )
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def get_by_id(db: AsyncSession, order_id: str) -> Optional[Order]:
        """
        Retrieves a single order by ID with customer details and line items loaded.

        Use Case:
        - Used for live order tracking, customer receipt view, and admin status updates.

        Parameters:
        - db: The active async database session.
        - order_id: UUID string of the order.

        Returns:
        - Order entity if found, None otherwise.
        """
        stmt = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(OrderItem.menu_item)
            )
            .where(Order.id == order_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_customer_orders(
        db: AsyncSession,
        customer_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Order]:
        """
        Retrieves order history for a specific customer, sorted newest first.

        Use Case:
        - Populates the customer's "My Orders" history page.

        Parameters:
        - db: The active async database session.
        - customer_id: UUID of the authenticated user.
        - limit: Maximum number of orders to fetch.
        - offset: Pagination offset.

        Returns:
        - List of Order entities for this customer.
        """
        stmt = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(OrderItem.menu_item)
            )
            .where(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_all_orders(
        db: AsyncSession,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Order]:
        """
        Retrieves all restaurant orders, with optional status filtering and pagination.

        Use Case:
        - Powers the Admin Order Management table with real-time status filtering (e.g. view only 'preparing' orders).

        Parameters:
        - db: The active async database session.
        - status: Optional status filter (e.g. 'placed', 'preparing').
        - limit: Maximum number of records.
        - offset: Pagination offset.

        Returns:
        - List of all matching Order entities across all customers.
        """
        stmt = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(OrderItem.menu_item)
            )
            .order_by(Order.created_at.desc())
        )
        if status:
            stmt = stmt.where(Order.status == status)
        stmt = stmt.limit(limit).offset(offset)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def update_status(
        db: AsyncSession,
        order: Order,
        new_status: str
    ) -> Order:
        """
        Updates an order's status and commits the change.

        Use Case:
        - Progresses orders through kitchen workflow (placed -> confirmed -> preparing -> ready -> picked_up).

        Parameters:
        - db: The active async database session.
        - order: The existing Order entity.
        - new_status: The target status string.

        Returns:
        - Updated Order entity.
        """
        order.status = new_status
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def get_dashboard_aggregates(db: AsyncSession) -> Dict[str, Any]:
        """
        Computes restaurant analytics via database aggregation.

        Use Case:
        - Powers the Admin Dashboard with operational insights:
          1. Today's total orders and gross revenue (excluding cancelled orders).
          2. Average order value (AOV) for today.
          3. Live active kitchen orders count (placed, confirmed, preparing, ready).
          4. Distribution breakdown of orders by status.
          5. Top 5 highest selling menu items with units sold and revenue generated.
          6. The 10 most recent orders.

        Parameters:
        - db: The active async database session.

        Returns:
        - Dictionary structured for `DashboardResponseData`.
        """
        # Start of today in UTC
        now = datetime.now(timezone.utc)
        start_of_today = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        
        # 1. Total orders today and revenue today
        today_stmt = (
            select(
                func.count(Order.id).label("total_orders"),
                func.coalesce(func.sum(Order.total_amount), 0.0).label("total_revenue")
            )
            .where(Order.created_at >= start_of_today)
            .where(Order.status != OrderStatus.CANCELLED.value)
        )
        today_res = await db.execute(today_stmt)
        today_row = today_res.one()
        total_orders_today = int(today_row.total_orders or 0)
        total_revenue_today = float(today_row.total_revenue or 0.0)
        avg_order_value = round(total_revenue_today / total_orders_today, 2) if total_orders_today > 0 else 0.0

        # 2. Active orders count (placed, confirmed, preparing, ready)
        active_statuses = [
            OrderStatus.PLACED.value,
            OrderStatus.CONFIRMED.value,
            OrderStatus.PREPARING.value,
            OrderStatus.READY.value
        ]
        active_stmt = (
            select(func.count(Order.id))
            .where(Order.status.in_(active_statuses))
        )
        active_res = await db.execute(active_stmt)
        active_orders_count = int(active_res.scalar_one() or 0)

        # 3. Status breakdown
        status_stmt = (
            select(Order.status, func.count(Order.id).label("count"))
            .group_by(Order.status)
        )
        status_res = await db.execute(status_stmt)
        orders_by_status = [{"status": row.status, "count": int(row.count)} for row in status_res.all()]

        # 4. Top selling items (units sold and revenue generated)
        top_items_stmt = (
            select(
                MenuItem.id.label("menu_item_id"),
                MenuItem.name.label("name"),
                Category.name.label("category_name"),
                func.sum(OrderItem.quantity).label("units_sold"),
                func.sum(OrderItem.subtotal).label("revenue_generated")
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Category, MenuItem.category_id == Category.id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(Order.status != OrderStatus.CANCELLED.value)
            .group_by(MenuItem.id, MenuItem.name, Category.name)
            .order_by(desc("units_sold"))
            .limit(5)
        )
        top_items_res = await db.execute(top_items_stmt)
        top_selling_items = [
            {
                "menu_item_id": row.menu_item_id,
                "name": row.name,
                "category_name": row.category_name,
                "units_sold": int(row.units_sold or 0),
                "revenue_generated": float(row.revenue_generated or 0.0)
            }
            for row in top_items_res.all()
        ]

        # 5. Recent orders
        recent_orders_stmt = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(OrderItem.menu_item)
            )
            .order_by(Order.created_at.desc())
            .limit(10)
        )
        recent_res = await db.execute(recent_orders_stmt)
        recent_orders = list(recent_res.scalars().all())

        return {
            "summary": {
                "total_orders_today": total_orders_today,
                "total_revenue_today": round(total_revenue_today, 2),
                "average_order_value_today": avg_order_value,
                "active_orders_count": active_orders_count,
            },
            "orders_by_status": orders_by_status,
            "top_selling_items": top_selling_items,
            "recent_orders": recent_orders
        }
