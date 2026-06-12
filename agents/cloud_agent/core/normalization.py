"""Normalization layer — converts raw adapter output into the unified TaskResponse schema.

Raw adapters return provider-specific key names and units. This module maps
them to the canonical field names used in TaskResponse.metrics.
"""

from __future__ import annotations
from typing import Any, Dict


# ── Canonical metric name aliases ─────────────────────────────────────────────
# Maps provider-specific keys → canonical names used in TaskResponse.metrics
_ALIASES: Dict[str, str] = {
    # CPU
    "cpu":                      "cpu_utilization_pct",
    "cpuPercent":               "cpu_utilization_pct",
    "CPUUtilization":           "cpu_utilization_pct",
    "cpu_percent":              "cpu_utilization_pct",
    # Memory
    "memory":                   "memory_utilization_pct",
    "memoryPercent":            "memory_utilization_pct",
    "MemoryUtilization":        "memory_utilization_pct",
    "mem_percent":              "memory_utilization_pct",
    # Network
    "networkIn":                "network_in_mbps",
    "NetworkIn":                "network_in_mbps",
    "networkOut":               "network_out_mbps",
    "NetworkOut":               "network_out_mbps",
    # Disk
    "diskReadIOPS":             "disk_read_iops",
    "DiskReadOps":              "disk_read_iops",
    "diskWriteIOPS":            "disk_write_iops",
    "DiskWriteOps":             "disk_write_iops",
    # Errors
    "errorRate":                "error_rate_pct",
    "ErrorCount":               "error_rate_pct",
    # Latency
    "latencyP99":               "latency_p99_ms",
    "Latency":                  "latency_p99_ms",
}


def normalize_metrics(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw adapter metrics dict to canonical key names.

    Unknown keys are kept as-is to avoid data loss.
    """
    normalized: Dict[str, Any] = {}
    for key, value in raw.items():
        canonical = _ALIASES.get(key, key)
        normalized[canonical] = value
    return normalized


def normalize_resource_list(raw_list: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    """
    Ensure each resource descriptor in a discovery list has the required fields.
    Missing fields are filled with sensible defaults.
    """
    canonical_list = []
    for item in raw_list:
        canonical_list.append({
            "id":     item.get("id") or item.get("resource_id") or "unknown",
            "name":   item.get("name") or item.get("Name") or "unknown",
            "type":   item.get("type") or item.get("resource_type") or "unknown",
            "status": item.get("status") or item.get("State") or "unknown",
            "region": item.get("region") or item.get("Region") or "unknown",
            "tags":   item.get("tags") or item.get("Tags") or {},
            **{k: v for k, v in item.items() if k not in {"id", "name", "type", "status", "region", "tags"}},
        })
    return canonical_list
