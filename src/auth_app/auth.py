from passlib.context import CryptContext

# from src.auth_app.service import AuthService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password):
    """Создает хеш пользовательского пароля."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Верифицирует пользовательский пароль."""
    return pwd_context.verify(plain_password, hashed_password)


# async def authenticate_user(username: str, password: str):
#     """Аутентифицирует пользователя."""
#     user = await AuthService.get_one_or_none(username=username)
#     if user:
#         return user
#
#     if user and verify_password(password, user.hashed_password):
#         return user
