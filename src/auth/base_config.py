import logging

from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy, BearerTransport

from config import JWT_SECRET

cookie_transport = CookieTransport(cookie_max_age=3600, cookie_secure=False)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

SECRET = JWT_SECRET


def get_jwt_strategy() -> JWTStrategy:
    logging.debug('Inside get_jwt_strategy')
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

