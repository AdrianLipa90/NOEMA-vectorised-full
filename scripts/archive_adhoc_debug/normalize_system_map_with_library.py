#!/usr/bin/env python3
"""Build a provenance-only projection of the canonical map and NOEMA_LIBRARY.

This tool deliberately does *not* assign orbital coordinates, edge weights,
phase vectors, or performance priorities.  Such values require a declared
measurement and a formula bound to that measurement.  The output is an
auditable, refreshable projection for consumers that need to know exactly
which structural claims are backed by the current map, cards, runtime files,
and library index.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VOLUME_ROOT = ROOT.parents[1]
MAP_PATH = ROOT / "system_map_v2.json"
LIBRARY_DB = VOLUME_ROOT / "NOEMA_LIBRARY" / "INDEX" / "noema_knowledge.db"
PROJECTION_PATH = ROOT / "integration" / "registries" / "system_map_library" / "current.json"
RECEIPTS_ROOT = ROOT / "integration" / "reports" / "system_map_library_normalization" / "receipts"


def _canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _repo_path(value: str) -> Path | None:
    if not value:
        return None
    candidate = Path(value)
    return candidate if candidate.is_absolute() else ROOT / candidate


def _file_evidence(path: Path | None, *, declared_path: str) -> dict[str, Any]:
    if path is None:
        return {"declared_path": declared_path, "status": "not_declared"}
    if not path.is_file():
        return {"declared_path": declared_path, "status": "missing"}
    return {
        "declared_path": declared_path,
        "status": "verified",
        "sha256": _sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _library_snapshot() -> dict[str, Any]:
    if not LIBRARY_DB.is_file():
        return {"status": "unavailable", "path": str(LIBRARY_DB), "reason": "library index is missing"}
    with sqlite3.connect(f"file:{LIBRARY_DB}?mode=ro", uri=True) as connection:
        tables = [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        table_counts = {
            table: connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            for table in tables
        }
        rows = connection.execute(
            "SELECT section, content, updated_at FROM system_map ORDER BY id"
        ).fetchall()
    sections = [
        {
            "section": section,
            "content_sha256": _sha256_bytes(content.encode("utf-8")),
            "updated_at": updated_at,
        }
        for section, content, updated_at in rows
    ]
    return {
        "status": "verified",
        "path": str(LIBRARY_DB),
        "sha256": _sha256_file(LIBRARY_DB),
        "table_counts": table_counts,
        "system_map_sections": sections,
    }


def _system_projection(system: dict[str, Any]) -> dict[str, Any]:
    card_path = str(system.get("card_file") or "")
    runtime_path = str(system.get("runtime_file") or "")
    source_paths = [str(item) for item in system.get("sources", []) if isinstance(item, str)]
    return {
        "id": system["id"],
        "ordinal": system.get("ordinal"),
        "type": system.get("type"),
        "card": _file_evidence(_repo_path(card_path), declared_path=card_path),
        "runtime": _file_evidence(_repo_path(runtime_path), declared_path=runtime_path),
        "sources": [_file_evidence(_repo_path(path), declared_path=path) for path in source_paths],
    }


def build_projection() -> dict[str, Any]:
    map_bytes = MAP_PATH.read_bytes()
    system_map = json.loads(map_bytes.decode("utf-8"))
    systems = system_map.get("systems")
    edges = system_map.get("connections")
    if not isinstance(systems, list) or not isinstance(edges, list):
        raise ValueError("system_map_v2.json requires systems and connections arrays")
    ids = {item.get("id") for item in systems if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(ids) != len(systems):
        raise ValueError("system map contains missing or duplicate system identifiers")
    projected_systems = [_system_projection(item) for item in systems]
    projected_edges = []
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("connection must be an object")
        source = edge.get("from")
        target = edge.get("to")
        endpoints_known = source in ids and target in ids
        projected_edges.append(
            {
                "edge_sha256": _sha256_bytes(_canonical_bytes(edge)),
                "from": source,
                "to": target,
                "type": edge.get("type"),
                "protocol": edge.get("protocol"),
                "topology_status": "verified" if endpoints_known else "external_or_unresolved",
                "weight": {
                    "value": None,
                    "status": "not_computable",
                    "reason": "the canonical edge contract has no per-edge measurement, unit, definition, source, or bounds",
                },
                "phase_measurement_contract": {
                    "status": "missing",
                    "required_before_any_phase_control": [
                        "measured 36D phase vector",
                        "timestamped coherence snapshot",
                        "declared formula",
                        "evidence-bound control policy",
                        "before-and-after benchmark",
                    ],
                },
            }
        )
    library = _library_snapshot()
    summary = next((item for item in library.get("system_map_sections", []) if item["section"] == "system_map_v2_summary"), None)
    return {
        "schema": "noema.system-map-library-projection/v1",
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "policy": {
            "topology_source": "system_map_v2.json",
            "library_role": "evidence_index_and_freshness_audit",
            "numeric_inference": "forbidden_without_measurement_contract",
            "phase_control": "not represented until a measured control contract exists",
        },
        "canonical_map": {
            "path": str(MAP_PATH),
            "sha256": _sha256_bytes(map_bytes),
            "systems": len(systems),
            "connections": len(edges),
        },
        "library": library,
        "library_map_summary": {
            "status": "historical_or_missing" if summary else "missing",
            "record": summary,
            "reason": "library summary is not an identity-level replacement for the canonical map",
        },
        "systems": projected_systems,
        "edges": projected_edges,
    }


def _atomic_replace(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.parent / f".{path.name}.{os.getpid()}.partial"
    if partial.exists():
        raise FileExistsError(partial)
    try:
        with partial.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(partial, path)
    finally:
        if partial.exists():
            partial.unlink()


def _write_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != payload:
            raise OSError(f"receipt collision: {path}")
        return
    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="refresh the derived projection and receipt")
    args = parser.parse_args(argv)
    projection = build_projection()
    payload = _pretty_bytes(projection)
    projection_hash = _sha256_bytes(payload)
    result = {
        "status": "preview",
        "projection_path": str(PROJECTION_PATH),
        "projection_sha256": projection_hash,
        "systems": projection["canonical_map"]["systems"],
        "edges": projection["canonical_map"]["connections"],
    }
    if args.write:
        _atomic_replace(PROJECTION_PATH, payload)
        receipt = {
            "schema": "noema.system-map-library-normalization-receipt/v1",
            "projection_path": str(PROJECTION_PATH),
            "projection_sha256": projection_hash,
            "canonical_map_sha256": projection["canonical_map"]["sha256"],
            "library_sha256": projection["library"].get("sha256"),
            "numeric_inference_used": False,
            "orbital_values_synthesized": False,
            "phase_control_actions_executed": False,
        }
        receipt_path = RECEIPTS_ROOT / f"{projection_hash}.json"
        _write_once(receipt_path, _canonical_bytes(receipt))
        result.update({"status": "written", "receipt_path": str(receipt_path)})
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
