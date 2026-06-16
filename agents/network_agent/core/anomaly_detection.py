"""Network anomaly detection — interface utilization, error rates, BGP sessions."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from config.settings import settings


@dataclass
class NetworkAnomalyReport:
    status_level: str = "healthy"
    insights:     List[str] = field(default_factory=list)


def detect_network_anomalies(interfaces: List[Dict[str, Any]]) -> NetworkAnomalyReport:
    """Evaluate interface metric lists for utilization and error-rate anomalies."""
    report = NetworkAnomalyReport()
    severity_rank = {"healthy": 0, "warning": 1, "critical": 2}

    for iface in interfaces:
        name  = iface.get("name", "unknown")
        util  = iface.get("utilization_pct")
        in_err  = iface.get("in_errors", 0)
        out_err = iface.get("out_errors", 0)
        status  = iface.get("status", "up")

        if status == "down":
            report.insights.append(f"Interface {name} is DOWN.")
            if severity_rank["warning"] > severity_rank[report.status_level]:
                report.status_level = "warning"

        if util is not None:
            try:
                util = float(util)
                if util >= settings.INTERFACE_UTIL_CRITICAL_PCT:
                    report.insights.append(f"Interface {name} utilization CRITICAL at {util:.1f}%.")
                    report.status_level = "critical"
                elif util >= settings.INTERFACE_UTIL_WARNING_PCT:
                    report.insights.append(f"Interface {name} utilization elevated at {util:.1f}%.")
                    if severity_rank["warning"] > severity_rank[report.status_level]:
                        report.status_level = "warning"
            except (TypeError, ValueError):
                pass

        total_err = int(in_err or 0) + int(out_err or 0)
        if total_err > 100:
            report.insights.append(f"Interface {name} has high error count: {total_err} errors.")
            if severity_rank["warning"] > severity_rank[report.status_level]:
                report.status_level = "warning"

    return report
