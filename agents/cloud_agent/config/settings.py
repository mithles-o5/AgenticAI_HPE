"""Cloud Agent settings — all values driven from environment variables."""

from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Service identity
    SERVICE_NAME: str = "cloud-agent"
    SERVICE_PORT: int = 8005

    # Capability Registry — agents POST their oasf_record.json here on startup
    CAPABILITY_REGISTRY_URL: str = "http://localhost:8020"

    # Credential Vault — agents fetch secrets from here at task-execution time
    CRED_VAULT_URL: str = "http://cred-vault:8200"
    SERVICE_TOKEN: str = ""       # Injected at runtime by the deployment platform

    # MCP Orchestrator callback (optional — for push-back results)
    MCP_ORCHESTRATOR_URL: Optional[str] = None

    # Retry configuration (tenacity)
    RETRY_ATTEMPTS: int = 3
    RETRY_WAIT_SECONDS: float = 1.0

    # Anomaly detection thresholds (generic, provider-agnostic)
    CPU_WARNING_THRESHOLD: float = 75.0
    CPU_CRITICAL_THRESHOLD: float = 90.0
    MEMORY_WARNING_THRESHOLD: float = 80.0
    MEMORY_CRITICAL_THRESHOLD: float = 95.0
    ERROR_RATE_WARNING_THRESHOLD: float = 0.05    # 5%
    ERROR_RATE_CRITICAL_THRESHOLD: float = 0.15   # 15%


settings = Settings()
