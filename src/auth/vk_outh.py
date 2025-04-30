from fastapi import Request, APIRouter
from pydantic import BaseModel

from src.config import settings

router = APIRouter(tags=["vk_auth"])

# # Данные из VK
# VK_CLIENT_ID = settings.VK_OAUTH_CLIENT_ID
# VK_CLIENT_SECRET = settings.VK_OAUTH_CLIENT_SECRET
# VK_REDIRECT_URI = settings.VK_REDIRECT_URI


class VKAuthData(BaseModel):
    token: str
    email: str | None = None
    vk_user_id: int


@router.post("/auth/vk/callback")
async def auth_vk_callback(request: Request):
    # Получаем raw body запроса
    raw_body = await request.body()
    print("Raw request body:", raw_body.decode())

    try:
        # Парсим JSON данные
        data = await request.json()
        print("Получены данные от VK:", data)

        # Проверяем обязательные поля
        if not data.get('token'):
            print("Ошибка: отсутствует token")
            return {"status": "error", "message": "Token is required"}

        if not data.get('vk_user_id'):
            print("Ошибка: отсутствует vk_user_id")
            return {"status": "error", "message": "User ID is required"}

        # Выводим детальную информацию
        print("\nДетализация данных:")
        print(f"VK User ID: {data.get('vk_user_id')}")
        print(f"Access Token: {data.get('token')[:15]}...")  # Выводим только начало токена
        print(f"Email: {data.get('email', 'не предоставлен')}")
        print(f"Полные данные: {data}")

        # Здесь можно добавить обработку данных (сохранение в БД и т.д.)

        return {
            "status": "success",
            "message": "Авторизация прошла успешно",
            "vk_user_id": data.get('vk_user_id')
        }

    except Exception as e:
        print(f"Ошибка при обработке запроса: {str(e)}")
        return {"status": "error", "message": "Invalid request data"}

