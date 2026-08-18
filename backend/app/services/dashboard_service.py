from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.order_repo import OrderRepository


class DashboardService:
    @staticmethod
    async def get_dashboard_metrics(db: AsyncSession) -> Dict[str, Any]:
        return await OrderRepository.get_dashboard_aggregates(db)
