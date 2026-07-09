import sys

FILE_CONTENT = '''"""
Lightweight deterministic NLP Query Agent for intent and identifier extraction.
Hybrid fallback to LLM for complex queries.
"""

from __future__ import annotations

import logging
import re
import os
import json
import urllib.request
import urllib.error
import ipaddress
import string
from typing import NamedTuple, List, Literal, Union, Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------------------------

QUERY_AGENT_CONFIDENCE_THRESHOLD = float(os.environ.get("QUERY_AGENT_CONFIDENCE_THRESHOLD", "0.7"))
OLLAMA_MODEL: str = os.environ.get("QUERY_AGENT_LLM_MODEL", "qwen2.5:7b")
OLLAMA_TIMEOUT: float = float(os.environ.get("QUERY_AGENT_LLM_TIMEOUT", "3.0"))

_FALLBACK_PAYLOAD: dict = {
    "identifier": "",
    "action": "STATUS",
    "category": "Operational",
    "raw_query": "",
}

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
    re.compile(r'^(?P<attr>.+?)\\s+of\\s+(?P<ident>.+?)\\s+to\\s+(?P<val>.+)$', re.IGNORECASE),
    re.compile(r'^(?P<attr>.+?)\\s+to\\s+(?P<val>.+?)\\s+for\\s+(?P<ident>.+)$', re.IGNORECASE),
    re.compile(r'^(?P<attr>.+?)\\s+to\\s+(?P<val>.+)$', re.IGNORECASE),
]

# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

VALID_ACTIONS = {
    "ON", "OFF", "RESET", "RELOAD", "COLD_BOOT", "STATUS", "LIST",
    "CREATE", "DELETE", "ALLOCATE", "DEALLOCATE", "UPDATE",
    "FETCH_EVENT_LOG", "CLEAR_EVENT_LOG", "DISCOVER_INVENTORY",
    "MOUNT_VIRTUAL_MEDIA", "FETCH_SENSORS", "SYNC_CMDB",
    "POLICY_SYNC", "FAILOVER", "FAILBACK", "RESCAN"
}
VALID_CATEGORIES = {"Operational", "Provisioning"}

def _validate_action(action: str) -> bool:
    return isinstance(action, str) and action in VALID_ACTIONS

def _validate_category(category: str) -> bool:
    return isinstance(category, str) and category in VALID_CATEGORIES

def _validate_identifier(identifier: str) -> bool:
    if not identifier:
        return False
    try:
        ipaddress.ip_address(identifier)
        return True
    except ValueError:
        pass
    if "." in identifier:
        if re.match(r"^[a-zA-Z0-9\-\.]+$", identifier):
            return True
    if re.match(r"^[a-zA-Z0-9\-\_\.]+$", identifier) and len(identifier) >= 3:
        return True
    return False

# ---------------------------------------------------------------------------
# LLM Provider Layer
# ---------------------------------------------------------------------------

class AttributeItem(BaseModel):
    key: str
    value: Union[str, int, float, bool]

class LLMQuerySchema(BaseModel):
    identifier: str = Field(description="The canonical device name, IP address, or serial number.")
    action: str = Field(description="The explicit normalized action intent.")
    category: Literal["Operational", "Provisioning"]
    resource_type: str = Field(default="", description="The specific resource being managed.")
    attributes: List[AttributeItem] = Field(default_factory=list)
    multi_intent: bool = Field(default=False)
    ambiguous: bool = Field(default=False, description="Set to true if there is linguistic syntactic ambiguity.")
    unhandled: str = Field(default="")
    confidence: float = Field(ge=0.0, le=1.0)
    raw_query: str = Field(default="")

def _dispatch_llm_provider(prompt: str, schema: Dict[str, Any], provider_name: str) -> Dict[str, Any]:
    if provider_name == "ollama":
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "format": schema,
            "stream": False
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as response:
                res_data = response.read().decode("utf-8")
                res_json = json.loads(res_data)
                response_text = res_json.get("response", "").strip()
                return json.loads(response_text)
        except Exception as e:
            return {"_error": f"{type(e).__name__}: {e}"}
    return {"_error": f"Provider '{provider_name}' not implemented"}

def _llm_extract(query: str) -> dict | None:
    providers = []
    primary = os.environ.get("QUERY_AGENT_LLM_PROVIDER", "ollama").lower()
    secondary = os.environ.get("QUERY_AGENT_LLM_PROVIDER_SECONDARY", "").lower()
    if primary: providers.append(primary)
    if secondary and secondary != primary: providers.append(secondary)
    if not providers: providers.append("ollama")

    schema = LLMQuerySchema.model_json_schema()
    prompt = (
        "You are a deterministic natural-language infrastructure command parser.\\n"
        "Your job is ONLY to extract information explicitly stated in the user's query.\\n"
        "Output ONLY a JSON object matching the provided JSON schema.\\n"
        "\\n"
        f"User query: {query}\\n"
        f"JSON Schema: {json.dumps(schema)}"
    )

    for idx, provider in enumerate(providers):
        res = _dispatch_llm_provider(prompt, schema, provider)
        if "_error" in res:
            logger.debug(f"[QueryAgent] LLM provider '{provider}' failed: {res['_error']}")
            continue
            
        action = res.get("action", "")
        category = res.get("category", "")
        if not _validate_action(action) or not _validate_category(category):
            print(f"[QueryAgent] LLM returned invalid action/category | provider={provider}")
            continue
            
        return {
            "identifier": res.get("identifier", ""),
            "action": action,
            "category": category,
            "resource_type": res.get("resource_type", ""),
            "attributes": res.get("attributes", []),
            "multi_intent": res.get("multi_intent", False),
            "ambiguous": res.get("ambiguous", False),
            "confidence": res.get("confidence", 0.0),
            "raw_query": query,
            "llm_fallback_used": True,
            "llm_provider": provider
        }

    print("[QueryAgent] Returning fallback result | reason='All LLM providers failed and Regex confidence was low. Failing closed.'")
    return None

# ---------------------------------------------------------------------------
# Query Agent
# ---------------------------------------------------------------------------

class QueryAgent:
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

        # If stripping everything resulted in empty identifier but we had something before,
        # it means the identifier itself was entirely composed of noise words (e.g. "all routers").
        # If the user passed "all routers" and action is STATUS or LIST, restoring it allows downstreams to parse it.
        # So we restore if identifier is empty but remaining_query was not.
        if not identifier and remaining_query:
            if remaining_query in ["all", "all routers", "all switches", "all devices", "network"]:
                identifier = remaining_query

        # Extract resource type for downstream schema consistency
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
        
        # 5. Confidence Scoring
        confidence = 0.9 
        if not identifier:
            confidence = 0.5
        elif action == "STATUS" and remaining_query == q:
            # If nothing was parsed out and it just defaulted to STATUS
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

    @staticmethod
    def parse_query_llm(query: str) -> dict:
        llm_res = _llm_extract(query)
        if llm_res and "identifier" in llm_res:
            return llm_res
        return _FAIL_CLOSED_PAYLOAD.copy()

    @staticmethod
    def parse_query_hybrid(query: str) -> dict:
        regex_res = QueryAgent._parse(query)
        if regex_res.get("confidence", 0.0) >= QUERY_AGENT_CONFIDENCE_THRESHOLD:
            return regex_res
        
        llm_res = QueryAgent.parse_query_llm(query)
        if llm_res.get("action") == "UNPARSEABLE":
            return regex_res
        return llm_res

    @staticmethod
    def parse_query(query: str) -> dict:
        return QueryAgent.parse_query_hybrid(query)

    @staticmethod
    def parse_update_payload(query: str) -> dict | None:
        res = QueryAgent._parse(query)
        if res.get("action") == "UPDATE" and res.get("attributes"):
            return {"attribute": res["attributes"][0]["key"], "value": res["attributes"][0]["value"]}
        return None
'''

with open(r'c:\AgenticAI_HPE\resource_resolver\query_agent.py', 'w', encoding='utf-8') as f:
    f.write(FILE_CONTENT)
