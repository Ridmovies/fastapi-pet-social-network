from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.database import SessionDep
from src.users.auth import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
)
from src.users.models import User
from src.users.schemas import Token, UserInSchema, UserOutSchema
from src.users.service import UserService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("")
async def get_all_users(session: SessionDep):
    return await UserService.get_all(session)


@user_router.post("")
async def create_user(user_data: UserInSchema, session: SessionDep):
    return await UserService.create_user(user_data, session)


@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.get("/me/", response_model=UserOutSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@user_router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]