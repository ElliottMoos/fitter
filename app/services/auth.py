from typing import Type
import jwt
import logging
from pydantic import ValidationError

from passlib.context import CryptContext

from app.core.settings import settings
from app.models.fitter import FitterBase
from app.models.token import JWTCreds, JWTMeta, JWTPayload


logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"])


class AuthService:
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    def generate_session_token(
        self, fitter: Type[FitterBase], secret_key: str = settings.SECRET_KEY
    ) -> str:
        jwt_meta = JWTMeta()
        jwt_creds = JWTCreds(sub=fitter.id, username=fitter.username)
        jwt_payload = JWTPayload(**jwt_meta.dict(), **jwt_creds.dict())
        return jwt.encode(
            jwt_payload.dict(), secret_key, algorithm=settings.JWT_ALGORITHM
        )

    def get_fitter_username_from_token(
        self, token: str, secret_key: str = settings.SECRET_KEY
    ) -> str | None:
        try:
            decoded_token = jwt.decode(
                token,
                secret_key,
                audience=settings.JWT_AUDIENCE,
                algorithms=[settings.JWT_ALGORITHM],
            )
            payload = JWTPayload(**decoded_token)
            return payload.username
        except (jwt.PyJWTError, ValidationError) as e:
            logger.exception(e)
