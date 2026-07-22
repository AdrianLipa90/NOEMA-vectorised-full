"""Canonical, non-mutating system inventory for the NOEMA portal.

The daemon registry describes processes while ``system_map_v2.json`` describes
logical systems.  The portal must show both without pretending that duplicate
process rows are duplicate systems or that a map card is a live process.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
import re
import time
from typing import Any, Iterable, Mapping


SCHEMA = "NOEMA_PORTAL_SYSTEM_CATALOG/1"
_SLUG_RE = re.compile(r"[^a-z0-9]+")
_HEALTH_ORDER = {"error": 0, "inactive": 1, "stale": 2, "unknown": 3, "running": 4}


def _slug(value: Any) -> str:
    slug = _SLUG_RE.sub("-", str(value or "unknown").casefold()).strip("-")
    return slug or "unknown"


def _runtime_health(row: Mapping[str, Any]) -> str:
    if not bool(row.get("alive")):
        return "inactive"
    status = str(row.get("status") or "unknown").casefold()
    if status in {"error", "failed"}:
        return "error"
    if status in {"stale", "degraded"}:
        return "stale"
    return "running"


def _worst_health(values: Iterable[str]) -> str:
    return min(values, key=lambda value: _HEALTH_ORDER.get(value, _HEALTH_ORDER["unknown"]), default="unknown")


@dataclass(frozen=True)
class RuntimeInstance:
    instance_id: str
    name: str
    pid: int | None
    health: str
    uptime_s: float | None
    surface_claims: tuple[str, ...]
    source: str = "noema_registry"

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["surface_claims"] = list(self.surface_claims)
        return value


def build_system_catalog(
    runtime_rows: Iterable[Mapping[str, Any]],
    map_rows: Iterable[Mapping[str, Any]],
    *,
    observed_at: float | None = None,
) -> dict[str, Any]:
    """Return logical systems plus all their runtime instances.

    Runtime names are grouped only for the logical summary.  Every individual
    process remains in ``instances`` so a duplicate can be diagnosed rather
    than silently discarded.
    """
    observed_at = float(observed_at if observed_at is not None else time.time())
    runtime_by_name: dict[str, list[RuntimeInstance]] = defaultdict(list)
    for row in runtime_rows:
        name = str(row.get("name") or "unknown")
        pid_raw = row.get("pid")
        pid = int(pid_raw) if isinstance(pid_raw, int) and pid_raw > 0 else None
        claims = row.get("surface_claims", [])
        claims = claims if isinstance(claims, list) else []
        instance = RuntimeInstance(
            instance_id=f"runtime:{_slug(name)}:{pid or 'none'}",
            name=name,
            pid=pid,
            health=_runtime_health(row),
            uptime_s=float(row["uptime"]) if isinstance(row.get("uptime"), (int, float)) else None,
            surface_claims=tuple(sorted({str(item) for item in claims if item})),
        )
        runtime_by_name[_slug(name)].append(instance)

    systems: list[dict[str, Any]] = []
    mapped_runtime_names: set[str] = set()
    for row in map_rows:
        if not isinstance(row, Mapping):
            continue
        system_id = str(row.get("id") or row.get("name") or "unknown")
        name = str(row.get("name") or system_id)
        key = _slug(name)
        instances = runtime_by_name.get(key, [])
        mapped_runtime_names.add(key)
        health = _worst_health(instance.health for instance in instances) if instances else "not_runtime"
        systems.append(
            {
                "system_id": system_id,
                "name": name,
                "ordinal": row.get("ordinal"),
                "layer": row.get("layer"),
                "description": row.get("description") or "",
                "source": "system_map_v2.json",
                "runtime_health": health,
                "instance_count": len(instances),
                "instances": [instance.to_dict() for instance in instances],
                "metrics": {
                    "instance_count": len(instances),
                    "running_instances": sum(1 for instance in instances if instance.health == "running"),
                    "stale_instances": sum(1 for instance in instances if instance.health == "stale"),
                },
            }
        )

    for key, instances in sorted(runtime_by_name.items()):
        if key in mapped_runtime_names:
            continue
        systems.append(
            {
                "system_id": f"runtime:{key}",
                "name": instances[0].name,
                "ordinal": None,
                "layer": "runtime_unmapped",
                "description": "Runtime instance without a matching system-map record.",
                "source": "noema_registry",
                "runtime_health": _worst_health(instance.health for instance in instances),
                "instance_count": len(instances),
                "instances": [instance.to_dict() for instance in instances],
                "metrics": {
                    "instance_count": len(instances),
                    "running_instances": sum(1 for instance in instances if instance.health == "running"),
                    "stale_instances": sum(1 for instance in instances if instance.health == "stale"),
                },
            }
        )

    systems.sort(key=lambda item: (str(item.get("layer") or ""), str(item["name"]).casefold()))
    all_instances = [instance for instances in runtime_by_name.values() for instance in instances]
    return {
        "schema": SCHEMA,
        "observed_at": observed_at,
        "source": {"map": "system_map_v2.json", "runtime": "noema_registry"},
        "summary": {
            "logical_systems": len(systems),
            "runtime_instances": len(all_instances),
            "running_instances": sum(1 for instance in all_instances if instance.health == "running"),
            "stale_instances": sum(1 for instance in all_instances if instance.health == "stale"),
            "unmapped_runtime_systems": sum(1 for item in systems if item["layer"] == "runtime_unmapped"),
        },
        "systems": systems,
    }


__all__ = ["SCHEMA", "RuntimeInstance", "build_system_catalog"]
