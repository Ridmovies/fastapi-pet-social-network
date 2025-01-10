from fastapi import APIRouter

# from src.auth_app.auth import authenticate_user
from src.auth_app.schemas import UserInSchema, UserOutSchema
from src.auth_app.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


# @router.post("/sign-in", response_model=UserOutSchema)
# async def sign_in(user_data: UserInSchema):
#     user = await AuthService.get_one_or_none(username=user_data.username)
#     if user is None:
#         return {"message": "user not found"}
#     return await authenticate_user(user_data)


@router.post("/sign-up")
async def sign_up(user_data: UserInSchema):
    return await AuthService.register(user_data)

@router.post("/sign-out")
async def sign_out():
    return {"message": "sign-out"}
