from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from app.core.settings import settings


def get_iat():
    return datetime.timestamp(datetime.utcnow())


def get_exp():
    return datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=settings.SESSION_TOKEN_EXPIRES_MINUTES)
    )


class JWTMeta(BaseModel):
    iss: str = "fitter.com"
    aud: str = "fitter:auth"
    iat: float = Field(default_factory=get_iat)
    exp: float = Field(default_factory=get_exp)


class JWTCreds(BaseModel):
    sub: int
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    pass


class Token(BaseModel):
    token: str
    expires: int

    @property
    def expires_in(self) -> int:
        return self.expires - int(datetime.now().timestamp())

    @property
    def expires_date(self) -> datetime:
        return datetime.fromtimestamp(self.expires)
