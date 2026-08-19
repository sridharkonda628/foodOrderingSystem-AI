"""
Main FastAPI Application Entrypoint.

Use Case:
- Configures the FastAPI server, lifespan events, CORS policies, logging middleware,
  exception handlers, and mounts all versioned API route modules.
- Serves as the central backend integration point for the Food Ordering System.
"""

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
    """
    Application lifespan context manager.

    Use Case:
    - Runs startup tasks before the server starts accepting incoming requests
      (e.g., initializes database tables if they do not exist).
    - Cleans up resources or database connections upon application shutdown.
    """
    # Initialize database tables on startup (especially convenient for dev/SQLite)
    await init_db()
    yield


# Instantiate the FastAPI application with metadata and lifespan handler
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Food Ordering System with AI-Powered Natural Language Menu Search (KPi-Tech AI Software Engineer Assignment)",
    lifespan=lifespan
)

# Configure Cross-Origin Resource Sharing (CORS) to allow frontend clients (e.g. Vite/React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom logging and latency tracking middleware
app.add_middleware(RequestLoggingMiddleware)

# Register custom exception handlers for consistent API error responses
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Mount API Route Modules with the configured API version prefix (e.g., /api)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(menu.router, prefix=settings.API_V1_STR)
app.include_router(orders.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(health.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """
    Root information endpoint.

    Use Case:
    - Provides quick verification that the backend service is running.
    - Returns basic metadata including project name, version, and documentation link.
    """
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_prefix": settings.API_V1_STR
    }
