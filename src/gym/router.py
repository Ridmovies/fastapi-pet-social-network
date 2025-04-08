from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from src.auth.dependencies import UserDep
from src.database import SessionDep
from src.gym.models import GymWorkout, Exercise
from src.gym.schemas import GymWorkoutCreate, ExerciseCreate, GymWorkoutRead, ExerciseSetCreate
from src.gym.service import GymWorkoutService, ExerciseService, ExerciseSetService

router = APIRouter(prefix="/gym", tags=["gym"])


@router.get("", response_model=list[GymWorkoutRead])
async def get_all_gym_workouts(session: SessionDep):
    return await GymWorkoutService.get_all(
        session=session, options=[joinedload(GymWorkout.exercises).joinedload(Exercise.sets)]
    )

@router.post("")
async def create_gym_workouts(session: SessionDep, data: GymWorkoutCreate, user: UserDep):
    return await GymWorkoutService.create(
        session=session, data=data, user_id=user.id
    )


@router.delete("/{gym_id}")
async def delete_gym_workouts(session: SessionDep, gym_id: int, user: UserDep):
    return await GymWorkoutService.delete(session=session, user_id=user.id, model_id=gym_id)


### Exercise

@router.get("/{gym_id}/exercise")
async def get_all_exercise(session: SessionDep, gym_id: int):
    return await ExerciseService.get_one_by_id(session=session, model_id=gym_id)

@router.post("/exercise")
async def add_exercise(session: SessionDep, data: ExerciseCreate, user: UserDep):
    return await ExerciseService.create(session=session, data=data, user_id=user.id)

### ExerciseSet
@router.post("/exercise-set")
async def add_exercise_set(session: SessionDep, data: ExerciseSetCreate):
    return await ExerciseSetService.create_without_user(session=session, data=data)
