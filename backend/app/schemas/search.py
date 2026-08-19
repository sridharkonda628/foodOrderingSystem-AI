"""
Natural Language AI Search Pydantic Schemas.

Use Case:
- Validates natural language food search queries (`SearchQueryRequest`).
- Represents structured search intents extracted from NLP queries (`SearchIntent`).
- Serializes scored dishes with match explanations and highlights (`ScoredMenuItemOut`, `SearchResponseData`).
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.menu import MenuItemOut


class SearchQueryRequest(BaseModel):
    """
    Request schema for natural language search queries.

    Use Case: Accepts freeform natural language prompts like "spicy paneer under 200".
    """
    query: str = Field(..., min_length=1, max_length=300, description="Natural language search query")
    limit: Optional[int] = Field(10, ge=1, le=50)


class SearchIntent(BaseModel):
    """
    Structured search intent extracted from natural language.

    Use Case:
    - Holds hard constraints (vegetarian, spicy, price limits) and soft preferences (tags, keywords)
      extracted by AI/NLP for database filtering and hybrid ranking.
    """
    vegetarian: Optional[bool] = None
    spicy: Optional[bool] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    category: Optional[str] = None
    preferred_tags: List[str] = Field(default_factory=list)
    avoid_tags: List[str] = Field(default_factory=list)
    meal_type: Optional[str] = None
    extracted_keywords: List[str] = Field(default_factory=list)


class ScoredMenuItemOut(MenuItemOut):
    """
    Response schema for a ranked search result item.

    Use Case:
    - Extends `MenuItemOut` with calculated relevance score (0.0 to 1.0),
      human-readable match explanation, and visual tag highlights.
    """
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    match_explanation: str
    match_highlights: List[str] = Field(default_factory=list)


class SearchResponseData(BaseModel):
    """
    Top-level payload returned by the AI search endpoint.

    Use Case:
    - Provides detected search intent, execution latency, search mode ('ai' | 'fallback' | 'cached'),
      and the ranked list of matched dishes.
    """
    query: str
    normalized_query: str
    detected_intent: SearchIntent
    results_count: int
    search_mode: str  # 'ai' | 'fallback' | 'cached'
    execution_time_ms: float
    items: List[ScoredMenuItemOut]
