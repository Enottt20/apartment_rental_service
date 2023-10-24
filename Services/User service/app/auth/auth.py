import uuid
from uuid import UUID
from fastapi_users import FastAPIUsers
from app.database.models import User
from app.manager import get_user_manager
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy, BearerTransport,
)


class AuthInitializer():
    def __init__(self):
        self.secret_phrase: str|None = None
        self.cookie_transport = None
        self.auth_backend = None

    def initializer(self, secret):
        self.secret_phrase = secret
        self.cookie_transport = BearerTransport(tokenUrl="auth/jwt/login")
        #self.cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600,cookie_secure=False)
        self.auth_backend = AuthenticationBackend(
            name="jwt",
            transport=self.cookie_transport,
            get_strategy=self.get_jwt_strategy,
        )

    def get_jwt_strategy(self) -> JWTStrategy:
        return JWTStrategy(secret=self.secret_phrase, lifetime_seconds=3600)

    def get_auth_backend(self) -> AuthenticationBackend:
        return self.auth_backend

    def get_fastapi_users(self) -> FastAPIUsers[User, UUID]:
        return FastAPIUsers[User, uuid.UUID](get_user_manager, [self.get_auth_backend()])

