from typing import List, Optional
from pydantic import BaseSettings, validator, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fittr"
    PROJECT_VERSION: str = "0.1.0"
    SECRET_KEY: str = "secret"
    JWT_ISSUER: str = "fittr.com"
    JWT_ALGORITHM: str = "HS256"
    JWT_AUDIENCE: str = "fittr:auth"
    SESSION_TOKEN_EXPIRES_MINUTES: int = 480
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "db"
    POSTGRES_DB: str = "app"
    DB_URL: Optional[str]

    @validator("DB_URL", pre=True)
    def build_db_url(cls, v, values):
        if isinstance(v, str):
            return v
        return (
            "postgresql+psycopg2://"
            + f"{values.get('POSTGRES_USER')}"
            + ":"
            + f"{values.get('POSTGRES_PASSWORD')}"
            + "@"
            + f"{values.get('POSTGRES_SERVER')}"
            + "/"
            f"{values.get('POSTGRES_DB')}"
        )

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
