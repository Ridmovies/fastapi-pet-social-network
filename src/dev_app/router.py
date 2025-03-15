import httpx
from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from src.database import engine, SessionDep, Base

router = APIRouter(prefix="/dev", tags=["dev"])


@router.get("")
async def root():
    return {"message": "Hello World"}


@router.delete("/drop_db")
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        # Удаляем таблицу alembic_version
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        # await conn.run_sync(Base.metadata.create_all)
    return {"message": "Database dropped"}


@router.get("/check-db-connection")
async def check_db_connection(session: SessionDep):
    """Check if the database connection is successful"""
    await session.execute(text("SELECT 1"))
    return {"message": "Connection to the database successful"}


async def get_github_commits(owner: str, repo: str, limit: int = 5):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch commits from GitHub",
            )
        commits = response.json()
        return commits[:limit]  # Возвращаем только последние `limit` коммитов
