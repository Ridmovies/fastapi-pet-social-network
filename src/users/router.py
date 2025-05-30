from fastapi import APIRouter
from sqlalchemy import exists, select
from sqlalchemy.orm import joinedload, selectinload

from src.auth.dependencies import UserDep
from src.auth.schemas import UserRead, UserCreate
from src.database import SessionDep
from src.users.models import User, user_to_user
from src.users.service import UserService

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("", response_model=list[UserRead])
async def get_all_users(session: SessionDep):
    return await UserService.get_all_users(session)


@user_router.get("/me", response_model=UserRead)
async def read_users_me(
        current_user: UserDep,
        session: SessionDep
):
    return await UserService.get_one_by_id(
        session=session, model_id=current_user.id, options=[
            joinedload(User.profile),
            joinedload(User.following),
            joinedload(User.followers),
            joinedload(User.workout_statistics)
        ]
    )



@user_router.get("/{user_id}/profile", response_model=UserRead)
async def get_user_profile_by_id(session: SessionDep, user_id: int):
    return await UserService.get_one_by_id(
        session=session, model_id=user_id, options=[joinedload(User.profile)]
    )


@user_router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id_with_followers(session: SessionDep, user_id: int):
    return await UserService.get_one_by_id(
        session=session, model_id=user_id, options=[selectinload(User.following)]
    )


@user_router.post("/{follow_user_id}/follow")
async def follow_user(session: SessionDep, follow_user_id: int, current_user: UserDep):
    """Подписываемся на пользователя"""
    # Проверка, чтобы пользователь не мог подписаться на самого себя
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


@user_router.get("/is-following/{target_user_id}")
async def check_following(session: SessionDep, user: UserDep, target_user_id: int):
    # Асинхронный запрос с exists()
    query = select(
        exists().where(
            user_to_user.c.follower_id == user.id,
            user_to_user.c.following_id == target_user_id
        )
    )

    result = await session.execute(query)
    is_following = result.scalar()  # Получаем True/False

    return {"is_following": is_following}