import pytest

auth_prefix = f"/api/v1/auth"

@pytest.mark.asyncio
async def test_user_creation(client):
    response = await client.get(url="/dev")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_abc(client):
    assert 1 == 1