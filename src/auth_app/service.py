from starlette.exceptions import HTTPException

from src.auth_app.auth import get_password_hash
from src.auth_app.models import User
from src.auth_app.schemas import UserOutSchema, UserInSchema
from src.database import async_session
from src.services import BaseService


class AuthService(BaseService):
    model = User

    @classmethod
    async def register(cls, user_data: UserInSchema):
        async with async_session() as session:
            user = await AuthService.get_one_or_none(username=user_data.username)
            if user:
                raise HTTPException(status_code=400, detail="User already exists")

            hashed_password = await get_password_hash(user_data.password)
            user = User(username=user_data.username, hashed_password=hashed_password)
            session.add(user)
            await session.commit()
            return user


    # @classmethod
    # async def login(cls, user_data: UserInSchema):
    #     async with async_session() as session:
    #         username = user_data.username
    #         user = await session.get(cls.model, username=username)
    #         return user
    #         # if user and user.check_password(password):
    #         #     return user
    #         # return None
    #




