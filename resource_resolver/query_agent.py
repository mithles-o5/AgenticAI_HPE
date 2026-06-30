"""Lightweight deterministic NLP Query Agent for intent and identifier extraction.
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
from typing import NamedTuple, List, Literal, Union, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------------------------

QUERY_AGENT_CONFIDENCE_THRESHOLD = float(os.environ.get("QUERY_AGENT_CONFIDENCE_THRESHOLD", "0.7"))
OLLAMA_MODEL: str = os.environ.get("QUERY_AGENT_LLM_MODEL", "qwen2.5:7b")
OLLAMA_TIMEOUT: float = float(os.environ.get("QUERY_AGENT_LLM_TIMEOUT", "3.0"))

class _Mapping(NamedTuple):
    pattern: re.Pattern
    action: str
    category: str

def _compile(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)

_ACTION_MAPPINGS: tuple[_Mapping, ...] = (
    _Mapping(_compile(r"\b(turn on|power on|start)\b"),              "ON",            "Operational"),
    _Mapping(_compile(r"\b(turn off|power off|shutdown)\b"),          "OFF",           "Operational"),
    _Mapping(_compile(r"\b(cold boot)\b"),                            "COLD_BOOT",     "Operational"),
    _Mapping(_compile(r"\b(event log|event logs|system log|system logs|sel|log entries|iml|integrated management log)\b"),
                                                                      "FETCH_EVENT_LOG", "Operational"),
    _Mapping(_compile(r"\b(clear.*log|reset.*log|wipe.*log|erase.*log)\b"),
                                                                      "CLEAR_EVENT_LOG", "Operational"),
    _Mapping(_compile(r"\b(hardware inventory|inventory|discover.*hardware|hw inventory|discover.*inventory)\b"),
                                                                      "DISCOVER_INVENTORY", "Operational"),
    _Mapping(_compile(r"\b(mount|virtual media|insert.*media|attach.*iso|mount.*iso|mount.*image|attach.*image)\b"),
                                                                      "MOUNT_VIRTUAL_MEDIA", "Operational"),
    _Mapping(_compile(r"\b(sensor|thermal|fan|psu|power supply|environmental|inlet temperature|fan speed)\b"),
                                                                      "FETCH_SENSORS",  "Operational"),
    _Mapping(_compile(r"\b(cmdb sync|sync cmdb|poll cycle|trigger.*poll|manual poll|sync.*metrics|poll.*trigger)\b"),
                                                                      "SYNC_CMDB",      "Operational"),
    _Mapping(_compile(r"\b(change|update|set|modify|configure|patch)\b"), "UPDATE",    "Operational"),
    _Mapping(_compile(r"\b(reboot|restart|reset)\b"),                 "RESET",         "Operational"),
    _Mapping(_compile(r"\b(reload)\b"),                               "RELOAD",        "Operational"),
    _Mapping(_compile(r"\b(policy sync|sync)\b"),                     "POLICY_SYNC",   "Operational"),
    _Mapping(_compile(r"\b(failover)\b"),                             "FAILOVER",      "Operational"),
    _Mapping(_compile(r"\b(failback)\b"),                             "FAILBACK",      "Operational"),
    _Mapping(_compile(r"\b(rescan)\b"),                               "RESCAN",        "Operational"),
    _Mapping(_compile(r"\b(list)\b"),                                 "LIST",          "Operational"),
    _Mapping(_compile(r"\b(status|check|state|lookup|show|find|get|retrieve|fetch|read|display)\b"),
                                                                      "STATUS",        "Operational"),
    _Mapping(_compile(r"\b(provision|create)\b"),                     "CREATE",        "Provisioning"),
    _Mapping(_compile(r"\b(allocate|deploy)\b"),                      "ALLOCATE",      "Provisioning"),
    _Mapping(_compile(r"\b(deallocate|release)\b"),                   "DEALLOCATE",    "Provisioning"),
    _Mapping(_compile(r"\b(deprovision|destroy|delete)\b"),           "DELETE",        "Provisioning"),
)

_PREFIX_NOISE: frozenset[str] = frozenset({
    "the", "a", "an", "of", "for", "on", "at", "to", "my", "our", "their", "is", "was", "be", "about",
    "device", "resource", "system", "systems", "storage-system", "storage_system", "storage-systems", "storage_systems",
    "storage-pool", "storage_pool", "storage-pools", "storage_pools", "storage-volume", "storage_volume", "storage-volumes", "storage_volumes",
    "server", "switch", "router", "firewall", "storage", "named", "called", "name", "with", "by", "having",
    "change", "update", "set", "modify", "configure", "patch", "status", "check", "state", "lookup", "show", "find", "get", "query"
})

_SUFFIX_NOISE: frozenset[str] = frozenset({
    "the", "of", "for", "on", "at", "to", "my", "our", "their", "is", "was", "be", "about",
    "device", "resource", "system", "systems", "storage-system", "storage_system", "storage-systems", "storage_systems",
    "storage-pool", "storage_pool", "storage-pools", "storage_pools", "storage-volume", "storage_volume", "storage-volumes", "storage_volumes",
    "server", "switch", "router", "firewall", "storage", "named", "called", "name", "with", "by", "having",
    "change", "update", "set", "modify", "configure", "patch", "status", "check", "state", "lookup", "show", "find", "get", "query"
})

_BOUNDARY_PUNCT: re.Pattern = re.compile(r"^[,;:!?()\[\]\"']+|[,;:!?()\[\]\"']+$")

_FIELD_ALIASES: Dict[str, str] = {
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

_FALLBACK_PAYLOAD: dict = {
    "identifier": "",
    "action": "STATUS",
    "category": "Operational",
}

_FAIL_CLOSED_PAYLOAD: dict = {
    "identifier": "",
    "action": "UNPARSEABLE",
    "category": "Error",
}


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
    """Validate identifier against IP, FQDN, or Serial-number patterns."""
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
    attributes: List[AttributeItem] = Field(default_factory=list)
    multi_intent: bool = Field(default=False)
    ambiguous: bool = Field(default=False, description="Set to true if there is linguistic syntactic ambiguity.")
    unhandled: str = Field(default="")
    confidence: float = Field(ge=0.0, le=1.0)

def _dispatch_llm_provider(prompt: str, schema: Dict[str, Any], provider_name: str) -> Dict[str, Any]:
    """Execute LLM request against the configured provider."""
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
    
    # Future enterprise providers can be integrated here
    return {"_error": f"Provider '{provider_name}' not implemented"}

def _llm_extract(query: str) -> dict | None:
    """Orchestrate LLM parsing with provider failover and validation."""
    providers = []
    primary = os.environ.get("QUERY_AGENT_LLM_PROVIDER", "ollama").lower()
    secondary = os.environ.get("QUERY_AGENT_LLM_PROVIDER_SECONDARY", "").lower()
    if primary: providers.append(primary)
    if secondary and secondary != primary: providers.append(secondary)
    if not providers: providers.append("ollama")

    schema = LLMQuerySchema.model_json_schema()
    prompt = (
        "You are a deterministic natural language infrastructure command parser.\n"
        "Extract details from this query and output ONLY a JSON object matching the JSON schema below.\n"
        "Rules:\n"
        "1. For boot order or target changes (e.g. CD, USB, PXE, BIOS Setup), set action=UPDATE and attributes=[{\"key\": \"Boot\", \"value\": \"<NormalizedTarget>\"}] using Pxe/Cd/Usb/Hdd/BiosSetup/UefiTarget.\n"
        "2. If multiple actions are present (e.g. A and then B), parse only the first action/identifier, set multi_intent=true, and put the rest in unhandled.\n"
        "3. If the query uses a pronoun ('it', 'this') without a clear device name, set ambiguous=true.\n"
        f"User query: {query}\n"
        f"JSON Schema: {json.dumps(schema)}"
    )

    for idx, provider in enumerate(providers):
        res = _dispatch_llm_provider(prompt, schema, provider)
        if "_error" in res:
            err = res["_error"]
            if "timeout" in err.lower():
                logger.warning("[QueryAgent] LLM timeout | provider=%s error=%r", provider, err)
            else:
                logger.warning("[QueryAgent] LLM parse failure | provider=%s error=%r", provider, err)
                
            if idx < len(providers) - 1:
                logger.info("[QueryAgent] Provider failover | failed=%s next=%s", provider, providers[idx+1])
            continue
            
        try:
            validated = LLMQuerySchema.model_validate(res)
            payload = validated.model_dump()
            
            if not _validate_action(payload["action"]) or not _validate_category(payload["category"]):
                logger.warning("[QueryAgent] LLM returned invalid action/category | provider=%s", provider)
                continue
                
            logger.info("[QueryAgent] LLM parse success | provider=%s action=%s identifier=%s query=%r", 
                        provider, payload["action"], payload["identifier"], query)
            return payload
            
        except Exception as e:
            logger.warning("[QueryAgent] Validation Error on LLM output | provider=%s error=%s", provider, e)
            continue
            
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
    def _parse_update_details(query: str) -> dict:
        m1 = re.search(
            r"\b(?:change|set|update|modify|configure|patch)\b"
            r"(?:\s+the)?\s+(?P<attr>[\w_]+)\s+(?:of|for|on)\s+"
            r"(?P<device>[\w\-\.]+)"
            r"(?:\s+to|\s*=|\s+)\s+"
            r"(?P<value>[\w\.\-]+)",
            query, re.IGNORECASE
        )
        if m1:
            raw_attr = m1.group("attr").strip().lower()
            return {
                "device": m1.group("device").strip(),
                "attribute": _FIELD_ALIASES.get(raw_attr, raw_attr.replace(" ", "_")),
                "value": QueryAgent._coerce_value(m1.group("value").strip())
            }

        m2 = re.search(
            r"\b(?:change|set|update|modify|configure|patch)\b"
            r"\s+(?P<device>[\w\-\.]+)"
            r"\s+to\s+"
            r"(?P<attr>[\w_]+)"
            r"\s+(?P<value>[\w\.\-]+)",
            query, re.IGNORECASE
        )
        if m2:
            raw_attr = m2.group("attr").strip().lower()
            return {
                "device": m2.group("device").strip(),
                "attribute": _FIELD_ALIASES.get(raw_attr, raw_attr.replace(" ", "_")),
                "value": QueryAgent._coerce_value(m2.group("value").strip())
            }

        m3 = re.search(
            r"\b(?:change|set|update|modify|configure|patch)\b"
            r"\s+(?P<device>[\w\-\.]+)"
            r"\s+(?P<attr>(?!to\b)[\w_]+)"
            r"(?:\s+to\s+|\s*=\s*|\s+)"
            r"(?P<value>[\w\.\-]+)",
            query, re.IGNORECASE
        )
        if m3:
            raw_attr = m3.group("attr").strip().lower()
            return {
                "device": m3.group("device").strip(),
                "attribute": _FIELD_ALIASES.get(raw_attr, raw_attr.replace(" ", "_")),
                "value": QueryAgent._coerce_value(m3.group("value").strip())
            }
        return {}

    @staticmethod
    def _extract_device_identifier(query: str, action: str) -> str:
        pattern = r"\b(?:server|array|volume|pool|system)(?:\s+(?:named|called))?\s+([a-zA-Z0-9\-\_\.]+)"
        m = re.search(pattern, query, re.IGNORECASE)
        if m: return m.group(1).strip()
        
        m_fallback = re.search(r"\b(?:of|for|on|at|to)\s+([a-zA-Z0-9\-\_\.]+)", query, re.IGNORECASE)
        if m_fallback:
            val = m_fallback.group(1).strip()
            if not re.match(r"^\d+$", val) and val.upper() not in {"WARNING", "CRITICAL", "OK"}:
                return val
        return ""

    @staticmethod
    def _parse(query: str) -> dict:
        """Deterministic regex parsing with confidence scoring."""
        if not isinstance(query, str) or not query.strip():
            return dict(_FALLBACK_PAYLOAD) | {"confidence": 0.0, "ambiguous": False}
            
        query_clean = query.strip()
        matched_action = None
        matched_category = None
        identifier = query_clean
        ambiguous = False
        attributes = []

        matches = []
        for mapping in _ACTION_MAPPINGS:
            m = mapping.pattern.search(query_clean)
            if m: matches.append((mapping, m))

        if not matches:
            return dict(_FALLBACK_PAYLOAD) | {"confidence": 0.0, "ambiguous": False}

        # Filter out matches that are substrings of larger matches
        filtered_matches = []
        for map1, m1 in matches:
            is_submatch = False
            for map2, m2 in matches:
                if map1.action == map2.action: continue
                # if m1's matched text is fully inside m2's matched text
                if m1.start() >= m2.start() and m1.end() <= m2.end():
                    is_submatch = True
                    break
            if not is_submatch:
                filtered_matches.append((map1, m1))
                
        # If filtering removed everything, just fall back to original matches (shouldn't happen)
        if not filtered_matches:
            filtered_matches = matches

        unique_actions = {m[0].action for m in filtered_matches}
        
        # STATUS verbs (fetch, get, show) are often used as prefixes for other commands 
        # (e.g. "fetch event logs"). Ignore STATUS if there's another specific action.
        if "STATUS" in unique_actions and len(unique_actions) > 1:
            unique_actions.remove("STATUS")
            
        if len(unique_actions) > 1:
            ambiguous = True

        # Use the first mapping from our filtered list (highest priority)
        best_mapping, best_match = filtered_matches[0]
        matched_action = best_mapping.action
        matched_category = best_mapping.category
        
        before = query_clean[: best_match.start()].strip()
        after  = query_clean[best_match.end() :].strip()
        identifier = f"{before} {after}".strip() if before or after else ""

        if matched_action == "UPDATE":
            details = QueryAgent._parse_update_details(query_clean)
            if details and details.get("device"):
                identifier = details["device"]
                attributes.append({"key": details["attribute"], "value": details["value"]})
        elif matched_action in {
            "MOUNT_VIRTUAL_MEDIA", "FETCH_EVENT_LOG", "CLEAR_EVENT_LOG",
            "DISCOVER_INVENTORY", "FETCH_SENSORS", "SYNC_CMDB",
            "CREATE", "DELETE", "ALLOCATE", "DEALLOCATE",
            "STATUS", "POWER_ON", "POWER_OFF", "RESET"
        }:
            extracted = QueryAgent._extract_device_identifier(query_clean, matched_action)
            if extracted: identifier = extracted
            elif matched_action == "SYNC_CMDB": identifier = ""

        identifier = re.sub(r"\s{2,}", " ", identifier)
        identifier = _BOUNDARY_PUNCT.sub("", identifier).strip()

        words = identifier.split()
        while words and words[0].lower() in _PREFIX_NOISE:
            if matched_action == "LIST" and words[0].lower() in {"server", "servers", "storage_pool", "storage_pools", "storage_system", "storage_systems", "pool", "pools", "volume", "volumes"}: break
            words.pop(0)
        while words and words[-1].lower() in _SUFFIX_NOISE:
            if matched_action == "LIST" and words[-1].lower() in {"server", "servers", "storage_pool", "storage_pools", "storage_system", "storage_systems", "pool", "pools", "volume", "volumes"}: break
            words.pop()
        identifier = " ".join(words)

        if identifier.lower() in {"it", "this", "that", "the device", "the server", "the system", "the array", "the pool"}:
            ambiguous = True
            identifier = ""

        if matched_action in {"LIST", "SYNC_CMDB"}:
            identifier = ""

        # Confidence Scoring
        if matched_action in {"LIST", "SYNC_CMDB"}:
            confidence = 1.0 if not ambiguous else 0.5
        elif matched_action and identifier:
            conversational_noise = re.search(r"\b(can you|could you|please|investigate|why|what happened|i think)\b", query_clean, re.IGNORECASE)
            if conversational_noise or ambiguous:
                confidence = 0.6
            else:
                confidence = 0.9
        elif matched_action and not identifier:
            confidence = 0.3
        else:
            confidence = 0.0

        return {
            "identifier": identifier,
            "action": matched_action,
            "category": matched_category,
            "attributes": attributes,
            "ambiguous": ambiguous,
            "confidence": confidence
        }

    @staticmethod
    def parse_query(query: str) -> dict:
        """
        Parse a raw user query into a structured routing payload.
        Delegates to parse_query_hybrid for intelligent routing.
        """
        return parse_query_hybrid(query)

    @staticmethod
    def parse_update_payload(query: str) -> dict:
        """
        Extract the attribute name and new value from an UPDATE query.
        """
        details = QueryAgent._parse_update_details(query)
        if not details:
            return {}
        return {
            "attribute": details["attribute"],
            "value": details["value"]
        }


def parse_query_hybrid(query: str) -> dict:
    """
    Hybrid query parsing layer.
    Deterministic Regex-first processing, escalating to LLM on low confidence.
    Fails closed if confidence is insufficient.
    """
    try:
        regex_res = QueryAgent._parse(query)
        confidence = regex_res.get("confidence", 0.0)

        # Validate the regex result as well!
        is_regex_valid = (
            _validate_action(regex_res.get("action", "")) and 
            _validate_category(regex_res.get("category", ""))
        )

        if confidence >= QUERY_AGENT_CONFIDENCE_THRESHOLD and is_regex_valid:
            logger.info("[QueryAgent] Regex parse success | confidence=%.2f action=%s identifier=%s query=%r", 
                        confidence, regex_res.get("action"), regex_res.get("identifier"), query)
            return regex_res

        logger.info("[QueryAgent] Regex parse low confidence | confidence=%.2f. Escalating to LLM | query=%r", confidence, query)
        
        llm_res = _llm_extract(query)
        if llm_res is not None:
            return llm_res
            
        logger.warning("[QueryAgent] Returning fallback result | reason='All LLM providers failed and Regex confidence was low. Failing closed.'")
        return dict(_FAIL_CLOSED_PAYLOAD)

    except Exception as exc:
        logger.warning("[QueryAgent] Parse error — using fallback | error=%s query=%r", exc, query)
        return dict(_FALLBACK_PAYLOAD)
