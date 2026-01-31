"""
Application configuration using Pydantic Settings.

Loads configuration from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sis_manager"

    # API Keys
    claude_api_key: str = ""

    # Application
    debug: bool = False
    app_name: str = "SISStateReportingManager"
    api_prefix: str = "/api"

    # Security
    secret_key: str = "change-this-in-production"
    password: str = "admin"  # Simple password auth for internal tool

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]


# Global settings instance
settings = Settings()
