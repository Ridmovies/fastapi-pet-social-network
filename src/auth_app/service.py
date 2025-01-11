from starlette.exceptions import HTTPException

from src.auth_app.models import User
from src.database import async_session
from src.services import BaseService


class AuthService(BaseService):
    model = User

    @classmethod
    async def register(cls, username: str, hashed_password: str):
        async with async_session() as session:
            user = await AuthService.get_one_or_none(username=username)
            if user:
                raise HTTPException(status_code=400, detail="User already exists")

            return await AuthService.insert(username=username, hashed_password=hashed_password)




