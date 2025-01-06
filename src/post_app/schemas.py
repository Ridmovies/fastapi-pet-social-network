from pydantic import BaseModel


class PostSchema(BaseModel):
    content: str