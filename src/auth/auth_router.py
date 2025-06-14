from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.auth.backend import auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.user_manager import get_user_manager, google_oauth_client, vk_oauth_client
from src.config import settings
from src.users.models import User

auth_router = APIRouter()
SECRET = settings.SECRET_KEY


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)


auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)



auth_router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        SECRET,
        # redirect_url="https://127.0.0.1:8000/api/v1/auth/google/callback",
        # можете автоматически привязать эту учетную запись OAuth к существующей учетной записи пользователя
        # associate_by_email=True, # is dangerous, please do not enable
        # установить is_verified в true для учетных записей OAuth
        # is_verified_by_default=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)


auth_router.include_router(
    fastapi_users.get_oauth_router(
        vk_oauth_client, # <--- Твой клиент VK ID
        auth_backend,
        SECRET,

    ),
    prefix="/auth/vk", # <--- Уникальный префикс для роутов VK (например, /auth/vk/authorize, /auth/vk/callback)
    tags=["auth"],
)

current_user = fastapi_users.current_user()
current_user_or_guest = fastapi_users.current_user(optional=True)
