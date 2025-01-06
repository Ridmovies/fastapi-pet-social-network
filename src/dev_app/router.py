from fastapi import APIRouter
from sqlalchemy import text

from src.database import engine, SessionDep
from src.models import Base

router = APIRouter(prefix="/dev", tags=["dev"])

@router.get("")
async def root():
    return {"message": "Hello World"}


@router.delete("/drop_db")
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "Database dropped"}


@router.get("/check-db-connection")
async def check_db_connection(session: SessionDep):
    """Check if the database connection is successful"""
    await session.execute(text("SELECT 1"))
    return {"message": "Connection to the database successful"}