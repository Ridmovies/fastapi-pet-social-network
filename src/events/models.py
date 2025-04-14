from datetime import datetime, UTC
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from src.database import Base


if TYPE_CHECKING:
    from src.users.models import User
    from src.posts.models import Comment


class WorkoutType(PyEnum):
    RUN = "RUN"
    BICYCLE = "BICYCLE"
    WALK = "WALK"
    # Можно добавить другие типы


class Event(Base):
    """Модель спортивного мероприятия"""

    __tablename__ = "event"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True)  # Название мероприятия
    description: Mapped[Optional[str]]  # Описание
    # type: #Mapped[WorkoutType] = mapped_column(
    #     Enum(WorkoutType, name="workouttype", create_constraint=False),
    #     default=WorkoutType.WALK
    # )
    start_datetime: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC))
    end_datetime: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC), nullable=True)
    location: Mapped[str | None]  # Место проведения
    # max_participants: Mapped[Optional[int]]  # Максимальное количество участников
    is_private: Mapped[bool] = mapped_column(default=False)  # Приватное/публичное
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC))

    # Организатор мероприятия (связь с User)
    # organizer_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    organizer: Mapped["User"] = relationship(back_populates="organized_events")

    # Участники мероприятия (многие-ко-многим с User)
    participants: Mapped[List["User"]] = relationship(
        secondary="event_participation",
        back_populates="events_participated"
    )

    # # Дополнительные поля для разных типов спорта
    # required_equipment: Mapped[Optional[str]]  # Необходимое снаряжение
    # skill_level: Mapped[Optional[str]]  # Уровень подготовки (новичок, любитель, про)

    # Статус мероприятия (планируется, идет, завершено, отменено)
    status: Mapped[str] = mapped_column(default="planned")
    comments: Mapped[List["Comment"]] = relationship(back_populates="event")

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}')>"


class EventParticipation(Base):
    """Ассоциативная таблица для участия в мероприятиях"""

    __tablename__ = "event_participation"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC))
    # role: Mapped[Optional[str]]  # Например, "участник", "капитан", "запасной"