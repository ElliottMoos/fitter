from typing import Type
import jwt
from pydantic import ValidationError

from passlib.context import CryptContext

from app.core.settings import settings
from app.models.fitter import FitterBase
from app.models.token import JWTCreds, JWTMeta, JWTPayload, Token

pwd_context = CryptContext(shemes=["bcrypt"], deprecated="auto")


class AuthService:
    def hash_password(self, *, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, *, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    def generate_session_token(
        self, *, fitter: Type[FitterBase], secret_key: str = settings.SECRET_KEY
    ) -> Token:
        jwt_meta = JWTMeta()
        jwt_creds = JWTCreds(sub=fitter.id, username=fitter.username)
        jwt_payload = JWTPayload(**jwt_meta.dict(), **jwt_creds.dict())
        session_token = Token(
            jwt.encode(
                jwt_payload.dict(), secret_key, algorithm=settings.JWT_ALGORITHM
            ),
            jwt_meta.exp,
        )
        return session_token

    def get_fitter_id_from_token(
        self, *, token: Token, secret_key: str = settings.SECRET_KEY
    ):
        try:
            decoded_token = jwt.decode(
                token.token, secret_key, algorithms=[settings.JWT_ALGORITHM]
            )
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise ValueError
        return payload.username
