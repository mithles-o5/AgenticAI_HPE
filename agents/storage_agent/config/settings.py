"""Storage Agent settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    SERVICE_NAME: str = "storage-agent"
    SERVICE_PORT: int = 8007

    CAPABILITY_REGISTRY_URL: str = "http://localhost:8020"
    CRED_VAULT_URL: str = "http://cred-vault:8200"
    SERVICE_TOKEN: str = ""

    RETRY_ATTEMPTS: int = 3
    RETRY_WAIT_SECONDS: float = 1.0

    # Anomaly thresholds
    CAPACITY_WARNING_PCT: float = 75.0
    CAPACITY_CRITICAL_PCT: float = 90.0
    IOPS_WARNING_THRESHOLD: int = 50000
    IOPS_CRITICAL_THRESHOLD: int = 80000
    LATENCY_WARNING_MS: float = 10.0
    LATENCY_CRITICAL_MS: float = 50.0

    # Poll handler
    POLL_INTERVAL_SECONDS: int = 300    # every 5 minutes


settings = Settings()
