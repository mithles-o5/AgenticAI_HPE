from pydantic import BaseModel
from typing import Any

class PostRestLoginSessionsRequest(BaseModel):
    userName: str = None
    password: str = None

class PostRestLoginSessionsAuthTokenRequest(BaseModel):
    sessionToken: str = None
    scopeUris: list = None

class PostRestServerHardwareRequest(BaseModel):
    hostname: str = None
    username: str = None
    password: str = None
    force: bool = None
    licensingIntent: str = None
    configurationState: str = None
    initialScopeUris: list = None

class PostRestServerHardwareDiscoveryRequest(BaseModel):
    mpHostsAndRanges: list = None
    username: str = None
    password: str = None
    licensingIntent: str = None
    configurationState: str = None
    initialScopeUris: list = None

class PostRestServerHardwareFirmwareComplianceRequest(BaseModel):
    firmwareBaselineId: str = None
    serverUUID: str = None

class PutRestServerHardwareIdEnvironmentalconfigurationRequest(BaseModel):
    calibratedMaxPower: int = None

