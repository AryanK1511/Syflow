from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Syflow"
    VERSION: str = "0.0.1"
    LOG_LEVEL: str = "INFO"
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ISSUER: str
    AUTH0_ALGORITHMS: str = "RS256"

    class Config:
        env_file = ".env"


settings = Settings()
