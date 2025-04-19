from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import validator, AnyHttpUrl, Field
from typing import List, Union, Set

class Settings(BaseSettings):
    # Pydantic will automatically look for a .env file in the current or parent directories
    # Ensure your .env file is in the project root or backend directory when running.
    model_config = SettingsConfigDict(env_file_encoding='utf-8', extra='ignore')

    # --- Core Settings --- Required in environment ---
    SECRET_KEY: str = Field(..., description="Secret key for JWT token generation")
    DATABASE_URL: str = Field(..., description="Async database connection string (e.g., postgresql+asyncpg://user:pass@host:port/db)")

    # --- Database --- Optional ---
    DB_ECHO_LOG: bool = Field(default=False, description="Set to True to log SQL statements")

    # --- Celery --- Required if using background tasks ---
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0", description="URL for the Celery message broker (Redis)")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0", description="URL for the Celery result backend (Redis)")

    # --- CORS --- Defaults are for local development. Override with env var. ---
    # Environment variable should be a comma-separated string, e.g., "http://localhost:5173,http://127.0.0.1:5173,https://your-frontend.com"
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = Field(default="http://localhost:5173,http://127.0.0.1:5173", description="Allowed origins for CORS requests")

    # --- File Conversion Settings --- Optional defaults, override in .env ---
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024, description="Maximum file upload size in bytes (Default: 10MB)")
    # Comma-separated string in .env, e.g., "image/jpeg,image/png,application/pdf"
    ALLOWED_CONTENT_TYPES: str = Field(default="image/jpeg,image/png,application/pdf,text/plain", description="Allowed MIME types for file uploads")
    # Comma-separated string in .env, e.g., "pdf,docx,txt"
    SUPPORTED_OUTPUT_FORMATS: str = Field(default="pdf,png,jpg,txt", description="Supported output formats for conversion")

    # --- Parsed Settings (available after initialization) ---
    parsed_allowed_content_types: Set[str] = set()
    parsed_supported_output_formats: Set[str] = set()
    parsed_backend_cors_origins: List[AnyHttpUrl] = []

    @validator("parsed_backend_cors_origins", pre=True, always=True)
    def assemble_cors_origins(cls, v, values) -> List[AnyHttpUrl]:
        origins_str_or_list = values.get("BACKEND_CORS_ORIGINS", "")
        if isinstance(origins_str_or_list, str):
            # Parse comma-separated string
            return [item.strip() for item in origins_str_or_list.split(",") if item.strip()]
        elif isinstance(origins_str_or_list, list):
            return origins_str_or_list
        raise ValueError(f"Invalid BACKEND_CORS_ORIGINS value: {origins_str_or_list}")

    @validator("parsed_allowed_content_types", pre=True, always=True)
    def assemble_allowed_content_types(cls, v, values) -> Set[str]:
        content_types_str = values.get("ALLOWED_CONTENT_TYPES", "")
        return {item.strip().lower() for item in content_types_str.split(",") if item.strip()}

    @validator("parsed_supported_output_formats", pre=True, always=True)
    def assemble_supported_output_formats(cls, v, values) -> Set[str]:
        formats_str = values.get("SUPPORTED_OUTPUT_FORMATS", "")
        return {item.strip().lower() for item in formats_str.split(",") if item.strip()}

    # --- Storage Directories --- Optional defaults, ensure they exist or are created ---
    TEMP_DIR: str = Field(default="./temp_uploads", description="Directory for temporary file uploads relative to backend root.")
    CONVERTED_DIR: str = Field(default="./converted_files", description="Directory to store successfully converted files relative to backend root.")

    # --- Other potential configurations ---
    # PROJECT_NAME: str = "Universal File Converter"
    # API_V1_STR: str = "/api/v1"
    # TEMP_DIR: str = "/tmp/file_converter" # Example for configurable temp dir


settings = Settings()

# Example usage check:
# print(f"Secret Key Loaded: {'Yes' if settings.SECRET_KEY else 'No'}")
# print(f"Database URL: {settings.DATABASE_URL}")
# print(f"Allowed Origins: {settings.parsed_backend_cors_origins}")
# print(f"Max Upload Size: {settings.MAX_UPLOAD_SIZE}")
# print(f"Allowed Types: {settings.parsed_allowed_content_types}")
# print(f"Output Formats: {settings.parsed_supported_output_formats}") 