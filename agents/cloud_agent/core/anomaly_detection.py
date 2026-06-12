"""Anomaly detection engine — evaluates normalized metrics against configurable thresholds.

Works on the canonical metric names produced by normalization.py.
Completely provider-agnostic: the same rules apply to AWS, Azure, GCP, or any custom adapter.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from config.settings import settings


@dataclass
class AnomalyRule:
    """A single threshold rule for one metric."""
    metric:         str
    warning_level:  float
    critical_level: float
    unit:           str = "%"

    def evaluate(self, value: float) -> Tuple[str, str]:
        """
        Returns (status_level, insight_message).
        status_level: 'healthy' | 'warning' | 'critical'
        """
        if value >= self.critical_level:
            return (
                "critical",
                f"{self.metric} is CRITICAL at {value}{self.unit} "
                f"(threshold: {self.critical_level}{self.unit})",
            )
        if value >= self.warning_level:
            return (
                "warning",
                f"{self.metric} is elevated at {value}{self.unit} "
                f"(threshold: {self.warning_level}{self.unit})",
            )
        return "healthy", ""


# ── Default rule set (driven by settings) ─────────────────────────────────────
DEFAULT_RULES: List[AnomalyRule] = [
    AnomalyRule(
        metric="cpu_utilization_pct",
        warning_level=settings.CPU_WARNING_THRESHOLD,
        critical_level=settings.CPU_CRITICAL_THRESHOLD,
        unit="%",
    ),
    AnomalyRule(
        metric="memory_utilization_pct",
        warning_level=settings.MEMORY_WARNING_THRESHOLD,
        critical_level=settings.MEMORY_CRITICAL_THRESHOLD,
        unit="%",
    ),
    AnomalyRule(
        metric="error_rate_pct",
        warning_level=settings.ERROR_RATE_WARNING_THRESHOLD * 100,   # stored as 0-1, display as %
        critical_level=settings.ERROR_RATE_CRITICAL_THRESHOLD * 100,
        unit="%",
    ),
    AnomalyRule(
        metric="latency_p99_ms",
        warning_level=500.0,
        critical_level=1000.0,
        unit="ms",
    ),
]


@dataclass
class AnomalyReport:
    status_level: str = "healthy"          # overall worst level
    insights:     List[str] = field(default_factory=list)


def detect_anomalies(
    metrics: Dict[str, Any],
    rules: List[AnomalyRule] = DEFAULT_RULES,
) -> AnomalyReport:
    """
    Run all rules against the normalized metrics dict.

    Returns an AnomalyReport with the aggregate status_level and list of insights.
    """
    report = AnomalyReport()
    severity_rank = {"healthy": 0, "warning": 1, "critical": 2}

    for rule in rules:
        raw_value = metrics.get(rule.metric)
        if raw_value is None:
            continue
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            continue

        level, insight = rule.evaluate(value)
        if insight:
            report.insights.append(insight)
        if severity_rank[level] > severity_rank[report.status_level]:
            report.status_level = level

    return report
