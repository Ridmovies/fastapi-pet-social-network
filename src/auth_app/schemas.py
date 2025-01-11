from pydantic import BaseModel, Field


class UserOutSchema(BaseModel):
    id: int
    username: str

class UserInSchema(BaseModel):
    username: str
    password: str

