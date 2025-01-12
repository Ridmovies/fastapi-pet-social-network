from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, Request
import jwt
from jwt import InvalidTokenError

from src.auth_app.models import User
from src.auth_app.service import AuthService
from src.config import settings
from src.exceptions import (
    NotAuthUserException,
    TokenExpireException,
    TokenInvalidException,
)


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise NotAuthUserException
    return access_token


async def get_current_user_id(access_token: str = Depends(get_access_token)) -> int:
    """Позволяет получить текущего пользователя."""
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
    except InvalidTokenError:
        raise TokenInvalidException
    user_id: int = int(payload.get("subject"))
    expire = payload.get("exp")
    if expire < datetime.now(timezone.utc).timestamp():
        raise TokenExpireException
    return user_id


async def get_current_user(
    access_token: str = Depends(get_access_token),
) -> User | None:
    """Позволяет получить текущего пользователя."""
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
    except InvalidTokenError:
        raise TokenInvalidException
    user_id: int = int(payload.get("subject"))
    expire = payload.get("exp")
    if expire < datetime.now(timezone.utc).timestamp():
        raise TokenExpireException

    user: User | None = await AuthService.get_one_by_id(user_id)
    return user


UserDep = Annotated[User, Depends(get_current_user)]


# async def get_admin_user(admin: UserDep):
#     """Проверяет юзера на администратора"""
#     if not admin.is_admin:
#         raise NotAuthUserException
#     return admin
