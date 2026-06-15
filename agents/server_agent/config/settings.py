from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Service identity
    AGENT_NAME: str = "server-agent"
    AGENT_VERSION: str = "1.0.0"
    PORT: int = 8009

    # External services
    CAPABILITY_REGISTRY_URL: str = "http://localhost:8020"
    CRED_VAULT_URL: str = "http://localhost:8200"
    SERVICE_TOKEN: str = "mock-service-token"
    CMDB_URL: str = "http://localhost:8004"

    # Polling
    POLL_ENABLED: bool = True
    POLL_INTERVAL_SECONDS: int = 120
    POLL_SERVER_LIST_SOURCE: str = "cmdb"   # "cmdb" or "static"

    # Anomaly thresholds
    CPU_WARNING_THRESHOLD: float = 80.0
    MEMORY_WARNING_THRESHOLD: float = 85.0
    TEMPERATURE_WARNING_THRESHOLD: float = 75.0   # Celsius
    TEMPERATURE_CRITICAL_THRESHOLD: float = 90.0
    FAN_FAILURE_STATUS_VALUES: str = "Failed,CriticalFailure,Critical"
    PSU_FAILURE_STATUS_VALUES: str = "Failed,CriticalFailure,Critical"
    DISK_PREDICTIVE_FAILURE_FLAG: bool = True
    EVENT_LOG_CRITICAL_SEVERITIES: str = "Critical,Fatal"

    # Retry
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_MULTIPLIER: float = 1.5
    REDFISH_TIMEOUT_SECONDS: int = 15

    LOG_LEVEL: str = "INFO"

settings = Settings()
