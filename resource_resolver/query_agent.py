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
    # Power
    _Mapping(_compile(r"\b(turn on|power on|start)\b"),              "ON",          "Operational"),
    _Mapping(_compile(r"\b(turn off|power off|shutdown)\b"),          "OFF",         "Operational"),
    _Mapping(_compile(r"\b(cold boot)\b"),                            "COLD_BOOT",   "Operational"),
    # Reset / reload
    _Mapping(_compile(r"\b(reboot|restart|reset)\b"),                 "RESET",       "Operational"),
    _Mapping(_compile(r"\b(reload)\b"),                               "RELOAD",      "Operational"),
    # HA / network ops — policy sync BEFORE plain sync
    _Mapping(_compile(r"\b(policy sync|sync)\b"),                     "POLICY_SYNC", "Operational"),
    _Mapping(_compile(r"\b(failover)\b"),                             "FAILOVER",    "Operational"),
    _Mapping(_compile(r"\b(failback)\b"),                             "FAILBACK",    "Operational"),
    # Storage / discovery
    _Mapping(_compile(r"\b(rescan)\b"),                               "RESCAN",      "Operational"),
    # Read / query
    _Mapping(_compile(r"\b(status|check|state|lookup|show|find|get)\b"), "STATUS",   "Operational"),
    # Provisioning
    _Mapping(_compile(r"\b(provision|create)\b"),                     "CREATE",      "Provisioning"),
    _Mapping(_compile(r"\b(allocate|deploy)\b"),                      "ALLOCATE",    "Provisioning"),
    _Mapping(_compile(r"\b(deallocate|release)\b"),                   "DEALLOCATE",  "Provisioning"),
    _Mapping(_compile(r"\b(deprovision|destroy|delete)\b"),           "DELETE",      "Provisioning"),
    # Future extensibility — add new rows here, no flow logic changes needed:
    # _Mapping(_compile(r"\b(migrate)\b"),                            "MIGRATE",     "Provisioning"),
    # _Mapping(_compile(r"\b(patch)\b"),                              "PATCH",       "Operational"),
    # _Mapping(_compile(r"\b(quarantine)\b"),                         "QUARANTINE",  "Operational"),
    # _Mapping(_compile(r"\b(snapshot)\b"),                           "SNAPSHOT",    "Operational"),
)

# Noise words stripped from the leading edge of the extracted identifier
_PREFIX_NOISE: frozenset[str] = frozenset({
    "the", "a", "an", "of", "for", "on", "at", "to", "my", "our", "their", "is", "was", "be", "about",
    "device", "resource",
    "server", "switch", "router", "firewall", "storage",
})

# Noise words stripped from the trailing edge of the extracted identifier
_SUFFIX_NOISE: frozenset[str] = frozenset({
    "the", "of", "for", "on", "at", "to", "my", "our", "their", "is", "was", "be", "about",
    "device", "resource",
    "server", "switch", "router", "firewall", "storage",
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

        # --- 2. Collapse internal whitespace (multi-space → single space) ---
        identifier = re.sub(r"\s{2,}", " ", identifier)

        # --- 3. Strip boundary punctuation (preserves hyphens/underscores/dots mid-token) ---
        identifier = _BOUNDARY_PUNCT.sub("", identifier).strip()

        # --- 4. Strip prefix noise words ---
        words = identifier.split()
        while words and words[0].lower() in _PREFIX_NOISE:
            words = words[1:]

        # --- 5. Strip suffix noise words ---
        while words and words[-1].lower() in _SUFFIX_NOISE:
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
