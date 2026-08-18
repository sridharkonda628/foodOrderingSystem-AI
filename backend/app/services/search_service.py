import time
import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.base import AIProvider
from app.ai.mock_provider import MockAIProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.ranking import HybridRankingEngine
from app.ai.cache import search_cache
from app.core.config import settings
from app.models.menu_item import MenuItem
from app.repositories.menu_repo import MenuRepository
from app.schemas.search import (
    SearchQueryRequest,
    SearchIntent,
    ScoredMenuItemOut,
    SearchResponseData
)
from app.schemas.menu import MenuItemOut

logger = logging.getLogger("kpitech_food_order")


class MenuSearchService:
    @staticmethod
    def get_ai_provider() -> AIProvider:
        if settings.AI_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            return OpenAIProvider()
        return MockAIProvider()

    @classmethod
    async def search(
        cls,
        db: AsyncSession,
        request: SearchQueryRequest
    ) -> SearchResponseData:
        start_time = time.perf_counter()
        raw_query = request.query.strip()
        normalized_query = " ".join(raw_query.lower().split())

        # 1. Check Query Cache
        cached_data = search_cache.get(normalized_query)
        if cached_data:
            cached_data.search_mode = "cached"
            cached_data.execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return cached_data

        # 2. Extract Intent via AI Provider with Graceful Fallback
        provider = cls.get_ai_provider()
        search_mode = "ai"
        try:
            intent: SearchIntent = await provider.extract_intent(raw_query)
        except Exception as exc:
            logger.warning(f"AI Provider failed for query '{raw_query}': {exc}. Falling back to deterministic NLP.")
            fallback_provider = MockAIProvider()
            intent = await fallback_provider.extract_intent(raw_query)
            search_mode = "fallback"

        # 3. Retrieve Candidates from DB using Deterministic Hard Filters
        candidates: List[MenuItem] = await MenuRepository.get_search_candidates(
            db=db,
            max_price=intent.max_price,
            is_vegetarian=intent.vegetarian,
            is_spicy=intent.spicy,
            category_id=None
        )

        # 4. Hybrid Multi-Signal Ranking
        ranked_candidates = HybridRankingEngine.rank_items(
            query=raw_query,
            intent=intent,
            items=candidates
        )

        # Apply Limit
        top_items = ranked_candidates[: request.limit]

        # 5. Generate Match Explanations
        scored_results: List[ScoredMenuItemOut] = []
        for item, score, highlights in top_items:
            try:
                explanation = await provider.generate_explanation(
                    query=raw_query,
                    item_name=item.name,
                    item_desc=item.description,
                    dietary_tags=item.dietary_tags,
                    price=item.price,
                    is_vegetarian=item.is_vegetarian,
                    is_spicy=item.is_spicy
                )
            except Exception:
                explanation = f"Matches '{raw_query}' (₹{item.price:,.0f})"

            scored_item = ScoredMenuItemOut(
                id=item.id,
                name=item.name,
                description=item.description,
                category_id=item.category_id,
                category_name=item.category.name if item.category else None,
                category_slug=item.category.slug if item.category else None,
                price=item.price,
                is_vegetarian=item.is_vegetarian,
                is_spicy=item.is_spicy,
                dietary_tags=item.dietary_tags,
                is_available=item.is_available,
                popularity_score=item.popularity_score,
                created_at=item.created_at,
                updated_at=item.updated_at,
                relevance_score=score,
                match_explanation=explanation,
                match_highlights=highlights
            )
            scored_results.append(scored_item)

        execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        response_data = SearchResponseData(
            query=raw_query,
            normalized_query=normalized_query,
            detected_intent=intent,
            results_count=len(scored_results),
            search_mode=search_mode,
            execution_time_ms=execution_time_ms,
            items=scored_results
        )

        # Store in cache for 5 minutes
        search_cache.set(normalized_query, response_data, ttl_seconds=300)

        return response_data
