from fastapi import APIRouter
from src.achievements.service import AchievementService
from src.database import SessionDep


router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/{user_id}")
async def get_user_achievements(session: SessionDep, user_id: int):
    return await AchievementService.get_all(session=session, user_id=user_id)