"""
Asynchronous Database Engine and Session Management.

Use Case:
- Configures the SQLAlchemy AsyncEngine and session factory (`AsyncSessionLocal`).
- Provides the `get_db` FastAPI dependency for request-scoped database transactions.
- Provides `init_db` for automatic table creation upon startup and test runs.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
from app.db.base import Base

# Specific connect arguments for SQLite multi-threaded async execution
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Create the global async engine instance
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args
)

# Async session factory for spawning new database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency yielding an isolated asynchronous database session per request.

    Use Case:
    - Injected into FastAPI route handlers (`Depends(get_db)`).
    - Automatically rolls back any uncommitted changes if an exception is raised,
      and guarantees session closure in the `finally` block.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initializes all database tables mapped to the declarative Base.

    Use Case:
    - Called during application startup (in `lifespan`) and before tests or seeding.
    - Creates tables if they do not already exist.
    """
    import app.models  # noqa: F401 - ensures all model definitions are registered in Base.metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
