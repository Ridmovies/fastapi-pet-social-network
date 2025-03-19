from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.auth.schemas import TokenSchema
from src.auth.pwd_utils import get_hashed_password, verify_password
from src.database import async_session
from src.services import BaseService
from src.users.models import User
from src.users.schemas import UserCreate


class AuthService(BaseService):
    model = User

    @classmethod
    async def create_user(cls, session: AsyncSession, user: UserCreate) -> User:
        hashed_password = get_hashed_password(user.password)
        user_instance = cls.model(
            username=user.username, hashed_password=hashed_password
        )
        session.add(user_instance)
        await session.commit()
        return user_instance

    @classmethod
    async def get_user_by_username(cls, username: str) -> User | None:
        async with async_session() as session:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
