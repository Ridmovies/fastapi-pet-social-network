import base64
import hashlib
from datetime import datetime

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
SECRET_KEY = settings.SECRET_KEY

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
    print(f"[{datetime.now()}] Перенаправляем на VK OAuth URL: {auth_url}")
    return RedirectResponse(url=auth_url)


# Эндпоинт для обработки колбэка от VK (после авторизации пользователя)
@router.get("/auth/vk/callback")
async def vk_callback(
    code: str,
    request: Request,
    state: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
    device_id: str | None = None,  # <--- ДОБАВЬ ЭТО!
):
    callback_start_time = datetime.now()
    print(f"[{callback_start_time}] --- Получен GET-callback от VK.com ---")
    print(f"[{callback_start_time}] Code received: {code}")

    # 1. Проверка state (CSRF защита)
    print(f"[{datetime.now()}] DEBUG: vk_callback - State from VK URL: {state}")
    session_state = request.session.pop("vk_oauth_state", None)
    print(f"[{datetime.now()}] DEBUG: vk_callback - State from session.pop(): {session_state}")

    if state is None or state != session_state:
        error_msg = "Invalid state parameter or CSRF attack detected. State from VK: {}, State from session: {}".format(state, session_state)
        print(f"[{datetime.now()}] ОШИБКА: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)

    if error:
        error_msg = f"VK Error: {error}, Description: {error_description}"
        print(f"[{datetime.now()}] ОШИБКА: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)

    # Получаем code_verifier из сессии
    code_verifier = request.session.pop("vk_code_verifier", None)
    print(f"[{datetime.now()}] DEBUG: vk_callback - Code verifier from session.pop(): {code_verifier}")
    if not code_verifier:
        error_msg = "Code verifier not found in session."
        print(f"[{datetime.now()}] ОШИБКА: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)

    # Шаг 2: Обмен code на access_token
    token_params = {
        "client_id": VK_CLIENT_ID,
        # Маскируем client_secret для логирования, чтобы не светить его полностью
        "client_secret": VK_CLIENT_SECRET,
        # <--- ВАЖНО: Документация не показывает client_secret в запросе, но он ДОЛЖЕН быть!
        "redirect_uri": VK_REDIRECT_URI,
        "code": code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        # Также, документация VK ID (для PKCE) часто требует device_id и state в этом запросе
        # Даже если state проверяется ранее, они могут требовать его тут для валидации.
        # Если у тебя есть device_id из колбэка VK, его тоже нужно передать!
        "state": state,  # Добавь state, который ты получил в колбэке
        "device_id": request.query_params.get("device_id")  # Получаем device_id из параметров URL колбэка
    }
    token_url = "https://id.vk.com/oauth2/auth"

    print(f"[{datetime.now()}] Обмениваем код на токен...")
    print(f"[{datetime.now()}] DEBUG: Parameters for token exchange (sensitive parts masked):")
    # Более безопасное логирование, скрывающее полный секрет
    log_token_params = token_params.copy()
    if 'client_secret' in log_token_params:
        log_token_params['client_secret'] = log_token_params['client_secret'][:4] + '...' + log_token_params['client_secret'][-4:]
    print(f"[{datetime.now()}] {log_token_params}")
    print(f"[{datetime.now()}] DEBUG: Posting to token URL: {token_url}")

    token_exchange_start_time = datetime.now()
    async with httpx.AsyncClient() as client:
        try:
            # token_response = await client.post(token_url, params=token_params)
            token_response = await client.post(token_url, data=token_params)  # <-- ПРАВИЛЬНО (data - это body)
            token_exchange_end_time = datetime.now()
            print(f"[{token_exchange_end_time}] DEBUG: Time taken for token exchange POST: {token_exchange_end_time - token_exchange_start_time}")

            token_response.raise_for_status() # Выбросит исключение для 4xx/5xx ошибок
            token_data = token_response.json()
            print(f"[{datetime.now()}] DEBUG: Full VK token response status: {token_response.status_code}")
            print(f"[{datetime.now()}] DEBUG: Full VK token response headers: {token_response.headers}")
            print(f"[{datetime.now()}] DEBUG: Full VK token response body: {token_response.text}")
            print(f"[{datetime.now()}] Ответ от VK API (access_token): {token_data}")
        except httpx.HTTPStatusError as e:
            error_details = f"HTTPStatusError: {e.response.status_code} - {e.response.text}"
            print(f"[{datetime.now()}] ОШИБКА ПРИ ОБМЕНЕ ТОКЕНА: {error_details}")
            print(f"[{datetime.now()}] RESPONSE BODY ON ERROR: {e.response.text}") # Логируем тело ответа при ошибке
            raise HTTPException(status_code=500, detail=f"Failed to exchange code for token: {e.response.text}")
        except Exception as e:
            error_details = f"Unknown error during token exchange: {e}"
            print(f"[{datetime.now()}] ОШИБКА: {error_details}")
            raise HTTPException(status_code=500, detail=error_details)

    # Проверяем наличие access_token и user_id
    if "access_token" not in token_data or "user_id" not in token_data:
        print("Отсутствует access_token или user_id в ответе VK")
        raise HTTPException(status_code=500, detail="Access token or user ID not found in VK response.")

    access_token = token_data["access_token"]
    user_id = token_data["user_id"]
    email = token_data.get("email")
    expires_in = token_data.get("expires_in")
    refresh_token = token_data.get("refresh_token")

    print(f"[{datetime.now()}] Получен access_token для user_id: {user_id}")
    if email:
        print(f"[{datetime.now()}] Email: {email}")

    # Шаг 3: Получение детальной информации о пользователе (используем access_token)
    vk_api_url = f"https://api.vk.com/method/users.get"
    user_params = {
        'user_ids': user_id,
        'fields': 'photo_200,first_name,last_name,screen_name,email',
        'access_token': access_token,
        'v': '5.131'
    }

    print(f"[{datetime.now()}] Запрашиваем данные пользователя {user_id}...")
    user_data_request_start_time = datetime.now()
    async with httpx.AsyncClient() as client:
        try:
            user_response = await client.get(vk_api_url, params=user_params)
            user_data_request_end_time = datetime.now()
            print(f"[{user_data_request_end_time}] DEBUG: Time taken for users.get: {user_data_request_end_time - user_data_request_start_time}")

            user_response.raise_for_status()
            vk_user_data = user_response.json()
            print(f"[{datetime.now()}] Ответ от VK API users.get: {vk_user_data}")
        except httpx.HTTPStatusError as e:
            error_details = f"HTTPStatusError: {e.response.status_code} - {e.response.text}"
            print(f"[{datetime.now()}] ОШИБКА ПРИ ЗАПРОСЕ users.get: {error_details}")
            raise HTTPException(status_code=500, detail=f"Failed to get user info from VK: {e.response.text}")
        except Exception as e:
            error_details = f"Unknown error while fetching user info: {e}"
            print(f"[{datetime.now()}] ОШИБКА: {error_details}")
            raise HTTPException(status_code=500, detail=error_details)

    if 'response' not in vk_user_data or not vk_user_data['response']:
        error_msg = "Не удалось получить данные пользователя VK (пустой ответ)."
        print(f"[{datetime.now()}] ОШИБКА: {error_msg} Raw response: {vk_user_data}")
        raise HTTPException(status_code=400, detail=error_msg)

    user_info = vk_user_data['response'][0]
    user_info['access_token'] = access_token
    user_info['user_id'] = user_id
    user_info['refresh_token'] = refresh_token
    user_info['email'] = email if email else user_info.get('email')

    request.session['user'] = user_info
    print(f"[{datetime.now()}] Пользователь {user_info.get('first_name')} {user_info.get('last_name')} ({user_info['user_id']}) успешно авторизован и добавлен в сессию.")

    return RedirectResponse(url="/")