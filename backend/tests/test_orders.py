"""
Order Processing and State Machine Integration Tests.

Use Case:
- Validates:
  1. Order creation, accurate server-side price snapshotting, and sequential state progression.
  2. Immediate checkout rejection (HTTP 409) when cart contains an unavailable/out-of-stock item.
  3. Strict state machine rejection (HTTP 400) when attempting an illegal status transition (e.g. placed -> ready).
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_order_creation_and_price_snapshot(client: AsyncClient, customer_token: str, admin_token: str):
    """
    Test Case: Checkout calculation, price snapshotting, and valid state machine progression.

    Use Case:
    - 1. Fetches available dishes.
    - 2. Submits checkout payload and asserts server computes the total price correctly.
    - 3. Steps through valid state progression: placed -> confirmed -> preparing -> ready -> picked_up.
    """
    # 1. Fetch available menu items
    menu_res = await client.get("/api/menu?available_only=true")
    items = menu_res.json()["data"]
    assert len(items) >= 2
    item1, item2 = items[0], items[1]

    # 2. Place order with calculated total check on backend
    order_payload = {
        "items": [
            {"menu_item_id": item1["id"], "quantity": 2},
            {"menu_item_id": item2["id"], "quantity": 1}
        ],
        "delivery_notes": "Please ring doorbell"
    }
    expected_total = round((item1["price"] * 2) + (item2["price"] * 1), 2)

    order_res = await client.post(
        "/api/orders",
        json=order_payload,
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert order_res.status_code == 201
    order_data = order_res.json()["data"]
    assert order_data["status"] == "placed"
    assert order_data["total_amount"] == expected_total
    assert len(order_data["items"]) == 2
    order_id = order_data["id"]

    # 3. Verify state machine progression: placed -> confirmed -> preparing -> ready -> picked_up
    transitions = ["confirmed", "preparing", "ready", "picked_up"]
    for next_status in transitions:
        stat_res = await client.patch(
            f"/api/admin/orders/{order_id}/status",
            json={"status": next_status},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert stat_res.status_code == 200
        assert stat_res.json()["data"]["status"] == next_status


@pytest.mark.asyncio
async def test_order_rejection_for_unavailable_item(client: AsyncClient, customer_token: str):
    """
    Test Case: Out-of-Stock / Unavailable Dish Order Prevention.

    Use Case:
    - Verifies that attempting to checkout with an unavailable item raises ItemUnavailableException (HTTP 409 Conflict).
    """
    # Find the unavailable item in the database
    menu_res = await client.get("/api/menu?available_only=false")
    all_items = menu_res.json()["data"]
    unavail_item = next((i for i in all_items if not i["is_available"]), None)
    assert unavail_item is not None

    # Attempt order -> must fail with 409 Conflict / ItemUnavailableException
    order_res = await client.post(
        "/api/orders",
        json={
            "items": [{"menu_item_id": unavail_item["id"], "quantity": 1}],
            "delivery_notes": "Test"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert order_res.status_code == 409
    assert order_res.json()["error"]["code"] == "ITEM_UNAVAILABLE"


@pytest.mark.asyncio
async def test_invalid_order_state_transitions(client: AsyncClient, customer_token: str, admin_token: str):
    """
    Test Case: Order State Machine Constraint Enforcement.

    Use Case:
    - Verifies that attempting an illegal skip (e.g. PLACED -> READY) fails with HTTP 400 / INVALID_STATE_TRANSITION.
    """
    # Create order
    menu_res = await client.get("/api/menu?available_only=true")
    item = menu_res.json()["data"][0]
    
    order_res = await client.post(
        "/api/orders",
        json={"items": [{"menu_item_id": item["id"], "quantity": 1}]},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    order_id = order_res.json()["data"]["id"]

    # Attempt illegal skip: placed -> ready (must fail with 400 Bad Request)
    bad_res = await client.patch(
        f"/api/admin/orders/{order_id}/status",
        json={"status": "ready"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert bad_res.status_code == 400
    assert bad_res.json()["error"]["code"] == "INVALID_STATE_TRANSITION"
