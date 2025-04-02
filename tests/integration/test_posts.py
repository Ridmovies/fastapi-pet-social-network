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
# async def test_jwt_login(client: AsyncClient):
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



# Параметры для создания постов
POST_CREATION_DATA = [
    ({"content": "Post 1", "community_id": 1}, 200),  # Успешное создание поста
    # ({"content": "", "community_id": 1}, 422),  # Пустой контент (должен вернуть ошибку)
    # ({"content": "Post 2", "community_id": 999}, 404),  # Несуществующее сообщество
]

# Параметры для удаления постов
POST_DELETION_DATA = [
    (1, 204),  # Успешное удаление поста
    (999, 404),  # Несуществующий пост
]


@pytest.mark.asyncio
@pytest.mark.parametrize("post_data, expected_status_code", POST_CREATION_DATA)
async def test_create_post(client: AsyncClient, post_data, expected_status_code):
    # Авторизация пользователя
    login_data = {
        "grant_type": "password",
        "username": "user1",
        "password": "string",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = await client.post(f"{version_prefix}/auth/login", data=login_data)
    assert response.status_code == 200

    # Создание сообщества
    response = await client.post(f"{version_prefix}/community",
                                 json={
                                     "name": "common",
                                     "description": "common description",
                                 })

    # Подготовка данных для запроса
    # files = {}
    # if image_file:
    #     # Создаем тестовый файл изображения
    #     with open(image_file, "wb") as f:
    #         f.write(b"fake image data")
    #
    #     files["image"] = (image_file, open(image_file, "rb"), "image/jpeg")

    # Преобразуем данные формы
    form_data = {}
    for key, value in post_data.items():
        form_data[key] = (None, str(value))

    # Создание поста
    response = await client.post(
        f"{version_prefix}/post",
        # files=files,
        data=form_data
    )
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize("post_id, expected_status_code", POST_DELETION_DATA)
async def test_delete_post(client: AsyncClient, post_id, expected_status_code):
    # Авторизация пользователя
    login_data = {
        "grant_type": "password",
        "username": "user1",
        "password": "string",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = await client.post(f"{version_prefix}/auth/login", data=login_data)
    assert response.status_code == 200

    # Удаление поста
    response = await client.delete(f"{version_prefix}/post/{post_id}")
    assert response.status_code == expected_status_code




# Параметры для создания комментариев
COMMENT_CREATION_DATA = [
    ({"content": "Comment 1", "post_id": 2,}, 201),  # Успешное создание комментария
    ({"content": "", "post_id": 2,}, 422),  # Пустой контент (должен вернуть ошибку)
]

# Параметры для удаления комментариев
COMMENT_DELETION_DATA = [
    (2, 204),  # Успешное удаление комментария
    (3, 204),  # Успешное удаление комментария
    (999, 404),  # Несуществующий комментарий
]


@pytest.mark.asyncio
@pytest.mark.parametrize("comment_data, expected_status_code", COMMENT_CREATION_DATA)
async def test_create_comment(client: AsyncClient, comment_data, expected_status_code):
    # Авторизация пользователя
    login_data = {
        "grant_type": "password",
        "username": "user1",
        "password": "string",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = await client.post(f"{version_prefix}/auth/login", data=login_data)
    assert response.status_code == 200

    # Создание поста (для тестирования комментариев)
    post_response = await client.post(f"{version_prefix}/post", data={"content": "Test Post", "community_id": 1})
    assert post_response.status_code == 200

    # Создание комментария
    response = await client.post(f"{version_prefix}/comments", json=comment_data)
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize("comment_id, expected_status_code", COMMENT_DELETION_DATA)
async def test_delete_comment(client: AsyncClient, comment_id, expected_status_code):
    # Авторизация пользователя
    login_data = {
        "grant_type": "password",
        "username": "user1",
        "password": "string",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = await client.post(f"{version_prefix}/auth/login", data=login_data)
    assert response.status_code == 200

    # Создание поста (для тестирования комментариев)
    post_response = await client.post(f"{version_prefix}/post", data={"content": "Test Post", "community_id": 1})
    assert post_response.status_code == 200
    post_id = post_response.json()["id"]

    # Создание комментария (для тестирования удаления)
    comment_response = await client.post(f"{version_prefix}/comments", json={"content": "Test Comment", "post_id": 2})
    assert comment_response.status_code == 201


    response = await client.delete(f"{version_prefix}/comments/{comment_id}")
    assert response.status_code == expected_status_code
