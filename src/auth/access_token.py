# from fastapi import Depends
# from fastapi_users_db_sqlalchemy.access_token import (
#     SQLAlchemyBaseAccessTokenTable,
#     SQLAlchemyAccessTokenDatabase,
# )
# from sqlalchemy import Integer, ForeignKey
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import declared_attr, Mapped, mapped_column
#
# from src.auth.utils import get_async_session
# from src.database import Base
#
# from fastapi_users_db_sqlalchemy.access_token import (
#     SQLAlchemyAccessTokenDatabase,
# )
#
#
# class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
#     @declared_attr
#     def user_id(cls) -> Mapped[int]:
#         return mapped_column(
#             Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
#         )
#
#
# async def get_access_token_db(
#     session: AsyncSession = Depends(get_async_session),
# ):
#     yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
