from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from app.core.settings import settings


def get_iat():
    return datetime.timestamp(datetime.now()) - 100


def get_exp():
    return datetime.timestamp(
        datetime.now() + timedelta(minutes=settings.SESSION_TOKEN_EXPIRES_MINUTES)
    )


class JWTMeta(BaseModel):
    iss: str = settings.JWT_ISSUER
    aud: str = settings.JWT_AUDIENCE
    iat: float = Field(default_factory=get_iat)
    exp: float = Field(default_factory=get_exp)


class JWTCreds(BaseModel):
    sub: int
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    pass
