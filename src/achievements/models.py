from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base


if TYPE_CHECKING:
    from src.users.models import User


class Achievement(Base):
    """Модель достижения пользователя"""

    __tablename__ = "achievement"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Связь с пользователем
    user: Mapped["User"] = relationship("User", back_populates="achievements")
