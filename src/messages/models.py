from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base


if TYPE_CHECKING:
    from src.users.models import User

class Message(Base):
    """Модель личного сообщения"""

    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(nullable=False)  # Текст сообщения
    read: Mapped[bool] = mapped_column(default=False)  # Прочитано ли сообщение
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC)
    )
    is_read: Mapped[bool] = mapped_column(default=False)  # Прочитано ли сообщение

    # Связь с отправителем (пользователь, который отправил сообщение)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    sender: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id], back_populates="sent_messages"
    )

    # Связь с получателем (пользователь, который получил сообщение)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    receiver: Mapped["User"] = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_messages"
    )