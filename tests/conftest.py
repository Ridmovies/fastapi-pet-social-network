from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

import pytest_asyncio

from src.config import settings
from src.database import engine, Base
from src.main import app


@pytest_asyncio.fixture(scope="module", autouse=True)
async def prepare_database():
    if settings.MODE != "TEST":
        raise Exception

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


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient) -> AsyncGenerator[AsyncClient, None]:
    """Create an authenticated http client."""
    # Данные для авторизации
    login_data = {
        "grant_type": "password",
        "email": "test_user@example.com",
        "password": "string",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    # Выполняем запрос на авторизацию
    response = await client.post("api/v1/auth/login", data=login_data)
    assert response.status_code == 200

    # Получаем токен из ответа
    token_data = response.json()
    access_token = token_data["access_token"]
    token_type = token_data["token_type"]

    # Устанавливаем заголовок авторизации для клиента
    client.headers.update({
        "Authorization": f"{token_type} {access_token}"
    })

    yield client

    # Очищаем заголовки после завершения теста
    client.headers.pop("Authorization", None)