import sys
import re

with open(r'c:\AgenticAI_HPE\resource_resolver\query_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace everything from _FAIL_CLOSED_PAYLOAD to the end of _parse, and then replace parse_update_payload.
# But we must preserve parse_query_hybrid and parse_query.

new_registries_and_parse = '''
_FAIL_CLOSED_PAYLOAD: dict = {
    "identifier": "",
    "action": "UNPARSEABLE",
    "category": "Error",
    "raw_query": "",
}

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

class ActionRegistryItem(NamedTuple):
    action: str
    category: str
    pattern: re.Pattern

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

NOISE_GENERIC = [
    "device", "devices", "resource", "system", "systems"
]

NOISE_ATTRIBUTES = [
    "health", "firmware", "version", "temperature", "status", "capacity", "free", "total", "power", "memory", "cpu", "cores", "state"
]

ALL_NOISE = set(NOISE_STOP_WORDS + NOISE_GENERIC + NOISE_ATTRIBUTES)
PREFIX_PATTERN = re.compile(r'^(?:' + '|'.join(map(re.escape, ALL_NOISE)) + r')(?:\s+|$)', re.IGNORECASE)
SUFFIX_PATTERN = re.compile(r'(?:^|\s+)(?:' + '|'.join(map(re.escape, ALL_NOISE)) + r')$', re.IGNORECASE)

PAYLOAD_PATTERNS = [
    re.compile(r'^(?P<attr>.+?)\\s+of\\s+(?P<ident>.+?)\\s+to\\s+(?P<val>.+)$', re.IGNORECASE),
    re.compile(r'^(?P<attr>.+?)\\s+to\\s+(?P<val>.+?)\\s+for\\s+(?P<ident>.+)$', re.IGNORECASE),
    re.compile(r'^(?P<attr>.+?)\\s+to\\s+(?P<val>.+)$', re.IGNORECASE),
]

# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------
'''

content_split_1 = content.split('_FAIL_CLOSED_PAYLOAD: dict = {')[0]
content_split_2 = content.split('# ---------------------------------------------------------------------------\\n# Validators')[1]

part_2_up_to_class = content_split_2.split('class QueryAgent:')[0]
part_2_after_class = content_split_2.split('class QueryAgent:')[1]

new_query_agent_top = '''class QueryAgent:
    """
    Lightweight, stateless, deterministic NLP preprocessing layer.
    """

    @staticmethod
    def _coerce_value(val_str: str) -> str | int | float | bool:
        v = val_str.lower()
        if v in {"true", "yes", "on", "enable", "enabled"}: return True
        if v in {"false", "no", "off", "disable", "disabled"}: return False
        try: return int(val_str)
        except ValueError: pass
        try: return float(val_str)
        except ValueError: pass
        return val_str

    @staticmethod
    def _parse(query: str) -> dict:
        """Pipeline extraction of action, identifier, and payload."""
        if not query or not isinstance(query, str):
            return _FAIL_CLOSED_PAYLOAD.copy()

        # 1. Normalization
        q = " ".join(query.lower().strip().split())
        punctuation_to_strip = ".,;:!?()[]\\\"'"
        q = q.strip(punctuation_to_strip)

        # 2. Action Detection
        action = "STATUS"
        category = "Operational"
        remaining_query = q
        
        for reg_item in ACTION_REGISTRY:
            m = reg_item.pattern.search(remaining_query)
            if m:
                action = reg_item.action
                category = reg_item.category
                remaining_query = remaining_query[:m.start()] + remaining_query[m.end():]
                remaining_query = " ".join(remaining_query.split())
                break

        # 3. Payload Extraction
        payload_dict = {}
        if action == "UPDATE":
            for pat in PAYLOAD_PATTERNS:
                m = pat.search(remaining_query)
                if m:
                    d = m.groupdict()
                    attr = d.get("attr", "").strip().replace(" ", "_")
                    val = d.get("val", "").strip()
                    ident = d.get("ident", "").strip()
                    
                    if attr in _FIELD_ALIASES:
                        attr = _FIELD_ALIASES[attr]
                        
                    payload_dict = {"attribute": attr, "value": val}
                    if ident:
                        remaining_query = ident
                    else:
                        remaining_query = remaining_query[:m.start()] + remaining_query[m.end():]
                    remaining_query = " ".join(remaining_query.split())
                    break

        # 4. Identifier Extraction
        prev = None
        identifier = remaining_query
        
        # Guard clause: if it's already empty, don't try to strip
        while identifier != prev and identifier:
            prev = identifier
            identifier = PREFIX_PATTERN.sub('', identifier).strip()
            identifier = SUFFIX_PATTERN.sub('', identifier).strip()

        if not identifier and remaining_query:
            if remaining_query in ["all", "all routers", "all switches", "all devices", "network"]:
                identifier = remaining_query

        # 5. Extract resource type ONLY (no device type inference)
        resource_type = ""
        words = identifier.lower().split()
        if any(k in words for k in ['firmware', 'firmwares']): resource_type = 'firmware'
        elif any(k in words for k in ['sensor', 'sensors', 'thermal', 'temperature']): resource_type = 'sensor'
        elif any(k in words for k in ['inventory', 'hardware', 'hw']): resource_type = 'inventory'
        elif any(k in words for k in ['media', 'iso', 'image']): resource_type = 'media'
        elif any(k in words for k in ['certificate', 'certificates', 'ca']): resource_type = 'certificate'
        elif any(k in words for k in ['metric', 'metrics', 'telemetry']): resource_type = 'metric'
        elif any(k in words for k in ['account', 'accounts', 'user', 'users']): resource_type = 'account'
        elif any(k in words for k in ['session', 'sessions', 'login']): resource_type = 'session'
        elif any(k in words for k in ['event', 'events', 'log', 'logs']): resource_type = 'event'
        elif any(k in words for k in ['license', 'licenses']): resource_type = 'license'
        elif any(k in words for k in ['profile', 'profiles']): resource_type = 'profile'
        elif any(k in words for k in ['power', 'powerstate']): resource_type = 'power'
        elif any(k in words for k in ['issue', 'issues', 'alert', 'alerts']): resource_type = 'issue'
        elif any(k in words for k in ['port', 'ports', 'interface', 'interfaces']): resource_type = 'port'
        elif any(k in words for k in ['route', 'routes']): resource_type = 'route'

        # Strip resource_type from identifier if present
        if resource_type:
            noise_words = {
                'firmware', 'firmwares', 'certificate', 'certificates', 'ca', 'metric', 'metrics', 'telemetry',
                'account', 'accounts', 'user', 'users', 'session', 'sessions', 'login', 'event', 'events', 'log', 'logs',
                'license', 'licenses', 'profile', 'profiles', 'power', 'powerstate', 'issue', 'issues', 'alert', 'alerts',
                'port', 'ports', 'interface', 'interfaces', 'route', 'routes',
                'sensor', 'sensors', 'thermal', 'temperature', 'inventory', 'hardware', 'hw', 'media', 'iso', 'image'
            }
            identifier = " ".join([w for w in identifier.split() if w.lower() not in noise_words]).strip()
        
        # Strip generic noise again just in case (e.g. "for" after resource_type removal)
        prev = None
        while identifier != prev and identifier:
            prev = identifier
            identifier = PREFIX_PATTERN.sub('', identifier).strip()
            identifier = SUFFIX_PATTERN.sub('', identifier).strip()

        # Confidence Scoring
        confidence = 0.9 
        if not identifier:
            confidence = 0.5
        elif action == "STATUS" and remaining_query == q:
            confidence = 0.7
            
        if identifier in {"it", "this", "that", "the device", "the server", "the system"}:
            confidence = 0.2
            identifier = ""
            
        if action == "UNPARSEABLE":
            confidence = 0.1

        # Determine attributes payload
        attributes = []
        if payload_dict:
            attributes.append({"key": payload_dict["attribute"], "value": QueryAgent._coerce_value(payload_dict["value"])})

        return {
            "identifier": identifier,
            "action": action,
            "category": category,
            "resource_type": resource_type,
            "attributes": attributes,
            "multi_intent": False,
            "ambiguous": confidence < 0.4,
            "confidence": confidence,
            "raw_query": query,
        }
'''

parse_query_and_below = '    @staticmethod\\n    def parse_query(query: str) -> dict:' + part_2_after_class.split('    @staticmethod\\n    def parse_query(query: str) -> dict:')[1]

# We need to replace parse_update_payload!
parse_update_payload_new = '''    @staticmethod
    def parse_update_payload(query: str) -> dict | None:
        """Extract attribute and value for UPDATE actions."""
        res = QueryAgent._parse(query)
        if res.get("action") == "UPDATE" and res.get("attributes"):
            return {"attribute": res["attributes"][0]["key"], "value": res["attributes"][0]["value"]}
        return None

def parse_query_hybrid(query: str) -> dict:'''

parse_query_and_below = parse_query_and_below.split('    @staticmethod\\n    def parse_update_payload(query: str) -> dict | None:')[0] + parse_update_payload_new + parse_query_and_below.split('def parse_query_hybrid(query: str) -> dict:')[1]

final_content = content_split_1 + new_registries_and_parse + part_2_up_to_class + new_query_agent_top + parse_query_and_below

with open(r'c:\AgenticAI_HPE\resource_resolver\query_agent.py', 'w', encoding='utf-8') as f:
    f.write(final_content)
