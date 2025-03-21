from fastapi import APIRouter, status

from src.database import SessionDep
from src.messages.service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/{user_id}")
async def get_user_messages(session: SessionDep, user_id: int):
    return await MessageService.get_all(session=session, user_id=user_id)


# @router.post("/{user_id}", response_model=AchievementRead)
# async def create_achievement(session: SessionDep, user_id: int, data: AchievementCreate):
#     return await AchievementService.create(
#         session=session, user_id=user_id, data=data
#     )
#
# @router.delete("/{user_id}/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_achievement(session: SessionDep, user_id: int, achievement_id: int):
#     return await AchievementService.delete(
#         session=session, user_id=user_id, model_id=achievement_id
#     )