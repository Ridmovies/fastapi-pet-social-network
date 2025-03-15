from typing import Annotated

from fastapi import Depends

from src.auth.auth_router import current_user
from src.database import User


UserDep = Annotated[User, Depends(current_user)]