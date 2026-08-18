import time
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.config import settings
from app.schemas.common import APIResponse

router = APIRouter(prefix="/health", tags=["Health & Observability"])


@router.get("", response_model=APIResponse[dict])
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"

    return APIResponse(
        success=(db_status == "healthy"),
        data={
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "database": db_status,
            "ai_provider": settings.AI_PROVIDER,
            "timestamp": time.time()
        },
        message="System health status"
    )


@router.get("/ai", response_model=APIResponse[dict])
async def ai_health_check():
    provider_type = settings.AI_PROVIDER
    is_ready = True
    details = "Mock NLP provider ready"
    
    if provider_type == "openai":
        if not settings.OPENAI_API_KEY:
            is_ready = False
            details = "OpenAI selected but OPENAI_API_KEY is not provided (falls back to mock)"
        else:
            details = f"OpenAI configured with model {settings.OPENAI_MODEL}"

    return APIResponse(
        success=is_ready,
        data={
            "provider": provider_type,
            "configured": is_ready,
            "details": details
        },
        message="AI subsystem status"
    )
