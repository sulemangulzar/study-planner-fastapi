from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/studyplanner"
    )
    JWT_SECRET: str = "change_me"
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file="./.env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()  # type: ignore
