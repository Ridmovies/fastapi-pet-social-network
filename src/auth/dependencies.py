from typing import Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_router import current_user, current_user_or_guest
from src.auth.utils import get_async_session
from src.users.models import User

UserDep = Annotated[User, Depends(current_user)]
UserOrGuestDep = Annotated[User, Depends(current_user_or_guest)]

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]