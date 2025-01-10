from pydantic import BaseModel, Field


class UserOutSchema(BaseModel):
    username: str
    hashed_password: str


class UserInSchema(BaseModel):
    username: str
    password: str

