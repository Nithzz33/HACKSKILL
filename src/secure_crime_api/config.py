from __future__ import annotations

import secrets
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SECURE_API_",
        extra="ignore",
    )

    environment: str = "development"
    database_path: Path = Path("data/secure_system.db")
    jwt_secret: str = Field(default_factory=lambda: secrets.token_urlsafe(64))
    jwt_issuer: str = "secure-crime-api"
    token_ttl_minutes: int = 30
    rate_limit_per_minute: int = 120
    max_request_bytes: int = 26_214_400
    allowed_hosts: str = "localhost,127.0.0.1,testserver"
    cors_origins: str = ""
    bootstrap_username: str | None = None
    bootstrap_password: str | None = None
    bootstrap_full_name: str = "Bootstrap Administrator"
    bootstrap_role: str = "super_admin"
    bootstrap_district: str = "state"
    demo_mode: bool = False
    demo_password: str = "admin123"

    @field_validator("jwt_secret")
    @classmethod
    def validate_jwt_secret(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("SECURE_API_JWT_SECRET must be at least 32 characters")
        return value

    @field_validator("token_ttl_minutes", "rate_limit_per_minute", "max_request_bytes")
    @classmethod
    def validate_positive_ints(cls, value: int) -> int:
        if value < 1:
            raise ValueError("security limits must be positive")
        return value

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def allowed_host_list(self) -> list[str]:
        return [item.strip() for item in self.allowed_hosts.split(",") if item.strip()]

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if bool(settings.bootstrap_username) != bool(settings.bootstrap_password):
        raise ValueError("bootstrap username and password must be provided together")
    return settings
