from fastapi import APIRouter, HTTPException, status, Response

from src.auth_app.auth import authenticate_user, get_password_hash, create_access_token
from src.auth_app.schemas import UserInSchema, UserOutSchema
from src.auth_app.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-in")
async def sign_in(response: Response, user_data: UserInSchema):
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    access_token = create_access_token({"subject": user.id})
    # httponly=True important for safety!!!
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return access_token


@router.post("/sign-up")
async def sign_up(user_data: UserInSchema):
    hashed_password = await get_password_hash(user_data.password)
    return await AuthService.register(user_data.username, hashed_password)


@router.post("/sign-out")
async def sign_out():
    return {"message": "sign-out"}
