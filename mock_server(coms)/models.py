from pydantic import BaseModel
from typing import Any
BaseModel.model_config['extra'] = 'allow'

class PostComputeOpsMgmtV1beta2ApprovalPoliciesRequest(BaseModel):
    name: str = None
    description: str = None
    policyData: dict = None

class PatchComputeOpsMgmtV1beta2ApprovalPoliciesPolicyIdRequest(BaseModel):
    name: str = None
    description: str = None
    policyData: dict = None

class PatchComputeOpsMgmtV1beta2ApprovalRequestsRequestIdRequest(BaseModel):
    approvalState: str = None
    requestRemarks: str = None

class PostComputeOpsMgmtV1beta2ApprovalRequestsRequestIdApproveRequest(BaseModel):
    approvalState: str = None
    remarks: str = None

class PostComputeOpsMgmtV1beta1ActivationKeysRequest(BaseModel):
    description: str = None

class PostComputeOpsMgmtV1beta1ActivationTokensRequest(BaseModel):
    deviceId: str = None
    durationMinutes: int = None

class PostComputeOpsMgmtV1beta1AhsFilesRequest(BaseModel):
    filename: str = None
    description: str = None

class PatchComputeOpsMgmtV1beta1AhsFilesIdRequest(BaseModel):
    description: str = None

class PostComputeOpsMgmtV1beta1ExternalServicesRequest(BaseModel):
    name: str = None
    endpoint: str = None
    apiKey: str = None

class PatchComputeOpsMgmtV1beta1ExternalServicesIdRequest(BaseModel):
    status: str = None

class PostComputeOpsMgmtV1beta1FiltersRequest(BaseModel):
    name: str = None
    criteria: dict = None

class PatchComputeOpsMgmtV1beta1FiltersIdRequest(BaseModel):
    name: str = None

class PostComputeOpsMgmtV1GroupsRequest(BaseModel):
    name: str = None

class PatchComputeOpsMgmtV1GroupsGroupIdRequest(BaseModel):
    name: str = None

class PostComputeOpsMgmtV1beta3GroupsRequest(BaseModel):
    name: str = None

class PatchComputeOpsMgmtV1beta3GroupsGroupIdRequest(BaseModel):
    name: str = None

class PostComputeOpsV1beta2GroupsRequest(BaseModel):
    name: str = None

class PatchComputeOpsV1beta2GroupsGroupIdRequest(BaseModel):
    name: str = None

class PostComputeOpsMgmtV1JobsRequest(BaseModel):
    name: str = None
    targetResource: dict = None

class PatchComputeOpsMgmtV1JobsIdRequest(BaseModel):
    status: str = None

class PostComputeOpsMgmtV1beta3JobsRequest(BaseModel):
    name: str = None

class PatchComputeOpsMgmtV1beta3JobsIdRequest(BaseModel):
    status: str = None

class PostComputeOpsMgmtV1beta2JobsRequest(BaseModel):
    name: str = None

class PatchComputeOpsMgmtV1beta2JobsIdRequest(BaseModel):
    status: str = None

class PostComputeOpsMgmtV1MetricsConfigurationsRequest(BaseModel):
    name: str = None
    enabled: bool = None
    intervalSeconds: int = None

class PatchComputeOpsMgmtV1MetricsConfigurationsIdRequest(BaseModel):
    enabled: bool = None

class PostComputeOpsMgmtV1beta1OneviewAppliancesRequest(BaseModel):
    name: str = None
    ipAddress: str = None
    username: str = None
    password: str = None

class PostComputeOpsMgmtV1beta2ReportsRequest(BaseModel):
    name: str = None
    reportType: str = None
    schedule: str = None

class PostComputeOpsMgmtV1beta2SchedulesRequest(BaseModel):
    name: str = None
    frequency: str = None
    target: dict = None

class PatchComputeOpsMgmtV1beta2SchedulesIdRequest(BaseModel):
    status: str = None

class PostComputeOpsMgmtV1beta1ServerLocationsLocationIdServersRequest(BaseModel):
    serverId: str = None

class DeleteComputeOpsMgmtV1beta1ServerLocationsLocationIdServersRequest(BaseModel):
    serverId: str = None

class PostComputeOpsV1beta1ServerSettingsRequest(BaseModel):
    name: str = None
    settings: dict = None

class PatchComputeOpsV1beta1ServerSettingsIdRequest(BaseModel):
    settings: dict = None

class PostComputeOpsMgmtV1SettingsRequest(BaseModel):
    name: str = None
    value: dict = None

class PatchComputeOpsMgmtV1SettingsIdRequest(BaseModel):
    value: bool = None

class PostComputeOpsMgmtV1beta1SettingsRequest(BaseModel):
    name: str = None
    value: str = None

class PatchComputeOpsMgmtV1beta1SettingsIdRequest(BaseModel):
    value: bool = None

class PatchComputeOpsMgmtV1ServersRequest(BaseModel):
    filter: str = None
    updates: dict = None

class PostComputeOpsMgmtV1ServersRequest(BaseModel):
    name: str = None
    ipAddress: str = None
    credentials: dict = None

class PatchComputeOpsMgmtV1ServersIdRequest(BaseModel):
    name: str = None

class PostComputeOpsMgmtV1ServersIdClearAlertRequest(BaseModel):
    alertId: str = None

class PatchComputeOpsMgmtV1beta2ServersRequest(BaseModel):
    filter: str = None
    updates: dict = None

class PostComputeOpsMgmtV1beta2ServersRequest(BaseModel):
    name: str = None
    ipAddress: str = None
    credentials: dict = None

class PatchComputeOpsMgmtV1beta2ServersIdRequest(BaseModel):
    name: str = None

class PostComputeOpsMgmtV1beta2ServersIdClearAlertRequest(BaseModel):
    alertId: str = None

class PostComputeOpsMgmtV1UserPreferencesRequest(BaseModel):
    emailNotifications: bool = None
    theme: str = None

class PutComputeOpsMgmtV1UserPreferencesIdRequest(BaseModel):
    emailNotifications: bool = None
    theme: str = None

class PostComputeOpsMgmtV1UserPreferencesSubscribeRequest(BaseModel):
    notificationType: str = None
    email: str = None

class PostComputeOpsMgmtV1UserPreferencesUnsubscribeRequest(BaseModel):
    notificationType: str = None
    email: str = None

class PostComputeOpsMgmtV1beta1UserPreferencesRequest(BaseModel):
    emailNotifications: bool = None

class PutComputeOpsMgmtV1beta1UserPreferencesIdRequest(BaseModel):
    emailNotifications: bool = None

class PostComputeOpsMgmtV1beta1WebhooksRequest(BaseModel):
    name: str = None
    url: str = None
    events: list = None

class PatchComputeOpsMgmtV1beta1WebhooksWebhookIdRequest(BaseModel):
    events: list = None

class PostComputeOpsMgmtV1GroupsGroupIdDevicesRequest(BaseModel):
    devices: list = None

class PostComputeOpsMgmtV1GroupsGroupIdDevicesUnassignRequest(BaseModel):
    devices: list = None


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


class ServerPowerActionRequest(BaseModel):
    action: str


class ServerFirmwareUpdateRequest(BaseModel):
    firmware_version: str



