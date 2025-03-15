import pytest
from httpx import AsyncClient

auth_prefix = f"/api/v1/users"


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient):
    response = await client.get(url=f"{auth_prefix}")
    assert response.status_code == 200
    assert response.json() == []


# @pytest.mark.asyncio
# async def test_create_user(client: AsyncClient):
#     # Подготовка данных для запроса
#     user_data = {
#         "username": "testuser",
#         "password": "testpassword"
#     }
#
#     # Выполнение POST-запроса к роуту
#     response = await client.post(url=f"{auth_prefix}", json=user_data)
#
#     # Проверка статуса ответа
#     assert response.status_code == 200
#
#     # Проверка тела ответа
#     response_data = response.json()
#     assert response_data["username"] == "testuser"
#     assert "id" in response_data  # Проверяем, что ID пользователя был создан
#


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("test_user", "example", 201),
        ("test_user", "example", 400),
        ("test_user_2", "example", 201),
        ("12", "123456", 422),  # Короткий логин
        ("abc", "123456", 201),
        ("1abc", "123456", 422),  # Начинается с цифры
        ("test_user_3", "12345", 422),  # короткий пароль
        ("Capitalize", "12345", 422),  # Заглавная буква
        ("gh$@#$%@", "123456", 422),  # спец символы
    ],
)
async def test_create_user(
    username: str, password: str, status_code: int, client: AsyncClient
) -> None:
    response = await client.post(
        url=f"{auth_prefix}", json={"username": username, "password": password}
    )
    assert response.status_code == status_code
