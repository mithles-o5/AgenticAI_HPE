"""Mock network adapter — no hardware required, deterministic for testing."""

from __future__ import annotations
import random
from typing import Any, Dict, List, Optional

from adapters.base import BaseNetworkAdapter


class MockNetworkAdapter(BaseNetworkAdapter):

    @property
    def protocol_name(self) -> str:
        return "mock"

    def fetch_interface_metrics(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        rng = random.Random(hash(device_id) & 0xFFFF)
        count = parameters.get("interface_count", 4)
        return [
            {
                "name":                 f"GigabitEthernet{i}/0/0",
                "status":               "up" if rng.random() > 0.1 else "down",
                "in_octets_per_sec":    round(rng.uniform(1e4, 1e8), 0),
                "out_octets_per_sec":   round(rng.uniform(1e4, 5e7), 0),
                "in_errors":            rng.randint(0, 50),
                "out_errors":           rng.randint(0, 20),
                "utilization_pct":      round(rng.uniform(1.0, 95.0), 2),
            }
            for i in range(1, int(count) + 1)
        ]

    def push_config(self, device_id, config_payload, credentials, parameters) -> Dict[str, Any]:
        return {
            "result":    "success",
            "detail":    f"[MOCK] Config pushed to {device_id}.",
            "config":    config_payload,
        }

    def discover_neighbors(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        return [
            {"neighbor_id": f"sw-mock-00{i}", "neighbor_port": f"Gi{i}/0/0", "local_port": f"Gi0/{i}"}
            for i in range(1, 4)
        ]

    def health_check(self, device_id, credentials, parameters) -> Dict[str, Any]:
        seed = sum(ord(c) for c in device_id)
        healthy = seed % 7 != 0
        return {
            "healthy": healthy,
            "detail":  "Device reachable." if healthy else "MOCK: Simulated unreachable device.",
        }
