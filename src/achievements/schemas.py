from pydantic import BaseModel


class AchievementCreate(BaseModel):
    title: str
    description: str | None
    user_id: int


class AchievementRead(BaseModel):
    id: int

