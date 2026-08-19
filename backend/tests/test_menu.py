"""
Menu and Category Management Integration Tests.

Use Case:
- Validates category listing, vegetarian filtering, admin role enforcement for dish creation,
  and dish availability toggling.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_categories_and_menu_items(client: AsyncClient):
    """
    Test Case: Public Menu Browsing.

    Use Case:
    - 1. Fetches categories and verifies seeded categories exist.
    - 2. Filters dishes by `is_vegetarian=true` and asserts all returned items are vegetarian.
    """
    # 1. Categories
    cat_res = await client.get("/api/menu/categories")
    assert cat_res.status_code == 200
    categories = cat_res.json()["data"]
    assert len(categories) >= 7

    # 2. Filter menu items by vegetarian
    veg_res = await client.get("/api/menu?is_vegetarian=true")
    assert veg_res.status_code == 200
    veg_items = veg_res.json()["data"]
    assert len(veg_items) > 0
    assert all(it["is_vegetarian"] is True for it in veg_items)


@pytest.mark.asyncio
async def test_admin_menu_management(client: AsyncClient, admin_token: str, customer_token: str):
    """
    Test Case: Role-restricted Menu Item Creation and Availability Toggling.

    Use Case:
    - 1. Verifies that customers cannot create menu items (HTTP 403 Forbidden).
    - 2. Verifies that admins can create new menu items with full attributes.
    - 3. Verifies that admins can toggle dish availability (in stock vs 86'd).
    """
    # 1. Customer cannot create menu item (Forbidden 403)
    create_payload = {
        "name": "Unauthorized Dish",
        "description": "Should fail",
        "category_id": 1,
        "price": 199.0,
        "is_vegetarian": True,
        "is_spicy": False,
        "dietary_tags": ["starter"],
        "is_available": True
    }
    cust_res = await client.post(
        "/api/menu",
        json=create_payload,
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert cust_res.status_code == 403

    # 2. Admin creates menu item
    admin_create_payload = {
        "name": "Chef Special Paneer Platter",
        "description": "Assorted gourmet tandoori paneer skewers",
        "category_id": 1,
        "price": 320.0,
        "is_vegetarian": True,
        "is_spicy": True,
        "dietary_tags": ["special", "high-protein"],
        "is_available": True
    }
    create_res = await client.post(
        "/api/menu",
        json=admin_create_payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_res.status_code == 201
    created_item = create_res.json()["data"]
    item_id = created_item["id"]
    assert created_item["name"] == "Chef Special Paneer Platter"

    # 3. Admin toggles availability
    toggle_res = await client.patch(
        f"/api/menu/{item_id}/availability",
        json={"is_available": False},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert toggle_res.status_code == 200
    assert toggle_res.json()["data"]["is_available"] is False
