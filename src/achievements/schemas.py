from datetime import datetime

from pydantic import BaseModel

class AchievementBase(BaseModel):
    title: str
    description: str | None

class AchievementCreate(AchievementBase):
    pass


class AchievementRead(AchievementBase):
    id: int
    created_at: datetime

