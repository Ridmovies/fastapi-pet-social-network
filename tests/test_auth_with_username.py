import pytest
from httpx import AsyncClient

version_prefix = "/api/v1"


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    json_data = {
        "username": "user",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }
    response = await client.post(f"{version_prefix}/users", json=json_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_jwt_login(client: AsyncClient):
    # Данные для авторизации
    login_data = {
        "grant_type": "password",  # Обязательный параметр, должен быть "password"
        "username": "user",  # Обязательный параметр
        "password": "string",  # Обязательный параметр
        "scope": "",  # Необязательный параметр, отправляем пустым
        "client_id": "",  # Необязательный параметр, отправляем пустым
        "client_secret": "",  # Необязательный параметр, отправляем пустым
    }

    # Отправляем POST-запрос на эндпоинт /auth/jwt/login
    response = await client.post(f"{version_prefix}/auth/login",
        data=login_data,  # Используем `data` для передачи данных в формате x-www-form-urlencoded
    )
    # Проверяем статус код ответа
    assert (
        response.status_code == 200
    )  # Ожидаем статус код 204, если авторизация успешна

    # Проверяем, что в ответе есть cookie
    cookies = response.cookies
    # Проверяем наличие конкретной cookie
    if "access_token" not in cookies:
        print("Cookie 'access_token' not found in response.")
    else:
        print(f"access_token: {cookies['access_token']}")

    # Шаг 2: Получение данных профиля с использованием cookie
    headers = {
        "Cookie": f"access_token={cookies['access_token']}"
    }  # Добавление куки в заголовок
    response = await client.get(f"{version_prefix}/auth/me", headers=headers)

    # Отладочная информация
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Body: {response.text}")

    assert response.status_code == 200
    assert response.json()["username"] == "user"
    assert response.json()["id"] == 1


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
        # Успешная регистрация
        (
            {**DEFAULT_USER_DATA, "username": "user1", "password": "string"},
            201,
        ),
        # Пользователь с таким email уже существует
        (
            {**DEFAULT_USER_DATA, "username": "user", "password": "string"},
            409,
        ),
    ],
)
async def test_register_user2(client: AsyncClient, user_data, expected_status_code):
    response = await client.post(f"{version_prefix}/users", json=user_data)
    assert response.status_code == expected_status_code
#