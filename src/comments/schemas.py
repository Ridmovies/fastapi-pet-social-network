from pydantic import BaseModel, Field



class CommentBase(BaseModel):
    content: str = Field(min_length=2, max_length=100)
    post_id: int | None = None  # Явно указываем None как значение по умолчанию
    event_id: int | None = None  # Явно указываем None как значение по умолчанию


class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int


class CommentCreate(CommentBase):
    pass
