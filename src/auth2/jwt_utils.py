# from datetime import datetime, timedelta, timezone
# from typing import Annotated, Optional
#
# import jwt
# from fastapi import Depends, Request, WebSocketException
# from fastapi.security import OAuth2PasswordBearer
# from jwt import InvalidTokenError
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status
# from starlette.websockets import WebSocket
#
# from src.auth2.exception import credentials_exception
# from src.auth2.pwd_utils import verify_password
# from src.auth2.schemas import TokenData
# from src.config import settings
# from src.database import async_session
# from src.users.models import User
# from src.users.service import UserService
#
# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
#
#
# async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
#     user: User | None = await UserService.get_one_or_none(session=session, username=username)
#     if not user:
#         raise credentials_exception
#     if not verify_password(password, user.hashed_password):
#         raise credentials_exception
#     return user
#
#
# async def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_user_by_username(username: str) -> User | None:
#     async with async_session() as session:
#         user: User | None = await UserService.get_one_or_none(session=session, username=username)
#         if not user:
#             raise credentials_exception
#         return user
#
#
# def get_access_token(request: Request):
#     """This function is used to get the access token for cookie transport"""
#     access_token = request.cookies.get("pet_app_access_token")
#     if not access_token:
#         raise credentials_exception
#     return access_token
#
#
# async def get_optional_token(request: Request):
#     """This function is used to get the access token for cookie transport"""
#     access_token = request.cookies.get("pet_app_access_token")
#     return access_token
#
#
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
#
#
# async def get_current_user_or_guest(
#     token: Annotated[str, Depends(get_optional_token)]
# ) -> Optional[User]:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str | None = payload.get("sub")
#         if username is None:
#             return None  # Возвращаем None вместо выбрасывания исключения
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         return None  # Возвращаем None, если токен невалидный
#
#     user: User | None = await get_user_by_username(username=token_data.username)
#     return user  # Возвращаем пользователя или None, если пользователь не найден
#
#
# async def get_ws_user(
#         websocket: WebSocket,
#         session: AsyncSession = Depends(async_session),
# ) -> User:
#     # Получаем токен из query параметров
#     token = websocket.query_params.get("token")
#     if not token:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if not username:
#             await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#             raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#
#         user = await UserService.get_one_or_none(session=session, username=username)
#         if not user:
#             await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#             raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#
#         return user
#     except JWTError:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#
# UserOrGuestDep = Annotated[Optional[User], Depends(get_current_user_or_guest)]
# UserDep = Annotated[User, Depends(get_current_user)]
# WsUserDep = Annotated[User, Depends(get_ws_user)]