from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import BaseService

from src.users.models import User, user_to_user
from src.users.pwd_utils import get_password_hash
from src.users.schemas import UserInSchema


class UserService(BaseService):
    model = User


    @classmethod
    async def create_user(cls, data: UserInSchema, session: AsyncSession) -> User:
        """Создание нового пользователя"""
        username = data.username
        # Проверяем, существует ли пользователь с таким username
        existing_user = await session.execute(
            select(User).where(User.username == username)
        )
        if existing_user.scalar():
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
        # Если пользователя нет, создаем нового
        hashed_password = get_password_hash(data.password)
        new_user = User(username=username, hashed_password=hashed_password)
        session.add(new_user)
        await session.commit()
        return new_user


    @classmethod
    async def get_user_by_username(cls, session: AsyncSession, username: str, ) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def follow_user(
            cls,
            session: AsyncSession,
            follow_user_id: int,
            current_user: User,

    ):
        """Подписываемся на пользователя"""
        # Получить пользователя на которого хотим подписаться по id
        user_to_follow: User = await UserService.get_one_by_id(session=session, model_id=follow_user_id)
        if current_user and user_to_follow:
            from sqlalchemy.exc import IntegrityError
            try:
                # Увеличиваем популярность на 1
                # user_to_follow.popularity += 1

                # Вставка в таблицу новой записи, только если составное значение уникально
                ins = user_to_user.insert().values(
                    follower_id=current_user.id, following_id=user_to_follow.id
                )
                await session.execute(ins)
                await session.commit()
                return {"result": True}

            except IntegrityError as e:
                return {
                    "result": False,
                    "error_type": "IntegrityError",
                    "error_message": str(e.args),
                }

            except Exception as e:
                return {
                    "result": False,
                    "error_type": "OtherError",
                    "error_message": str(e),
                }
        return {"result": False}