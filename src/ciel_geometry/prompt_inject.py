from __future__ import annotations

"""Shared prompt-inject helpers for CIELingo and agent hooks."""

from collections import defaultdict
from typing import Any, Mapping

PROMPT_INJECT_TIMEOUT_SECONDS = 120


def collect_noema_metrics_summary() -> dict[str, Any]:
    """Collect the current NOEMA metric snapshot without relying on a server."""
    try:
        from ciel_geometry.noema_metrics import summary as noema_summary

        data = noema_summary()
        return dict(data) if isinstance(data, dict) else {"total": 0, "metrics": {}}
    except Exception:
        return {"total": 0, "ok": 0, "warning": 0, "critical": 0, "unknown": 0, "metrics": {}}


def render_noema_metrics_block(metrics_summary: Mapping[str, Any] | None) -> str:
    """Render a compact, sorted metrics block for prompt injection."""
    metrics_summary = dict(metrics_summary or {})
    metrics = metrics_summary.get("metrics", {})
    if not isinstance(metrics, dict) or not metrics:
        return ""

    try:
        from ciel_geometry.noema_metrics import get_registry

        defs = get_registry().definitions
    except Exception:
        defs = {}

    grouped: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for key, sample in metrics.items():
        if not isinstance(sample, dict):
            continue
        category = getattr(defs.get(key), "category", "other") if defs else "other"
        grouped[str(category)].append((str(key), dict(sample)))

    category_order = ["system", "coherence", "ethics", "memory", "daemon", "other"]
    lines = ["=== NOEMA_METRICS_BEGIN ==="]
    lines.append(
        "summary="
        f"total={int(metrics_summary.get('total', len(metrics)))} "
        f"ok={int(metrics_summary.get('ok', 0))} "
        f"warning={int(metrics_summary.get('warning', 0))} "
        f"critical={int(metrics_summary.get('critical', 0))} "
        f"unknown={int(metrics_summary.get('unknown', 0))}"
    )
    if metrics_summary.get("timestamp") is not None:
        lines.append(f"timestamp={metrics_summary.get('timestamp')}")

    for category in category_order:
        items = grouped.get(category)
        if not items:
            continue
        lines.append(f"[{category}]")
        for key, sample in sorted(items, key=lambda item: item[0]):
            value = sample.get("value")
            unit = sample.get("unit", "")
            status = sample.get("status", "unknown")
            source = sample.get("source", "")
            desc = str(sample.get("description", "")).strip()
            lines.append(
                f"- {key}: {value}"
                f"{f' {unit}' if unit else ''}"
                f" | status={status}"
                f"{f' | source={source}' if source else ''}"
                f"{f' | {desc}' if desc else ''}"
            )

    lines.append("=== NOEMA_METRICS_END ===")
    return "\n".join(lines)


def build_prompt_inject_context(
    *,
    message: str,
    cielingo_block: str = "",
    metrics_summary: Mapping[str, Any] | None = None,
    inject_label: str = "CIELINGO_START_PROMPT_INJECT",
) -> str:
    """Build the final prompt-inject context block."""
    parts: list[str] = [f"=== {inject_label}_BEGIN ==="]
    if cielingo_block.strip():
        parts.append(cielingo_block.strip())
    metrics_block = render_noema_metrics_block(metrics_summary)
    if metrics_block:
        parts.append(metrics_block)
    parts.append("=== ORIGINAL_PROMPT_BEGIN ===")
    parts.append(message[:8000])
    parts.append("=== ORIGINAL_PROMPT_END ===")
    parts.append(f"=== {inject_label}_END ===")
    return "\n".join(parts)


__all__ = [
    "PROMPT_INJECT_TIMEOUT_SECONDS",
    "build_prompt_inject_context",
    "collect_noema_metrics_summary",
    "render_noema_metrics_block",
]
