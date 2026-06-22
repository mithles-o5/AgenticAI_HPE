from pydantic import BaseModel
BaseModel.model_config['extra'] = 'allow'

class DeviceSchema(BaseModel):
    id: str = None
    serial_number: str
    ip_address: str = None
    fqdn: str = None
    management_source: str
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


