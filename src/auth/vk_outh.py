import httpx
from fastapi import Request, APIRouter, HTTPException
from pydantic import BaseModel

from src.config import settings

router = APIRouter(tags=["vk_auth"])

# Данные из VK
VK_CLIENT_ID = settings.VK_OAUTH_CLIENT_ID
VK_CLIENT_SECRET = settings.VK_OAUTH_CLIENT_SECRET
VK_REDIRECT_URI = settings.VK_REDIRECT_URI




class VkSdkLoginPayload(BaseModel):
    access_token: str
    user_id: int
    refresh_token: str | None = None
    email: str | None = None # <-- Добавили email

@router.post("/auth/vk/sdk-login") # <-- Вот этот эндпоинт!
async def vk_sdk_login_backend(payload: VkSdkLoginPayload, request: Request):
    print(f"[{request.client.host}] Получен POST-запрос от клиента с данными VK ID SDK:")
    print(f"VK User ID: {payload.user_id}")
    print(f"Access Token: {payload.access_token[:15]}...") # Выводим только начало
    print(f"Refresh Token: {payload.refresh_token[:15]}..." if payload.refresh_token else "отсутствует")

    try:
        # Шаг 1: Получение детальной информации о пользователе с VK API
        # Это подтверждает, что access_token действителен и позволяет получить доп. инфо
        vk_api_url = f"https://api.vk.com/method/users.get"
        user_params = {
            'user_ids': payload.user_id,
            'fields': 'photo_200,first_name,last_name,screen_name,email',  # <-- Убедись, что 'email' здесь
            'access_token': payload.access_token,
            'v': '5.131'
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(vk_api_url, params=user_params)
            response.raise_for_status() # Выбросит исключение для 4xx/5xx ответов
            vk_user_data = response.json()

            # *********** Добавь эту строку, чтобы увидеть весь ответ от VK ***********
            print("Полный ответ от VK API users.get:", vk_user_data)
            # **************************************************************************

            if 'response' not in vk_user_data or not vk_user_data['response']:
                raise HTTPException(status_code=400, detail="Не удалось получить данные пользователя VK.")

            user_info = vk_user_data['response'][0]
            user_info['access_token'] = payload.access_token
            user_info['refresh_token'] = payload.refresh_token
            user_info['vk_id'] = payload.user_id # Добавляем VK ID для удобства
            user_info['email'] = user_info.get('email')  # Если email не пришел из users.get, то будет None

            # Шаг 2: Сохранение информации о пользователе в сессии FastAPI
            request.session['user'] = user_info
            print(f"Пользователь {user_info.get('first_name')} {user_info.get('last_name')} ({user_info['vk_id']}) успешно авторизован и добавлен в сессию.")

            # Шаг 3: Возвращаем успешный ответ клиенту
            return {"message": "Авторизация через VK ID SDK успешна!", "user_id": user_info['vk_id']}

    except httpx.HTTPStatusError as e:
        print(f"HTTP ошибка VK API: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к VK API: {e.response.text}")
    except Exception as e:
        print(f"Неизвестная ошибка VK SDK login backend: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера при авторизации: {e}")
