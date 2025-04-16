from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Load .env file located in the project root
    model_config = SettingsConfigDict(env_file='../../.env', env_file_encoding='utf-8', extra='ignore')

    DATABASE_URL: str = "postgresql+asyncpg://user:password@host:port/dbname" # Default if not in .env
    SECRET_KEY: str = "default_secret_key"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Add other configurations here as needed
    # e.g., API_V1_STR: str = "/api/v1"


settings = Settings() 