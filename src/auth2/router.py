from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.auth2.exception import credentials_exception
from src.auth2.jwt_utils import authenticate_user, create_access_token, get_current_user, UserDep
from src.auth2.schemas import TokenSchema
from src.config import settings
from src.database import SessionDep
from src.users.models import User
from src.users.schemas import UserRead

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
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
            key="pet_app_access_token",
            value=access_token,
            httponly=True,
        )
        return TokenSchema(access_token=access_token, token_type="cookie")
    return TokenSchema(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout(response: Response, request: Request):
    if settings.JWT_TRANSPORT == "COOKIE":
        if request.cookies.get("pet_app_access_token"):
            response.delete_cookie(key="pet_app_access_token", httponly=True)
        return {"message": "Cookie deleted"}
