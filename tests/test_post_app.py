import pytest

auth_prefix = f"/api/v1"

@pytest.mark.asyncio
async def test_user_creation(client):
    response = await client.get(url=f"{auth_prefix}/dev")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

