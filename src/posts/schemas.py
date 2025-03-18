from fastapi import Form
from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    content: str
    community_id: int = Field(default=1)  # Значение по умолчанию

    # @classmethod
    # def as_form(cls, content: str = Form(...)):
    #     return cls(content=content)


## Comments Schema


class CommentBase(BaseModel):
    content: str


class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int


class CommentCreate(CommentBase):
    pass
