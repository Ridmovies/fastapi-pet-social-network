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
@pytest.mark.parametrize(
    "follow_user_id, expected_status, expected_detail",
    [
        # Успешная подписка на пользователя с ID 2
        (2, 200, None),
        # # Повторная подписка на пользователя с ID 2 (должна вернуть ошибку)
        # (2, 400, "Вы уже подписаны на этого пользователя"),
        # # Попытка подписаться на самого себя (должна вернуть ошибку)
        # (1, 400, "Нельзя подписаться на самого себя"),
        # # Попытка подписаться на несуществующего пользователя (должна вернуть ошибку)
        # (999, 404, "Пользователь для подписки не найден"),
    ],
)
async def test_following(client: AsyncClient, follow_user_id, expected_status, expected_detail):
    # Данные для авторизации
    login_data = {
        "grant_type": "password",  # Обязательный параметр, должен быть "password"
        "username": "test_user@example.com",  # Обязательный параметр
        "password": "string",  # Обязательный параметр
        "scope": "",  # Необязательный параметр, отправляем пустым
        "client_id": "",  # Необязательный параметр, отправляем пустым
        "client_secret": "",  # Необязательный параметр, отправляем пустым
    }

    # Авторизация пользователя
    response = await client.post(
        f"{version_prefix}/auth/login",
        data=login_data,  # Используем `data` для передачи данных в формате x-www-form-urlencoded
    )
    assert response.status_code == 204  # Ожидаем успешную авторизацию

    # Отправляем запрос на подписку
    response = await client.post(f"{version_prefix}/users/{follow_user_id}/follow")

    # Проверяем статус код и сообщение об ошибке (если есть)
    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()["detail"] == expected_detail

# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "user_id, expected_status, expected_detail",
#     [
#         # Успешная отписка от пользователя с ID 2
#         (2, 200, None),
#         # Повторная отписка от пользователя с ID 2 (должна вернуть ошибку)
#         (2, 400, "Вы не подписаны на этого пользователя"),
#         # Попытка отписаться от самого себя (должна вернуть ошибку)
#         (1, 400, "Нельзя отписаться от самого себя"),
#         # Попытка отписаться от несуществующего пользователя (должна вернуть ошибку)
#         (999, 404, "Пользователь для отписки не найден"),
#     ],
# )
# async def test_unfollowing(client: AsyncClient, user_id, expected_status, expected_detail):
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
#     # Авторизация пользователя
#     response = await client.post(
#         f"{version_prefix}/auth/login",
#         data=login_data,  # Используем `data` для передачи данных в формате x-www-form-urlencoded
#     )
#     assert response.status_code == 200  # Ожидаем успешную авторизацию
#
#     # Отправляем запрос на отписку
#     response = await client.delete(f"{version_prefix}/users/{user_id}/unfollow")
#
#     # Проверяем статус код и сообщение об ошибке (если есть)
#     assert response.status_code == expected_status
#     if expected_detail:
#         assert response.json()["detail"] == expected_detail
