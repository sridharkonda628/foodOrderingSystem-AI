from typing import List
from pydantic import BaseModel
from app.schemas.order import OrderOut


class MetricSummary(BaseModel):
    total_orders_today: int
    total_revenue_today: float
    average_order_value_today: float
    active_orders_count: int


class StatusCount(BaseModel):
    status: str
    count: int


class TopItemMetric(BaseModel):
    menu_item_id: str
    name: str
    category_name: str
    units_sold: int
    revenue_generated: float


class DashboardResponseData(BaseModel):
    summary: MetricSummary
    orders_by_status: List[StatusCount]
    top_selling_items: List[TopItemMetric]
    recent_orders: List[OrderOut]
