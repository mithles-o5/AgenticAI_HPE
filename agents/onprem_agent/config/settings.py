import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8008
    HOST: str = "0.0.0.0"
    ONEVIEW_URL: str = "http://localhost:8000"
    COMOPS_URL: str = "http://localhost:8001"
    CRED_VAULT_URL: str = "http://localhost:8002"
    SERVICE_TOKEN: str = "mock-service-token"
    CAPABILITY_REGISTRY_URL: str = "http://localhost:8020"
    CMDB_URL: str = "http://localhost:8004"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
