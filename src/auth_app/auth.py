from datetime import timedelta, timezone, datetime

from passlib.context import CryptContext
import jwt

from src.auth_app.service import AuthService
from src.config import settings

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password):
    """Создает хеш пользовательского пароля."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Верифицирует пользовательский пароль."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(username: str, password: str):
    """Аутентифицирует пользователя."""
    user = await AuthService.get_one_or_none(username=username)
    if user is None:
        return {"message": "user not found"}
    if user and verify_password(password, user.hashed_password):
        return user