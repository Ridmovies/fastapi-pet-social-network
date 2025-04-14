import pytest
from httpx import AsyncClient

version_prefix = "/api/v1"

# Параметры по умолчанию
DEFAULT_USER_DATA = {
    "is_active": True,
    "is_superuser": False,
    "is_verified": False,
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_data, expected_status_code",
    [
        (
                {**DEFAULT_USER_DATA, "email": "test_user@example.com", "password": "string"},
                201,
        ),
        (
                {**DEFAULT_USER_DATA, "email": "test_user2@example.com", "password": "string"},
                201,
        ),
    ],
)
async def test_register_user(client: AsyncClient, user_data, expected_status_code):
    response = await client.post(f"{version_prefix}/auth/register", json=user_data)
    assert response.status_code == expected_status_code



@pytest.mark.asyncio
async def test_get_user(auth_client: AsyncClient):
    response = await auth_client.get(f"{version_prefix}/users/1/profile")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_event(auth_client: AsyncClient):
    event_data = {
        "title": "Тестовое событие",
        "description": "Описание тестового события",
        "start_datetime": "2023-12-24T12:00:00",
        "location": "Москва, Россия",
        "user_id": 1,  # Идентификатор пользователя, создавшего событие
    }

    response = await auth_client.post(f"{version_prefix}/events", json=event_data)

    # Выводим подробную информацию при ошибке
    if response.status_code != 200:
        print("\nError details:")
        print(f"Status code: {response.status_code}")
        print("Response body:", response.json())

    assert response.status_code == 200


EVENT_CREATION_DATA = [
    ({"title": "Event 1", "description": "Description 1", "start_datetime": "2023-12-24T12:00:00", "location": "Location 1", "user_id": 1}, 200),
    ({"title": "Event 2", "start_datetime": "2023-12-24T12:00:00", "user_id": 1}, 200),
    ({"title": "Event 2", "start_datetime": "2023-12-24T12:00:00", "user_id": 999}, 404), # Ошибка 404 - нет такого пользователя
    ({"title": "Event 2"}, 422),
    ({"start_datetime": "2023-12-24T12:00:00"}, 422),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("event_data, expected_status_code", EVENT_CREATION_DATA)
async def test_create_event_with_params(auth_client: AsyncClient, event_data, expected_status_code):


    response = await auth_client.post(f"{version_prefix}/events", json=event_data)

    # Выводим подробную информацию при ошибке
    if response.status_code != 200:
        print("\nError details:")
        print(f"Status code: {response.status_code}")
        print("Response body:", response.json())

    assert response.status_code == expected_status_code

