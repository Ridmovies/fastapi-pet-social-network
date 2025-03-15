from typing import Annotated, AsyncGenerator, TYPE_CHECKING

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import NullPool, Integer, Table, Column, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DB_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, echo=False, **DATABASE_PARAMS)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


# Таблица используется для установления связей между пользователями,
# где каждый пользователь может следовать за другим пользователем.
user_to_user = Table(
    "user_to_user",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("user.id"), primary_key=True),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    # tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    # Отношение 'following', которое показывает, на кого данный пользователь подписан
    following: Mapped[list["User"]] = relationship(
        "User",
        lambda: user_to_user,
        primaryjoin=lambda: User.id == user_to_user.c.follower_id,
        secondaryjoin=lambda: User.id == user_to_user.c.following_id,
        backref="followers",
        lazy="selectin",
    )

    def is_following(self, user: "User"):
        """Проверяет, подписан ли текущий пользователь на другого пользователя."""
        return user.id in [user.id for user in self.following]

    def __repr__(self) -> str:
        return f"<User(username={self.email})>"


if TYPE_CHECKING:
    from src.tasks.models import Task
    from src.posts.models import Post


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
