from os import getenv

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = getenv("ENV_FILE", ".env")

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


settings = Settings()