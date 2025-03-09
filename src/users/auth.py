from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.config import settings
from src.database import async_session
from src.users.exception import credentials_exception
from src.users.models import User
from src.users.pwd_utils import verify_password
from src.users.schemas import TokenData
from src.users.service import UserService

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
    user: User | None = await UserService.get_one_or_none(session=session, username=username)
    if not user:
        raise credentials_exception
    if not verify_password(password, user.hashed_password):
        raise credentials_exception
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_by_username(username: str) -> User | None:
    async with async_session() as session:
        user: User | None = await UserService.get_one_or_none(session=session, username=username)
        if not user:
            raise credentials_exception
        return user


def get_access_token(request: Request):
    """This function is used to get the access token for cookie transport"""
    access_token = request.cookies.get("access_token")
    if not access_token:
        # raise credentials_exception
        return None
    return access_token


# async def get_current_user(
#     token: (
#         Annotated[str, Depends(oauth2_scheme)]
#         if settings.JWT_TRANSPORT == "BEARER"
#         else Annotated[str, Depends(get_access_token)]
#     ),
# ) -> User | None:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str | None = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user: User | None = await get_user_by_username(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme if settings.JWT_TRANSPORT == "BEARER" else get_access_token),
) -> Optional[User]:
    if not token:
        return None  # Если токен отсутствует, возвращаем None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            return None  # Если username отсутствует, возвращаем None
        token_data = TokenData(username=username)
    except InvalidTokenError:
        return None  # Если токен невалиден, возвращаем None

    user: User | None = await get_user_by_username(username=token_data.username)
    return user  # Возвращаем пользователя или None, если пользователь не найден


UserDep = Annotated[User, Depends(get_current_user)]
