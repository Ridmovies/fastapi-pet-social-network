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


class CannotUnfollowSelfError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Нельзя отписаться от самого себя")

class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Пользователь для отписки не найден")

class NotFollowingError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Вы не подписаны на этого пользователя")

class DatabaseError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Ошибка базы данных")

class InternalServerError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Внутренняя ошибка сервера")