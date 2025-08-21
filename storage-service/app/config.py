from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MinIO Settings
    MINIO_ENDPOINT: str = "http://minio:9000"
    MINIO_ACCESS_KEY: str = "minio"
    MINIO_SECRET_KEY: str = "minio123"
    PRESIGN_TTL_SECONDS: int = 600

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://app:app@postgres:5432/ossdb"

    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"

    # Auth Service dependency (for token validation)
    JWT_SECRET: str = "change_me_in_production"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
