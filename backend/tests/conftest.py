"""
Pytest Test Fixtures and Async Test Harness Configuration.

Use Case:
- Configures an isolated SQLite test database for asynchronous test execution.
- Auto-seeds default admin/customer accounts, menu categories, 26 AI dishes, and sample orders before test suite runs.
- Provides async HTTP test clients (`AsyncClient`) and pre-authenticated admin/customer bearer tokens.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.seed import seed_data

# Dedicated test SQLite database file
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_food_ordering.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """
    Session-scoped test database lifecycle fixture.

    Use Case:
    - Creates fresh database tables, runs the seed script to load baseline test data,
      and cleans up tables after the test session finishes.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Run initial seed dataset into the test database
    async with TestingSessionLocal() as session:
        import app.seed
        app.seed.AsyncSessionLocal = TestingSessionLocal
        await app.seed.seed_data()

    yield

    # Teardown database tables upon test completion
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    """
    Dependency override replacing production database sessions with test database sessions.
    """
    async with TestingSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Apply FastAPI dependency override
app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def client():
    """
    Asynchronous HTTP test client fixture.

    Use Case:
    - Simulates incoming REST API requests against the FastAPI app.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def admin_token(client: AsyncClient) -> str:
    """
    Fixture providing an authenticated Admin JWT bearer token.

    Use Case:
    - Injected into test cases verifying admin-restricted operations.
    """
    res = await client.post(
        "/api/auth/login",
        json={"email": "admin@kpitech.com", "password": "AdminPass123!"}
    )
    assert res.status_code == 200
    return res.json()["data"]["access_token"]


@pytest_asyncio.fixture
async def customer_token(client: AsyncClient) -> str:
    """
    Fixture providing an authenticated Customer JWT bearer token.

    Use Case:
    - Injected into test cases verifying customer checkout and order history.
    """
    res = await client.post(
        "/api/auth/login",
        json={"email": "customer@example.com", "password": "CustomerPass123!"}
    )
    assert res.status_code == 200
    return res.json()["data"]["access_token"]
