# from typing import TYPE_CHECKING
#
# from sqlalchemy import Table, Column, Integer, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.models import Base
#
#
# # Таблица используется для установления связей между пользователями,
# # где каждый пользователь может следовать за другим пользователем.
# user_to_user = Table(
#     "user_to_user",
#     Base.metadata,
#     Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
#     Column("following_id", Integer, ForeignKey("user.id"), primary_key=True),
# )
#
#
# class User(Base):
#     username: Mapped[str] = mapped_column(unique=True)
#     hashed_password: Mapped[bytes]
#
#     tasks: Mapped[list["Task"]] = relationship(back_populates="user")
#     posts: Mapped[list["Post"]] = relationship(back_populates="user")
#
#     # Отношение 'following', которое показывает, на кого данный пользователь подписан
#     following: Mapped[list["User"]] = relationship(
#         "User",
#         lambda: user_to_user,
#         primaryjoin=lambda: User.id == user_to_user.c.follower_id,
#         secondaryjoin=lambda: User.id == user_to_user.c.following_id,
#         backref="followers",
#         lazy="selectin",
#     )
#
#     def is_following(self, user: "User"):
#         """Проверяет, подписан ли текущий пользователь на другого пользователя."""
#         return user.id in [user.id for user in self.following]
#
#
#     def __repr__(self) -> str:
#         return f"<User(username={self.username})>"
#
# if TYPE_CHECKING:
#     from src.tasks.models import Task
#     from src.posts.models import Post