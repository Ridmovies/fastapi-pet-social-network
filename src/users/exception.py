from fastapi import HTTPException
from starlette import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

user_already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User Already Exists.",
)