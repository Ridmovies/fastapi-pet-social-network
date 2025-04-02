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
                {**DEFAULT_USER_DATA, "username": "user1", "password": "string"},
                201,
        ),
        (
                {**DEFAULT_USER_DATA, "username": "user2", "password": "string"},
                201,
        ),
    ],
)
async def test_register_user(client: AsyncClient, user_data, expected_status_code):
    response = await client.post(f"{version_prefix}/users", json=user_data)
    assert response.status_code == expected_status_code


# @pytest.mark.asyncio
# async def test_login(client: AsyncClient):
#     # Данные для авторизации
#     login_data = {
#         "grant_type": "password",  # Обязательный параметр, должен быть "password"
#         "username": "user1",  # Обязательный параметр
#         "password": "string",  # Обязательный параметр
#         "scope": "",  # Необязательный параметр, отправляем пустым
#         "client_id": "",  # Необязательный параметр, отправляем пустым
#         "client_secret": "",  # Необязательный параметр, отправляем пустым
#     }
#
#     response = await client.post(f"{version_prefix}/auth/login", data=login_data)
#     assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user(auth_client: AsyncClient):
    response = await auth_client.get(f"{version_prefix}/users/1/profile")
    assert response.status_code == 200


# EVENT_CREATION_DATA = [
#     ({"content": "Post 1", "community_id": 1}, 200),  # Успешное создание поста
#     # ({"content": "", "community_id": 1}, 422),  # Пустой контент (должен вернуть ошибку)
#     # ({"content": "Post 2", "community_id": 999}, 404),  # Несуществующее сообщество
# ]



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



