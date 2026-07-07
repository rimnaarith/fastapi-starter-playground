from os import getenv

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = getenv("ENV_FILE", ".env")

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    STORAGE_DRIVER: str = "local"
    UPLOAD_DIR: str = "uploads"
    S3_BUCKET: str = ""
    S3_REGION: str = ""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


settings = Settings()