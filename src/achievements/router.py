from fastapi import APIRouter, status

from src.achievements.schemas import AchievementCreate, AchievementRead
from src.achievements.service import AchievementService
from src.database import SessionDep


router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/{user_id}", response_model=list[AchievementRead])
async def get_user_achievements(session: SessionDep, user_id: int):
    return await AchievementService.get_all(session=session, user_id=user_id)


@router.post("/{user_id}", response_model=AchievementRead)
async def create_achievement(session: SessionDep, user_id: int, data: AchievementCreate):
    return await AchievementService.create(
        session=session, user_id=user_id, data=data
    )

@router.delete("/{user_id}/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_achievement(session: SessionDep, user_id: int, achievement_id: int):
    return await AchievementService.delete(
        session=session, user_id=user_id, model_id=achievement_id
    )