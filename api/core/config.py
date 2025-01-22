# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ISSUER: str
    AUTH0_ALGORITHMS: str = "RS256"

    class Config:
        env_file = ".env"


settings = Settings()
