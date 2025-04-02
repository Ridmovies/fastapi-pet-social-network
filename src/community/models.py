from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.posts.models import Post
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
    posts: Mapped[list["Post"]] = relationship(back_populates="community")

    chat: Mapped["CommunityChat"] = relationship(
        "CommunityChat",
        back_populates="community",
        uselist=False,
        cascade="all, delete-orphan"
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


class CommunityChat(Base):
    """Модель чата сообщества"""

    __tablename__ = "community_chat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    community_id: Mapped[int] = mapped_column(Integer, ForeignKey("community.id"))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC)
    )

    community: Mapped["Community"] = relationship("Community", back_populates="chat")
    messages: Mapped[list["CommunityMessage"]] = relationship(
        "CommunityMessage",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="CommunityMessage.created_at"
    )


class CommunityMessage(Base):
    """Модель сообщения в чате сообщества"""

    __tablename__ = "community_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("community_chat.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    text: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC)
    )

    chat: Mapped["CommunityChat"] = relationship("CommunityChat", back_populates="messages")
    user: Mapped["User"] = relationship("User")