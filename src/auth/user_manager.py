from typing import Optional

from fastapi import Depends, Request, Response

from fastapi_users import BaseUserManager, IntegerIDMixin
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2

from src.auth.utils import get_user_db
from src.config import settings
from src.database import async_session
from src.users.models import User, Profile


SECRET = settings.SECRET_KEY


google_oauth_client = GoogleOAuth2(
    client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
    # scopes=["openid", "email", "profile"],  # Только необходимые scope
)


vk_oauth_client = OAuth2(
    client_id=settings.VK_OAUTH_CLIENT_ID,
    client_secret=settings.VK_OAUTH_CLIENT_SECRET,
    authorize_endpoint="https://id.vk.com/authorize",
    access_token_endpoint="https://id.vk.com/oauth2/auth",  # <-- ВОТ ОН, ПРАВИЛЬНЫЙ ПАРАМЕТР!
    base_scopes=["email", "offline", "friends"],  # <-- scopes передаем сюда
    name="vk_id", # Уникальное имя для твоего провайдера
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        async with async_session() as session:
            # Создаем профиль для нового пользователя
            profile = Profile(user_id=user.id)
            print(f"Username {user.email}")
            user.username = user.email.split('@')[0]
            session.add(profile)
            await session.commit()

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        """
        Perform logic after user login.

        :param user: The user that is logging in
        :param request: Optional FastAPI request
        :param response: Optional response built by the transport.
        Defaults to None
        """
        print(f"User {user.id} has logged in.")
        return


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
