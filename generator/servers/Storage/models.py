from pydantic import BaseModel
from typing import Any

class PatchDataServicesV1beta1DualAuthOperationsIdRequest(BaseModel):
    state: str = None
    checkedByEmail: str = None
    checkedByUri: str = None
    checkedAt: str = None

class PatchDataServicesV1beta1IssuesIdRequest(BaseModel):
    state: str = None
    resolutionDetails: str = None

class PostDataServicesV1beta1SecretsRequest(BaseModel):
    service: str = None
    name: str = None
    secret: dict = None

class PatchDataServicesV1beta1SecretsIdRequest(BaseModel):
    secret: dict = None
    description: str = None

class PatchDataServicesV1beta1SettingsIdRequest(BaseModel):
    value: bool = None

class PostDataServicesV1beta1SoftwareReleasesIdDownloadRequest(BaseModel):
    file: str = None

