from fastapi import APIRouter, status
from sqlalchemy.orm import joinedload

from src.auth2.jwt_utils import UserDep
from src.database import SessionDep
from src.workout.models import Workout
from src.workout.schemas import WorkoutCreate
from src.workout.service import WorkoutService

router = APIRouter(prefix="/workout", tags=["workout"])


@router.get("/{user_id}")
async def get_user_workout(session: SessionDep, user: UserDep, user_id: int):
    return await WorkoutService.get_all(
        session=session,
        user_id=user_id,
        options=[joinedload(Workout.run), joinedload(Workout.bicycle), joinedload(Workout.walk)]
    )

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_workout(session: SessionDep, user: UserDep, data: WorkoutCreate):
    return await WorkoutService.create_workout(
        session=session,
        user_id=user.id,
        data=data
    )

