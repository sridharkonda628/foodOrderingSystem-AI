"""
Admin Dashboard Metrics Integration Tests.

Use Case:
- Validates role-based authorization for the Restaurant Manager Dashboard (customers blocked with 403, admins permitted).
- Asserts presence and integrity of aggregated analytics (KPI summaries, status counts, top-sellers, and recent orders).
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_dashboard_metrics(client: AsyncClient, admin_token: str, customer_token: str):
    """
    Test Case: Dashboard access control and metric computation.

    Use Case:
    - 1. Verifies that customers are rejected with HTTP 403 Forbidden.
    - 2. Verifies that admins successfully receive aggregated operational metrics and orders.
    """
    # 1. Customer rejected with 403 Forbidden
    cust_res = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert cust_res.status_code == 403

    # 2. Admin access granted
    admin_res = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_res.status_code == 200
    data = admin_res.json()["data"]
    
    # Assert metric fields
    assert "summary" in data
    assert "total_orders_today" in data["summary"]
    assert "total_revenue_today" in data["summary"]
    assert "orders_by_status" in data
    assert "top_selling_items" in data
    assert "recent_orders" in data
    assert len(data["recent_orders"]) > 0
