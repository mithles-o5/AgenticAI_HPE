"""
com_mock/agents/validator.py
────────────────────────────
Agent 5 — ValidatorAgent

Validates synthesized data for:
  1. Referential integrity — every ref field must point to an existing URI
  2. Required fields — non-nullable required refs must be populated
  3. Enum compliance — enum fields must use a valid value

If errors are found and retries < max_validation_retries, the failed resource
types are sent back to the DataSynthesizer for regeneration.

This validation-retry loop is what makes the generated data trustworthy.
"""

from __future__ import annotations

import logging
from typing import Callable, Coroutine

from com_mock.resource_graph import ONEVIEW_RESOURCE_SCHEMAS

logger = logging.getLogger(__name__)


async def run_validator(
    state: dict,
    report: Callable[[str], Coroutine],
) -> dict:
    """
    LangGraph node: ValidatorAgent

    Checks all synthesized resources and flags types that need regeneration.
    """
    synthesized: dict[str, list[dict]] = state.get("synthesized_data", {})
    retries: dict[str, int] = dict(state.get("validation_retries", {}))
    max_retries: int = state.get("max_validation_retries", 3)
    is_hpe: bool = state.get("is_hpe_oneview", False)

    schemas = ONEVIEW_RESOURCE_SCHEMAS if is_hpe else {}

    await report("🔎 ValidatorAgent: checking referential integrity...")

    # Build URI lookup: slug → set of URIs
    uri_sets: dict[str, set[str]] = {
        slug: {r.get("uri", "") for r in items}
        for slug, items in synthesized.items()
    }

    all_errors: dict[str, list[str]] = {}
    needs_retry: list[str] = []

    for resource_slug, instances in synthesized.items():
        schema = schemas.get(resource_slug, {})
        fields = schema.get("fields", {})
        errors: list[str] = []

        for idx, item in enumerate(instances):
            for field_name, spec in fields.items():
                ftype = spec.get("type", "")
                value = item.get(field_name)

                # ── Ref check ─────────────────────────────────────────
                if ftype == "ref":
                    target = spec.get("target", "")
                    required = spec.get("required", False)
                    nullable = spec.get("nullable", True)

                    if value is None:
                        if required:
                            errors.append(
                                f"[{idx}] {field_name}: required ref is null "
                                f"(target: {target})"
                            )
                    else:
                        target_uris = uri_sets.get(target, set())
                        if target_uris and value not in target_uris:
                            errors.append(
                                f"[{idx}] {field_name}={value!r} not found in {target}"
                            )

                # ── Array ref check ───────────────────────────────────
                elif ftype == "array_ref":
                    target = spec.get("target", "")
                    uris: list = value if isinstance(value, list) else []
                    target_uris = uri_sets.get(target, set())
                    if target_uris:
                        for uri in uris:
                            if uri not in target_uris:
                                errors.append(
                                    f"[{idx}] {field_name}[] has unknown URI {uri!r} "
                                    f"(target: {target})"
                                )

                # ── Enum check ────────────────────────────────────────
                elif ftype in ("enum", "enum_int"):
                    allowed = spec.get("values", [])
                    if allowed and value not in allowed and value is not None:
                        errors.append(
                            f"[{idx}] {field_name}={value!r} not in allowed values {allowed}"
                        )

        if errors:
            all_errors[resource_slug] = errors
            current_retries = retries.get(resource_slug, 0)
            if current_retries < max_retries:
                needs_retry.append(resource_slug)
                retries[resource_slug] = current_retries + 1
                await report(
                    f"  ⚠️  {resource_slug}: {len(errors)} errors "
                    f"(retry {current_retries + 1}/{max_retries})"
                )
            else:
                await report(
                    f"  ⛔ {resource_slug}: {len(errors)} errors — "
                    f"max retries reached, proceeding with warnings"
                )
        else:
            await report(f"  ✅ {resource_slug}: valid")

    passed = len(synthesized) - len(all_errors)
    await report(
        f"🔎 Validation complete: {passed}/{len(synthesized)} types passed | "
        f"{len(needs_retry)} scheduled for retry"
    )

    new_status = "synthesizing" if needs_retry else "seeding"

    return {
        "validation_errors":     all_errors,
        "validation_retries":    retries,
        "retry_resource_types":  needs_retry,
        "status":                new_status,
        "progress_log":          state.get("progress_log", [])
                                 + [
                                     f"Validation: {passed}/{len(synthesized)} passed, "
                                     f"{len(needs_retry)} retrying"
                                 ],
    }
