from sqlalchemy.orm import Mapped

from src.models import Base


class Post(Base):
    content: Mapped[str]