"""Storage anomaly detection — capacity utilization, IOPS, and latency."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from config.settings import settings


@dataclass
class StorageAnomalyReport:
    status_level: str = "healthy"
    insights:     List[str] = field(default_factory=list)


def detect_storage_anomalies(
    capacity: Dict[str, Any],
    performance: Dict[str, Any],
) -> StorageAnomalyReport:
    report = StorageAnomalyReport()
    severity_rank = {"healthy": 0, "warning": 1, "critical": 2}

    def _bump(level: str, msg: str):
        report.insights.append(msg)
        if severity_rank[level] > severity_rank[report.status_level]:
            report.status_level = level

    # Capacity
    util = capacity.get("utilization_pct")
    if util is not None:
        try:
            util = float(util)
            if util >= settings.CAPACITY_CRITICAL_PCT:
                _bump("critical", f"Capacity CRITICAL at {util:.1f}% (threshold: {settings.CAPACITY_CRITICAL_PCT}%)")
            elif util >= settings.CAPACITY_WARNING_PCT:
                _bump("warning", f"Capacity elevated at {util:.1f}% (threshold: {settings.CAPACITY_WARNING_PCT}%)")
        except (TypeError, ValueError):
            pass

    # IOPS
    total_iops = (performance.get("read_iops", 0) or 0) + (performance.get("write_iops", 0) or 0)
    if total_iops >= settings.IOPS_CRITICAL_THRESHOLD:
        _bump("critical", f"Total IOPS CRITICAL at {total_iops} (threshold: {settings.IOPS_CRITICAL_THRESHOLD})")
    elif total_iops >= settings.IOPS_WARNING_THRESHOLD:
        _bump("warning", f"Total IOPS elevated at {total_iops} (threshold: {settings.IOPS_WARNING_THRESHOLD})")

    # Latency
    for lat_key, label in [("read_latency_ms", "Read"), ("write_latency_ms", "Write")]:
        lat = performance.get(lat_key)
        if lat is not None:
            try:
                lat = float(lat)
                if lat >= settings.LATENCY_CRITICAL_MS:
                    _bump("critical", f"{label} latency CRITICAL at {lat:.1f}ms (threshold: {settings.LATENCY_CRITICAL_MS}ms)")
                elif lat >= settings.LATENCY_WARNING_MS:
                    _bump("warning", f"{label} latency elevated at {lat:.1f}ms (threshold: {settings.LATENCY_WARNING_MS}ms)")
            except (TypeError, ValueError):
                pass

    return report
