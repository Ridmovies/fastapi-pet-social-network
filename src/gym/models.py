import enum
from datetime import datetime, UTC
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.users.models import User


class MuscleGroup(enum.Enum):
    BACK = "спина"
    TRICEPS = "трицепс"
    CHEST = "грудь"
    SHOULDERS = "плечи"
    CORE = "кор"
    BICEPS = "бицепс"
    FOREARM = "предплечье"
    THIGHS = "бёдра"
    GLUTES = "ягодицы"
    CALVES = "голень"
    FULL_BODY = "всё тело"

class Equipment(enum.Enum):
    ANY = "всё оборудование"
    NONE = "без оборудования"
    BARBELL = "штанга"
    DUMBBELLS = "гантели"
    RESISTANCE_BANDS = "резинки"
    BENCH = "скамья"
    KETTLEBELLS = "гири"
    WEIGHT_PLATES = "блины"
    GYMNASTIC_BALL = "гимнастический мяч"
    EZ_BAR = "EZ штанга"
    PULL_UP_BAR = "перекладина"
    MACHINES = "тренажёры"

class DifficultyLevel(enum.Enum):
    ALL = "Все"
    BEGINNER = "Начинающий"
    INTERMEDIATE = "Средний"
    ADVANCED = "Продвинутый"


class GymWorkout(Base):
    __tablename__ = "gym_workout"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    equipment: Mapped[Equipment] = mapped_column(default=Equipment.ANY)
    difficulty: Mapped[DifficultyLevel] = mapped_column(default=DifficultyLevel.ALL)
    workout_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(UTC))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(UTC))

    # Связь с пользователем
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # user: Mapped["User"] = relationship(back_populates="gym_workouts")

    # Связь с упражнениями
    exercises: Mapped[List["Exercise"]] = relationship(back_populates="gym_workout", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    muscle_group: Mapped[MuscleGroup] = mapped_column(default=MuscleGroup.FULL_BODY)

    # Связь с тренировкой
    gym_workout_id: Mapped[int] = mapped_column(ForeignKey("gym_workout.id"))
    gym_workout: Mapped["GymWorkout"] = relationship(back_populates="exercises")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Связь с подходами
    sets: Mapped[List["ExerciseSet"]] = relationship(back_populates="exercise", cascade="all, delete-orphan")


class ExerciseSet(Base):
    __tablename__ = "exercise_set"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reps: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True)  # в секундах
    order: Mapped[int] = mapped_column(Integer)  # порядковый номер подхода

    # Связь с упражнением
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise.id"))
    exercise: Mapped["Exercise"] = relationship(back_populates="sets")