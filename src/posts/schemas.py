from fastapi import Form
from pydantic import BaseModel


class PostSchema(BaseModel):
    content: str

    @classmethod
    def as_form(cls, content: str = Form(...)):
        return cls(content=content)
