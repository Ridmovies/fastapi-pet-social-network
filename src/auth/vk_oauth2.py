import base64
import hashlib

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from urllib.parse import urlencode, urlunparse
import httpx
import secrets

from src.config import settings

router = APIRouter(tags=[" VK OAuth2"])
templates = Jinja2Templates(directory="templates") # Убедись, что папка 'templates' существует

# # *** Важные настройки (убедись, что они в твоем .env или в переменных окружения) ***
# VK_CLIENT_ID = os.environ.get("VK_CLIENT_ID", "ТВОЙ_VK_CLIENT_ID")
# VK_CLIENT_SECRET = os.environ.get("VK_CLIENT_SECRET", "ТВОЙ_VK_CLIENT_SECRET")
# # Этот URL должен быть тем же, что и в настройках VK: Доверенный Redirect URL
# VK_REDIRECT_URI = "https://localhost/api/v1/auth/vk/callback"
# # SECRET_KEY для SessionMiddleware (убедись, что он задан и длинный)
# SECRET_KEY = os.environ.get("SECRET_KEY", "ТВОЙ_ОЧЕНЬ_ДЛИННЫЙ_СЕКРЕТНЫЙ_КЛЮЧ_ДЛЯ_СЕССИЙ_МИНИМУМ_32_СИМВОЛА")

VK_CLIENT_ID = settings.VK_OAUTH_CLIENT_ID
VK_CLIENT_SECRET = settings.VK_OAUTH_CLIENT_SECRET
VK_REDIRECT_URI = settings.VK_REDIRECT_URI
SECRET_KEY = "hg4356ghj56g4hj67gj5h6g786jh7g8j6h78ghj6g8jh67jh354k6jh4jk7h"

# Функция для генерации code_verifier (случайной строки)
def generate_code_verifier():
    return secrets.token_urlsafe(96)

# Функция для генерации code_challenge (SHA256 Base64url от code_verifier)
def generate_code_challenge(code_verifier):
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(s256).decode('utf-8').rstrip('=')

# Эндпоинт для начала авторизации (кнопка "Войти через VK ID")
@router.get("/auth/vk/login")
async def vk_login(request: Request):
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    state = secrets.token_urlsafe(32)

    request.session["vk_code_verifier"] = code_verifier
    request.session["vk_oauth_state"] = state

    params = {
        "client_id": VK_CLIENT_ID,
        "redirect_uri": VK_REDIRECT_URI,
        "scope": "email",
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state
    }
    auth_url = urlunparse(("https", "id.vk.com", "/authorize", "", urlencode(params), ""))
    print(f"Перенаправляем на VK OAuth URL: {auth_url}")
    return RedirectResponse(url=auth_url)


# Эндпоинт для обработки колбэка от VK (после авторизации пользователя)
@router.get("/auth/vk/callback")
async def vk_callback(
    code: str, # VK отправит нам code после успешной авторизации
    request: Request,
    state: str | None = None, # VK вернет state, который мы должны проверить
    error: str | None = None, # Если VK вернул ошибку
    error_description: str | None = None, # Описание ошибки
):
    print("--- Получен GET-callback от VK.com ---")
    print(f"Code: {code}")

    # 1. Проверка state (CSRF защита)
    if state is None or state != request.session.pop("vk_oauth_state", None):
        print("Ошибка: Несоответствие state или state отсутствует в сессии. Возможная CSRF атака.")
        raise HTTPException(status_code=400, detail="Invalid state parameter or CSRF attack detected.")

    if error:
        print(f"Error: {error}, Description: {error_description}")
        raise HTTPException(status_code=400, detail=f"VK Error: {error_description}")

    # Получаем code_verifier из сессии
    code_verifier = request.session.pop("vk_code_verifier", None)
    if not code_verifier:
        print("Ошибка: code_verifier отсутствует в сессии.")
        raise HTTPException(status_code=400, detail="Code verifier not found in session.")

    # Шаг 2: Обмен code на access_token
    token_params = {
        "client_id": VK_CLIENT_ID,
        "client_secret": VK_CLIENT_SECRET,
        "redirect_uri": VK_REDIRECT_URI,
        "code": code,
        "code_verifier": code_verifier, # <--- PKCE параметр
        "grant_type": "authorization_code",
    }
    token_url = "https://oauth.vk.com/access_token"

    print("Обмениваем код на токен...")
    async with httpx.AsyncClient() as client:
        try:
            token_response = await client.post(token_url, params=token_params)
            token_response.raise_for_status() # Выбросит исключение для 4xx/5xx ошибок
            token_data = token_response.json()
            print(f"Ответ от VK API (access_token): {token_data}")
        except httpx.HTTPStatusError as e:
            print(f"Ошибка при обмене токена: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=500, detail=f"Failed to exchange code for token: {e.response.text}")
        except Exception as e:
            print(f"Неизвестная ошибка при обмене токена: {e}")
            raise HTTPException(status_code=500, detail="An error occurred during token exchange.")

    # Проверяем наличие access_token и user_id
    if "access_token" not in token_data or "user_id" not in token_data:
        print("Отсутствует access_token или user_id в ответе VK")
        raise HTTPException(status_code=500, detail="Access token or user ID not found in VK response.")

    access_token = token_data["access_token"]
    user_id = token_data["user_id"]
    email = token_data.get("email") # Email может быть в ответе access_token, если запрошен scope
    expires_in = token_data.get("expires_in")
    refresh_token = token_data.get("refresh_token") # Если запрошен scope offline

    print(f"Получен access_token для user_id: {user_id}")
    if email:
        print(f"Email: {email}")

    # Шаг 3: Получение детальной информации о пользователе (используем access_token)
    vk_api_url = f"https://api.vk.com/method/users.get"
    user_params = {
        'user_ids': user_id,
        'fields': 'photo_200,first_name,last_name,screen_name,email', # Снова запрашиваем email
        'access_token': access_token,
        'v': '5.131'
    }

    print(f"Запрашиваем данные пользователя {user_id}...")
    async with httpx.AsyncClient() as client:
        try:
            user_response = await client.get(vk_api_url, params=user_params)
            user_response.raise_for_status()
            vk_user_data = user_response.json()
            print(f"Ответ от VK API users.get: {vk_user_data}")
        except httpx.HTTPStatusError as e:
            print(f"Ошибка при запросе users.get: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=500, detail=f"Failed to get user info from VK: {e.response.text}")
        except Exception as e:
            print(f"Неизвестная ошибка при запросе users.get: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while fetching user info.")

    if 'response' not in vk_user_data or not vk_user_data['response']:
        print("Не удалось получить данные пользователя VK (пустой ответ).")
        raise HTTPException(status_code=400, detail="Could not retrieve VK user data.")

    user_info = vk_user_data['response'][0]
    user_info['access_token'] = access_token
    user_info['user_id'] = user_id # Сохраняем VK ID, который пришел с токеном
    user_info['refresh_token'] = refresh_token # Сохраняем refresh_token, если он есть
    user_info['email'] = email if email else user_info.get('email') # Приоритет email из токена, иначе из users.get

    # Шаг 3: Сохранение информации о пользователе в сессии FastAPI
    request.session['user'] = user_info
    print(f"Пользователь {user_info.get('first_name')} {user_info.get('last_name')} ({user_info['user_id']}) успешно авторизован и добавлен в сессию.")

    return RedirectResponse(url="/") # Перенаправляем на главную страницу после авторизации
