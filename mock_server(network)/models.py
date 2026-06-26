from pydantic import BaseModel
BaseModel.model_config['extra'] = 'allow'

class DeviceSchema(BaseModel):
    id: str = None
    serial_number: str = None
    ip_address: str = None
    fqdn: str = None
    management_source: str = None
    source_host: str = None
    source_device_id: str = None
    device_type: str = None


class NetworkVlanRequest(BaseModel):
    vlan_id: int
    name: str


class NetworkPortStatusRequest(BaseModel):
    status: str


class ArubaVlanRequest(BaseModel):
    vlan_id: int
    name: str = None


class ArubaPortStatusRequest(BaseModel):
    status: str

class Aruba_generateaccesstoken_Request(BaseModel):
    grant_type: str = None
    client_id: str = None
    client_secret: str = None

class Aruba_placedevicesonfloorv1_Request(BaseModel):
    devicesOnFloor: list = None

class Aruba_removedevicesonfloorv1_Request(BaseModel):
    removeDevices: dict = None

class Aruba_changedeviceassignmentv1_Request(BaseModel):
    deviceAssignment: dict = None

class Aruba_placeplanneddevicesonfloorv1_Request(BaseModel):
    devicesOnFloor: list = None

class Aruba_removeplanneddevicesonfloorv1_Request(BaseModel):
    removeDevices: dict = None

class Aruba_createfloorv1_Request(BaseModel):
    file: str = None
    buildingId: str = None
    buildingName: str = None
    ceilingHeight: float = None
    name: str = None
    ordinal: float = None
    buildingAddress: dict = None
    buildingType: str = None
    buildingCoordinates: list = None

class Aruba_updatefloormapv1_Request(BaseModel):
    floorMapInput: dict = None

class Aruba_scalefloormapv1_Request(BaseModel):
    floorMapScaleInput: dict = None

class Aruba_replaceimagev1_Request(BaseModel):
    file: str = None

class Aruba_updatebuildingv1_Request(BaseModel):
    buildingInput: dict = None

class Aruba_importfloorsv1_Request(BaseModel):
    file: str = None
    importLevel: str = None
    siteName: str = None

class Aruba_createwalltypesv1_Request(BaseModel):
    items: list = None

class Aruba_updatewalltypesv1_Request(BaseModel):
    items: list = None

class Aruba_deletewalltypesv1_Request(BaseModel):
    items: list = None

class Aruba_createwallsv1_Request(BaseModel):
    items: list = None

class Aruba_updatewallsv1_Request(BaseModel):
    items: list = None

class Aruba_deletewallsv1_Request(BaseModel):
    items: list = None

class Aruba_createzonesv1_Request(BaseModel):
    items: list = None

class Aruba_updatezonesv1_Request(BaseModel):
    items: list = None

class Aruba_deletezonesv1_Request(BaseModel):
    items: list = None

class Aruba_clearalerts_Request(BaseModel):
    keys: list = None
    reason: str = None
    notes: str = None

class Aruba_deferalerts_Request(BaseModel):
    keys: list = None
    deferUntil: str = None

class Aruba_setactivealerts_Request(BaseModel):
    keys: list = None

class Aruba_setpriorityalerts_Request(BaseModel):
    keys: list = None
    priority: str = None

class Aruba_updateuserreport_Request(BaseModel):
    name: str = None
    email: dict = None

class Aruba_downloadreportlink_Request(BaseModel):
    exportType: str = None

class Aruba_putdeviceadminlocationv1_Request(BaseModel):
    cartesianCoordinates: dict = None
    center: dict = None
    lciUncertainty: dict = None
    altitude: dict = None

class Aruba_startaprangingscanv1_Request(BaseModel):
    scanStartTime: str = None

class Aruba_updateassettagdatabyassettagidv1_Request(BaseModel):
    name: str = None
    customId: str = None
    notes: str = None
    labels: list = None

class Aruba_createassettagdatabyassettagidv1_Request(BaseModel):
    name: str = None
    customId: str = None
    notes: str = None
    labels: list = None

class Aruba_createwebhookv1_Request(BaseModel):
    input: str = None

class Aruba_updatewebhookv1_Request(BaseModel):
    input: str = None

class Aruba_patchwebhookv1_Request(BaseModel):
    input: str = None

class Aruba_initiatepvospingv1_Request(BaseModel):
    destination: str = None
    useIpv6: bool = None
    packetSize: int = None
    count: int = None
    loopbackPort: int = None
    vlan: int = None
    ipAddress: str = None
    includeRawOutput: bool = None

class Aruba_initiatepvostraceroutev1_Request(BaseModel):
    destination: str = None
    sourceInterface: str = None
    loopbackPort: int = None
    vlan: int = None
    ipAddress: str = None
    includeRawOutput: bool = None

class Aruba_initiatepvospoebouncev1_Request(BaseModel):
    ports: list = None

class Aruba_initiatepvosportbouncev1_Request(BaseModel):
    ports: list = None

class Aruba_initiatepvoscabletestv1_Request(BaseModel):
    ports: list = None

class Aruba_runaossshowcommandsv1_Request(BaseModel):
    commands: list = None

class Aruba_initiateappingv1_Request(BaseModel):
    destination: str = None
    packetSize: int = None
    count: int = None
    interfacePort: str = None
    vlan: int = None
    role: str = None
    includeRawOutput: bool = None

class Aruba_initiateaptraceroutev1_Request(BaseModel):
    destination: str = None
    sourceInterface: str = None
    includeRawOutput: bool = None

class Aruba_initiateapspeedtestv1_Request(BaseModel):
    iperfServerAddress: str = None
    protocol: str = None
    serverPort: int = None
    bandwidth: int = None
    includeReverse: bool = None
    secondsToMeasure: int = None
    parallel: int = None
    omit: int = None
    windowSize: int = None

class Aruba_initiateaphttpv1_Request(BaseModel):
    url: str = None
    timeout: int = None

class Aruba_initiateaphttpsv1_Request(BaseModel):
    url: str = None
    timeout: int = None

class Aruba_initiateaptcpv1_Request(BaseModel):
    host: str = None
    port: int = None
    timeout: int = None

class Aruba_initiateapnslookupv1_Request(BaseModel):
    host: str = None
    dnsServer: str = None

class Aruba_initiateapaaav1_Request(BaseModel):
    serverName: str = None
    username: str = None
    password: str = None

class Aruba_runapshowcommandsv1_Request(BaseModel):
    commands: list = None

class Aruba_disconnectuserbymacapv1_Request(BaseModel):
    userMacAddress: str = None

class Aruba_disconnectuserbynetworkapv1_Request(BaseModel):
    networkName: str = None

class Aruba_initiatecxpingv1_Request(BaseModel):
    destination: str = None
    useIpv6: bool = None
    packetSize: int = None
    count: int = None
    useManagementInterface: bool = None
    vrfName: str = None
    includeRawOutput: bool = None

class Aruba_initiatecxtraceroutev1_Request(BaseModel):
    destination: str = None
    useIpv6: bool = None
    useManagementInterface: bool = None
    vrfName: str = None
    includeRawOutput: bool = None

class Aruba_initiatecxpoebouncev1_Request(BaseModel):
    ports: list = None

class Aruba_initiatecxportbouncev1_Request(BaseModel):
    ports: list = None

class Aruba_initiatecxcabletestv1_Request(BaseModel):
    ports: list = None

class Aruba_initiatecxhttpv1_Request(BaseModel):
    protocol: str = None
    destination: str = None
    vrfName: str = None
    sourceInterface: str = None
    sourcePort: int = None
    nameServer: str = None

class Aruba_initiatecxaaav1_Request(BaseModel):
    authMethodType: str = None
    radiusServerIp: str = None
    radiusServerPort: int = None
    vrfName: str = None
    username: str = None
    password: str = None

class Aruba_runcxshowcommandsv1_Request(BaseModel):
    commands: list = None

class Aruba_initiategwpingv1_Request(BaseModel):
    destination: str = None
    packetSize: int = None
    count: int = None
    ttl: int = None
    dscp: int = None
    dontFragmentFlag: bool = None
    sourceInterface: str = None
    vlan: float = None
    useIpv6: bool = None
    includeRawOutput: bool = None

class Aruba_rungatewaypingsweepv1_Request(BaseModel):
    destination: str = None
    count: int = None
    startPacketSize: int = None
    endPacketSize: int = None
    sweepInterval: int = None

class Aruba_initiategwtraceroutev1_Request(BaseModel):
    destination: str = None
    vlanIp: str = None
    includeRawOutput: bool = None

class Aruba_initiategwpoebouncev1_Request(BaseModel):
    ports: list = None

class Aruba_initiategwportbouncev1_Request(BaseModel):
    ports: list = None

class Aruba_initiategwiperfv1_Request(BaseModel):
    iperfServerAddress: str = None
    port: int = None
    duration: int = None
    parallel: int = None
    omit: int = None
    includeReverse: bool = None
    vlanInterface: str = None
    protocol: str = None
    includeRawOutput: bool = None

class Aruba_initiategwhttpv1_Request(BaseModel):
    url: str = None
    count: int = None
    interval: int = None
    includeRawOutput: bool = None

class Aruba_initiategwhttpsv1_Request(BaseModel):
    url: str = None
    count: int = None
    interval: int = None
    includeRawOutput: bool = None

class Aruba_rungwshowcommandsv1_Request(BaseModel):
    commands: list = None

class Aruba_disconnectclientbymacgwv1_Request(BaseModel):
    clientMacAddress: str = None
