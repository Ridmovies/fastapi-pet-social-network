from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str



class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool

