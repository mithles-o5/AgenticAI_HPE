"""
com_mock/resource_graph.py
──────────────────────────
The crown jewel of the beast upgrade.

Defines ONEVIEW_RESOURCE_SCHEMAS — a deep knowledge base of every HPE OneView
resource type, complete with:
  • Field types, enums, ranges, and patterns
  • Cross-resource foreign-key relationships
  • Cascade rules (nullify / restrict / cascade-delete)
  • Which operations trigger async tasks
  • Bidirectional relationship tracking

The ResourceGraph class enforces this knowledge at runtime: every create,
update, and delete goes through it, keeping the entire mock store consistent.
"""

from __future__ import annotations

import hashlib
import random
import string
import uuid
from typing import Any, Optional

# ── Resource Schema Registry ─────────────────────────────────────────────────
#
# Field descriptor keys:
#   type        : string | integer | boolean | enum | enum_int | ref
#                 | version | serial | computed | array_ref | nested
#   values      : list of allowed values (for enum / enum_int)
#   min / max   : numeric bounds
#   pattern     : hint string for generators (not regex)
#   nullable    : bool (default False for refs)
#   required    : bool (default False)
#   mutable     : bool (default True) — False means field is set on create only
#   target      : resource slug for ref / array_ref types
#   bidirectional: field name on the target resource that back-links here

ONEVIEW_RESOURCE_SCHEMAS: dict[str, dict] = {

    # ── SERVERS ──────────────────────────────────────────────────────────

    "server-hardware": {
        "type_name": "ServerHardwareV11",
        "base_path": "/rest/server-hardware",
        "category": "SERVERS",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 1800,
        "fields": {
            "name":                 {"type": "string",   "pattern": "Encl{encl}, bay {bay}",  "mutable": False},
            "model":                {"type": "enum",     "values": ["ProLiant DL360 Gen10", "ProLiant DL380 Gen10", "ProLiant DL560 Gen10", "ProLiant BL460c Gen10 Plus", "ProLiant DL325 Gen10 Plus"]},
            "powerState":           {"type": "enum",     "values": ["On", "Off", "PoweringOn", "PoweringOff", "Resetting"], "mutable": True},
            "processorCount":       {"type": "integer",  "min": 1, "max": 4},
            "processorCoreCount":   {"type": "integer",  "min": 8, "max": 64},
            "processorSpeedMhz":    {"type": "integer",  "min": 2100, "max": 3800},
            "memoryMb":             {"type": "enum_int", "values": [32768, 65536, 131072, 262144, 524288]},
            "mpModel":              {"type": "enum",     "values": ["iLO5", "iLO6"]},
            "mpFirmwareVersion":    {"type": "version",  "major": 3, "minor_range": [0, 9]},
            "serialNumber":         {"type": "serial",   "length": 10},
            "partNumber":           {"type": "string"},
            "formFactor":           {"type": "enum",     "values": ["HalfHeight", "FullHeight", "TowerServer"]},
            "position":             {"type": "integer",  "min": 1, "max": 16},
            "serverProfileUri":     {"type": "ref",      "target": "server-profiles",      "nullable": True,  "mutable": False},
            "serverHardwareTypeUri":{"type": "ref",      "target": "server-hardware-types","nullable": False, "required": True},
            "serverGroupUri":       {"type": "ref",      "target": "enclosures",           "nullable": True},
            "locationUri":          {"type": "ref",      "target": "enclosures",           "nullable": True},
            "portMap":              {"type": "computed"},
        },
        "relationships": {
            "serverHardwareTypeUri": {"target": "server-hardware-types", "cascade": "restrict"},
            "serverProfileUri":      {"target": "server-profiles",       "cascade": "nullify",
                                      "bidirectional": "serverHardwareUri"},
            "serverGroupUri":        {"target": "enclosures",            "cascade": "nullify"},
        },
    },

    "server-hardware-types": {
        "type_name": "ServerHardwareTypeV3",
        "base_path": "/rest/server-hardware-types",
        "category": "SERVERS",
        "task_operations": set(),
        "task_duration_ms": 0,
        "fields": {
            "name":             {"type": "string"},
            "model":            {"type": "enum",    "values": ["ProLiant DL360 Gen10", "ProLiant DL380 Gen10", "ProLiant BL460c Gen10"]},
            "platform":         {"type": "enum",    "values": ["RackMount", "BladeSystem", "Synergy"]},
            "pxeBootPolicies":  {"type": "computed"},
            "bootModes":        {"type": "computed"},
        },
        "relationships": {},
    },

    "server-profiles": {
        "type_name": "ServerProfileV13",
        "base_path": "/rest/server-profiles",
        "category": "SERVERS",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 2500,
        "fields": {
            "name":                     {"type": "string"},
            "description":              {"type": "string"},
            "status":                   {"type": "enum",    "values": ["OK", "Warning", "Critical", "Disabled", "Unknown"]},
            "serverHardwareUri":        {"type": "ref",     "target": "server-hardware",          "nullable": True},
            "serverHardwareTypeUri":    {"type": "ref",     "target": "server-hardware-types",    "nullable": False, "required": True},
            "serverProfileTemplateUri": {"type": "ref",     "target": "server-profile-templates", "nullable": True},
            "enclosureUri":             {"type": "ref",     "target": "enclosures",               "nullable": True},
            "enclosureBay":             {"type": "integer", "min": 1, "max": 16},
            "affinity":                 {"type": "enum",    "values": ["Bay", "BayAndServer"]},
            "wipeForceNoPowerOff":      {"type": "boolean"},
            "connectionSettings":       {"type": "computed"},
            "boot":                     {"type": "computed"},
            "bios":                     {"type": "computed"},
            "localStorage":             {"type": "computed"},
            "sanStorage":               {"type": "computed"},
        },
        "relationships": {
            "serverHardwareUri":        {"target": "server-hardware",          "cascade": "nullify",
                                         "bidirectional": "serverProfileUri"},
            "serverHardwareTypeUri":    {"target": "server-hardware-types",    "cascade": "restrict"},
            "serverProfileTemplateUri": {"target": "server-profile-templates", "cascade": "nullify"},
            "enclosureUri":             {"target": "enclosures",               "cascade": "nullify"},
        },
    },

    "server-profile-templates": {
        "type_name": "ServerProfileTemplateV9",
        "base_path": "/rest/server-profile-templates",
        "category": "SERVERS",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 1200,
        "fields": {
            "name":                  {"type": "string"},
            "description":           {"type": "string"},
            "serverHardwareTypeUri": {"type": "ref", "target": "server-hardware-types", "nullable": False, "required": True},
            "enclosureGroupUri":     {"type": "ref", "target": "enclosure-groups",      "nullable": True},
            "affinity":              {"type": "enum", "values": ["Bay", "BayAndServer"]},
            "connectionSettings":    {"type": "computed"},
            "boot":                  {"type": "computed"},
            "bios":                  {"type": "computed"},
        },
        "relationships": {
            "serverHardwareTypeUri": {"target": "server-hardware-types", "cascade": "restrict"},
            "enclosureGroupUri":     {"target": "enclosure-groups",      "cascade": "nullify"},
        },
    },

    # ── NETWORKING ───────────────────────────────────────────────────────

    "ethernet-networks": {
        "type_name": "EthernetNetworkV4",
        "base_path": "/rest/ethernet-networks",
        "category": "NETWORKING",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 800,
        "fields": {
            "name":                     {"type": "string"},
            "vlanId":                   {"type": "integer",  "min": 1,   "max": 4094},
            "purpose":                  {"type": "enum",     "values": ["General", "Management", "FaultTolerance", "VMMigration", "iSCSI"]},
            "smartLink":                {"type": "boolean"},
            "privateNetwork":           {"type": "boolean"},
            "ethernetNetworkType":      {"type": "enum",     "values": ["Tagged", "Untagged", "Tunnel", "NotApplicable"]},
            "defaultTypicalBandwidth":  {"type": "integer",  "min": 100,  "max": 10000},
            "defaultMaximumBandwidth":  {"type": "integer",  "min": 100,  "max": 10000},
            "subnetUri":                {"type": "ref",      "target": "id-pools-ipv4-subnets", "nullable": True},
        },
        "relationships": {
            "subnetUri": {"target": "id-pools-ipv4-subnets", "cascade": "nullify"},
        },
    },

    "fc-networks": {
        "type_name": "FCNetworkV4",
        "base_path": "/rest/fc-networks",
        "category": "NETWORKING",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 800,
        "fields": {
            "name":                 {"type": "string"},
            "fabricType":           {"type": "enum",    "values": ["FabricAttach", "DirectAttach"]},
            "linkStabilityTime":    {"type": "integer", "min": 1,   "max": 1800},
            "autoLoginRedistribution": {"type": "boolean"},
            "managedSanUri":        {"type": "ref",     "target": "fc-sans/managed-sans", "nullable": True},
        },
        "relationships": {
            "managedSanUri": {"target": "fc-sans/managed-sans", "cascade": "nullify"},
        },
    },

    "network-sets": {
        "type_name": "NetworkSetV6",
        "base_path": "/rest/network-sets",
        "category": "NETWORKING",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 600,
        "fields": {
            "name":                     {"type": "string"},
            "networkUris":              {"type": "array_ref", "target": "ethernet-networks"},
            "defaultTypicalBandwidth":  {"type": "integer", "min": 100, "max": 10000},
            "defaultMaximumBandwidth":  {"type": "integer", "min": 100, "max": 10000},
        },
        "relationships": {
            "networkUris": {"target": "ethernet-networks", "cascade": "remove_from_array"},
        },
    },

    # ── STORAGE ──────────────────────────────────────────────────────────

    "storage-systems": {
        "type_name": "StorageSystemV5",
        "base_path": "/rest/storage-systems",
        "category": "STORAGE",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 3000,
        "fields": {
            "name":             {"type": "string"},
            "hostname":         {"type": "string", "pattern": "storage{n}.lab.local"},
            "family":           {"type": "enum",   "values": ["StoreServ", "StoreVirtual", "Nimble", "Primera"]},
            "model":            {"type": "enum",   "values": ["HPE 3PAR 8200", "HPE Primera 630", "HPE Nimble AF40"]},
            "firmware":         {"type": "version","major": 4, "minor_range": [1, 5]},
            "status":           {"type": "enum",   "values": ["OK", "Warning", "Critical", "Unknown"]},
            "totalCapacityGiB": {"type": "integer","min": 1000, "max": 100000},
            "freeCapacityGiB":  {"type": "integer","min": 100,  "max": 50000},
        },
        "relationships": {},
    },

    "storage-pools": {
        "type_name": "StoragePoolV4",
        "base_path": "/rest/storage-pools",
        "category": "STORAGE",
        "task_operations": set(),
        "task_duration_ms": 0,
        "fields": {
            "name":               {"type": "string"},
            "storageSystemUri":   {"type": "ref",     "target": "storage-systems",  "nullable": False, "required": True},
            "status":             {"type": "enum",    "values": ["OK", "Warning", "Critical"]},
            "totalCapacityGiB":   {"type": "integer", "min": 500,  "max": 50000},
            "freeCapacityGiB":    {"type": "integer", "min": 50,   "max": 25000},
            "raidLevel":          {"type": "enum",    "values": ["RAID5", "RAID6", "RAID1", "RAID10"]},
        },
        "relationships": {
            "storageSystemUri": {"target": "storage-systems", "cascade": "cascade-delete"},
        },
    },

    "volumes": {
        "type_name": "StorageVolumeV9",
        "base_path": "/rest/volumes",
        "category": "STORAGE",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 2000,
        "fields": {
            "name":             {"type": "string"},
            "description":      {"type": "string"},
            "storagePoolUri":   {"type": "ref",     "target": "storage-pools",   "nullable": False, "required": True},
            "storageSystemUri": {"type": "ref",     "target": "storage-systems", "nullable": True},
            "provisionedCapacityGiB": {"type": "integer", "min": 10, "max": 10000},
            "provisioningType": {"type": "enum",    "values": ["Thin", "Full", "Dedup"]},
            "isShareable":      {"type": "boolean"},
            "isBootVolume":     {"type": "boolean"},
            "status":           {"type": "enum",    "values": ["OK", "Warning", "Critical"]},
        },
        "relationships": {
            "storagePoolUri":   {"target": "storage-pools",   "cascade": "restrict"},
            "storageSystemUri": {"target": "storage-systems", "cascade": "nullify"},
        },
    },

    # ── FACILITIES ───────────────────────────────────────────────────────

    "enclosures": {
        "type_name": "EnclosureV7",
        "base_path": "/rest/enclosures",
        "category": "FACILITIES",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 3500,
        "fields": {
            "name":             {"type": "string",   "pattern": "Encl{n}"},
            "enclosureModel":   {"type": "enum",     "values": ["HPE BladeSystem c7000", "HPE Synergy 12000 Frame", "HPE Synergy 13000 Frame"]},
            "enclosureTypeUri": {"type": "ref",      "target": "enclosure-types", "nullable": True},
            "enclosureGroupUri":{"type": "ref",      "target": "enclosure-groups","nullable": True},
            "status":           {"type": "enum",     "values": ["OK", "Warning", "Critical", "Disabled", "Unknown"]},
            "deviceBayCount":   {"type": "integer",  "min": 8, "max": 16},
            "powerSupplyBayCount": {"type": "integer","min": 4,"max": 10},
            "fanBayCount":      {"type": "integer",  "min": 6, "max": 10},
            "serialNumber":     {"type": "serial",   "length": 10},
            "partNumber":       {"type": "string"},
            "rackName":         {"type": "string"},
        },
        "relationships": {
            "enclosureTypeUri":  {"target": "enclosure-types",  "cascade": "nullify"},
            "enclosureGroupUri": {"target": "enclosure-groups", "cascade": "nullify"},
        },
    },

    "enclosure-groups": {
        "type_name": "EnclosureGroupV9",
        "base_path": "/rest/enclosure-groups",
        "category": "FACILITIES",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 900,
        "fields": {
            "name":                 {"type": "string"},
            "enclosureCount":       {"type": "integer", "min": 1, "max": 4},
            "interconnectBayMappings": {"type": "computed"},
            "ipAddressingMode":     {"type": "enum", "values": ["DHCP", "External", "IPPOOL", "Unmanaged"]},
        },
        "relationships": {},
    },

    "racks": {
        "type_name": "RackV2",
        "base_path": "/rest/racks",
        "category": "FACILITIES",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 600,
        "fields": {
            "name":          {"type": "string", "pattern": "Rack-{n}"},
            "depth":         {"type": "integer","min": 600,  "max": 1200},
            "height":        {"type": "integer","min": 1400, "max": 2200},
            "width":         {"type": "integer","min": 400,  "max": 800},
            "uHeight":       {"type": "integer","min": 12,   "max": 42},
            "rackMounts":    {"type": "computed"},
        },
        "relationships": {},
    },

    # ── ACTIVITY ─────────────────────────────────────────────────────────

    "tasks": {
        "type_name": "TaskResourceV2",
        "base_path": "/rest/tasks",
        "category": "ACTIVITY",
        "task_operations": set(),
        "task_duration_ms": 0,
        "fields": {
            "taskType":              {"type": "enum",    "values": ["User", "Appliance", "Background"]},
            "taskState":             {"type": "enum",    "values": ["New", "Starting", "Running", "Suspended", "Completed", "Terminated", "Killed", "Error", "Warning", "Pending"]},
            "name":                  {"type": "string"},
            "percentComplete":       {"type": "integer", "min": 0, "max": 100},
            "stateReason":           {"type": "string"},
            "progressUpdates":       {"type": "computed"},
            "associatedResourceUri": {"type": "string"},
            "associatedResource":    {"type": "computed"},
            "owner":                 {"type": "string"},
        },
        "relationships": {},
    },

    "alerts": {
        "type_name": "AlertResourceV3",
        "base_path": "/rest/alerts",
        "category": "ACTIVITY",
        "task_operations": {"PUT"},
        "task_duration_ms": 0,
        "fields": {
            "alertTypeID":       {"type": "string"},
            "severity":          {"type": "enum",    "values": ["OK", "Warning", "Critical", "Unknown", "Disabled"]},
            "alertState":        {"type": "enum",    "values": ["Active", "Locked", "Cleared"]},
            "description":       {"type": "string"},
            "correctiveAction":  {"type": "string"},
            "resourceUri":       {"type": "string"},
            "resourceName":      {"type": "string"},
            "resourceCategory":  {"type": "string"},
            "changeLog":         {"type": "computed"},
        },
        "relationships": {},
    },

    "events": {
        "type_name": "EventResourceV2",
        "base_path": "/rest/events",
        "category": "ACTIVITY",
        "task_operations": set(),
        "task_duration_ms": 0,
        "fields": {
            "eventTypeID":      {"type": "string"},
            "severity":         {"type": "enum",    "values": ["OK", "Warning", "Critical", "Unknown"]},
            "description":      {"type": "string"},
            "resourceUri":      {"type": "string"},
            "resourceName":     {"type": "string"},
            "resourceCategory": {"type": "string"},
            "details":          {"type": "computed"},
        },
        "relationships": {},
    },

    # ── FIRMWARE ─────────────────────────────────────────────────────────

    "firmware-drivers": {
        "type_name": "FwDriverV1",
        "base_path": "/rest/firmware-drivers",
        "category": "FIRMWARE",
        "task_operations": {"DELETE"},
        "task_duration_ms": 1000,
        "fields": {
            "name":         {"type": "string", "pattern": "SPP{year}.{month}.{rev}"},
            "version":      {"type": "version","major": 2024, "minor_range": [1, 12]},
            "releaseDate":  {"type": "string"},
            "resourceType": {"type": "string"},
            "fwComponents": {"type": "computed"},
        },
        "relationships": {},
    },

    # ── SETTINGS ─────────────────────────────────────────────────────────

    "scopes": {
        "type_name": "ScopeV3",
        "base_path": "/rest/scopes",
        "category": "SETTINGS",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 500,
        "fields": {
            "name":         {"type": "string"},
            "description":  {"type": "string"},
        },
        "relationships": {},
    },
}


# ── Data Synthesizer ─────────────────────────────────────────────────────────

_ADJECTIVES = [
    "Primary", "Secondary", "Backup", "Staging", "Production",
    "Dev", "Test", "QA", "Demo", "Core", "Edge", "Main",
    "North", "South", "East", "West", "Central", "Lab",
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon",
]

_ALERT_DESCRIPTIONS = [
    "Fan redundancy reduced in enclosure bay {n}.",
    "iLO firmware update is recommended for server in bay {n}.",
    "Network connectivity lost on uplink {n}.",
    "Storage pool utilization exceeded 80%.",
    "Power redundancy lost — PSU {n} has failed.",
    "Temperature threshold exceeded in enclosure.",
    "SAN zone configuration mismatch detected.",
    "Firmware compliance check failed for server profile.",
]


def _make_uuid(seed: str) -> str:
    uid = hashlib.md5(seed.encode()).hexdigest()
    return f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"


def _serial(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def _version(major: int, minor_range: tuple[int, int]) -> str:
    minor = random.randint(*minor_range)
    patch = random.randint(0, 9)
    return f"{major}.{minor:02d}.{patch:02d}"


def synthesize_resource(
    resource_slug: str,
    index: int,
    schema: dict,
    existing_refs: dict[str, list[str]],
) -> dict:
    """
    Generate one realistic resource instance.

    Args:
        resource_slug : e.g. "server-hardware"
        index         : instance index (0-based) for determinism
        schema        : field schema dict from ONEVIEW_RESOURCE_SCHEMAS
        existing_refs : slug → list of existing URIs for reference resolution
    """
    resource_id = _make_uuid(f"{resource_slug}:{index}")
    base_path = schema.get("base_path", f"/rest/{resource_slug}")
    uri = f"{base_path}/{resource_id}"
    adj = _ADJECTIVES[index % len(_ADJECTIVES)]
    now_base = f"2025-0{(index % 9) + 1}-{(index % 28) + 1:02d}T{(index * 2) % 24:02d}:00:00.000Z"

    resource: dict[str, Any] = {
        "type":     schema.get("type_name", resource_slug),
        "uri":      uri,
        "eTag":     _make_uuid(f"etag:{resource_slug}:{index}"),
        "created":  now_base,
        "modified": now_base,
    }

    fields = schema.get("fields", {})

    for field_name, spec in fields.items():
        ftype = spec.get("type", "string")

        if ftype == "computed":
            resource[field_name] = _computed_field(field_name, resource_slug, index)

        elif ftype == "string":
            pattern = spec.get("pattern", "")
            if pattern:
                val = pattern.replace("{n}", str(index + 1))
                val = val.replace("{encl}", str((index // 4) + 1))
                val = val.replace("{bay}", str((index % 8) + 1))
                val = val.replace("{year}", "2024")
                val = val.replace("{month}", f"{(index % 12) + 1:02d}")
                val = val.replace("{rev}", f"{index + 1:02d}")
                resource[field_name] = val
            else:
                resource[field_name] = f"{adj} {resource_slug.replace('-', ' ').title()} {index + 1}"

        elif ftype == "enum":
            vals = spec.get("values", ["unknown"])
            resource[field_name] = vals[index % len(vals)]

        elif ftype == "enum_int":
            vals = spec.get("values", [0])
            resource[field_name] = vals[index % len(vals)]

        elif ftype == "integer":
            lo, hi = spec.get("min", 0), spec.get("max", 100)
            # Deterministic spread across the range
            step = max(1, (hi - lo) // 10)
            resource[field_name] = min(hi, lo + (index * step) % (hi - lo + 1))

        elif ftype == "boolean":
            resource[field_name] = bool(index % 2)

        elif ftype == "version":
            major = spec.get("major", 1)
            minor_range = tuple(spec.get("minor_range", [0, 9]))
            resource[field_name] = _version(major, minor_range)

        elif ftype == "serial":
            length = spec.get("length", 10)
            # Deterministic serial based on seed
            random.seed(f"{resource_slug}:{field_name}:{index}")
            resource[field_name] = _serial(length)
            random.seed()  # reset

        elif ftype == "ref":
            target = spec.get("target", "")
            nullable = spec.get("nullable", False)
            refs = existing_refs.get(target, [])
            if refs:
                resource[field_name] = refs[index % len(refs)]
            elif nullable:
                resource[field_name] = None
            else:
                resource[field_name] = None  # will be caught by validator

        elif ftype == "array_ref":
            target = spec.get("target", "")
            refs = existing_refs.get(target, [])
            # Pick 1-3 refs
            count = min(len(refs), max(1, (index % 3) + 1))
            resource[field_name] = refs[:count] if refs else []

    # Always add 'name' if not already set
    if "name" not in resource:
        resource["name"] = f"{adj} {resource_slug.replace('-', ' ').title()} {index + 1}"

    # Add 'description'
    if "description" not in resource and "description" in fields:
        resource["description"] = (
            f"Auto-generated {resource_slug.replace('-', ' ')} instance #{index + 1}"
        )

    return resource


def _computed_field(field_name: str, resource_slug: str, index: int) -> Any:
    """Return a sensible placeholder for complex nested computed fields."""
    computed_defaults: dict[str, Any] = {
        "portMap": {
            "deviceSets": [
                {
                    "deviceSlots": [
                        {
                            "slotNumber": 1,
                            "location": "Flb",
                            "physicalFunctionCount": 2,
                            "ports": [
                                {"portNumber": 0, "portName": "1", "type": "Ethernet"},
                                {"portNumber": 1, "portName": "2", "type": "Ethernet"},
                            ],
                        }
                    ]
                }
            ]
        },
        "connectionSettings": {
            "manageConnections": True,
            "connections": [],
        },
        "boot": {
            "manageBoot": True,
            "order": ["HardDisk", "PXE"],
        },
        "bios": {
            "manageBios": False,
            "overriddenSettings": [],
        },
        "localStorage": {
            "sasLogicalJBODs": [],
            "controllers": [],
        },
        "sanStorage": {
            "manageSanStorage": False,
            "hostOSType": "Windows 2012 / WS2012 R2",
            "volumeAttachments": [],
        },
        "progressUpdates": [],
        "fwComponents": [
            {"componentVersion": "1.0.0", "componentName": "System ROM", "swKeyNameList": ["P89"]},
        ],
        "interconnectBayMappings": [],
        "rackMounts": [],
        "bootModes": [{"mode": "UEFI", "pxeBootPolicy": "Auto"}],
        "pxeBootPolicies": [{"macAddress": f"AA:BB:CC:DD:EE:{index:02X}"}],
        "associatedResource": {
            "resourceName": f"Resource-{index + 1}",
            "associationType": "MANAGED_BY",
        },
        "changeLog": [],
        "details": [],
    }
    return computed_defaults.get(field_name, {})


# ── Relationship Graph Engine ─────────────────────────────────────────────────


class ResourceGraph:
    """
    Enforces referential integrity across all resource types.

    Wraps the raw database engine (injected at runtime) and applies
    the cascade / nullify / restrict rules from ONEVIEW_RESOURCE_SCHEMAS
    before every mutating operation.
    """

    def __init__(self, db: Any) -> None:
        self.db = db
        self.schemas = ONEVIEW_RESOURCE_SCHEMAS

    def get_schema(self, resource_type: str) -> Optional[dict]:
        return self.schemas.get(resource_type)

    async def validate_references(
        self, resource_type: str, data: dict
    ) -> list[str]:
        """
        Check that every ref field points to an existing resource.
        Returns a list of error strings (empty = all good).
        """
        schema = self.get_schema(resource_type)
        if not schema:
            return []

        errors: list[str] = []
        fields = schema.get("fields", {})

        for field_name, spec in fields.items():
            ftype = spec.get("type", "")
            value = data.get(field_name)

            if ftype == "ref" and value is not None:
                target_slug = spec.get("target", "")
                exists = await self.db.resource_exists_by_uri(target_slug, value)
                if not exists:
                    nullable = spec.get("nullable", False)
                    required = spec.get("required", False)
                    if required:
                        errors.append(
                            f"Required reference {field_name}={value!r} "
                            f"not found in {target_slug}"
                        )
                    elif not nullable:
                        errors.append(
                            f"Reference {field_name}={value!r} "
                            f"not found in {target_slug}"
                        )

            elif ftype == "array_ref":
                target_slug = spec.get("target", "")
                uris: list = value if isinstance(value, list) else []
                for uri in uris:
                    exists = await self.db.resource_exists_by_uri(target_slug, uri)
                    if not exists:
                        errors.append(
                            f"Array reference {field_name}[] contains "
                            f"unknown URI {uri!r} (target: {target_slug})"
                        )

        return errors

    async def apply_delete_cascades(
        self, resource_type: str, resource_uri: str
    ) -> list[str]:
        """
        When a resource is deleted, apply cascade rules to dependents.
        Returns list of log messages describing what was cascaded.
        """
        schema = self.get_schema(resource_type)
        if not schema:
            return []

        log: list[str] = []

        # Find all other schemas that reference this resource_type
        for other_slug, other_schema in self.schemas.items():
            for field_name, rel in other_schema.get("relationships", {}).items():
                if rel.get("target") != resource_type:
                    continue

                cascade = rel.get("cascade", "nullify")
                dependent_resources = await self.db.find_by_field_uri(
                    other_slug, field_name, resource_uri
                )

                for dep in dependent_resources:
                    dep_uri = dep.get("uri", "?")

                    if cascade == "cascade-delete":
                        await self.db.delete_resource(other_slug, dep_uri)
                        log.append(f"CASCADE DELETE: {other_slug} {dep_uri}")

                    elif cascade == "nullify":
                        await self.db.patch_resource(
                            other_slug, dep_uri, {field_name: None}
                        )
                        log.append(f"NULLIFY: {other_slug} {dep_uri} .{field_name} = null")

                    elif cascade == "restrict":
                        log.append(
                            f"RESTRICT: Cannot delete {resource_type} {resource_uri} "
                            f"— referenced by {other_slug} {dep_uri} .{field_name}"
                        )

                    elif cascade == "remove_from_array":
                        current: list = dep.get(field_name, [])
                        updated = [u for u in current if u != resource_uri]
                        await self.db.patch_resource(
                            other_slug, dep_uri, {field_name: updated}
                        )
                        log.append(
                            f"REMOVE FROM ARRAY: {other_slug} {dep_uri} "
                            f".{field_name} removed {resource_uri}"
                        )

        return log

    async def apply_bidirectional_link(
        self,
        resource_type: str,
        resource_uri: str,
        data: dict,
    ) -> None:
        """
        After creating/updating a resource, update the reverse-link field on
        any referenced resource that has a `bidirectional` relationship declared.
        """
        schema = self.get_schema(resource_type)
        if not schema:
            return

        for field_name, rel in schema.get("relationships", {}).items():
            back_field = rel.get("bidirectional")
            if not back_field:
                continue

            target_uri = data.get(field_name)
            if not target_uri:
                continue

            target_slug = rel.get("target", "")
            await self.db.patch_resource(
                target_slug, target_uri, {back_field: resource_uri}
            )

    def has_restrict_blocker(
        self, resource_type: str, resource_uri: str, dependents: list[dict]
    ) -> bool:
        """Return True if any restrict cascade would block deletion."""
        schema = self.get_schema(resource_type)
        if not schema:
            return False

        for other_slug, other_schema in self.schemas.items():
            for _, rel in other_schema.get("relationships", {}).items():
                if rel.get("target") == resource_type and rel.get("cascade") == "restrict":
                    return bool(dependents)

        return False
