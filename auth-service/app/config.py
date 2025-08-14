from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # JWT
    JWT_SECRET: str = "change_me_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://app:app@postgres:5432/ossdb"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # Default Admin User
    DEFAULT_ADMIN_EMAIL: str = "admin@demo.gov"
    DEFAULT_ADMIN_PASSWORD: str = "Admin!234"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
