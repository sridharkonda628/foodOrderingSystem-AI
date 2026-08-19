"""
Admin Dashboard and Analytics Schemas.

Use Case:
- Defines response models for the real-time Restaurant Manager Dashboard:
  - Metric summary (today's orders, revenue, average order value, active kitchen orders).
  - Status breakdown distribution.
  - Top 5 selling dishes.
  - Recent live incoming orders.
"""

from typing import List
from pydantic import BaseModel
from app.schemas.order import OrderOut


class MetricSummary(BaseModel):
    """
    High-level operational metrics for today.

    Use Case: Displayed in top KPI metric cards on Admin Dashboard.
    """
    total_orders_today: int
    total_revenue_today: float
    average_order_value_today: float
    active_orders_count: int


class StatusCount(BaseModel):
    """
    Count of orders grouped by lifecycle status.

    Use Case: Displayed in order status breakdown charts.
    """
    status: str
    count: int


class TopItemMetric(BaseModel):
    """
    Performance metric for high-demand menu items.

    Use Case: Identifies best-selling dishes by units sold and revenue.
    """
    menu_item_id: str
    name: str
    category_name: str
    units_sold: int
    revenue_generated: float


class DashboardResponseData(BaseModel):
    """
    Comprehensive aggregated dashboard response.

    Use Case: Feeds the Admin Dashboard analytics page in a single efficient payload.
    """
    summary: MetricSummary
    orders_by_status: List[StatusCount]
    top_selling_items: List[TopItemMetric]
    recent_orders: List[OrderOut]
