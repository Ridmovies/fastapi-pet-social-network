from fastapi import HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from pydantic import BaseModel

from src.config import settings

router = APIRouter(tags=["google_auth"])

# @router.get("/auth/google/callback2")
# async def auth_google_callback2(code: str):
#     print(f"1111111111111111111111111111111111111111111111111111111111111111")
#     return RedirectResponse("/")

# # Конфигурация Google OAuth
# GOOGLE_CLIENT_ID = settings.GOOGLE_OAUTH_CLIENT_ID
# GOOGLE_CLIENT_SECRET = settings.GOOGLE_OAUTH_CLIENT_SECRET
# REDIRECT_URI = "https://127.0.0.1:8000/api/v1/auth/google/callback"




# class GoogleToken(BaseModel):
#     id_token: str


# @router.get("/login/google")
# async def login_google():
#     # Перенаправляем пользователя на страницу авторизации Google
#     from google_auth_oauthlib.flow import Flow
#     flow = Flow.from_client_config(
#         client_config={
#             "web": {
#                 "client_id": GOOGLE_CLIENT_ID,
#                 "client_secret": GOOGLE_CLIENT_SECRET,
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://accounts.google.com/o/oauth2/token",
#                 "redirect_uris": [REDIRECT_URI]
#             }
#         },
#         scopes=["openid", "https://www.googleapis.com/auth/userinfo.email",
#                 "https://www.googleapis.com/auth/userinfo.profile"]
#     )
#     authorization_url, state = flow.authorization_url(
#         access_type="offline",
#         include_granted_scopes="true"
#     )
#     print("authorization_url:", authorization_url)
#     return RedirectResponse(authorization_url)


# @router.get("/auth/google/callback")
# async def auth_google_callback(code: str):
#     # Обмениваем код на токен
#     from google_auth_oauthlib.flow import Flow
#     flow = Flow.from_client_config(
#         client_config={
#             "web": {
#                 "client_id": GOOGLE_CLIENT_ID,
#                 "client_secret": GOOGLE_CLIENT_SECRET,
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://accounts.google.com/o/oauth2/token",
#                 "redirect_uris": [REDIRECT_URI]
#             }
#         },
#         scopes=["openid", "https://www.googleapis.com/auth/userinfo.email",
#                 "https://www.googleapis.com/auth/userinfo.profile"]
#     )
#     flow.redirect_uri = REDIRECT_URI
#     flow.fetch_token(code=code)
#
#     # Получаем информацию о пользователе
#     credentials = flow.credentials
#     id_info = id_token.verify_oauth2_token(
#         credentials.id_token,
#         requests.Request(),
#         GOOGLE_CLIENT_ID
#     )
#
#     # Здесь вы можете создать/найти пользователя в своей БД
#     # и создать сессию/JWT токен для своего приложения
#
#     print("Google user info:", id_info)
#     return RedirectResponse("/")
#
#
# @router.post("/auth/google/token")
# async def auth_google_token(token: GoogleToken):
#     # Валидация токена (для мобильных приложений)
#     try:
#         id_info = id_token.verify_oauth2_token(
#             token.id_token,
#             requests.Request(),
#             GOOGLE_CLIENT_ID
#         )
#         return {"user_info": id_info}
#     except ValueError:
#         raise HTTPException(status_code=403, detail="Invalid token")
