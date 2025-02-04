from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str

class UserOutSchema(UserSchema):
    id: int

class UserInSchema(UserSchema):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None