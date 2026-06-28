"""Lightweight deterministic NLP Query Agent for intent and identifier extraction."""

from __future__ import annotations

import logging
import re
from typing import NamedTuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants — defined once at module level, never rebuilt per call
# ---------------------------------------------------------------------------

class _Mapping(NamedTuple):
    pattern: re.Pattern
    action: str
    category: str


def _compile(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)


# Action mappings — order matters:
#   1. Multi-word phrases BEFORE their single-word subsets.
#   2. Within each alternation group, longer phrase left of shorter.
_ACTION_MAPPINGS: tuple[_Mapping, ...] = (
    # Power — longest phrase first
    _Mapping(_compile(r"\b(turn on|power on|start)\b"),              "ON",            "Operational"),
    _Mapping(_compile(r"\b(turn off|power off|shutdown)\b"),          "OFF",           "Operational"),
    _Mapping(_compile(r"\b(cold boot)\b"),                            "COLD_BOOT",     "Operational"),

    # ── Semantic intents — checked FIRST so they win over generic verbs ──────
    # Event log / system event log (before "get"/"show" which would match STATUS)
    _Mapping(_compile(r"\b(event log|event logs|system log|system logs|sel|log entries|iml|integrated management log)\b"),
                                                                      "FETCH_EVENT_LOG", "Operational"),
    # Clear / reset log
    _Mapping(_compile(r"\b(clear.*log|reset.*log|wipe.*log|erase.*log)\b"),
                                                                      "CLEAR_EVENT_LOG", "Operational"),
    # Hardware inventory
    _Mapping(_compile(r"\b(hardware inventory|inventory|discover.*hardware|hw inventory|discover.*inventory)\b"),
                                                                      "DISCOVER_INVENTORY", "Operational"),
    # Virtual media / ISO / image mount
    _Mapping(_compile(r"\b(mount|virtual media|insert.*media|attach.*iso|mount.*iso|mount.*image|attach.*image)\b"),
                                                                      "MOUNT_VIRTUAL_MEDIA", "Operational"),
    # Sensor / environmental audit
    _Mapping(_compile(r"\b(sensor|thermal|fan|psu|power supply|environmental|inlet temperature|fan speed)\b"),
                                                                      "FETCH_SENSORS",  "Operational"),
    # CMDB sync / poll cycle trigger
    _Mapping(_compile(r"\b(cmdb sync|sync cmdb|poll cycle|trigger.*poll|manual poll|sync.*metrics|poll.*trigger)\b"),
                                                                      "SYNC_CMDB",      "Operational"),

    # Update / modify — BEFORE reset so "configure" wins
    _Mapping(_compile(r"\b(change|update|set|modify|configure|patch)\b"), "UPDATE",    "Operational"),
    # Reset / reload
    _Mapping(_compile(r"\b(reboot|restart|reset)\b"),                 "RESET",         "Operational"),
    _Mapping(_compile(r"\b(reload)\b"),                               "RELOAD",        "Operational"),
    # HA / network ops — policy sync BEFORE plain sync
    _Mapping(_compile(r"\b(policy sync|sync)\b"),                     "POLICY_SYNC",   "Operational"),
    _Mapping(_compile(r"\b(failover)\b"),                             "FAILOVER",      "Operational"),
    _Mapping(_compile(r"\b(failback)\b"),                             "FAILBACK",      "Operational"),
    # Storage / discovery
    _Mapping(_compile(r"\b(rescan)\b"),                               "RESCAN",        "Operational"),
    # Read / query — STATUS is the last fallback for generic verbs
    _Mapping(_compile(r"\b(list)\b"),                                 "LIST",          "Operational"),
    _Mapping(_compile(r"\b(status|check|state|lookup|show|find|get|retrieve|fetch|read|display)\b"),
                                                                      "STATUS",        "Operational"),
    # Provisioning
    _Mapping(_compile(r"\b(provision|create)\b"),                     "CREATE",        "Provisioning"),
    _Mapping(_compile(r"\b(allocate|deploy)\b"),                      "ALLOCATE",      "Provisioning"),
    _Mapping(_compile(r"\b(deallocate|release)\b"),                   "DEALLOCATE",    "Provisioning"),
    _Mapping(_compile(r"\b(deprovision|destroy|delete)\b"),           "DELETE",        "Provisioning"),
)

# Noise words stripped from the leading edge of the extracted identifier
_PREFIX_NOISE: frozenset[str] = frozenset({
    "the", "a", "an", "of", "for", "on", "at", "to", "my", "our", "their", "is", "was", "be", "about",
    "device", "resource", "system", "systems", "storage-system", "storage_system", "storage-systems", "storage_systems",
    "storage-pool", "storage_pool", "storage-pools", "storage_pools", "storage-volume", "storage_volume", "storage-volumes", "storage_volumes",
    "server", "switch", "router", "firewall", "storage", "named", "called", "name", "with", "by", "having",
    "change", "update", "set", "modify", "configure", "patch", "status", "check", "state", "lookup", "show", "find", "get", "query"
})

# Noise words stripped from the trailing edge of the extracted identifier
_SUFFIX_NOISE: frozenset[str] = frozenset({
    "the", "of", "for", "on", "at", "to", "my", "our", "their", "is", "was", "be", "about",
    "device", "resource", "system", "systems", "storage-system", "storage_system", "storage-systems", "storage_systems",
    "storage-pool", "storage_pool", "storage-pools", "storage_pools", "storage-volume", "storage_volume", "storage-volumes", "storage_volumes",
    "server", "switch", "router", "firewall", "storage", "named", "called", "name", "with", "by", "having",
    "change", "update", "set", "modify", "configure", "patch", "status", "check", "state", "lookup", "show", "find", "get", "query"
})

# Characters considered "boundary punctuation" — stripped only when they
# appear at the very start or end of the identifier string.
# Hyphens, underscores, dots are preserved *within* tokens (rack42-n3, fw-core-01).
_BOUNDARY_PUNCT: re.Pattern = re.compile(r"^[,;:!?()\[\]\"']+|[,;:!?()\[\]\"']+$")

# Canonical fallback payload — returned on unrecoverable parse failure
_FALLBACK_PAYLOAD: dict = {
    "identifier": "",
    "action": "STATUS",
    "category": "Operational",
}


# ---------------------------------------------------------------------------
# Query Agent
# ---------------------------------------------------------------------------


class QueryAgent:
    """
    Lightweight, stateless, deterministic NLP preprocessing layer.

    Responsibilities:
        - Action extraction
        - Category extraction
        - Identifier extraction and normalization
        - Noise-word stripping
        - Structured payload generation

    Architecture contract:
        - Pure preprocessing — no DB, no cache, no resolver, no network calls.
        - Stateless and thread-safe.
        - Always returns a valid payload; never raises.
    """

    @staticmethod
    def parse_query(query: str) -> dict:
        """
        Parse a raw user query into a structured routing payload.

        Returns:
            dict with keys: ``identifier`` (str), ``action`` (str), ``category`` (str).
            Falls back to ``{"identifier": "", "action": "STATUS", "category": "Operational"}``
            on any unrecoverable parse error.
        """
        try:
            return QueryAgent._parse(query)
        except Exception as exc:  # pragma: no cover
            logger.warning("[QueryAgent] Parse error — using fallback | error=%s query=%r", exc, query)
            return dict(_FALLBACK_PAYLOAD)

    @staticmethod
    def _parse(query: str) -> dict:
        if not isinstance(query, str):
            return dict(_FALLBACK_PAYLOAD)
        query_clean = query.strip()
        if not query_clean:
            return dict(_FALLBACK_PAYLOAD)

        matched_action = "STATUS"
        matched_category = "Operational"
        identifier = query_clean

        # --- 1. Action matching (first match wins; ordering in _ACTION_MAPPINGS is authoritative) ---
        for mapping in _ACTION_MAPPINGS:
            m = mapping.pattern.search(query_clean)
            if m:
                matched_action = mapping.action
                matched_category = mapping.category
                # Excise the matched phrase; join the surrounding parts
                before = query_clean[: m.start()].strip()
                after  = query_clean[m.end() :].strip()
                identifier = f"{before} {after}".strip() if before or after else ""
                break

        # For UPDATE queries, extract just the device name from consolidated parsing logic
        if matched_action == "UPDATE":
            details = QueryAgent._parse_update_details(query_clean)
            if details and details.get("device"):
                identifier = details["device"]

        # For all semantic intent actions, apply dedicated device extraction
        # because the matched phrase removal leaves garbled text (URLs, prepositions, etc.)
        elif matched_action in {
            "MOUNT_VIRTUAL_MEDIA", "FETCH_EVENT_LOG", "CLEAR_EVENT_LOG",
            "DISCOVER_INVENTORY", "FETCH_SENSORS", "SYNC_CMDB"
        }:
            extracted = QueryAgent._extract_device_identifier(query_clean, matched_action)
            if extracted:
                identifier = extracted
            # For SYNC_CMDB with no device context, use empty identifier (global sync)
            elif matched_action == "SYNC_CMDB":
                identifier = ""

        # --- 2. Collapse internal whitespace (multi-space → single space) ---
        identifier = re.sub(r"\s{2,}", " ", identifier)

        # --- 3. Strip boundary punctuation (preserves hyphens/underscores/dots mid-token) ---
        identifier = _BOUNDARY_PUNCT.sub("", identifier).strip()

        # --- 4. Strip prefix noise words ---
        words = identifier.split()
        while words and words[0].lower() in _PREFIX_NOISE:
            if matched_action == "LIST" and words[0].lower() in {"server", "servers", "storage_pool", "storage_pools", "storage_system", "storage_systems", "pool", "pools", "volume", "volumes"}:
                break
            words = words[1:]

        # --- 5. Strip suffix noise words ---
        while words and words[-1].lower() in _SUFFIX_NOISE:
            if matched_action == "LIST" and words[-1].lower() in {"server", "servers", "storage_pool", "storage_pools", "storage_system", "storage_systems", "pool", "pools", "volume", "volumes"}:
                break
            words = words[:-1]

        identifier = " ".join(words)

        logger.debug(
            "[QueryAgent] Parsed query | action=%s category=%s identifier=%r",
            matched_action, matched_category, identifier,
        )

        return {
            "identifier": identifier,
            "action": matched_action,
            "category": matched_category,
        }

    @staticmethod
    def _extract_device_identifier(query: str, action: str) -> str:
        """
        Extract the actual device/server identifier from a semantic action query.

        For queries like:
          "Mount ISO http://... to server dl360-prod-091"
          "Retrieve event logs for server apollo-node-104"
          "Run sensor audit on synergy-comp-143"

        Returns just the server serial/name (e.g. "dl360-prod-091").
        Falls back to empty string if no match.
        """
        # Pattern: look for "server <id>", "node <id>", "host <id>", "device <id>"
        server_keyword = re.search(
            r"\b(?:server|node|host|device|system|bmc|of|on|for)\s+([\w][\w\-\.]{2,})\b",
            query,
            re.IGNORECASE,
        )
        if server_keyword:
            candidate = server_keyword.group(1).strip()
            # Exclude obvious non-device words
            if candidate.lower() not in {
                "all", "the", "a", "my", "its", "this", "that", "every",
                "mock", "server", "servers", "devices", "metrics", "sync", "logs"
            }:
                return candidate

        # Pattern: device-like token = word with hyphen/digits (e.g. dl360-prod-091, apollo-node-104)
        # Looks for tokens like "word-word-digits" anywhere in the query
        device_token = re.search(
            r"\b([a-zA-Z][a-zA-Z0-9]*(?:[-_][a-zA-Z0-9]+){1,})\b",
            query,
        )
        if device_token:
            candidate = device_token.group(1)
            # Skip if it looks like a URL fragment or very common word
            if not candidate.startswith("http") and len(candidate) >= 5:
                return candidate

        return ""



    @staticmethod
    def _coerce_value(raw_value: str) -> object:
        """Coerce raw string value into boolean, int, float, or string."""
        val_lower = raw_value.strip().lower()
        if val_lower in {"true", "on", "enabled"}:
            return True
        if val_lower in {"false", "off", "disabled"}:
            return False

        try:
            return int(raw_value)
        except ValueError:
            try:
                return float(raw_value)
            except ValueError:
                return raw_value

    @staticmethod
    def _parse_update_details(query: str) -> dict:
        """
        Consolidated helper to parse UPDATE/PATCH queries.
        Returns a dict with 'device', 'attribute', and 'value' keys, or an empty dict.
        """
        # Custom boot configuration pattern matching
        # e.g., "Configure dl360-prod-091 to boot from PXE network on next restart"
        # or "Set boot order of dl360-prod-091 to CD-ROM"
        boot_match = re.search(
            r"\b(?:change|set|update|modify|configure|patch|boot)\b"
            r"\s+(?:the\s+)?(?:boot\s+order\s+of|boot\s+target\s+of|boot\s+of)?\s*"
            r"(?P<device>[\w\-\.]+)"
            r"\s+(?:to\s+boot\s+from|to\s+boot\s+order|to|boot\s+target)\s+"
            r"(?P<target>pxe|cd|hdd|bios|uefi|dvd|usb|network)"
            r"(?:\s+network|\s+rom|\s+setup)?",
            query,
            re.IGNORECASE
        )
        if boot_match:
            raw_device = boot_match.group("device").strip()
            raw_target = boot_match.group("target").strip().lower()
            
            # Map friendly names to standard Redfish BootSourceOverrideTarget values
            target_map = {
                "pxe": "Pxe",
                "network": "Pxe",
                "cd": "Cd",
                "dvd": "Cd",
                "usb": "Usb",
                "hdd": "Hdd",
                "bios": "BiosSetup",
                "uefi": "UefiTarget"
            }
            target_value = target_map.get(raw_target, "Pxe")
            
            return {
                "device": raw_device,
                "attribute": "Boot",
                "value": {
                    "BootSourceOverrideTarget": target_value,
                    "BootSourceOverrideEnabled": "Once"
                }
            }

        # Map natural language phrases to canonical field names
        _FIELD_ALIASES: dict[str, str] = {
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

        # Pattern 1: (change|set|update|modify|configure|patch) [the] <attribute> of/for/on <device> [to|=|space] <value>
        m1 = re.search(
            r"\b(?:change|set|update|modify|configure|patch)\b"
            r"\s+(?:the\s+)?"                           # optional "the"
            r"(?P<attr>[\w\s_]+?)"                       # attribute name (lazy)
            r"\s+(?:of|for|on)\s+"
            r"(?P<device>[\w\-\.]+)"
            r"(?:\s+to\s+|\s*=\s*|\s+)"                 # 'to', '=', or whitespace
            r"(?P<value>[\w\.\-]+)",
            query,
            re.IGNORECASE,
        )
        if m1:
            raw_device = m1.group("device").strip()
            raw_attr = m1.group("attr").strip().lower()
            raw_value = m1.group("value").strip()
            attribute = _FIELD_ALIASES.get(raw_attr, raw_attr.replace(" ", "_"))
            return {
                "device": raw_device,
                "attribute": attribute,
                "value": QueryAgent._coerce_value(raw_value)
            }

        # Pattern 2: (change|set|update|modify|configure|patch) <device> to <attribute> <value>
        m2 = re.search(
            r"\b(?:change|set|update|modify|configure|patch)\b"
            r"\s+(?P<device>[\w\-\.]+)"
            r"\s+to\s+"
            r"(?P<attr>[\w_]+)"
            r"\s+(?P<value>[\w\.\-]+)",
            query,
            re.IGNORECASE,
        )
        if m2:
            raw_device = m2.group("device").strip()
            raw_attr = m2.group("attr").strip().lower()
            raw_value = m2.group("value").strip()
            attribute = _FIELD_ALIASES.get(raw_attr, raw_attr.replace(" ", "_"))
            return {
                "device": raw_device,
                "attribute": attribute,
                "value": QueryAgent._coerce_value(raw_value)
            }

        # Pattern 3: (change|set|update|modify|configure|patch) <device> <attribute> [to|=|space] <value>
        m3 = re.search(
            r"\b(?:change|set|update|modify|configure|patch)\b"
            r"\s+(?P<device>[\w\-\.]+)"
            r"\s+(?P<attr>(?!to\b)[\w_]+)"              # exclude 'to'
            r"(?:\s+to\s+|\s*=\s*|\s+)"                 # 'to', '=', or whitespace
            r"(?P<value>[\w\.\-]+)",
            query,
            re.IGNORECASE,
        )
        if m3:
            raw_device = m3.group("device").strip()
            raw_attr = m3.group("attr").strip().lower()
            raw_value = m3.group("value").strip()
            attribute = _FIELD_ALIASES.get(raw_attr, raw_attr.replace(" ", "_"))
            return {
                "device": raw_device,
                "attribute": attribute,
                "value": QueryAgent._coerce_value(raw_value)
            }

        return {}

    @staticmethod
    def parse_update_payload(query: str) -> dict:
        """
        Extract the attribute name and new value from an UPDATE query.
        Delegates to _parse_update_details.
        """
        details = QueryAgent._parse_update_details(query)
        if not details:
            return {}
        return {
            "attribute": details["attribute"],
            "value": details["value"]
        }
