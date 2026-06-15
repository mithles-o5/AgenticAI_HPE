"""Mock storage adapter — deterministic, no external dependencies."""

from __future__ import annotations
import random
from typing import Any, Dict, List

from adapters.base import BaseStorageAdapter


class MockStorageAdapter(BaseStorageAdapter):

    @property
    def provider_name(self) -> str:
        return "mock"

    def fetch_capacity(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        rng = random.Random(hash(resource_id) & 0xFFFF)
        total = round(rng.uniform(10.0, 500.0), 2)
        used  = round(total * rng.uniform(0.1, 0.97), 2)
        return {
            "total_tb":       total,
            "used_tb":        used,
            "free_tb":        round(total - used, 2),
            "utilization_pct": round(used / total * 100, 2),
        }

    def fetch_performance(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        rng = random.Random(hash(resource_id + "perf") & 0xFFFF)
        return {
            "read_iops":         rng.randint(100, 100000),
            "write_iops":        rng.randint(50, 80000),
            "read_latency_ms":   round(rng.uniform(0.5, 80.0), 2),
            "write_latency_ms":  round(rng.uniform(0.5, 60.0), 2),
            "throughput_mbps":   round(rng.uniform(10.0, 2000.0), 1),
        }

    def execute_action(self, resource_id, resource_type, action, credentials, parameters) -> Dict[str, Any]:
        supported = {"create_volume", "delete_volume", "snapshot", "resize", "clone", "mount", "unmount"}
        if action.lower() not in supported:
            return {"result": "failed", "detail": f"Action '{action}' not supported. Supported: {sorted(supported)}"}
        return {"result": "success", "detail": f"[MOCK] Action '{action}' on {resource_type}/{resource_id}."}

    def discover_arrays(self, credentials, parameters) -> List[Dict[str, Any]]:
        count = parameters.get("limit", 3)
        return [
            {
                "id":          f"mock-array-{i:03d}",
                "name":        f"Mock-SAN-{i:03d}",
                "type":        "SAN" if i % 2 == 0 else "NAS",
                "status":      "online",
                "capacity_tb": round(100.0 * i, 1),
            }
            for i in range(1, int(count) + 1)
        ]

    def health_check(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        seed = sum(ord(c) for c in resource_id)
        healthy = seed % 6 != 0
        return {
            "healthy": healthy,
            "detail":  "All storage checks passed." if healthy else "Simulated storage fault.",
            "checks":  {"connectivity": "ok", "disk_health": "ok" if healthy else "error", "replication": "ok"},
        }
