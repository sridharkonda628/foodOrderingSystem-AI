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
    search_data = await MenuSearchService.search(db, request)
    return APIResponse(
        success=True,
        data=search_data,
        message=f"Found {search_data.results_count} matching dishes"
    )
