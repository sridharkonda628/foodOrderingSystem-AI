from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.core.logging import RequestLoggingMiddleware
from app.db.session import init_db
from app.api.routes import auth, menu, orders, admin, search, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup (especially convenient for dev/SQLite)
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Food Ordering System with AI-Powered Natural Language Menu Search (KPi-Tech AI Software Engineer Assignment)",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging & Latency Middleware
app.add_middleware(RequestLoggingMiddleware)

# Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Mount Routes
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(menu.router, prefix=settings.API_V1_STR)
app.include_router(orders.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(health.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_prefix": settings.API_V1_STR
    }
