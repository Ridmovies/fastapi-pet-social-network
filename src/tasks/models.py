from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.users.models import User


class Task(Base):
    title: Mapped[str]
    description: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    completed: Mapped[bool] = mapped_column(default=False)
    # priority: Mapped[Enum] = mapped_column(Enum('Low', 'Medium', 'High', name='priority_enum'), default='Low')

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")
