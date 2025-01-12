from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")

if TYPE_CHECKING:
    from src.task_app.models import Task