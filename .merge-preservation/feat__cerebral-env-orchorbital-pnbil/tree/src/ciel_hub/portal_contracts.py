"""Publiczne kontrakty danych dla portalu NOEMA.

Kontrakty oddzielają logiczny katalog systemów od obserwowanych instancji
procesu. Nie wykonują operacji runtime i nie zastępują braku danych zerem.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable


SYSTEM_CATALOG_VERSION = "noema.system-catalog/v1"
METRIC_CATALOG_VERSION = "noema.metric-catalog/v1"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalise_name(value: str | None) -> str:
    return "".join(char for char in (value or "").lower() if char.isalnum())


def build_system_catalog(system_map: dict[str, Any], runtime_instances: Iterable[dict[str, Any]], *, source: str, observed_at: str | None = None) -> dict[str, Any]:
    """Return each logical system once and retain every runtime instance."""
    observed_at = observed_at or _utc_now()
    source_systems = system_map.get("systems") if isinstance(system_map, dict) else []
    source_systems = source_systems if isinstance(source_systems, list) else []
    systems: list[dict[str, Any]] = []
    names: dict[str, list[str]] = {}
    # Declared card names are descriptive ("Kuramoto daemon", "NOEMA
    # Real-Imaginal Resonance Bridge") while registry process names are
    # short slugs ("kuramoto", "resonance") — exact-normalised equality
    # matched almost nothing.  daemon_names backs a substring fallback
    # below, restricted to type=="daemon" cards so it can't accidentally
    # match unrelated descriptive text in module/meta_skill card names.
    daemon_names: list[tuple[str, str]] = []
    for raw in source_systems:
        if not isinstance(raw, dict):
            continue
        system_id = str(raw.get("id") or "unknown")
        name = str(raw.get("name") or "Unnamed system")
        norm_name = _normalise_name(name)
        names.setdefault(norm_name, []).append(system_id)
        if raw.get("type") == "daemon":
            daemon_names.append((norm_name, system_id))
        systems.append({
            "system_id": system_id, "module_id": raw.get("layer") or raw.get("type") or None,
            "instance_ids": [], "name": name, "type": raw.get("type") or "unknown",
            "declared_status": raw.get("status") or "unknown", "runtime_status": "unobserved",
            "owner": raw.get("owner") or "system_map_v2",
            "claims": raw.get("card_data", {}).get("epistemic_boundary", {}) if isinstance(raw.get("card_data"), dict) else {},
            "source": raw.get("card_file") or source, "source_timestamp": observed_at,
            "freshness": {"status": "unknown", "age_seconds": None}, "depends_on": raw.get("depends_on_ids") or [],
        })
    system_by_id = {item["system_id"]: item for item in systems}
    instances: list[dict[str, Any]] = []
    for position, raw in enumerate(runtime_instances or []):
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name") or "Unnamed runtime")
        norm_runtime = _normalise_name(name)
        candidates = names.get(norm_runtime, [])
        if not candidates and norm_runtime:
            substring_hits = {
                sid for norm_card, sid in daemon_names
                if norm_runtime in norm_card or norm_card in norm_runtime
            }
            candidates = list(substring_hits)
        system_id = candidates[0] if len(candidates) == 1 else None
        instance_id = str(raw.get("instance_id") or f"runtime:{_normalise_name(name) or 'unknown'}:{raw.get('pid') or position}")
        alive = raw.get("alive")
        instance = {
            "instance_id": instance_id, "system_id": system_id, "name": name,
            "status": raw.get("status") or ("active" if alive is True else "unknown"),
            "pid": raw.get("pid") if isinstance(raw.get("pid"), int) and raw.get("pid") > 0 else None,
            "uptime_seconds": raw.get("uptime") if raw.get("uptime") is not None else raw.get("uptime_s"),
            "source": source, "source_timestamp": observed_at,
            "freshness": {"status": "fresh", "age_seconds": 0},
        }
        instances.append(instance)
        if system_id:
            system_by_id[system_id]["instance_ids"].append(instance_id)
            system_by_id[system_id]["runtime_status"] = "active" if alive else instance["status"]

    # A running process without a declared map card is still a logical runtime
    # system.  This groups duplicate launches while making the missing map
    # relationship explicit instead of silently dropping or guessing it.
    unmapped: dict[str, list[dict[str, Any]]] = {}
    for instance in instances:
        if instance["system_id"] is None:
            unmapped.setdefault(_normalise_name(instance["name"]) or "unknown", []).append(instance)
    for key, grouped in sorted(unmapped.items()):
        system_id = f"runtime:{key}"
        for instance in grouped:
            instance["system_id"] = system_id
        systems.append({
            "system_id": system_id, "module_id": None,
            "instance_ids": [instance["instance_id"] for instance in grouped],
            "name": grouped[0]["name"], "type": "runtime_unmapped",
            "declared_status": "not_mapped", "runtime_status": "active" if any(item["status"] == "active" for item in grouped) else "unknown",
            "owner": "daemon_registry", "claims": {}, "source": source,
            "source_timestamp": observed_at,
            "freshness": {"status": "fresh", "age_seconds": 0}, "depends_on": [],
        })
    return {
        "contract": SYSTEM_CATALOG_VERSION, "observed_at": observed_at, "source": source,
        "systems": systems, "instances": instances,
        "summary": {"logical_systems": len(systems), "runtime_instances": len(instances), "unlinked_instances": sum(item["system_id"] is None for item in instances), "unmapped_runtime_systems": len(unmapped)},
    }


def normalize_metric(metric: dict[str, Any], *, observed_at: str | None = None) -> dict[str, Any]:
    """Normalize a metric while retaining unavailable readings as ``None``."""
    observed_at = observed_at or _utc_now()
    value = metric.get("value")
    source_timestamp = metric.get("source_timestamp") if "source_timestamp" in metric else None
    return {
        "metric_id": metric.get("metric_id") or metric.get("key") or "unknown", "system_id": metric.get("system_id"),
        "label": metric.get("label") or metric.get("key") or "Unnamed metric", "value": value,
        "unit": metric.get("unit") or None, "direction": metric.get("direction") or "neutral",
        "thresholds": metric.get("thresholds") or {"good": metric.get("good_range"), "warning": metric.get("warn_range")},
        "definition": metric.get("definition") or metric.get("desc") or None, "formalism": metric.get("formalism") or None,
        "source": metric.get("source") or "unknown", "source_timestamp": source_timestamp,
        "observed_at": observed_at, "age_seconds": metric.get("age_seconds"),
        "status": metric.get("status") or ("unavailable" if value is None else "unknown"), "error": metric.get("error"),
        "receipt": metric.get("receipt"), "provenance": metric.get("provenance"),
    }
