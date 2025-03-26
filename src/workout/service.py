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
            workout_type: WorkoutType,
            map_filename: str,
            title: str | None
    ):
        # 1. Создаём основную тренировку
        workout = Workout(title=title, user_id=user_id, type=workout_type, map=map_filename)
        session.add(workout)
        await session.flush()  # Получаем ID тренировки

        # 2. Подготавливаем данные для активности
        activity_data = {
            "workout_id": workout.id,  # Критически важно!
            "distance_km": float(track_data["distance_km"]),
            "duration_sec": track_data["duration_sec"],
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

        total_duration = 0
        total_distance = 0
        if workouts:
            # Суммируем продолжительности
            total_duration = sum(workout.run.duration_sec for workout in workouts)
            total_distance = sum(workout.run.distance_km for workout in workouts)
        return {
            "total_distance_km": round(total_distance, 2),
            "total_duration_sec": total_duration
        }


    @classmethod
    async def workout_details(cls, session: AsyncSession, workout_id: int, user_id: int):
        query = (
            select(Workout)
            .filter_by(user_id=user_id, id=workout_id)
            .options(selectinload(Workout.run))
        )
        result = await session.execute(query)
        workout = result.scalar_one_or_none()
        if workout:
            return workout
            # return {
            #     "workout_id": workout.id,
            #     "type": workout.type,
            #     "distance_km": workout.run.distance_km,
            #     "duration_sec": workout.run.duration_sec,
            # }

