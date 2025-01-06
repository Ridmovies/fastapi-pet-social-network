from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

import pytest_asyncio

from src.database import engine
from src.main import app
from src.models import Base


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    # if settings.MODE != "TEST":
    #     raise Exception

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create a http client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
