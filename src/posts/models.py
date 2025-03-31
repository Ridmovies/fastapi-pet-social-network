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
