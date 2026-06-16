"""Storage normalization layer."""

from __future__ import annotations
from typing import Any, Dict, List

_CAPACITY_ALIASES: Dict[str, str] = {
    "totalCapacityTiB":   "total_tb",
    "usedCapacityTiB":    "used_tb",
    "freeCapacityTiB":    "free_tb",
    "utilizationPercent": "utilization_pct",
}

_PERF_ALIASES: Dict[str, str] = {
    "readIOPS":          "read_iops",
    "writeIOPS":         "write_iops",
    "readLatencyMs":     "read_latency_ms",
    "writeLatencyMs":    "write_latency_ms",
    "throughputMBps":    "throughput_mbps",
}


def normalize_capacity(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {_CAPACITY_ALIASES.get(k, k): v for k, v in raw.items()}


def normalize_performance(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {_PERF_ALIASES.get(k, k): v for k, v in raw.items()}


def normalize_array_list(raw_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "id":          item.get("id") or "unknown",
            "name":        item.get("name") or "unknown",
            "type":        item.get("type") or "unknown",
            "status":      item.get("status") or "unknown",
            "capacity_tb": item.get("capacity_tb") or item.get("capacityTiB") or 0.0,
            **{k: v for k, v in item.items() if k not in {"id", "name", "type", "status", "capacity_tb", "capacityTiB"}},
        }
        for item in raw_list
    ]
