"""
AI Natural Language Search API Endpoints.

Use Case:
- Provides the core intelligent food search endpoint:
  POST `/api/search`: Accepts natural language prompts (e.g., "healthy spicy vegetarian dinner under 200")
  and returns ranked matching menu items with structured intent analysis and match explanations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.common import APIResponse
from app.schemas.search import SearchQueryRequest, SearchResponseData
from app.services.search_service import MenuSearchService

router = APIRouter(prefix="/search", tags=["AI Search"])


@router.post("", response_model=APIResponse[SearchResponseData])
async def natural_language_search(
    request: SearchQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Executes an AI-powered natural language menu search.

    Use Case:
    - Main search bar on the customer food ordering interface.
    - Processes freeform food requests, extracts intent, applies candidate filters,
      runs multi-signal hybrid ranking, and returns dishes with match explanations.

    Parameters:
    - request: Search query and result limit.
    - db: Async database session.

    Returns:
    - APIResponse containing `SearchResponseData`.
    """
    search_data = await MenuSearchService.search(db, request)
    return APIResponse(
        success=True,
        data=search_data,
        message=f"Found {search_data.results_count} matching dishes"
    )
