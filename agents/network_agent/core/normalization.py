"""Network Agent normalization layer."""

from __future__ import annotations
from typing import Any, Dict, List

_INTERFACE_ALIASES: Dict[str, str] = {
    "ifInOctets":    "in_octets_per_sec",
    "ifOutOctets":   "out_octets_per_sec",
    "ifInErrors":    "in_errors",
    "ifOutErrors":   "out_errors",
    "utilPercent":   "utilization_pct",
    "operStatus":    "status",
    "ifName":        "name",
}


def normalize_interface_metrics(raw_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalise raw interface metric dicts to canonical field names."""
    normalized = []
    for item in raw_list:
        canonical: Dict[str, Any] = {}
        for k, v in item.items():
            canonical[_INTERFACE_ALIASES.get(k, k)] = v
        normalized.append(canonical)
    return normalized


def normalize_neighbor_list(raw_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ensure each neighbor dict has required fields."""
    return [
        {
            "neighbor_id":    item.get("neighbor_id") or item.get("remoteDeviceId") or "unknown",
            "neighbor_port":  item.get("neighbor_port") or item.get("remotePort") or "",
            "local_port":     item.get("local_port") or item.get("localPort") or "",
        }
        for item in raw_list
    ]
