from fastapi import Response, status
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy, BearerTransport
from starlette.responses import JSONResponse

from config import JWT_SECRET


class CustomCookieTransport(CookieTransport):
    async def get_login_response(self, token: str) -> Response:
        response_content = {"detail": "Login successful"}
        response = JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
        return self._set_login_cookie(response, token)


cookie_transport = CustomCookieTransport(cookie_max_age=3600)

SECRET = JWT_SECRET


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
