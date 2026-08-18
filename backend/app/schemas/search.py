from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.menu import MenuItemOut


class SearchQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=300, description="Natural language search query")
    limit: Optional[int] = Field(10, ge=1, le=50)


class SearchIntent(BaseModel):
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
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    match_explanation: str
    match_highlights: List[str] = Field(default_factory=list)


class SearchResponseData(BaseModel):
    query: str
    normalized_query: str
    detected_intent: SearchIntent
    results_count: int
    search_mode: str  # 'ai' | 'fallback' | 'cached'
    execution_time_ms: float
    items: List[ScoredMenuItemOut]
