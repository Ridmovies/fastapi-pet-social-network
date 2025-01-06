from sqlalchemy.orm import Mapped

from src.database import Base


class Post(Base):
    message: Mapped[str]