import pytest
from httpx import AsyncClient

version_prefix = "/api/v1"


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    json_data = {
        "email": "test_user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }
    response = await client.post(f"{version_prefix}/auth/register", json=json_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient):
    response = await client.get(f"{version_prefix}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(isinstance(user, dict) for user in response.json())
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "test_user@example.com"