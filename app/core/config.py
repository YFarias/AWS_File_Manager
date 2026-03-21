from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(default="AWS_File_manager", validation_alias="APP_NAME")
    app_version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    environment: str = Field(default="development", validation_alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    database_url: str = Field(
        default="sqlite+aiosqlite:///./aws_file_manager.db",
        validation_alias="DATABASE_URL",
    )
    sqlalchemy_echo: bool = Field(default=False, validation_alias="SQLALCHEMY_ECHO")

    aws_access_key_id: str = Field(default="", validation_alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(default="", validation_alias="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(default="us-east-1", validation_alias="AWS_REGION")
    aws_s3_bucket: str = Field(default="", validation_alias="AWS_S3_BUCKET")
    s3_presigned_url_expires_in: int = Field(
        default=900,
        validation_alias="S3_PRESIGNED_URL_EXPIRES_IN",
    )

    jwt_secret_key: str = Field(default="change-me", validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    jwt_audience: str | None = Field(default=None, validation_alias="JWT_AUDIENCE")
    jwt_issuer: str | None = Field(default=None, validation_alias="JWT_ISSUER")

    max_upload_size_bytes: int = Field(
        default=10 * 1024 * 1024,
        validation_alias="MAX_UPLOAD_SIZE_BYTES",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
