from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


if TYPE_CHECKING:
    from src.users.models import User
    from src.events.models import Event
    from src.posts.models import Post


class Comment(Base):
    """Модель комментария"""

    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String)  # Текст комментария
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id")
    )  # Автор комментария


    # Один из этих двух должен быть заполнен
    post_id: Mapped[Optional[int]] = mapped_column(ForeignKey("post.id"), nullable=True)
    event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("event.id"), nullable=True)


    # Связи
    user: Mapped["User"] = relationship(
        "User", back_populates="comments"
    )  # Автор комментария
    post: Mapped["Post"] = relationship(
        "Post", back_populates="comments"
    )  # Пост, к которому оставлен комментарий

    event: Mapped["Event"] = relationship(back_populates="comments")  # Новая связь

    __table_args__ = (
        CheckConstraint(
            'post_id IS NOT NULL OR event_id IS NOT NULL',
            name='check_comment_has_post_or_event'
        ),
    )
