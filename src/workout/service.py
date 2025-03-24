from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.services import BaseService
from src.workout.models import Workout, Walk, Run, Bicycle, WorkoutType
from src.workout.schemas import WorkoutCreate, ActivityBase


class WalkService(BaseService):
    model = Walk


class WorkoutService(BaseService):
    model = Workout

    @classmethod
    async def create_workout(cls, session: AsyncSession, user_id: int, data: WorkoutCreate):
        # Создание тренировки
        workout_data = data.model_dump(exclude={"run", "bicycle", "walk"})
        db_workout = cls.model(**workout_data, user_id=user_id)
        session.add(db_workout)

        # Создание подтипа активности, если он предоставлен
        if data.walk:
            walk_data = data.walk.model_dump()
            db_workout.walk = Walk(**walk_data)
            session.add(db_workout.walk)
        elif data.run:
            run_data = data.run.model_dump()
            db_workout.run = Run(**run_data)
            session.add(db_workout.run)
        elif data.bicycle:
            bicycle_data = data.bicycle.model_dump()
            db_workout.bicycle = Bicycle(**bicycle_data)
            session.add(db_workout.bicycle)

        await session.commit()
        return {"status": "success"}


    @classmethod
    async def create_workout_2(
            cls,
            session: AsyncSession,
            user_id: int,
            track_data: dict,
            workout_type: WorkoutType
    ):
        # 1. Создаём основную тренировку
        workout = Workout(user_id=user_id, type=workout_type)
        session.add(workout)
        await session.flush()  # Получаем ID тренировки

        # 2. Подготавливаем данные для активности
        activity_data = {
            "workout_id": workout.id,  # Критически важно!
            "distance_km": float(track_data["distance_km"]),
            "duration_min": float(track_data["duration_min"]),
            "avg_speed_kmh": float(track_data["avg_speed_kmh"])
        }

        # 3. Создаём конкретную активность
        if workout_type == WorkoutType.WALK:
            activity = Walk(**activity_data)
        elif workout_type == WorkoutType.RUN:
            activity = Run(**activity_data)
        elif workout_type == WorkoutType.BICYCLE:
            activity = Bicycle(**activity_data)
        else:
            raise ValueError("Invalid workout type")

        session.add(activity)
        await session.commit()

        return {"status": "success", "workout_id": workout.id}



    @classmethod
    async def get_run_stat(cls, session: AsyncSession, user_id: int):
        query = (
            select(Workout)
            .filter_by(user_id=user_id, type=WorkoutType.RUN)
            .options(selectinload(Workout.run))
        )

        result = await session.execute(query)
        workouts = result.scalars().all()
        if workouts:
            total_duration = sum(workout.run.duration_min for workout in workouts)
            total_distance = sum(workout.run.distance_km for workout in workouts)
        return {
            "total_distance_km": round(total_distance, 2),
            "total_duration_min": total_duration
        }

