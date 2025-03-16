from fastapi import APIRouter

from src.auth.dependencies import UserDep, SessionDep
from src.users.schemas import UserRead
from src.users.service import UserService


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("", response_model=list[UserRead])
async def get_all_users(session: SessionDep):
    return await UserService.get_all_users(session)


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
