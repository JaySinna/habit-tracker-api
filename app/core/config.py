from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Habit Tracker API"
    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALGO: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    DATABASE_URL: str = "sqlite:///./dev.db"  # swap to Postgres in prod

    class Config:
        env_file = ".env"


settings = Settings()
