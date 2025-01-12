from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends

from src.auth_app.auth import authenticate_user, get_password_hash, create_access_token
from src.auth_app.dependencies import get_current_user, UserDep
from src.auth_app.models import User
from src.auth_app.schemas import UserInSchema, UserOutSchema
from src.auth_app.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-in")
async def sign_in(response: Response, user_data: UserInSchema):
    """ Login user """
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    access_token = create_access_token({"subject": user.id})
    # httponly=True important for safety!!!
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return access_token


@router.post("/sign-up")
async def sign_up(user_data: UserInSchema):
    """ Register user """
    hashed_password = await get_password_hash(user_data.password)
    return await AuthService.register(user_data.username, hashed_password)


@router.post("/sign-out")
async def sign_out(response: Response):
    """ Logout user """
    response.delete_cookie(key="access_token")
    return {"message": "sign-out"}


@router.get("/me", response_model=UserOutSchema)
async def get_me(current_user: UserDep):
    """ Get user info """
    return current_user

