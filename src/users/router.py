from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from starlette import status

from src.auth2.jwt_utils import UserDep
from src.database import SessionDep
from src.users.exception import user_already_exists
from src.users.models import User
from src.users.schemas import UserRead, UserCreate
from src.users.service import UserService


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("", response_model=list[UserRead])
async def get_all_users(session: SessionDep):
    return await UserService.get_all_users(session)


@user_router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user_data: UserCreate):
    exist_user = await UserService.get_one_or_none(
        session=session, username=user_data.username
    )
    if exist_user:
        raise user_already_exists
    return await UserService.create_user(session, user_data)


@user_router.get("/{user_id}/profile")
async def get_user_profile_by_id(session: SessionDep, user_id: int):
    return await UserService.get_one_by_id(
        session=session, model_id=user_id, options=[joinedload(User.profile)]
    )


@user_router.get("/followers/{user_id}")
async def get_user_by_id_with_followers(session: SessionDep, user_id: int):
    return await UserService.get_user_by_id_with_followers(
        session=session, user_id=user_id
    )


@user_router.post("/{follow_user_id}/follow")
async def follow_user(session: SessionDep, follow_user_id: int, current_user: UserDep):
    """Подписываемся на пользователя"""
    return await UserService.follow_user(
        session=session, follow_user_id=follow_user_id, current_user=current_user
    )


@user_router.delete("/{follow_user_id}/unfollow")
async def unfollow_user(
    session: SessionDep, follow_user_id: int, current_user: UserDep
):
    """Отписка от пользователя по id"""
    return await UserService.unfollow_user(
        session=session, unfollow_user_id=follow_user_id, current_user=current_user
    )
