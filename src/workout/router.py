import os
from datetime import datetime, timedelta


from fastapi import APIRouter, status, UploadFile, File, HTTPException
from sqlalchemy.orm import joinedload

from src.auth2.jwt_utils import UserDep
from src.database import SessionDep
from src.workout import utils
from src.workout.models import Workout, WorkoutType
from src.workout.schemas import WorkoutCreate
from src.workout.service import WorkoutService
from src.workout.utils import create_map_filename

router = APIRouter(prefix="/workout", tags=["workout"])


@router.get("")
async def get_user_workout(session: SessionDep, user: UserDep):
    return await WorkoutService.get_all(
        session=session,
        user_id=user.id,
        options=[joinedload(Workout.run), joinedload(Workout.bicycle), joinedload(Workout.walk)]
    )


@router.get("/statistics")
async def get_user_workout_statistics(session: SessionDep, user: UserDep):
    return await WorkoutService.get_run_stat(
        session=session,
        user_id=user.id,
    )

@router.get("/{user_id}/run")
async def get_user_workout_by_run(session: SessionDep, user: UserDep, user_id: int):
    return await WorkoutService.get_run_stat(
        session=session,
        user_id=user_id,
    )

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_workout(session: SessionDep, user: UserDep, data: WorkoutCreate):
    return await WorkoutService.create_workout(
        session=session,
        user_id=user.id,
        data=data
    )


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(session: SessionDep, user: UserDep, workout_id: int):
    return await WorkoutService.delete(
        session=session,
        model_id=workout_id,
        user_id=user.id
    )

@router.get("/{workout_id}")
async def workout_details(session: SessionDep, user: UserDep, workout_id: int):
    return await WorkoutService.workout_details(
        session=session,
        workout_id=workout_id,
        user_id=user.id
    )



@router.post("/uploadgpx/")
async def upload_gpx_file(file: UploadFile = File(...)):
    return await utils.calculate_track_info(file)


@router.post("/uploadgpx/test")
async def upload_gpx_file(
        session: SessionDep,
        user: UserDep,
        workout_type: WorkoutType,
        file: UploadFile = File(...),
):
    """Тестовая функция для получения данных трека"""
    map_filename = create_map_filename()
    track_data = await utils.calculate_track_info(file, workout_type, map_filename)
    return await WorkoutService.create_workout_2(
        session=session,
        user_id=user.id,
        track_data=track_data,
        workout_type=workout_type,
        map_filename=map_filename
    )

