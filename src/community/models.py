from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.users.models import User


class Community(Base):
    """Модель сообщества"""

    __tablename__ = "community"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str]
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    creator: Mapped["User"] = relationship("User", back_populates="communities_created")
    members: Mapped[list["CommunityMember"]] = relationship(
        "CommunityMember", back_populates="community"
    )


class CommunityMember(Base):
    """
    Модель для связи между пользователем и сообществом

    Использование модели CommunityMember (или промежуточной таблицы) вместо прямой связи между
    User и Community является стандартной практикой в реляционных базах данных для реализации отношений
    многие-ко-многим (many-to-many). Это позволяет более гибко управлять данными и добавлять дополнительные
    атрибуты к связи между пользователями и сообществами.
    """

    __tablename__ = "community_member"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    community_id: Mapped[int] = mapped_column(Integer, ForeignKey("community.id"))

    user = relationship("User", back_populates="communities_joined")
    community = relationship("Community", back_populates="members")
