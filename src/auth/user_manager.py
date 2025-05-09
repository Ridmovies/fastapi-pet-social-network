from typing import Optional
import logging

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.exceptions import GetProfileError

from src.auth.utils import get_user_db
from src.config import settings
from src.database import async_session
from src.users.models import User, Profile


SECRET = settings.SECRET_KEY

# Настройка логирования (добавьте в начало файла, например, main.py)
logging.basicConfig(
    level=logging.DEBUG,  # Уровень DEBUG покажет все сообщения
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Пример логов в коде
logger = logging.getLogger("google_oauth")


class DebugGoogleOAuth2(GoogleOAuth2):
    async def get_profile(self, token: str):
        logger.debug(f"Запрос профиля Google с токеном: {token[:10]}...")  # Не логируем полный токен!
        try:
            # 1. Пробуем получить профиль через родительский метод
            response = await super().get_profile(token)
            logger.debug(f"Ответ Google: {response}")
            return response
        # 2. Если ошибка - логируем и пробрасываем её дальше
        except GetProfileError as e:
            logger.error(f"Ошибка Google OAuth: {e.response.status_code} - {e.response.text}")
            raise

# Then use this instead:
google_oauth_client = DebugGoogleOAuth2(
    client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
    # scopes=["openid", "email", "profile"],  # Только необходимые scope
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    # async def create(
    #     self,
    #     user_create: UserCreate,
    #     safe: bool = False,
    #     request: Optional[Request] = None,
    # ) -> models.UP:
    #     """
    #     Create a user in database.
    #
    #     Triggers the on_after_register handler on success.
    #
    #     :param user_create: The UserCreate model to create.
    #     :param safe: If True, sensitive values like is_superuser or is_verified
    #     will be ignored during the creation, defaults to False.
    #     :param request: Optional FastAPI request that
    #     triggered the operation, defaults to None.
    #     :raises UserAlreadyExists: A user already exists with the same e-mail.
    #     :return: A new user.
    #     """
    #     await self.validate_password(user_create.password, user_create)
    #
    #     existing_user = await self.user_db.get_by_email(user_create.email)
    #     if existing_user is not None:
    #         raise exceptions.UserAlreadyExists()
    #
    #     user_dict = (
    #         user_create.create_update_dict()
    #         if safe
    #         else user_create.create_update_dict_superuser()
    #     )
    #     password = user_dict.pop("password")
    #     user_dict["hashed_password"] = self.password_helper.hash(password)
    #
    #     created_user = await self.user_db.create(user_dict)
    #
    #     await self.on_after_register(created_user, request)
    #
    #     return created_user

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


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
