from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt

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
    except JWTError:
        raise TokenInvalidException
    user_id: int = int(payload.get("sub"))
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
    except JWTError:
        raise TokenInvalidException
    user_id: int = int(payload.get("subject"))
    expire = payload.get("exp")
    if expire < datetime.now(timezone.utc).timestamp():
        raise TokenExpireException

    user: User | None = await AuthService.get_one_by_id(user_id)
    return user
