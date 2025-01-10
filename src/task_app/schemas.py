from pydantic import BaseModel, Field


class TaskSchema(BaseModel):
    title: str
    description: str | None = None
    completed: bool = Field(default=False)
