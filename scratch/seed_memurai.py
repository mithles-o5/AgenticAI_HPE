import sys, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, ".."))
sys.path.insert(0, ROOT_DIR)
for p in ["resource_resolver"]:
    sys.path.insert(0, os.path.join(ROOT_DIR, p))

from cache import ResourceCache
from records import DeviceRecord

cache = ResourceCache()

device = DeviceRecord(
    id="12345678-1234-1234-1234-123456789012",
    serial_number="wan-r08-10017",
    fqdn="wan-r08-10017.local",
    management_source="coms",
    source_host="http://127.0.0.1:8001",
    source_device_id="wan-r08-10017",
    device_type="router"
)

cache.put_device(device)
print(f"Seeded {device.serial_number} into Memurai cache.")
