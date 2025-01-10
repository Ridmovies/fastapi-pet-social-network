from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Task(Base):
    title: Mapped[str]
    description: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    completed: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[Enum] = mapped_column(Enum('Low', 'Medium', 'High', name='priority_enum'), default='Low')