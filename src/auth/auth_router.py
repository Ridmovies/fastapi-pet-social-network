from fastapi import APIRouter
from fastapi_users import FastAPIUsers


from src.auth.backend import auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.user_manager import get_user_manager, google_oauth_client
from src.users.models import User

auth_router = APIRouter()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)


auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

auth_router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, "SECRET"),
    prefix="/auth/google",
    tags=["auth"],
)


current_user = fastapi_users.current_user()
current_user_or_guest = fastapi_users.current_user(optional=True)
