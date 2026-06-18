from pydantic import BaseModel
from typing import Any
BaseModel.model_config['extra'] = 'allow'

class PostRestLoginSessionsRequest(BaseModel):
    userName: str = None
    password: str = None

class PostRestLoginSessionsAuthTokenRequest(BaseModel):
    sessionID: str = None
    enabledPermissions: list = None

class PostRestCertificatesClientRabbitmqRequest(BaseModel):
    type: str = None
    commonName: str = None
    alternativeNames: list = None

class PostRestEthernetNetworksBulkRequest(BaseModel):
    type: str = None
    namePrefix: str = None
    vlanIdRange: str = None
    purpose: str = None
    privateNetwork: bool = None
    connectionTemplateUri: str = None
    ipv6SubnetUri: str = None
    subnetUri: str = None
    initialScopeUris: list = None
    smartLink: bool = None

class PutRestStorageVolumesIdRequest(BaseModel):
    name: str = None
    description: str = None
    capacityBytes: int = None
    provisioningType: str = None
    isShareable: bool = None

class PostRestRackManagersRequest(BaseModel):
    hostname: str = None
    username: str = None
    password: str = None
    force: bool = None
    fwBaselineUri: str = None
    fwExcludeNpars: bool = None
    fwReinstall: bool = None
    initialScopeUris: list = None
    licensingIntent: str = None
    name: str = None

class PostRestServerHardwareRequest(BaseModel):
    hostname: str = None
    username: str = None
    password: str = None
    force: bool = None
    licensingIntent: str = None
    configurationState: str = None
    initialScopeUris: list = None
    name: str = None

class PostRestServerHardwareDiscoveryRequest(BaseModel):
    mpHostsAndRanges: list = None
    username: str = None
    password: str = None
    licensingIntent: str = None
    configurationState: str = None
    initialScopeUris: list = None
    force: bool = None

class PostRestServerHardwareFirmwareComplianceRequest(BaseModel):
    firmwareBaselineId: str = None
    serverUUID: str = None


class CustomServerCreateRequest(BaseModel):
    name: str
    status: str = "OK"
    temperature: float = 25.0
    powerState: str = "On"
    serialNumber: str = None
    firmwareVersion: str = None
    memoryGiB: int = 128
    cpuCores: int = 32


class CustomServerUpdateRequest(BaseModel):
    name: str = None
    status: str = None
    temperature: float = None
    powerState: str = None
    serialNumber: str = None
    firmwareVersion: str = None
    memoryGiB: int = None
    cpuCores: int = None


class CustomSwitchCreateRequest(BaseModel):
    name: str
    status: str = "OK"
    temperature: float = 25.0
    powerState: str = "On"
    serialNumber: str = None
    firmwareVersion: str = None
    model: str = None
    ipAddress: str = None
    portCount: int = 24


class CustomSwitchUpdateRequest(BaseModel):
    name: str = None
    status: str = None
    temperature: float = None
    powerState: str = None
    serialNumber: str = None
    firmwareVersion: str = None
    model: str = None
    ipAddress: str = None
    portCount: int = None
