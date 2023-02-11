from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fitter"
    PROJECT_VERSION: str = "0.1.0"
    SECRET_KEY: str = "secret"
    JWT_ISSUER: str = "fitter.com"
    JWT_ALGORITHM: str = "HS256"
    JWT_AUDIENCE: str = "fitter:auth"
    SESSION_TOKEN_EXPIRES_MINUTES: int = 480


settings = Settings()
