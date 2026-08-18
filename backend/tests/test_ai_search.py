import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ai_search_query_spicy_vegetarian_under_200(client: AsyncClient):
    search_payload = {
        "query": "something spicy and vegetarian under 200 rupees",
        "limit": 5
    }
    res = await client.post("/api/search", json=search_payload)
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    data = body["data"]

    # 1. Verify structured intent extraction
    intent = data["detected_intent"]
    assert intent["vegetarian"] is True
    assert intent["spicy"] is True
    assert intent["max_price"] == 200.0

    # 2. Verify all returned candidates strictly conform to hard constraints
    items = data["items"]
    assert len(items) > 0
    for it in items:
        assert it["is_vegetarian"] is True
        assert it["is_spicy"] is True
        assert it["price"] <= 200.0
        assert it["is_available"] is True
        assert it["relevance_score"] > 0.0
        assert len(it["match_explanation"]) > 0


@pytest.mark.asyncio
async def test_ai_search_query_high_protein_and_light(client: AsyncClient):
    res = await client.post(
        "/api/search",
        json={"query": "high protein food that is light", "limit": 5}
    )
    assert res.status_code == 200
    items = res.json()["data"]["items"]
    assert len(items) > 0
    # Top results should have high protein and light tags
    top_item = items[0]
    assert any("protein" in tag for tag in top_item["dietary_tags"]) or "light" in top_item["dietary_tags"]


@pytest.mark.asyncio
async def test_ai_search_caching(client: AsyncClient):
    query = "healthy lunch not fried"
    
    # First search
    res1 = await client.post("/api/search", json={"query": query})
    assert res1.status_code == 200
    
    # Second identical search should hit cache
    res2 = await client.post("/api/search", json={"query": query})
    assert res2.status_code == 200
    assert res2.json()["data"]["search_mode"] == "cached"
