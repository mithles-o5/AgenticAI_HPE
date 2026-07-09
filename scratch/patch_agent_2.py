import re

with open(r'c:\AgenticAI_HPE\resource_resolver\query_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the registry section
match = re.search(r'_FAIL_CLOSED_PAYLOAD: dict = \{.*?\}', content, re.DOTALL)
if match:
    # First, let's inject _FIELD_ALIASES right after _FAIL_CLOSED_PAYLOAD
    registry_code = '''

# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------

_FIELD_ALIASES = {
    "temperature":           "temperature_celsius",
    "temp":                  "temperature_celsius",
    "health":                "health_status",
    "health status":         "health_status",
    "status":                "health_status",
    "free capacity":         "free_capacity_gb",
    "free_capacity":         "free_capacity_gb",
    "free storage":          "free_storage_gb",
    "total capacity":        "total_capacity_gb",
    "total_capacity":        "total_capacity_gb",
    "firmware":              "firmware_version",
    "firmware version":      "firmware_version",
    "power":                 "power_state",
    "power state":           "power_state",
    "memory":                "memory_gb",
    "cpu":                   "cpu_cores",
    "cpu cores":             "cpu_cores",
}

class ActionRegistryItem:
    def __init__(self, action, category, pattern):
        self.action = action
        self.category = category
        self.pattern = pattern

ACTION_ALIASES = {
    "ON": r"\\b(poweron|turn on|power on|start)\\b",
    "OFF": r"\\b(poweroff|turn off|power off|shutdown)\\b",
    "COLD_BOOT": r"\\b(cold boot|hard reset)\\b",
    "FETCH_EVENT_LOG": r"\\b(event log|event logs|system log|system logs|sel|log entries|iml|integrated management log)\\b",
    "CLEAR_EVENT_LOG": r"\\b(clear.*log|reset.*log|wipe.*log|erase.*log)\\b",
    "DISCOVER_INVENTORY": r"\\b(hardware inventory|inventory|discover.*hardware|hw inventory|discover.*inventory)\\b",
    "MOUNT_VIRTUAL_MEDIA": r"\\b(mount|virtual media|insert.*media|attach.*iso|mount.*iso|mount.*image|attach.*image)\\b",
    "FETCH_SENSORS": r"\\b(sensor|sensors|thermal|fan|psu|power supply|environmental|inlet temperature|fan speed)\\b",
    "SYNC_CMDB": r"\\b(cmdb sync|sync cmdb|poll cycle|trigger.*poll|manual poll|sync.*metrics|poll.*trigger)\\b",
    "UPDATE": r"\\b(change|update|set|modify|configure|patch)\\b",
    "RESET": r"\\b(reboot|restart|reset)\\b",
    "RELOAD": r"\\b(reload)\\b",
    "POLICY_SYNC": r"\\b(policy sync|sync)\\b",
    "FAILOVER": r"\\b(failover)\\b",
    "FAILBACK": r"\\b(failback)\\b",
    "RESCAN": r"\\b(rescan)\\b",
    "LIST": r"\\b(list)\\b",
    "STATUS": r"\\b(status|check|state|lookup|show|find|get|retrieve|fetch|read|display)\\b",
    "CREATE": r"\\b(provision|create)\\b",
    "ALLOCATE": r"\\b(allocate|deploy)\\b",
    "DEALLOCATE": r"\\b(deallocate|release)\\b",
    "DELETE": r"\\b(deprovision|destroy|delete|nuke)\\b",
}

import re
ACTION_REGISTRY = []
for act, pattern in ACTION_ALIASES.items():
    category = "Provisioning" if act in ["CREATE", "ALLOCATE", "DEALLOCATE", "DELETE"] else "Operational"
    ACTION_REGISTRY.append(ActionRegistryItem(act, category, re.compile(pattern, re.IGNORECASE)))

NOISE_STOP_WORDS = [
    "the", "a", "an", "of", "for", "on", "at", "to", "my", "our", "their", "is", "was", "be", "about", "from", "in", "are",
    "what", "who", "where", "how", "when", "could", "can", "would", "will", "do", "does", "did",
    "please", "kindly", "just", "now", "tell", "me", "show", "give", "i", "we", "us", "need", "want", "you", "it", "this", "that",
    "named", "called", "name", "with", "by", "having", "new"
]

NOISE_RESOURCE_TYPES = [
    "device", "devices", "resource", "system", "systems", "storage-system", "storage_system", "storage-systems", "storage_systems",
    "storage-pool", "storage_pool", "storage-pools", "storage_pools", "storage-volume", "storage_volume", "storage-volumes", "storage_volumes",
    "server", "switch", "switches", "router", "routers", "firewall", "storage", "node", "nodes", "database", "db", "virtual", "machine", "vm", "array", "network", "volume"
]

NOISE_ATTRIBUTES = [
    "health", "firmware", "version", "temperature", "status", "capacity", "free", "total", "power", "memory", "cpu", "cores", "state"
]

ALL_NOISE = set(NOISE_STOP_WORDS + NOISE_RESOURCE_TYPES + NOISE_ATTRIBUTES)
PREFIX_PATTERN = re.compile(r'^(?:' + '|'.join(map(re.escape, ALL_NOISE)) + r')(?:\s+|$)', re.IGNORECASE)
SUFFIX_PATTERN = re.compile(r'(?:^|\s+)(?:' + '|'.join(map(re.escape, ALL_NOISE)) + r')$', re.IGNORECASE)

PAYLOAD_PATTERNS = [
    re.compile(r'^(?P<attr>.+?)\s+of\s+(?P<ident>.+?)\s+to\s+(?P<val>.+)$', re.IGNORECASE),
    re.compile(r'^(?P<attr>.+?)\s+to\s+(?P<val>.+?)\s+for\s+(?P<ident>.+)$', re.IGNORECASE),
    re.compile(r'^(?P<attr>.+?)\s+to\s+(?P<val>.+)$', re.IGNORECASE),
]
'''
    # I need to find the _FAIL_CLOSED_PAYLOAD and replace from there to class QueryAgent
    # Wait, earlier I already replaced everything! 
    # Let's just rewrite the whole file from scratch using a python script.

'''
