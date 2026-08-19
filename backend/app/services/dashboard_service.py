"""
Admin Dashboard Analytics Service.

Use Case:
- Orchestrates the retrieval of high-level restaurant operational metrics,
  order volume, financial aggregates, and sales leaderboards for the Admin Dashboard.
"""

from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.order_repo import OrderRepository


class DashboardService:
    """
    Service providing aggregated analytics data for the Restaurant Manager.
    """

    @staticmethod
    async def get_dashboard_metrics(db: AsyncSession) -> Dict[str, Any]:
        """
        Retrieves real-time aggregated metrics for the admin dashboard.

        Use Case:
        - Called by `/api/admin/dashboard` to generate executive summary KPI cards,
          status distribution charts, top-selling items list, and recent orders.

        Parameters:
        - db: The active async database session.

        Returns:
        - Dictionary containing metric summary, orders by status, top items, and recent orders.
        """
        return await OrderRepository.get_dashboard_aggregates(db)
