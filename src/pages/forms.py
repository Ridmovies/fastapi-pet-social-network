from pydantic import BaseModel


class TaskForm(BaseModel):
    title: str
    description: str | None = None
    completed: bool
    priority: str = "Low"
