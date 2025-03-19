from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from src.auth.strategy import get_database_strategy, get_jwt_strategy
from src.auth.transport import bearer_transport, cookie_transport



# database_strategy and bearer_transport
# auth_backend = AuthenticationBackend(
#     name="access_token_db",
#     transport=bearer_transport,
#     get_strategy=get_database_strategy,
# )

# jwt_strategy and cookie_transport
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
