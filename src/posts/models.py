from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Post(Base):
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))