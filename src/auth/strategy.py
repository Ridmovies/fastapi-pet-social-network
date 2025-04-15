from fastapi import Depends
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users.authentication import JWTStrategy

from src.auth.access_token import AccessToken, get_access_token_db
from src.config import settings

SECRET = settings.SECRET_KEY
lifetime_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=lifetime_seconds)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=lifetime_seconds)
