from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from src.config import settings
from src.database import SessionDep
from src.users.auth import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
)
from src.users.exception import credentials_exception
from src.users.models import User
from src.users.schemas import UserInSchema, UserOutSchema, TokenSchema
from src.users.service import UserService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("")
async def get_all_users(session: SessionDep):
    return await UserService.get_all(session)


@user_router.get("/{user_id}", response_model=UserOutSchema)
async def get_user_by_id(session: SessionDep, user_id: int):
    return await UserService.get_one_by_id(session=session, model_id=user_id)



@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserInSchema, session: SessionDep):
    return await UserService.create_user(user_data, session)


@user_router.post("/token")
async def login_for_access_token(
    response: Response,
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchema:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    if settings.JWT_TRANSPORT == "COOKIE":
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
        )
        return TokenSchema(access_token=access_token, token_type="cookie")
    return TokenSchema(access_token=access_token, token_type="bearer")


@user_router.post("/logout")
async def logout(response: Response, request: Request):
    if settings.JWT_TRANSPORT == "COOKIE":
        if request.cookies.get("access_token"):
            response.delete_cookie(key="access_token", httponly=True)
        return {"message": "Cookie deleted"}


@user_router.get("/me", response_model=UserOutSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
