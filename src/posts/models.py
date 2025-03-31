from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.database import Base, SessionDep


if TYPE_CHECKING:
    from src.users.models import User
    from src.community.models import Community
    from src.comments.models import Comment


class Post(Base):
    __tablename__ = "post"

    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    community_id: Mapped[int] = mapped_column(ForeignKey("community.id"), nullable=False, default=1)
    image_path: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(back_populates="posts")
    likes: Mapped[list["Like"]] = relationship(
        back_populates="post", cascade="all, delete"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )  # Комментарии к посту
    community: Mapped["Community"] = relationship(back_populates="posts")




    def is_liked_by_user(self, session: SessionDep, user_id: int) -> bool:
        """Проверяет, поставил ли пользователь лайк на этот пост."""
        return (
            session.query(Like)
            .filter(Like.post_id == self.id, Like.user_id == user_id)
            .first()
            is not None
        )


class Like(Base):
    __tablename__ = "like"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC)
    )
    post: Mapped["Post"] = relationship(back_populates="likes")


# class Comment(Base):
#     """Модель комментария"""
#
#     __tablename__ = "comment"
#
#     content: Mapped[str] = mapped_column(String)  # Текст комментария
#     user_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("user.id")
#     )  # Автор комментария
#
#
#     # Один из этих двух должен быть заполнен
#     post_id: Mapped[Optional[int]] = mapped_column(ForeignKey("post.id"), nullable=True)
#     event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("event.id"), nullable=True)
#
#     # post_id: Mapped[int] = mapped_column(
#     #     Integer, ForeignKey("post.id")
#     # )  # Пост, к которому оставлен комментарий
#     #
#     # event_id: Mapped[int] = mapped_column(
#     #     Integer, ForeignKey("event.id"), nullable=True
#     # )
#
#     # Связи
#     user: Mapped["User"] = relationship(
#         "User", back_populates="comments"
#     )  # Автор комментария
#     post: Mapped["Post"] = relationship(
#         "Post", back_populates="comments"
#     )  # Пост, к которому оставлен комментарий
#
#     event: Mapped["Event"] = relationship(back_populates="comments")  # Новая связь
#
#     __table_args__ = (
#         CheckConstraint(
#             'post_id IS NOT NULL OR event_id IS NOT NULL',
#             name='check_comment_has_post_or_event'
#         ),
#     )
