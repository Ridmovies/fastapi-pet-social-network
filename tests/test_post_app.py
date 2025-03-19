import pytest

prefix = f"/api/v1/post"


@pytest.mark.asyncio
async def test_user_creation(client):
    response = await client.get(url=f"{prefix}")
    assert response.status_code == 200
