"""
Admin Operations API Endpoints.

Use Case:
- Provides protected endpoints restricted to users with the 'admin' role:
  1. GET `/api/admin/dashboard`: Real-time operational KPI summary, revenue, status breakdown, top sellers, and recent orders.
  2. GET `/api/admin/orders`: List all customer orders with status filtering.
  3. PATCH `/api/admin/orders/{order_id}/status`: Progress orders through the kitchen workflow state machine.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_active_admin
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.dashboard import DashboardResponseData, MetricSummary, StatusCount, TopItemMetric
from app.schemas.order import OrderOut, OrderStatusUpdate
from app.api.routes.orders import _format_order_out
from app.services.dashboard_service import DashboardService
from app.services.order_service import OrderService

router = APIRouter(prefix="/admin", tags=["Admin Operations"])


@router.get("/dashboard", response_model=APIResponse[DashboardResponseData])
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_active_admin)
):
    """
    Retrieves real-time analytics for the Restaurant Manager Dashboard.

    Use Case:
    - Renders KPI metric cards, status charts, best-selling dishes, and recent orders for kitchen management.

    Parameters:
    - db: Async database session.
    - admin: Verified admin user.

    Returns:
    - APIResponse containing `DashboardResponseData`.
    """
    raw_metrics = await DashboardService.get_dashboard_metrics(db)
    
    summary = MetricSummary(**raw_metrics["summary"])
    orders_by_status = [StatusCount(**s) for s in raw_metrics["orders_by_status"]]
    top_selling_items = [TopItemMetric(**t) for t in raw_metrics["top_selling_items"]]
    recent_orders = [_format_order_out(o) for o in raw_metrics["recent_orders"]]

    data = DashboardResponseData(
        summary=summary,
        orders_by_status=orders_by_status,
        top_selling_items=top_selling_items,
        recent_orders=recent_orders
    )
    return APIResponse(
        success=True,
        data=data,
        message="Dashboard analytics generated"
    )


@router.get("/orders", response_model=APIResponse[List[OrderOut]])
async def get_all_orders(
    status: Optional[str] = Query(None, description="Filter by status (placed, preparing, ready, etc.)"),
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_active_admin)
):
    """
    Retrieves all restaurant orders with optional status filtering.

    Use Case:
    - Populates the admin order management queue for kitchen staff.

    Parameters:
    - status: Optional lifecycle status filter.
    - limit: Page size limit.
    - offset: Page offset.
    - db: Async database session.
    - admin: Verified admin user.

    Returns:
    - APIResponse containing list of `OrderOut` records.
    """
    orders = await OrderService.get_all_orders_for_admin(db, status=status, limit=limit, offset=offset)
    data = [_format_order_out(o) for o in orders]
    return APIResponse(
        success=True,
        data=data,
        message="All restaurant orders retrieved"
    )


@router.patch("/orders/{order_id}/status", response_model=APIResponse[OrderOut])
async def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_active_admin)
):
    """
    Updates the lifecycle status of an order.

    Use Case:
    - Kitchen staff moves orders along the progression: placed -> confirmed -> preparing -> ready -> picked_up.

    Parameters:
    - order_id: UUID of the order to update.
    - data: Schema specifying target status.
    - db: Async database session.
    - admin: Verified admin user.

    Returns:
    - APIResponse containing updated `OrderOut`.
    """
    order = await OrderService.update_order_status(db, order_id, data.status.value, admin)
    return APIResponse(
        success=True,
        data=_format_order_out(order),
        message=f"Order status updated to '{data.status.value}'"
    )
