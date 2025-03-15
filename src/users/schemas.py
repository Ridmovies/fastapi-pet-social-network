# from pydantic import BaseModel, Field, field_validator
#
#
# class UserSchema(BaseModel):
#     username: str = Field(
#         min_length=3,
#         max_length=16,
#         pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$",  # Используйте `pattern` вместо `regex`
#     )
#
#     @field_validator("username")
#     def username_must_be_lowercase(cls, value):
#         if value != value.lower():
#             raise ValueError("Username must be lowercase")
#         return value
#
#
# class UserOutSchema(UserSchema):
#     id: int
#
# class UserInSchema(UserSchema):
#     password: str = Field(
#         min_length=6,
#         max_length=16)
#
#
# class TokenSchema(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     username: str | None = None
