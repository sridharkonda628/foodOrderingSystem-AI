import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_dashboard_metrics(client: AsyncClient, admin_token: str, customer_token: str):
    # Customer rejected
    cust_res = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert cust_res.status_code == 403

    # Admin access
    admin_res = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_res.status_code == 200
    data = admin_res.json()["data"]
    
    assert "summary" in data
    assert "total_orders_today" in data["summary"]
    assert "total_revenue_today" in data["summary"]
    assert "orders_by_status" in data
    assert "top_selling_items" in data
    assert "recent_orders" in data
    assert len(data["recent_orders"]) > 0
