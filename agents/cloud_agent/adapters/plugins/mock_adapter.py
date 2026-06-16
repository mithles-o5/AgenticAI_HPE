"""Mock cloud adapter — zero external dependencies, for local dev and testing."""

from __future__ import annotations
import random
import time
from typing import Any, Dict, List, Optional

from adapters.base import BaseCloudAdapter


class MockCloudAdapter(BaseCloudAdapter):
    """Simulates a cloud provider backend with deterministic-ish mock data."""

    @property
    def provider_name(self) -> str:
        return "mock"

    # ── fetch_metrics ─────────────────────────────────────────────────────────
    def fetch_metrics(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        # Handle state-dependent metrics: check if instance is stopped
        # By default, mock-vm-001 or any even resource index might be stopped.
        # Check if parameters specify a powerState or state == off/stopped.
        is_stopped = parameters.get("state") == "stopped" or parameters.get("powerState") == "Off" or "off" in resource_id.lower() or "stop" in resource_id.lower()
        
        if is_stopped:
            return {
                "cpu_utilization_pct":      0.0,
                "memory_utilization_pct":   0.0,
                "network_in_mbps":          0.0,
                "network_out_mbps":         0.0,
                "disk_read_iops":           0,
                "disk_write_iops":          0,
                "request_count":            0,
                "error_rate_pct":           0.0,
                "latency_p99_ms":           0.0,
                "uptime_seconds":           0,
                "power_state":              "OFF"
            }

        seed = sum(ord(c) for c in resource_id)
        rng = random.Random(seed + int(time.time() / 60))   # stable within a minute
        return {
            "cpu_utilization_pct":      round(rng.uniform(10.0, 95.0), 2),
            "memory_utilization_pct":   round(rng.uniform(20.0, 98.0), 2),
            "network_in_mbps":          round(rng.uniform(0.5, 100.0), 2),
            "network_out_mbps":         round(rng.uniform(0.5, 80.0), 2),
            "disk_read_iops":           rng.randint(10, 5000),
            "disk_write_iops":          rng.randint(5, 3000),
            "request_count":            rng.randint(0, 50000),
            "error_rate_pct":           round(rng.uniform(0.0, 20.0), 3),
            "latency_p99_ms":           round(rng.uniform(5.0, 800.0), 1),
            "uptime_seconds":           rng.randint(3600, 86400 * 30),
            "power_state":              "ON"
        }

    # ── execute_action ────────────────────────────────────────────────────────
    def execute_action(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        action: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        action_clean = action.lower().strip()
        if action_clean == "off":
            action_clean = "stop"
        elif action_clean == "on":
            action_clean = "start"

        supported = {"start", "stop", "restart", "resize", "terminate", "snapshot"}
        if action_clean not in supported:
            return {
                "result": "failed",
                "detail": f"Action '{action}' is not supported. Supported: {sorted(supported)}",
            }
        return {
            "result":      "success",
            "detail":      f"[MOCK] Action '{action_clean}' executed on {resource_type}/{resource_id}.",
            "resource_id": resource_id,
            "action":      action_clean,
            "region":      region,
        }

    # ── discover_resources ────────────────────────────────────────────────────
    def discover_resources(
        self,
        region: Optional[str],
        resource_type: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        count = parameters.get("limit", 5)
        return [
            {
                "id":     f"mock-{resource_type}-{i:03d}",
                "name":   f"Mock-{resource_type.upper()}-{i:03d}",
                "type":   resource_type,
                "status": "running" if i % 3 != 0 else "stopped",
                "region": region or "mock-region-1",
                "tags":   {"env": "mock", "owner": "cloud-agent"},
            }
            for i in range(1, int(count) + 1)
        ]

    # ── health_check ──────────────────────────────────────────────────────────
    def health_check(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        # Simulate an occasional warning for realism
        seed = sum(ord(c) for c in resource_id)
        healthy = seed % 5 != 0
        return {
            "healthy": healthy,
            "detail":  "All checks passed." if healthy else "Simulated health-check failure.",
            "checks": {
                "connectivity": "ok",
                "cpu":          "ok" if healthy else "warning",
                "memory":       "ok",
                "disk":         "ok",
            },
        }
