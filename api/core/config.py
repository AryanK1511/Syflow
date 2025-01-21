# app/core/config.py
from pydantic import BaseSettings, Field
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Syflow"
    DEBUG: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Add other configurations as needed

    class Config:
        env_file = ".env"

settings = Settings()
