from sqlalchemy import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.services import BaseService
from src.workout.models import Workout, Walk, Run, Bicycle, WorkoutType, WorkoutStatistics
from src.workout.schemas import WorkoutCreate, ActivityBase


class WalkService(BaseService):
    model = Walk


class WorkoutService(BaseService):
    model = Workout

    @classmethod
    async def get_user_workout(
            cls,
            session: AsyncSession,
            user_id: int,
            sort_by: str,
    ):
        # Разбиваем параметр на части
        if '_' in sort_by:
            sort_field, sort_order = sort_by.split('_', 1)
        else:
            sort_field = sort_by
            sort_order = "desc"

        # Базовый запрос
        query = select(Workout).where(Workout.user_id == user_id)

        # Определяем направление сортировки
        order_func = desc if sort_order.lower() == "desc" else asc

        # Применяем сортировку
        if sort_field == "title":
            query = query.order_by(order_func(Workout.title))
        elif sort_field == "type":
            query = query.order_by(order_func(Workout.type))
        elif sort_field == "distance":
            query = query.join(Workout.bicycle).order_by(order_func(Bicycle.distance_km))
        else:  # по умолчанию сортируем по дате
            query = query.order_by(order_func(Workout.created_at))

        # Загружаем связанные данные
        query = query.options(
            joinedload(Workout.run),
            joinedload(Workout.bicycle),
            joinedload(Workout.walk)
        )

        result = await session.execute(query)
        return result.scalars().unique().all()

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

    @classmethod
    async def refresh_total_statistics(cls, session: AsyncSession, user_id: int, track_data: dict):
        try:
            # Получаем статистику пользователя
            query = select(WorkoutStatistics).filter_by(user_id=user_id)
            result = await session.execute(query)
            stats = result.scalar_one_or_none()

            if not stats:
                stats = WorkoutStatistics(
                    user_id=user_id,
                    total_workouts=1,
                    total_distance_km=float(track_data["distance_km"]),
                    total_duration_sec=int(track_data["duration_sec"])
                )
                session.add(stats)
                await session.flush()  # Важно: получаем сгенерированный ID
            else:
                stats.total_workouts += 1
                stats.total_distance_km += float(track_data["distance_km"])
                stats.total_duration_sec += int(track_data["duration_sec"])

            await session.commit()
        except Exception as e:
            await session.rollback()
            raise

