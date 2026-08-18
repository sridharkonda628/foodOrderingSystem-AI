import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_registration_and_login(client: AsyncClient):
    # 1. Register new customer
    reg_payload = {
        "email": "newuser@example.com",
        "password": "SecurePassword123!",
        "full_name": "Test User",
        "role": "customer"
    }
    res = await client.post("/api/auth/register", json=reg_payload)
    assert res.status_code == 201
    body = res.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert body["data"]["user"]["email"] == "newuser@example.com"
    token = body["data"]["access_token"]

    # 2. Prevent duplicate email registration
    res_dup = await client.post("/api/auth/register", json=reg_payload)
    assert res_dup.status_code == 409
    assert res_dup.json()["success"] is False
    assert res_dup.json()["error"]["code"] == "CONFLICT"

    # 3. Login
    login_res = await client.post(
        "/api/auth/login",
        json={"email": "newuser@example.com", "password": "SecurePassword123!"}
    )
    assert login_res.status_code == 200
    assert login_res.json()["success"] is True
    assert "access_token" in login_res.json()["data"]

    # 4. Profile /me endpoint
    me_res = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_res.status_code == 200
    assert me_res.json()["data"]["email"] == "newuser@example.com"


@pytest.mark.asyncio
async def test_invalid_login_credentials(client: AsyncClient):
    res = await client.post(
        "/api/auth/login",
        json={"email": "admin@kpitech.com", "password": "WrongPassword!"}
    )
    assert res.status_code == 401
    assert res.json()["success"] is False
    assert res.json()["error"]["code"] == "UNAUTHORIZED"
