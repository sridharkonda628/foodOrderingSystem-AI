import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.seed import seed_data

# Use SQLite in-memory or dedicated test db file
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
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Run seed data in test db
    async with TestingSessionLocal() as session:
        # Override session in seed temporarily
        import app.seed
        app.seed.AsyncSessionLocal = TestingSessionLocal
        await app.seed.seed_data()

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def admin_token(client: AsyncClient) -> str:
    res = await client.post(
        "/api/auth/login",
        json={"email": "admin@kpitech.com", "password": "AdminPass123!"}
    )
    assert res.status_code == 200
    return res.json()["data"]["access_token"]


@pytest_asyncio.fixture
async def customer_token(client: AsyncClient) -> str:
    res = await client.post(
        "/api/auth/login",
        json={"email": "customer@example.com", "password": "CustomerPass123!"}
    )
    assert res.status_code == 200
    return res.json()["data"]["access_token"]
