from typing import TYPE_CHECKING, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, relationship, mapped_column, declared_attr

from src.database import Base


if TYPE_CHECKING:
    from src.posts.models import Post, Comment
    from src.achievements.models import Achievement
    from src.messages.models import Message
    from src.events.models import Event
    from src.gym.models import GymWorkout
    from src.workout.models import WorkoutStatistics

# Таблица используется для установления связей между пользователями,
# где каждый пользователь может следовать за другим пользователем.
user_to_user = Table(
    "user_to_user",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("user.id"), primary_key=True),
)


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True)  # Идентификатор пользователя
    username: Mapped[str] = mapped_column(unique=True, nullable=True)  # Имя пользователя
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")

    # tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )  # Посты пользователя
    communities_joined = relationship(
        "CommunityMember", back_populates="user", cascade="all, delete-orphan"
    )
    communities_created = relationship(
        "Community", back_populates="creator", cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )  # Комментарии пользователя
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", cascade="all, delete-orphan"
    )
    # Связь с достижениями
    achievements: Mapped[list["Achievement"]] = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")

    # Связь с отправленными сообщениями
    sent_messages: Mapped[list["Message"]] = relationship(
        "Message", foreign_keys="Message.user_id", back_populates="sender"
    )

    # Связь с полученными сообщениями
    received_messages: Mapped[list["Message"]] = relationship(
        "Message", foreign_keys="Message.receiver_id", back_populates="receiver"
    )


    # Отношение 'following', которое показывает, на кого данный пользователь подписан
    following: Mapped[list["User"]] = relationship(
        "User",
        lambda: user_to_user,
        primaryjoin=lambda: User.id == user_to_user.c.follower_id,
        secondaryjoin=lambda: User.id == user_to_user.c.following_id,
        backref="followers",
        cascade="all, delete",
    )

    # События, которые пользователь организовал
    organized_events: Mapped[List["Event"]] = relationship(
        back_populates="organizer",
        cascade="all, delete-orphan"
    )

    # События, в которых пользователь участвует
    events_participated: Mapped[List["Event"]] = relationship(
        secondary="event_participation",
        back_populates="participants"
    )

    workout_statistics: Mapped["WorkoutStatistics"] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(username={self.email})>"


# Модель профиля
class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"))

    # Связь с пользователем
    user = relationship("User", back_populates="profile")


    @hybrid_property
    def full_name(self):
        return f"test"

