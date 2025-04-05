import enum
from datetime import datetime, UTC
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base


if TYPE_CHECKING:
    from src.users.models import User


# Определение перечислимого типа для типов тренировок
class WorkoutType(enum.Enum):
    RUN = "run"
    BICYCLE = "bicycle"
    WALK = "walk"

class Workout(Base):
    """Модель тренировки"""

    __tablename__ = "workout"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC)
    )
    type: Mapped[WorkoutType] = mapped_column(default=WorkoutType.WALK)  # Использование перечисления
    map: Mapped[str] = mapped_column(nullable=True)

    # Связь с подмоделями
    run: Mapped[Optional["Run"]] = relationship(back_populates="workout", cascade="all, delete-orphan")
    bicycle: Mapped[Optional["Bicycle"]] = relationship(back_populates="workout", cascade="all, delete-orphan")
    walk: Mapped[Optional["Walk"]] = relationship(back_populates="workout", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Workout(id={self.id}, title={self.title}, type={self.type})"


# Базовая модель для общих полей
class Activity(Base):
    """Базовая модель для активности (бег, велосипед, ходьба)"""

    __abstract__ = True  # Это абстрактная модель, она не создаст таблицу в БД
    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workout.id"))
    distance_km: Mapped[float]  # Дистанция в километрах
    duration_sec: Mapped[int]  # Продолжительность в минутах
    avg_speed_kmh: Mapped[float]  # Средняя скорость в км/ч

# Подмодели, наследующиеся от Activity
class Run(Activity):
    """Модель бега"""

    __tablename__ = "run"

    workout: Mapped["Workout"] = relationship(back_populates="run")

class Bicycle(Activity):
    """Модель велосипеда"""

    __tablename__ = "bicycle"
    max_speed_kmh: Mapped[float | None]  # Максимальная скорость в км/ч

    workout: Mapped["Workout"] = relationship(back_populates="bicycle")

class Walk(Activity):
    """Модель ходьбы"""

    __tablename__ = "walk"
    avg_heart_rate_bpm: Mapped[int | None]  # Средняя частота пульса в био-митах

    workout: Mapped["Workout"] = relationship(back_populates="walk")


class WorkoutStatistics(Base):
    """Модель для хранения агрегированной статистики пользователя"""

    __tablename__ = "workout_statistics"

    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Добавлено autoincrement
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    total_workouts: Mapped[int] = mapped_column(default=0)
    total_distance_km: Mapped[float] = mapped_column(default=0.0)
    total_duration_sec: Mapped[int] = mapped_column(default=0)

    # Статистика по типам тренировок
    runs_count: Mapped[int] = mapped_column(default=0)
    runs_distance: Mapped[float] = mapped_column(default=0.0)

    bicycles_count: Mapped[int] = mapped_column(default=0)
    bicycles_distance: Mapped[float] = mapped_column(default=0.0)

    walks_count: Mapped[int] = mapped_column(default=0)
    walks_distance: Mapped[float] = mapped_column(default=0.0)

    # Связь с пользователем
    user: Mapped["User"] = relationship(back_populates="workout_statistics")