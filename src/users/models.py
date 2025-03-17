
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base

if TYPE_CHECKING:
    from src.tasks.models import Task
    from src.posts.models import Post, Comment

# Таблица используется для установления связей между пользователями,
# где каждый пользователь может следовать за другим пользователем.
user_to_user = Table(
    "user_to_user",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("user.id"), primary_key=True),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    # tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    communities_joined = relationship("CommunityMember", back_populates="user")
    communities_created = relationship("Community", back_populates="creator")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")  # Комментарии пользователя
    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")


    # Отношение 'following', которое показывает, на кого данный пользователь подписан
    following: Mapped[list["User"]] = relationship(
        "User",
        lambda: user_to_user,
        primaryjoin=lambda: User.id == user_to_user.c.follower_id,
        secondaryjoin=lambda: User.id == user_to_user.c.following_id,
        backref="followers",
        lazy="selectin",
    )

    def is_following(self, user: "User"):
        """Проверяет, подписан ли текущий пользователь на другого пользователя."""
        return user.id in [user.id for user in self.following]

    def __repr__(self) -> str:
        return f"<User(username={self.email})>"


# Модель профиля
class Profile(Base):
    __tablename__ = "profile"
    name: Mapped[str] = mapped_column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    # Связь с пользователем
    user = relationship("User", back_populates="profile")



