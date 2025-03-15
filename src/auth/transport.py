from fastapi_users.authentication import BearerTransport
from fastapi_users.authentication import CookieTransport

# bearer_transport
cookie_transport = CookieTransport(cookie_max_age=3600)


# bearer_transport
bearer_transport = BearerTransport(tokenUrl="api/v1/auth/jwt/login")
