from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    SESSION_TOKEN_EXPIRES_MINUTES: int = 480


settings = Settings()
