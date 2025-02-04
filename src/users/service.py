from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import BaseService

from src.users.models import User
from src.users.pwd_utils import get_password_hash
from src.users.schemas import UserInSchema, UserOutSchema


class UserService(BaseService):
    model = User


    @classmethod
    async def create_user(cls, data: UserInSchema, session: AsyncSession) -> User:
        username = data.username
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