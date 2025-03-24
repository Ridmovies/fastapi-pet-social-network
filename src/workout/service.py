from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.services import BaseService
from src.workout.models import Workout, Walk, Run, Bicycle, WorkoutType
from src.workout.schemas import WorkoutCreate

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

