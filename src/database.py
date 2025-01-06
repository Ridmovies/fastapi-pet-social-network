from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from src.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)

# TODO Using multiple asyncio event loops for testing app
# engine = create_async_engine(
#     "postgresql+asyncpg://user:pass@host/dbname",
#     poolclass=NullPool,
# )

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """ create __tablename__ table name """
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True)


async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]