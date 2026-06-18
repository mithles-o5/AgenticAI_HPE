from pydantic import BaseModel
from typing import Any
BaseModel.model_config['extra'] = 'allow'

class HostgroupcreateRequest(BaseModel):
    comment: str = None
    hostIds: list = None
    hostsToCreate: list = None
    name: str = None
    userCreated: bool = None

class HostgroupupdatebyidRequest(BaseModel):
    hostProximityValues: list = None
    hostsToCreate: list = None
    name: str = None
    removedHosts: list = None
    updatedHosts: list = None

class BulkmergehostgroupRequest(BaseModel):
    items: list = None

class HostgroupmergeRequest(BaseModel):
    hostGroupIds: list = None
    name: str = None

class HostcreateRequest(BaseModel):
    comment: str = None
    contact: str = None
    fqdn: str = None
    hostGroupIds: list = None
    initiatorIds: list = None
    initiatorsToCreate: list = None
    ipAddress: str = None
    isVvolHost: bool = None
    location: str = None
    model: str = None
    name: str = None
    operatingSystem: str = None
    persona: str = None
    protocol: str = None
    subnet: str = None
    userCreated: bool = None

class HostupdatebyidRequest(BaseModel):
    initiatorsToCreate: list = None
    name: str = None
    updatedInitiators: list = None

class UpdatehostchapbyidRequest(BaseModel):
    items: list = None

class GeneratechapkeybyidRequest(BaseModel):
    hmacNum: str = None
    secret: str = None
    system: str = None
    type: str = None

class BulkmergehostRequest(BaseModel):
    items: list = None

class MergehostRequest(BaseModel):
    hostIds: list = None
    name: str = None
    operatingSystem: str = None

class HostinitiatorcreateRequest(BaseModel):
    address: str = None
    driverVersion: str = None
    firmwareVersion: str = None
    hbaModel: str = None
    hostSpeed: int = None
    ipAddress: str = None
    name: str = None
    protocol: str = None
    vendor: str = None

class SystemlocateRequest(BaseModel):
    locateEnabled: bool = None

class AlertcontactscreateRequest(BaseModel):
    company: str = None
    companyCode: str = None
    country: str = None
    fax: str = None
    firstName: str = None
    includeSvcAlerts: bool = None
    lastName: str = None
    notificationSeverities: list = None
    preferredLanguage: str = None
    primaryEmail: str = None
    primaryPhone: str = None
    receiveEmail: bool = None
    receiveGrouped: bool = None
    secondaryEmail: str = None
    secondaryPhone: str = None

class AlertcontactsupdateRequest(BaseModel):
    company: str = None
    companyCode: str = None
    country: str = None
    fax: str = None
    firstName: str = None
    includeSvcAlerts: bool = None
    lastName: str = None
    notificationSeverities: list = None
    preferredLanguage: str = None
    primaryEmail: str = None
    primaryPhone: str = None
    receiveEmail: bool = None
    receiveGrouped: bool = None
    secondaryEmail: str = None
    secondaryPhone: str = None

class Devicetype1volumesetscreateRequest(BaseModel):
    appSetBusinessUnit: str = None
    appSetComments: str = None
    appSetImportance: str = None
    appSetName: str = None
    appSetType: str = None
    createAppSetQosConfigInput: dict = None
    customAppType: str = None
    members: list = None

class Devicetype1volumesetexportRequest(BaseModel):
    hostGroupIds: list = None
    proximity: str = None

class Devicetype1volumesetunexportRequest(BaseModel):
    hostGroupIds: list = None
    hostIds: list = None

class Devicetype1volumesetseditbyidRequest(BaseModel):
    addMembers: list = None
    appSetBusinessUnit: str = None
    appSetComments: str = None
    appSetImportance: str = None
    appSetName: str = None
    appSetType: str = None
    customAppType: str = None
    editAppSetQosConfigInput: dict = None
    removeMembers: list = None
    retainVolumeExportsOnRemoval: bool = None

class Devicetype1createprotectionpolicyRequest(BaseModel):
    policy: dict = None
    protectionPolicyType: str = None
    schedules: list = None

class Devicetype1editprotectionpoliciesRequest(BaseModel):
    createSchedules: list = None
    modifySchedules: list = None
    policy: dict = None
    protectionPolicyType: str = None
    removeSchedules: list = None

class Devicetype1fixprotectionpolicyRequest(BaseModel):
    policy: dict = None
    protectionPolicyType: str = None
    schedules: list = None

class Devicetype1removeprotectionpoliciesRequest(BaseModel):
    policies: list = None

class Devicetype1editproximitysettingsRequest(BaseModel):
    hosts: list = None

class Devicetype1actiononvolumesetsRequest(BaseModel):
    action: str = None
    parameters: dict = None

class Devicetype1volumesetssnapshotcreateRequest(BaseModel):
    comment: str = None
    expireSecs: int = None
    readOnly: bool = None
    retainSecs: int = None
    snapshotName: str = None
    vvNamePattern: str = None

class PostcertificateRequest(BaseModel):
    authorityChain: str = None
    commonName: str = None
    country: str = None
    days: int = None
    keyLength: int = None
    locality: str = None
    organization: str = None
    organizationUnit: str = None
    province: str = None
    service: str = None
    subjectAltName: dict = None
    type: str = None

class PutcertificateRequest(BaseModel):
    authorityChain: str = None
    certificate: str = None

class RemovecertificatesRequest(BaseModel):
    certificates: list = None

class EnclosurecardslocateiobyidRequest(BaseModel):
    locate: bool = None

class EnclosurepowerslocatepcmbyidRequest(BaseModel):
    locate: bool = None

class EnclosuresledslocatedrivebyidRequest(BaseModel):
    locate: bool = None

class EnclosureslocatebyidRequest(BaseModel):
    locate: bool = None

class EnclosureseditbyidRequest(BaseModel):
    id: str = None
    location: str = None

class Devicetype1backupactiononencryptionRequest(BaseModel):
    parameters: dict = None

class Devicetype1enableactiononencryptionRequest(BaseModel):
    parameters: dict = None

class Devicetype1rekeyactiononencryptionRequest(BaseModel):
    parameters: dict = None

class Devicetype1restoreactiononencryptionRequest(BaseModel):
    key: str = None
    parameters: dict = None

class Devicetype1setekmconfigurationRequest(BaseModel):
    parameters: dict = None

class Devicetype1setekmbackupactiononencryptionRequest(BaseModel):
    parameters: dict = None

class MailsettingsassociateRequest(BaseModel):
    authenticationRequired: str = None
    mailHostDomain: str = None
    mailHostServer: str = None
    password: str = None
    port: int = None
    senderEmailId: str = None
    username: str = None

class MailsettingsupdateRequest(BaseModel):
    authenticationRequired: str = None
    mailHostDomain: str = None
    mailHostServer: str = None
    password: str = None
    port: int = None
    senderEmailId: str = None
    username: str = None

class NetworkservicecimupdateRequest(BaseModel):
    cim: dict = None

class NetworkservicesnmpmgrcreateRequest(BaseModel):
    snmpConfig: list = None

class NetworkservicesnmpmgrupdateRequest(BaseModel):
    managerIP: str = None
    notify: str = None
    port: int = None
    retry: int = None
    timeoutSecs: int = None
    user: str = None
    version: int = None

class Devicetype1networkservicevasaconfigureRequest(BaseModel):
    action: str = None

class Devicetype1networkserviceconfigurevasaserviceRequest(BaseModel):
    certMgmt: str = None
    vasaStateEnabled: bool = None

class NetworksettingsassociateRequest(BaseModel):
    dnsAddresses: list = None
    ipv4Address: str = None
    ipv4Gateway: str = None
    ipv4SubnetMask: str = None
    ipv6Address: str = None
    ipv6Gateway: str = None
    ipv6PrefixLen: str = None
    proxyParams: dict = None

class NodeslocatebyidRequest(BaseModel):
    locate: bool = None

class NodecardlocatebyidRequest(BaseModel):
    locate: bool = None

class NodepowerslocatepcmbbyidRequest(BaseModel):
    locate: bool = None

class PortenableRequest(BaseModel):
    portEnable: bool = None

class Devicetype1portsclearRequest(BaseModel):
    ipType: str = None

class Devicetype1iscsiporteditRequest(BaseModel):
    gatewayAddress: str = None
    ipAddress: str = None
    label: str = None
    mtu: str = None
    netMask: str = None
    sendTargetGroupTag: int = None

class Devicetype1rcipporteditRequest(BaseModel):
    gatewayAddress: str = None
    gatewayAddressV6: str = None
    ipAddress: str = None
    ipAddressV6: str = None
    label: str = None
    mtu: str = None
    netMask: str = None
    netMaskV6: str = None
    speedConfigured: str = None

class Devicetype1fcporteditRequest(BaseModel):
    configMode: str = None
    connectionType: str = None
    interuptCoalesce: bool = None
    label: str = None
    speedConfigured: str = None
    uniqueWWN: bool = None
    vcn: bool = None

class Devicetype1iscsiportpingRequest(BaseModel):
    ipAddress: str = None
    ipAddressv6: str = None
    pingCount: int = None

class Devicetype1rcipportpingRequest(BaseModel):
    PacketSize: int = None
    WaitTime: int = None
    ipAddress: str = None
    ipAddressv6: str = None
    pingCount: int = None

class SnapshotclonecreateRequest(BaseModel):
    autoLun: bool = None
    destinationCpg: str = None
    destinationSnapshotCpg: str = None
    destinationVolume: str = None
    hostGroupId: str = None
    lun: int = None
    priority: str = None

class Devicetype1vlunexportforsnapshotRequest(BaseModel):
    LUN: list = None
    autoLun: bool = None
    hostGroupIds: list = None
    maxAutoLun: int = None
    noVcn: bool = None
    override: bool = None
    position: str = None
    proximity: str = None

class Devicetype1vlununexportforsnapshotRequest(BaseModel):
    hostGroupIds: list = None
    hostIds: list = None

class SupportsettingsassociateRequest(BaseModel):
    connectToHPE: str = None
    deviceId: str = None
    enterpriseServerURL: str = None
    miniInsploreEnabled: str = None
    rapForwarding: str = None
    remoteAccess: str = None
    remoteRequestAcknowledge: dict = None
    rtsEnabled: str = None

class SupportsettingsupdateRequest(BaseModel):
    connectToHPE: str = None
    deviceId: str = None
    enterpriseServerURL: str = None
    miniInsploreEnabled: str = None
    rapForwarding: str = None
    remoteAccess: str = None
    remoteRequestAcknowledge: dict = None
    rtsEnabled: str = None

class SystemsettingsassociateRequest(BaseModel):
    authMode: dict = None
    dateTime: str = None
    installationSites: dict = None
    name: str = None
    ntpAddresses: list = None
    remoteSyslogSettings: dict = None
    srinfo: dict = None
    supportContact: dict = None
    systemParameters: dict = None
    timezone: str = None

class SystemsettingsupdateRequest(BaseModel):
    authMode: dict = None
    dateTime: str = None
    installationSites: dict = None
    name: str = None
    ntpAddresses: list = None
    remoteSyslogSettings: dict = None
    srinfo: dict = None
    supportContact: dict = None
    systemParameters: dict = None
    timezone: str = None

class Devicetype1createvvolscRequest(BaseModel):
    comment: str = None
    domain: str = None
    hostIDs: list = None
    hostSetIDs: list = None
    keep: bool = None
    members: list = None
    name: str = None

class Devicetype1editvolscRequest(BaseModel):
    comment: str = None
    hostProximity: list = None
    members: list = None
    name: str = None

class Devicetype1attachdetachvolscRequest(BaseModel):
    action: str = None
    hostIDs: list = None
    hostSetIDs: list = None

class Devicetype1postquorumwitnessRequest(BaseModel):
    parameters: dict = None
    replicationPartnerSystemId: str = None
    srcReplicationId: str = None
    startQuorumWitness: bool = None
    targetReplicationId: str = None

class Devicetype1putquorumwitnessRequest(BaseModel):
    replicationPartnerSystemId: str = None
    startQuorumWitness: bool = None
    targetReplicationId: str = None

class Devicetype1postreplicationpartnersRequest(BaseModel):
    replicationPartners: list = None

class Devicetype1putreplicationpartnerRequest(BaseModel):
    addRcLinks: dict = None
    removeRcLinks: dict = None

class Devicetype1postremovereplicationpartnersRequest(BaseModel):
    replicationPartners: list = None

class AddtrustedcertificatesRequest(BaseModel):
    action: str = None
    parameters: dict = None

class RemovetrustedcertificatesRequest(BaseModel):
    trustedCertificates: list = None

class Devicetype1postvcentersettingsRequest(BaseModel):
    certChainPem: str = None
    description: str = None
    inetaddress: str = None
    name: str = None
    password: str = None
    port: int = None
    username: str = None

class Devicetype1putvcentersettingsRequest(BaseModel):
    certChainPem: str = None
    description: str = None
    inetaddress: str = None
    name: str = None
    password: str = None
    port: int = None
    username: str = None

class VolumecreateRequest(BaseModel):
    comments: str = None
    count: int = None
    dataReduction: bool = None
    name: str = None
    sizeMib: int = None
    snapCpg: str = None
    snapshotAllocWarning: int = None
    userAllocWarning: int = None
    userCpg: str = None

class VolumeeditRequest(BaseModel):
    conversionType: str = None
    dataReduction: bool = None
    name: str = None
    sizeMib: int = None
    snapshotAllocWarning: int = None
    snapshotCpgName: str = None
    userAllocWarning: int = None
    userCpgName: str = None

class VolumeclonecreateRequest(BaseModel):
    destinationVolume: str = None
    offlineClone: dict = None
    online: bool = None
    onlineClone: dict = None
    priority: str = None

class Devicetype1vlunexportRequest(BaseModel):
    LUN: list = None
    autoLun: bool = None
    hostGroupIds: list = None
    maxAutoLun: int = None
    noVcn: bool = None
    override: bool = None
    position: str = None
    proximity: str = None

class VolumesnapshotcreateRequest(BaseModel):
    comment: str = None
    customName: str = None
    expireSecs: int = None
    namePattern: str = None
    readOnly: bool = None
    retainSecs: int = None

class Devicetype1vlununexportRequest(BaseModel):
    hostGroupIds: list = None
    hostIds: list = None

class Devicetype1promoteclonevolumeRequest(BaseModel):
    priority: str = None

class Devicetype1resyncclonevolumeRequest(BaseModel):
    priority: str = None

class Devicetype1promotesnapshotRequest(BaseModel):
    priority: str = None
    target: str = None

class Devicetype2editstoragesystemsettingsbyidRequest(BaseModel):
    auto_switchover_enabled: bool = None
    autoclean_unmanaged_snapshots_enabled: bool = None
    autoclean_unmanaged_snapshots_ttl_unit: int = None
    cc_mode_enabled: bool = None
    date: int = None
    default_iscsi_target_scope: str = None
    group_snapshot_ttl: int = None
    group_target_name: str = None
    max_lock_period: int = None
    name: str = None
    ntp_server: str = None
    tdz_enabled: bool = None
    tdz_prefix: str = None
    timezone: str = None
    tlsv1_enabled: bool = None

class Devicetype2accesscontrolrecordcreateRequest(BaseModel):
    apply_to: str = None
    chap_user_id: str = None
    initiator_group_id: str = None
    lun: int = None
    pe_id: str = None
    pe_ids: list = None
    snap_id: str = None
    systemUid: str = None
    vol_id: str = None

class Devicetype2editaccesscontrolrecordbyidRequest(BaseModel):
    apply_to: str = None

class Devicetype2mergegroupsRequest(BaseModel):
    force: bool = None
    skip_secondary_mgmt_ip: bool = None
    src_group_ip: str = None
    src_group_name: str = None
    src_passphrase: str = None
    src_password: str = None
    src_username: str = None

class Devicetype2applicationservercreateRequest(BaseModel):
    description: str = None
    hostname: str = None
    metadata: list = None
    name: str = None
    password: str = None
    port: int = None
    server_type: str = None
    username: str = None

class Devicetype2applicationservereditRequest(BaseModel):
    description: str = None
    hostname: str = None
    metadata: list = None
    name: str = None
    port: int = None
    server_type: str = None
    username: str = None

class Devicetype2createarrayRequest(BaseModel):
    allow_lower_limits: bool = None
    create_pool: bool = None
    ctrlr_a_support_ip: str = None
    ctrlr_b_support_ip: str = None
    dedupe_disabled: bool = None
    name: str = None
    nic_list: list = None
    pool_description: str = None
    pool_name: str = None
    secondary_mgmt_ip: str = None
    serial: str = None

class Devicetype2editarraybyidRequest(BaseModel):
    name: str = None

class Devicetype2arrayfailoverRequest(BaseModel):
    force: bool = None

class Devicetype2diskeditRequest(BaseModel):
    disk_op: str = None
    force: bool = None

class Devicetype2createexternalkeymanagerRequest(BaseModel):
    description: str = None
    hostname: str = None
    name: str = None
    password: str = None
    port: int = None
    protocol: str = None
    username: str = None

class Devicetype2deleteexternalkeymanagerbyidRequest(BaseModel):
    passphrase: str = None

class Devicetype2editexternalkeymanagerbyidRequest(BaseModel):
    description: str = None
    hostname: str = None
    id: str = None
    name: str = None
    password: str = None
    port: int = None
    protocol: str = None
    username: str = None

class Devicetype2removeexternalkeymanagerbyidRequest(BaseModel):
    passphrase: str = None

class Devicetype2foldercreateRequest(BaseModel):
    access_protocol: str = None
    agent_type: str = None
    appserver_id: str = None
    description: str = None
    hostInitiatorGroupIDs: list = None
    hostInitiatorsIDs: list = None
    inherited_vol_perfpol_id: str = None
    limit_iops: int = None
    limit_mbps: int = None
    limit_size_bytes: int = None
    name: str = None
    overdraft_limit_pct: int = None
    pool_id: str = None
    provisioned_limit_size_bytes: int = None

class Devicetype2foldereditRequest(BaseModel):
    appserver_id: str = None
    description: str = None
    inherited_vol_perfpol_id: str = None
    limit_iops: int = None
    limit_mbps: int = None
    limit_size_bytes: int = None
    name: str = None
    overdraft_limit_pct: int = None
    provisioned_limit_size_bytes: int = None

class Devicetype2attachdetachvvolbyidRequest(BaseModel):
    action: str = None
    hostInitiatorGroupIDs: list = None
    hostInitiatorsIDs: list = None

class Devicetype2hostinitiatorgroupcreateRequest(BaseModel):
    access_protocol: str = None
    app_uuid: str = None
    description: str = None
    fc_initiators: list = None
    fc_tdz_ports: list = None
    host_type: str = None
    iscsi_initiators: list = None
    metadata: list = None
    name: str = None
    target_subnets: list = None

class Devicetype2updatehostinitiatorgroupbyidRequest(BaseModel):
    app_uuid: str = None
    description: str = None
    fc_initiators: list = None
    fc_tdz_ports: list = None
    host_type: str = None
    iscsi_initiators: list = None
    metadata: list = None
    name: str = None
    target_subnets: list = None

class Devicetype2initiatorscreateRequest(BaseModel):
    access_protocol: str = None
    alias: str = None
    chapuser_id: str = None
    initiator_group_id: str = None
    ip_address: str = None
    iqn: str = None
    label: str = None
    override_existing_alias: bool = None
    wwpn: str = None

class Devicetype2createlocalkeymanagerRequest(BaseModel):
    passphrase: str = None

class Devicetype2editlocalkeymanagerbyidRequest(BaseModel):
    active: bool = None
    new_passphrase: str = None
    passphrase: str = None

class Devicetype2editmailsettingsRequest(BaseModel):
    smtp_port: int = None
    smtp_server: str = None

class Devicetype2editnetworksettingbyidRequest(BaseModel):
    array_list: list = None
    iscsi_automatic_connection_method: bool = None
    iscsi_connection_rebalancing: bool = None
    mgmt_ip: str = None
    name: str = None
    route_list: list = None
    secondary_mgmt_ip: str = None
    subnet_list: list = None

class Devicetype2performancepolicycreateRequest(BaseModel):
    app_category: str = None
    block_size: int = None
    cache: bool = None
    cache_policy: str = None
    compress: bool = None
    dedupe_enabled: bool = None
    description: str = None
    name: str = None
    space_policy: str = None

class Devicetype2performancepolicyeditRequest(BaseModel):
    app_category: str = None
    cache: bool = None
    cache_policy: str = None
    compress: bool = None
    dedupe_enabled: bool = None
    description: str = None
    name: str = None
    space_policy: str = None

class Devicetype2editfcportRequest(BaseModel):
    online: bool = None

class Devicetype2createprotectiontemplateRequest(BaseModel):
    app_cluster_name: str = None
    app_id: str = None
    app_server: str = None
    app_service_name: str = None
    app_sync: str = None
    description: str = None
    name: str = None
    schedules: list = None

class Devicetype2editprotectiontemplateRequest(BaseModel):
    addSchedules: list = None
    app_cluster_name: str = None
    app_id: str = None
    app_server: str = None
    app_service_name: str = None
    app_sync: str = None
    description: str = None
    editSchedules: list = None
    name: str = None
    removeSchedules: list = None

class Devicetype2removeprotectiontemplateRequest(BaseModel):
    protectionTemplates: list = None

class Devicetype2provisioningworklowRequest(BaseModel):
    agent_type: str = None
    app_uuid: str = None
    appSetName: str = None
    count: int = None
    dedupe_enabled: bool = None
    downstreamPartner: str = None
    downstreamPartnerId: str = None
    encryption_cipher: str = None
    folder_id: str = None
    host_groups: list = None
    limit: int = None
    limit_iops: int = None
    limit_mbps: int = None
    name: str = None
    perfpolicy: dict = None
    perfpolicy_id: str = None
    pool_id: str = None
    protectionPolicyId: str = None
    protectionPolicySchedules: list = None
    replicationStartTime: int = None
    size: int = None
    suffix: int = None
    volColId: str = None
    volColName: str = None
    warn_level: int = None

class Devicetype2provisioningreviewRequest(BaseModel):
    host_groups: list = None

class Devicetype2locateshelfchassisRequest(BaseModel):
    cid: str = None
    status: bool = None

class Devicetype2activateshelfRequest(BaseModel):
    shelf_list: list = None

class Devicetype2cloneactiononsnapshotcollectionsRequest(BaseModel):
    clone_volumes: list = None

class Devicetype2editsnapshotbyidRequest(BaseModel):
    snapshot_list: list = None

class Devicetype2createpoolRequest(BaseModel):
    array_list: list = None
    dedupe_all_volumes: bool = None
    description: str = None
    name: str = None

class Devicetype2editpooldetailbyidRequest(BaseModel):
    array_list: list = None
    dedupe_all_volumes: bool = None
    dedupe_capable: bool = None
    description: str = None
    force: bool = None
    is_default: bool = None
    name: str = None

class Devicetype2mergepoolbyidRequest(BaseModel):
    force: bool = None
    target_pool_id: str = None

class Devicetype2editsystemsettingsRequest(BaseModel):
    alert_settings: dict = None
    date_timezone_settings: dict = None
    dns_settings: dict = None
    encryption_config: dict = None
    isns_settings: dict = None
    name: str = None
    proxy_settings: dict = None
    security_settings: dict = None
    smtp_settings: dict = None
    snmp_settings: dict = None
    support_settings: dict = None
    syslogd_settings: dict = None
    system_parameters: dict = None

class Devicetype2createreplicationpartnersRequest(BaseModel):
    replicationPartners: list = None

class Devicetype2editreplicationpartnersbyidRequest(BaseModel):
    replicationPartners: list = None

class Devicetype2pausereplicationpartnerRequest(BaseModel):
    replicationPartners: list = None

class Devicetype2resumereplicationpartnerRequest(BaseModel):
    replicationPartners: list = None

class Devicetype2testreplicationconfigurationRequest(BaseModel):
    replicationPartners: list = None

class Devicetype2removereplicationpartnerRequest(BaseModel):
    replicationPartners: list = None

class Devicetype2createwitnessRequest(BaseModel):
    host: str = None
    password: str = None
    port: int = None
    username: str = None

class Getdevicetype2uninitializedarraybyidRequest(BaseModel):
    id: str = None

class Devicetype2volumecollectioncreateRequest(BaseModel):
    agent_hostname: str = None
    agent_username: str = None
    app_cluster_name: str = None
    app_id: str = None
    app_server: str = None
    app_service_name: str = None
    app_sync: str = None
    description: str = None
    is_standalone_volcoll: bool = None
    metadata: list = None
    name: str = None
    prottmpl_id: str = None
    replication_type: str = None
    vcenter_hostname: str = None
    vcenter_username: str = None
    volume_list: list = None

class Devicetype2editvolumecollectionbyidRequest(BaseModel):
    agent_hostname: str = None
    agent_username: str = None
    app_cluster_name: str = None
    app_id: str = None
    app_server: str = None
    app_service_name: str = None
    app_sync: str = None
    description: str = None
    name: str = None
    vcenter_hostname: str = None
    vcenter_username: str = None

class Devicetype2addvolumestovolumecollectionsRequest(BaseModel):
    volume_ids: list = None

class Devicetype2actiononvolumecollectionidRequest(BaseModel):
    invoke_on_upstream_partner: bool = None
    replication_partner_id: str = None

class Devicetype2actiononvolumecollectionRequest(BaseModel):
    invoke_on_upstream_partner: bool = None
    no_reverse: bool = None
    override_upstream_down: bool = None
    replication_partner_id: str = None

class Devicetype2removevolumesfromvolumecollectionRequest(BaseModel):
    volume_ids: list = None

class Devicetype2createsnapshotcollectionsRequest(BaseModel):
    agent_type: str = None
    allow_writes: bool = None
    description: str = None
    disable_appsync: bool = None
    invoke_on_upstream_partner: bool = None
    is_external_trigger: bool = None
    lock_period: int = None
    metadata: list = None
    name: str = None
    replicate: bool = None
    replicate_to: str = None
    skip_db_consistency_check: bool = None
    snap_verify: bool = None
    start_online: bool = None
    vol_snap_attr_list: list = None

class Devicetype2removesnapshotcollectionRequest(BaseModel):
    force: bool = None
    snapshot_collections: list = None

class Devicetype2actiononsnapshotcollectionRequest(BaseModel):
    online: bool = None
    snapshot_collection_ids: list = None

class Devicetype2volumescreateRequest(BaseModel):
    agent_type: str = None
    app_uuid: str = None
    base_snap_id: str = None
    block_size: int = None
    cache_pinned: bool = None
    clone: bool = None
    dedupe_enabled: bool = None
    description: str = None
    dest_pool_id: str = None
    encryption_cipher: str = None
    folder_id: str = None
    limit: int = None
    limit_iops: int = None
    limit_mbps: int = None
    metadata: list = None
    multi_initiator: bool = None
    name: str = None
    online: bool = None
    owned_by_group_id: str = None
    perfpolicy_id: str = None
    pool_id: str = None
    read_only: bool = None
    reserve: int = None
    size: int = None
    snap_reserve: int = None
    snap_warn_level: int = None
    suffix: int = None
    warn_level: int = None

class Devicetype2editvolumebyidRequest(BaseModel):
    app_uuid: str = None
    caching_enabled: bool = None
    dedupe_enabled: bool = None
    description: str = None
    folder_id: str = None
    force: bool = None
    limit: int = None
    limit_iops: int = None
    limit_mbps: int = None
    name: str = None
    online: bool = None
    owned_by_group_id: str = None
    perfpolicy_id: str = None
    size: int = None

class Devicetype2movevolumeRequest(BaseModel):
    dest_pool_id: str = None

class Devicetype2restorevolumebyidRequest(BaseModel):
    base_snap_id: str = None
    enable_vol_offline: bool = None

class Devicetype2clonevolumebyidRequest(BaseModel):
    clone_volume_name: str = None
    host_group_id: str = None
    lun: int = None

class Devicetype2volumesexportRequest(BaseModel):
    apply_to: str = None
    force_apply_to: bool = None
    host_groups: list = None

class Devicetype2snapshotcreateRequest(BaseModel):
    app_uuid: str = None
    description: str = None
    lock_period: int = None
    metadata: list = None
    name: str = None
    online: bool = None
    writable: bool = None

class Devicetype2snapshotexportRequest(BaseModel):
    apply_to: str = None
    force_apply_to: bool = None
    host_groups: list = None

class Devicetype2deletesnapshotaccessbyidRequest(BaseModel):
    host_groups: list = None
    hosts: list = None

class Devicetype2deletevolumeaccessbyidRequest(BaseModel):
    host_groups: list = None
    hosts: list = None

class Devicetype4systemlocateRequest(BaseModel):
    locateEnabled: bool = None

class Devicetype4alertcontactscreateRequest(BaseModel):
    company: str = None
    companyCode: str = None
    country: str = None
    fax: str = None
    firstName: str = None
    includeSvcAlerts: bool = None
    lastName: str = None
    notificationSeverities: list = None
    preferredLanguage: str = None
    primaryEmail: str = None
    primaryPhone: str = None
    receiveEmail: bool = None
    receiveGrouped: bool = None
    secondaryEmail: str = None
    secondaryPhone: str = None

class Devicetype4alertcontactsupdateRequest(BaseModel):
    company: str = None
    companyCode: str = None
    country: str = None
    fax: str = None
    firstName: str = None
    includeSvcAlerts: bool = None
    lastName: str = None
    notificationSeverities: list = None
    preferredLanguage: str = None
    primaryEmail: str = None
    primaryPhone: str = None
    receiveEmail: bool = None
    receiveGrouped: bool = None
    secondaryEmail: str = None
    secondaryPhone: str = None

class Devicetype4volumesetscreateRequest(BaseModel):
    appSetBusinessUnit: str = None
    appSetComments: str = None
    appSetImportance: str = None
    appSetName: str = None
    appSetType: str = None
    createAppSetQosConfigInput: dict = None
    customAppType: str = None
    members: list = None
    ransomware: bool = None

class Devicetype4volumesetexportRequest(BaseModel):
    hostGroupDataMap: list = None
    hostGroupIds: list = None
    proximity: str = None

class Devicetype4volumesetunexportRequest(BaseModel):
    hostGroupIds: list = None
    hostIds: list = None

class Devicetype4volumesetseditbyidRequest(BaseModel):
    addMembers: list = None
    appSetBusinessUnit: str = None
    appSetComments: str = None
    appSetImportance: str = None
    appSetName: str = None
    appSetType: str = None
    customAppType: str = None
    editAppSetQosConfigInput: dict = None
    ransomware: bool = None
    removeMembers: list = None
    retainVolumeExportsOnRemoval: bool = None

class Devicetype4createprotectionpolicyRequest(BaseModel):
    policy: dict = None
    policyId: str = None
    protectionPolicyType: str = None
    protectionStoreId: str = None
    schedules: list = None

class Devicetype4editprotectionpoliciesRequest(BaseModel):
    createSchedules: list = None
    modifySchedules: list = None
    policy: dict = None
    protectionPolicyType: str = None
    removeSchedules: list = None

class Devicetype4fixprotectionpolicyRequest(BaseModel):
    policy: dict = None
    policyId: str = None
    protectionPolicyType: str = None
    protectionStoreId: str = None
    schedules: list = None

class Devicetype4removeprotectionpoliciesRequest(BaseModel):
    policies: list = None

class Devicetype4editproximitysettingsRequest(BaseModel):
    hostGroups: list = None
    hosts: list = None

class Devicetype4actiononvolumesetsRequest(BaseModel):
    action: str = None
    parameters: dict = None

class Devicetype4volumesetssnapshotcreateRequest(BaseModel):
    comment: str = None
    expireSecs: int = None
    readOnly: bool = None
    retainSecs: int = None
    snapshotName: str = None
    vvNamePattern: str = None

class Devicetype4postcertificateRequest(BaseModel):
    authorityChain: str = None
    commonName: str = None
    country: str = None
    days: int = None
    keyLength: int = None
    locality: str = None
    organization: str = None
    organizationUnit: str = None
    province: str = None
    service: str = None
    subjectAltName: dict = None
    type: str = None

class Devicetype4putcertificateRequest(BaseModel):
    authorityChain: str = None
    certificate: str = None
    vcGuid: str = None

class Devicetype4removecertificatesRequest(BaseModel):
    certificates: list = None

class Devicetype4enclosurecardslocateiobyidRequest(BaseModel):
    locate: bool = None

class Devicetype4enclosuresledslocatedrivebyidRequest(BaseModel):
    locate: bool = None

class Devicetype4enclosureslocatebyidRequest(BaseModel):
    locate: bool = None

class Devicetype4enclosureseditbyidRequest(BaseModel):
    id: str = None
    location: str = None

class Devicetype4backupactiononencryptionRequest(BaseModel):
    parameters: dict = None

class Devicetype4enableactiononencryptionRequest(BaseModel):
    parameters: dict = None

class Devicetype4rekeyactiononencryptionRequest(BaseModel):
    parameters: dict = None

class Devicetype4restoreactiononencryptionRequest(BaseModel):
    key: str = None
    parameters: dict = None

class Devicetype4setekmconfigurationRequest(BaseModel):
    parameters: dict = None

class Devicetype4setekmbackupactiononencryptionRequest(BaseModel):
    parameters: dict = None

class Devicetype4filesharecreateRequest(BaseModel):
    filesystemName: str = None
    hostAccess: list = None
    name: str = None
    protocol: list = None
    reduce: bool = None
    settingName: str = None
    sizeInMiB: int = None

class Devicetype4fileshareupdateRequest(BaseModel):
    additionalSizeInMiB: int = None
    hostAccess: list = None

class Devicetype4setlicenseRequest(BaseModel):
    parameters: dict = None

class Devicetype4mailsettingsassociateRequest(BaseModel):
    authenticationRequired: str = None
    mailHostDomain: str = None
    mailHostServer: str = None
    password: str = None
    port: int = None
    senderEmailId: str = None
    username: str = None

class Devicetype4mailsettingsupdateRequest(BaseModel):
    authenticationRequired: str = None
    mailHostDomain: str = None
    mailHostServer: str = None
    password: str = None
    port: int = None
    senderEmailId: str = None
    username: str = None

class Devicetype4networkservicecimupdateRequest(BaseModel):
    cim: dict = None

class Devicetype4networkservicesnmpmgrcreateRequest(BaseModel):
    snmpConfig: list = None

class Devicetype4networkservicesnmpmgrupdateRequest(BaseModel):
    authenticationPassword: str = None
    managerIP: str = None
    notify: str = None
    port: int = None
    privPassword: str = None
    retry: int = None
    timeoutSecs: int = None
    user: str = None
    userMode: str = None
    version: int = None

class Devicetype4networkservicevasaconfigureRequest(BaseModel):
    action: str = None

class Devicetype4networkserviceconfigurevasaserviceRequest(BaseModel):
    certMgmt: str = None
    cfgList: list = None
    nodeId: str = None
    vasaStateEnabled: bool = None

class Devicetype4networksettingsassociateRequest(BaseModel):
    dnsAddresses: list = None
    ipv4Address: str = None
    ipv4Gateway: str = None
    ipv4SubnetMask: str = None
    ipv6Address: str = None
    ipv6Gateway: str = None
    ipv6PrefixLen: str = None
    proxyParams: dict = None

class Devicetype4vasaprovideraddressconfigureRequest(BaseModel):
    configVpAddress: list = None

class Devicetype4vasaprovideraddressclearRequest(BaseModel):
    clearVpAddress: list = None

class Devicetype4nodeslocatebyidRequest(BaseModel):
    locate: bool = None

class Devicetype4portenableRequest(BaseModel):
    portEnable: bool = None

class Devicetype4portsclearRequest(BaseModel):
    ipType: str = None

class Devicetype4fileporteditRequest(BaseModel):
    ipAddress: str = None

class Devicetype4iscsiporteditRequest(BaseModel):
    enablePeer: bool = None
    ethernetFlowControl: str = None
    label: str = None
    mtu: str = None
    targetProtocol: str = None
    vlans: list = None

class Devicetype4nvmeporteditRequest(BaseModel):
    ethernetFlowControl: str = None
    label: str = None
    mtu: str = None
    targetProtocol: str = None
    vlans: list = None

class Devicetype4rcipporteditRequest(BaseModel):
    gatewayAddress: str = None
    gatewayAddressV6: str = None
    ipAddress: str = None
    ipAddressV6: str = None
    label: str = None
    mtu: str = None
    netMask: str = None
    netMaskV6: str = None
    speedConfigured: str = None

class Devicetype4fcporteditRequest(BaseModel):
    configMode: str = None
    connectionType: str = None
    interuptCoalesce: bool = None
    label: str = None
    speedConfigured: str = None
    uniqueWWN: bool = None
    vcn: bool = None

class Devicetype4fileportpingRequest(BaseModel):
    PacketSize: int = None
    WaitTime: int = None
    ipAddress: str = None
    pingCount: int = None

class Devicetype4iscsiportpingRequest(BaseModel):
    ipAddress: str = None
    ipAddressv6: str = None
    pingCount: int = None
    vlanId: str = None

class Devicetype4nvmeportpingRequest(BaseModel):
    PacketSize: int = None
    WaitTime: int = None
    ipAddress: str = None
    ipAddressv6: str = None
    pingCount: int = None

class Devicetype4rcipportpingRequest(BaseModel):
    PacketSize: int = None
    WaitTime: int = None
    ipAddress: str = None
    ipAddressv6: str = None
    pingCount: int = None

class Devicetype4restoresnapshotofsnapshotRequest(BaseModel):
    priority: str = None
    target: str = None

class Devicetype4snapshotclonecreateRequest(BaseModel):
    autoLun: bool = None
    destinationCpg: str = None
    destinationVolume: str = None
    hostGroupId: str = None
    lun: int = None
    priority: str = None

class Devicetype4vlunexportforsnapshotRequest(BaseModel):
    LUN: list = None
    autoLun: bool = None
    hostGroupIds: list = None
    maxAutoLun: int = None
    noVcn: bool = None
    override: bool = None
    position: str = None
    proximity: str = None

class Devicetype4snapshotofsnapshotcreateRequest(BaseModel):
    comment: str = None
    customName: str = None
    expireSecs: int = None
    namePattern: str = None
    readOnly: bool = None
    retainSecs: int = None

class Devicetype4vlununexportforsnapshotRequest(BaseModel):
    hostGroupIds: list = None
    hostIds: list = None

class Devicetype4supportsettingsassociateRequest(BaseModel):
    connectToHPE: str = None
    deviceId: str = None
    enterpriseServerURL: str = None
    miniInsploreEnabled: str = None
    remoteAccess: str = None
    remoteRequestAcknowledge: dict = None

class Devicetype4supportsettingsupdateRequest(BaseModel):
    connectToHPE: str = None
    deviceId: str = None
    enterpriseServerURL: str = None
    miniInsploreEnabled: str = None
    remoteAccess: str = None
    remoteRequestAcknowledge: dict = None

class Devicetype4switchlocatebyidRequest(BaseModel):
    locate: bool = None

class Devicetype4systemsettingsassociateRequest(BaseModel):
    authMode: dict = None
    dateTime: str = None
    enableFile: dict = None
    installationSites: dict = None
    name: str = None
    ntpAddresses: list = None
    remoteSyslogSettings: dict = None
    srinfo: dict = None
    supportContact: dict = None
    systemParameters: dict = None
    timezone: str = None

class Devicetype4systemsettingsupdateRequest(BaseModel):
    authMode: dict = None
    dateTime: str = None
    enableFile: dict = None
    installationSites: dict = None
    name: str = None
    ntpAddresses: list = None
    remoteSyslogSettings: dict = None
    srinfo: dict = None
    supportContact: dict = None
    systemParameters: dict = None
    timezone: str = None

class Devicetype4createvvolscRequest(BaseModel):
    domain: str = None
    hostIDs: list = None
    hostSetIDs: list = None
    name: str = None
    scType: str = None
    transportType: str = None

class Devicetype4storagecontainereditbyidRequest(BaseModel):
    comment: str = None
    growthLimitMiB: int = None
    growthSizeMiB: int = None
    growthWarnMiB: int = None
    name: str = None

class Devicetype4attachvolscRequest(BaseModel):
    action: str = None
    parameter: dict = None

class Devicetype4detachvolscRequest(BaseModel):
    action: str = None
    parameter: dict = None

class Devicetype4postquorumwitnessRequest(BaseModel):
    parameters: dict = None
    replicationPartnerSystemId: str = None
    srcReplicationId: str = None
    startQuorumWitness: bool = None
    targetReplicationId: str = None

class Devicetype4putquorumwitnessRequest(BaseModel):
    replicationPartnerSystemId: str = None
    startQuorumWitness: bool = None
    targetReplicationId: str = None

class Devicetype4postreplicationpartnersRequest(BaseModel):
    replicationPartners: list = None

class Devicetype4putreplicationpartnerRequest(BaseModel):
    addRcLinks: dict = None
    removeRcLinks: dict = None

class Devicetype4postremovereplicationpartnersRequest(BaseModel):
    replicationPartners: list = None

class Devicetype4addtrustedcertificatesRequest(BaseModel):
    action: str = None
    parameters: dict = None

class Devicetype4removetrustedcertificatesRequest(BaseModel):
    trustedCertificates: list = None

class Devicetype4postvcentersettingsRequest(BaseModel):
    certChainPem: str = None
    description: str = None
    inetaddress: str = None
    name: str = None
    password: str = None
    port: int = None
    username: str = None

class Devicetype4putvcentersettingsRequest(BaseModel):
    certChainPem: str = None
    description: str = None
    inetaddress: str = None
    name: str = None
    password: str = None
    port: int = None
    username: str = None

class Devicetype4postvmesettingsRequest(BaseModel):
    accessToken: str = None
    address: str = None
    certificateVerification: dict = None
    description: str = None
    name: str = None
    port: int = None

class Devicetype4putvmesettingsRequest(BaseModel):
    accessToken: str = None
    address: str = None
    certificateVerification: dict = None
    description: str = None
    name: str = None
    port: int = None

class Devicetype4volumecreateRequest(BaseModel):
    comments: str = None
    count: int = None
    dataReduction: bool = None
    name: str = None
    ransomware: bool = None
    sizeMib: int = None
    snapshotAllocWarning: int = None
    userAllocWarning: int = None
    userCpg: str = None

class Devicetype4volumeeditRequest(BaseModel):
    conversionType: str = None
    dataReduction: bool = None
    name: str = None
    ransomware: bool = None
    sizeMib: int = None
    snapshotAllocWarning: int = None
    userAllocWarning: int = None
    userCpgName: str = None

class Devicetype4volumeclonecreateRequest(BaseModel):
    destinationVolume: str = None
    offlineClone: dict = None
    online: bool = None
    onlineClone: dict = None
    priority: str = None

class Devicetype4vlunexportRequest(BaseModel):
    LUN: list = None
    autoLun: bool = None
    hostGroupIds: list = None
    maxAutoLun: int = None
    noVcn: bool = None
    override: bool = None
    position: str = None
    proximity: str = None

class Devicetype4volumesnapshotcreateRequest(BaseModel):
    comment: str = None
    customName: str = None
    expireSecs: int = None
    namePattern: str = None
    readOnly: bool = None
    retainSecs: int = None

class Devicetype4vlununexportRequest(BaseModel):
    hostGroupIds: list = None
    hostIds: list = None

class Devicetype4editclonevolumeRequest(BaseModel):
    ransomware: bool = None

class Devicetype4promoteclonevolumeRequest(BaseModel):
    priority: str = None

class Devicetype4resyncclonevolumeRequest(BaseModel):
    priority: str = None

class Devicetype4volumesnapshotschedulecreateRequest(BaseModel):
    allowSysOffsetMinute: bool = None
    atTime: int = None
    dayOfMonth: int = None
    days: str = None
    expireSecs: int = None
    name: str = None
    period: int = None
    periodUnit: str = None
    readOnly: bool = None
    retainSecs: int = None
    untilTime: int = None

class ArcuseditvolumesnapshotscheduleRequest(BaseModel):
    allowSysOffsetMinute: bool = None
    atTime: int = None
    dayOfMonth: int = None
    days: str = None
    name: str = None
    period: int = None
    periodUnit: str = None
    untilTime: int = None

class Devicetype4promotesnapshotRequest(BaseModel):
    priority: str = None
    target: str = None

class Devicetype4editsnapshotRequest(BaseModel):
    ransomware: bool = None

class ProvisioningrecommendationsRequest(BaseModel):
    hostGroupId: str = None
    productFamily: str = None
    sizeMib: int = None


class CloudVmCreateRequest(BaseModel):
    vm_name: str
    vcpu: int
    ram_gb: int


