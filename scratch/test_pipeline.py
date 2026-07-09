import re
from typing import Dict, Tuple, List, Any

NOISE_STOP_WORDS = [
    "the", "a", "an", "of", "for", "on", "at", "to", "my", "our", "their", "is", "was", "be", "about", "from", "in", "are",
    "what", "who", "where", "how", "when", "could", "can", "would", "will", "do", "does", "did",
    "please", "kindly", "just", "now", "tell", "me", "show", "give", "i", "we", "us", "need", "want", "you", "it", "this", "that",
    "named", "called", "name", "with", "by", "having", "new"
]

NOISE_RESOURCE_TYPES = [
    "device", "resource", "system", "systems", "storage-system", "storage_system", "storage-systems", "storage_systems",
    "storage-pool", "storage_pool", "storage-pools", "storage_pools", "storage-volume", "storage_volume", "storage-volumes", "storage_volumes",
    "server", "switch", "switches", "router", "routers", "firewall", "storage", "node", "nodes", "database", "db", "virtual", "machine", "vm", "array", "network", "volume"
]

NOISE_ATTRIBUTES = [
    "health", "firmware", "version", "temperature", "status", "capacity", "free", "total", "power", "memory", "cpu", "cores", "state"
]

ALL_NOISE = set(NOISE_STOP_WORDS + NOISE_RESOURCE_TYPES + NOISE_ATTRIBUTES)

# Use (?:\s+|$) to avoid splitting hyphenated words like switch-01
PREFIX_PATTERN = re.compile(r'^(?:' + '|'.join(map(re.escape, ALL_NOISE)) + r')(?:\s+|$)', re.IGNORECASE)
SUFFIX_PATTERN = re.compile(r'(?:^|\s+)(?:' + '|'.join(map(re.escape, ALL_NOISE)) + r')$', re.IGNORECASE)

PAYLOAD_PATTERNS = [
    re.compile(r'^(?P<attr>.+?)\s+of\s+(?P<ident>.+?)\s+to\s+(?P<val>.+)$', re.IGNORECASE),
    re.compile(r'^(?P<attr>.+?)\s+to\s+(?P<val>.+?)\s+for\s+(?P<ident>.+)$', re.IGNORECASE),
    re.compile(r'^(?P<attr>.+?)\s+to\s+(?P<val>.+)$', re.IGNORECASE),
]

def extract_payload(remaining_query: str, action: str) -> Tuple[Dict[str, Any], str]:
    if action == "UPDATE":
        for pat in PAYLOAD_PATTERNS:
            m = pat.search(remaining_query)
            if m:
                d = m.groupdict()
                attr = d.get("attr").strip().replace(" ", "_") if d.get("attr") else ""
                val = d.get("val").strip() if d.get("val") else ""
                ident = d.get("ident").strip() if d.get("ident") else ""
                
                return {"attribute": attr, "value": val}, ident
    return {}, remaining_query

def clean_identifier(query: str) -> str:
    prev = None
    while query != prev:
        prev = query
        query = PREFIX_PATTERN.sub('', query).strip()
        query = SUFFIX_PATTERN.sub('', query).strip()
    return query

test_rem = [
    ("firmware version of switch-01 to 1.2.3", "UPDATE"),
    ("status to offline for gl-ns-008", "UPDATE"),
    ("health status to OK", "UPDATE"),
    ("apollo-node-097", "UPDATE"),
    ("new storage array named alletra-999", "CREATE"),
    ("health of all routers", "STATUS"),
    ("firmware of apollo-node-029 to 2.1.0", "UPDATE"),
]

for rem, act in test_rem:
    payload, new_rem = extract_payload(rem, act)
    ident = clean_identifier(new_rem)
    print(f"[{rem}] -> Payload: {payload}, Identifier: '{ident}', Remainder: '{new_rem}'")
