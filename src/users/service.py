from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.operators import and_

from src.auth.schemas import UserCreate
# from src.auth2.pwd_utils import get_hashed_password
from src.services import BaseService
from src.users.models import User, user_to_user, Profile
# from src.users.schemas import UserCreate


class UserService(BaseService):
    model = User

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        query = select(User)
        result = await session.execute(query)
        return result.scalars().unique().all()  # Add unique() here


    @classmethod
    async def get_user_by_username(
        cls, session: AsyncSession, username: str
    ) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def get_user_by_username_with_following(
        cls, session: AsyncSession, username: str
    ) -> User | None:
        stmt = (
            select(User)
            .options(selectinload(User.following))
            .where(User.username == username)
        )
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def get_user_by_id_with_followers(
        cls, session: AsyncSession, user_id: int
    ) -> User:
        stmt = (
            select(User)
            .options(selectinload(User.following))  # Загружаем отношение `following`
            .where(User.id == user_id)
        )
        result = await session.execute(stmt)
        user = result.scalars().one_or_none()
        return user

    @classmethod
    async def follow_user(
            cls,
            session: AsyncSession,
            follow_user_id: int,
            current_user: User,
    ) -> dict:
        """
        Подписываемся на пользователя.

        :param session: Асинхронная сессия SQLAlchemy.
        :param follow_user_id: ID пользователя, на которого подписываемся.
        :param current_user: Текущий пользователь, который подписывается.
        :return: Словарь с результатом операции или ошибкой.
        """
        # Проверка, чтобы пользователь не мог подписаться на самого себя
        if current_user.id == follow_user_id:
            raise HTTPException(status_code=400, detail="Нельзя подписаться на самого себя")

        # Получаем пользователя, на которого хотим подписаться
        user_to_follow: User = await UserService.get_one_by_id(
            session=session, model_id=follow_user_id
        )
        if not user_to_follow:
            raise HTTPException(status_code=404, detail="Пользователь для подписки не найден")

        # Проверяем, не подписан ли уже текущий пользователь на целевого пользователя
        stmt = select(user_to_user).where(
            (user_to_user.c.follower_id == current_user.id)
            & (user_to_user.c.following_id == user_to_follow.id)
        )
        result = await session.execute(stmt)
        if result.scalar():
            raise HTTPException(status_code=400, detail="Вы уже подписаны на этого пользователя")

        # Пытаемся добавить запись о подписке
        try:
            ins = user_to_user.insert().values(
                follower_id=current_user.id, following_id=user_to_follow.id
            )
            await session.execute(ins)
            await session.commit()
            return {"result": True}

        except IntegrityError as e:
            await session.rollback()
            return {
                "result": False,
                "error_type": "IntegrityError",
                "error_message": str(e.args),
            }

        except Exception as e:
            await session.rollback()
            return {
                "result": False,
                "error_type": "OtherError",
                "error_message": str(e),
            }

    @classmethod
    async def _validate_unfollow_request(
            cls,
            current_user: User,
            unfollow_user_id: int,
            user_to_unfollow: Optional[User],
    ) -> None:
        """
        Проверяет валидность запроса на отписку.
        """
        if current_user.id == unfollow_user_id:
            raise HTTPException(
                status_code=400,
                detail="Нельзя отписаться от самого себя",
            )
        if not user_to_unfollow:
            raise HTTPException(
                status_code=404,
                detail="Пользователь для отписки не найден",
            )

    @classmethod
    async def _delete_follow_relationship(
            cls,
            session: AsyncSession,
            follower_id: int,
            following_id: int,
    ) -> int:
        """
        Удаляет запись о подписке из таблицы user_to_user.
        Возвращает количество удалённых строк.
        """
        query = delete(user_to_user).where(
            and_(
                user_to_user.c.follower_id == follower_id,
                user_to_user.c.following_id == following_id,
            )
        )
        result = await session.execute(query)
        return result.rowcount

    @classmethod
    async def unfollow_user(
            cls,
            session: AsyncSession,
            unfollow_user_id: int,
            current_user: User,
    ) -> dict:
        """
        Отписка от пользователя по id.
        """
        # Получаем пользователя, от которого хотим отписаться
        user_to_unfollow: Optional[User] = await UserService.get_one_by_id(
            session=session, model_id=unfollow_user_id
        )

        # Проверяем валидность запроса
        await cls._validate_unfollow_request(current_user, unfollow_user_id, user_to_unfollow)

        # Удаляем запись о подписке
        deleted_rows = await cls._delete_follow_relationship(
            session=session,
            follower_id=current_user.id,
            following_id=user_to_unfollow.id,
        )

        # Если запись не была удалена, значит, пользователь не был подписан
        if deleted_rows == 0:
            raise HTTPException(
                status_code=400,
                detail="Вы не подписаны на этого пользователя",
            )

        # Фиксируем изменения в базе данных
        await session.commit()

        return {"result": True}

