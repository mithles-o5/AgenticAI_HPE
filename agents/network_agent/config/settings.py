"""Network Agent settings — all values driven from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    SERVICE_NAME: str = "network-agent"
    SERVICE_PORT: int = 8006

    CAPABILITY_REGISTRY_URL: str = "http://localhost:8020"
    CRED_VAULT_URL: str = "http://cred-vault:8200"
    SERVICE_TOKEN: str = ""

    RETRY_ATTEMPTS: int = 3
    RETRY_WAIT_SECONDS: float = 1.0

    # Anomaly thresholds
    INTERFACE_UTIL_WARNING_PCT: float = 70.0
    INTERFACE_UTIL_CRITICAL_PCT: float = 90.0
    ERROR_RATE_WARNING_THRESHOLD: float = 0.01    # 1% of packets
    ERROR_RATE_CRITICAL_THRESHOLD: float = 0.05   # 5%
    BGP_SESSION_DOWN_CRITICAL: bool = True


settings = Settings()
