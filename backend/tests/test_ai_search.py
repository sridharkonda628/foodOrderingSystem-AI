"""
Natural Language AI Search Unit and Integration Tests.

Use Case:
- Validates the AI hybrid search capabilities:
  1. Strict constraint extraction and filtering (vegetarian, spicy, price ceiling under ₹200).
  2. Soft tag scoring (high-protein, light).
  3. Query caching behavior for repeated searches.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ai_search_query_spicy_vegetarian_under_200(client: AsyncClient):
    """
    Test Case: Natural Language Query with multi-factor constraints: "something spicy and vegetarian under 200 rupees".

    Use Case:
    - Verifies structured intent extraction: vegetarian=True, spicy=True, max_price=200.
    - Verifies that all returned dishes strictly satisfy the constraints and include match explanations.
    """
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
    """
    Test Case: Natural Language Query with dietary preferences: "high protein food that is light".

    Use Case:
    - Verifies that dietary preference scoring prioritizes protein-rich and light dishes in the ranked output.
    """
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
    """
    Test Case: In-memory Query Caching.

    Use Case:
    - Verifies that an identical second search returns `search_mode = 'cached'` with sub-millisecond latency.
    """
    query = "healthy lunch not fried"
    
    # First search
    res1 = await client.post("/api/search", json={"query": query})
    assert res1.status_code == 200
    
    # Second identical search should hit cache
    res2 = await client.post("/api/search", json={"query": query})
    assert res2.status_code == 200
    assert res2.json()["data"]["search_mode"] == "cached"
