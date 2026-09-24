#!/usr/bin/env python3
"""Canonicalize explicit system-map identities without synthesizing orbits."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "system_map_v2.json"
CARDS_ROOT = ROOT / "cards" / "base" / "noema_nonlocal_db"
REPORT_ROOT = ROOT / "integration" / "reports" / "system_map_canonicalization"

ID_ALIASES = {
    "011_CIELINGO_CARD_TRACE_ORCHORBITAL": (
        "noema:nonlocal_db:011_CIELINGO_CARD_TRACE_ORCHORBITAL"
    ),
    "noema:card:012:cielingo_polish_linguistic_surface": (
        "noema:nonlocal_db:012_CIELINGO_POLISH_LINGUISTIC_SURFACE"
    ),
}
UNRESOLVED_CQCL_ID = "noema:nonlocal_db:009_CIELINGO_CQCL_QUANTUM_VARIABLES"
CQCL_SOURCE_ID = "noema:card:026:cqcl_flavor_mixing"


def _canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _replace_exact_ids(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _replace_exact_ids(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_replace_exact_ids(item) for item in value]
    if isinstance(value, str):
        return ID_ALIASES.get(value, value)
    return value


def _replace_known_paths(value: Any) -> Any:
    volume_root = ROOT.parents[1]
    replacements = {
        "/tmp/noema_knowledge.db": str(
            volume_root / "CIEL_memories" / "state" / "noema_knowledge.db"
        ),
        "/tmp/noema_taskplan.db": str(
            volume_root / "CIEL_memories" / "state" / "noema_taskplan.db"
        ),
        "/home/adrian/new_volume_rw/NOEMA_PHASE_DATA/": str(
            volume_root / "NOEMA_PHASE_DATA"
        )
        + "/",
        "/home/adrian/new_volume_rw/NOEMA_LIBRARY/state_db": str(
            volume_root / "NOEMA_LIBRARY" / "agent_db" / "agent_state.db"
        ),
    }
    if isinstance(value, dict):
        return {key: _replace_known_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_replace_known_paths(item) for item in value]
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value
    return value


def _unresolved_record(former_connection: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": UNRESOLVED_CQCL_ID,
        "status": "removed_from_active_graph",
        "reason": "no matching system or card record exists in the canonical repository",
        "source_card": "cards/base/noema_nonlocal_db/026_CQCL_FLAVOR_MIXING.noema.card.json",
        "former_connection": former_connection,
        "former_connection_sha256": _sha256(_canonical_bytes(former_connection)),
    }


def _append_unique(records: list[dict[str, Any]], record: dict[str, Any]) -> None:
    if not any(item.get("id") == record.get("id") for item in records):
        records.append(record)


def _disable_raw_prompt_persistence(card: dict[str, Any]) -> None:
    if card.get("id") != "noema:card:030:opencode_raw_log_tsm_bridge":
        return
    card["description"] = (
        "Historical import bridge from explicitly selected archives into the TSM "
        "ledger after CIELingo framing. Live raw-prompt persistence is disabled; "
        "enabling it requires explicit, revocable user consent."
    )
    field_contract = card.setdefault("field_contract", {})
    field_contract["live_db"] = None
    field_contract["live_db_status"] = "disabled"
    field_contract["raw_prompt_storage_enabled"] = False
    field_contract["explicit_revocable_consent_required"] = True
    boundary = card.setdefault("epistemic_boundary", {})
    boundary["historical_consolidation_only"] = True
    boundary["raw_prompt_storage_enabled"] = False


def _canonicalize_card(path: Path, value: dict[str, Any]) -> dict[str, Any]:
    card = _replace_known_paths(_replace_exact_ids(value))
    if card.get("id") == CQCL_SOURCE_ID:
        former = UNRESOLVED_CQCL_ID
        depends_on = card.get("depends_on")
        if isinstance(depends_on, list):
            card["depends_on"] = [item for item in depends_on if item != former]
        unresolved = card.setdefault("unresolved_dependencies", [])
        if not isinstance(unresolved, list):
            raise ValueError(f"{path}: unresolved_dependencies must be an array")
        _append_unique(
            unresolved,
            {
                "id": former,
                "status": "removed_from_active_graph",
                "reason": "no matching system or card record exists in the canonical repository",
            },
        )
    _disable_raw_prompt_persistence(card)
    return card


def _external_node(endpoint: str, connections: list[dict[str, Any]]) -> dict[str, Any]:
    related = [
        connection
        for connection in connections
        if endpoint in {connection.get("from"), connection.get("to")}
    ]
    connection_ids = sorted(
        f"sha256:{_sha256(_canonical_bytes(connection))}" for connection in related
    )
    if endpoint in {"LEARNED_LESSONS.md", "system_map_v2.json"}:
        candidate = ROOT / endpoint
        if not candidate.is_file():
            raise FileNotFoundError(candidate)
        kind = "file"
        path: str | None = endpoint
    elif endpoint == "site":
        candidate = ROOT / "site"
        if not candidate.is_dir():
            raise FileNotFoundError(candidate)
        kind = "directory"
        path = "site/"
    elif endpoint == "filesystem":
        kind = "repository_boundary"
        path = None
    elif endpoint == "user":
        kind = "actor_boundary"
        path = None
    else:
        raise ValueError(f"no evidence-backed external-node rule for {endpoint!r}")
    return {
        "id": endpoint,
        "kind": kind,
        "status": "declared_external",
        "path": path,
        "source_connection_ids": connection_ids,
    }


def _canonicalize_map(value: dict[str, Any]) -> dict[str, Any]:
    system_map = _replace_known_paths(_replace_exact_ids(value))
    systems = system_map.get("systems")
    connections = system_map.get("connections")
    if not isinstance(systems, list) or not isinstance(connections, list):
        raise ValueError("system map requires systems and connections arrays")

    former_connections = [
        connection
        for connection in connections
        if connection.get("from") == UNRESOLVED_CQCL_ID
        or connection.get("to") == UNRESOLVED_CQCL_ID
    ]
    if len(former_connections) > 1:
        raise ValueError(
            f"expected one unresolved CQCL connection, found {len(former_connections)}"
        )
    if former_connections:
        former_connection = former_connections[0]
    else:
        existing_unresolved = system_map.get("unresolved_references", [])
        matches = [
            item
            for item in existing_unresolved
            if isinstance(item, dict) and item.get("id") == UNRESOLVED_CQCL_ID
        ]
        if len(matches) != 1 or not isinstance(
            matches[0].get("former_connection"), dict
        ):
            raise ValueError("unresolved CQCL provenance record is missing")
        former_connection = matches[0]["former_connection"]
    system_map["connections"] = [
        connection for connection in connections if connection is not former_connection
    ]

    for system in systems:
        if not isinstance(system, dict):
            continue
        if system.get("id") == "noema:nonlocal_db:011_CIELINGO_CARD_TRACE_ORCHORBITAL":
            system["name"] = "CIELingo Card Trace EEG and OrchORbital Router"
            system["ordinal_name"] = "CIELingo Card Trace EEG and OrchORbital Router"
        if system.get("id") == CQCL_SOURCE_ID:
            depends = system.get("depends_on_ids")
            if isinstance(depends, list):
                system["depends_on_ids"] = [
                    item for item in depends if item != UNRESOLVED_CQCL_ID
                ]
            satellites = system.get("satellites")
            if isinstance(satellites, list):
                system["satellites"] = [
                    item
                    for item in satellites
                    if not (
                        isinstance(item, dict)
                        and UNRESOLVED_CQCL_ID
                        in {item.get("from"), item.get("to")}
                    )
                ]
        if system.get("id") == "noema:card:030:opencode_raw_log_tsm_bridge":
            card_data = system.setdefault("card_data", {})
            if isinstance(card_data, dict):
                synthetic_card = {"id": system["id"], **card_data}
                _disable_raw_prompt_persistence(synthetic_card)
                system["description"] = synthetic_card["description"]
                system["card_data"] = {
                    key: item for key, item in synthetic_card.items() if key != "id"
                }
        if system.get("id") == "daemon:consolidator":
            system["reads"] = []
            system["read_source_status"] = "unavailable"
            system["read_source_reason"] = "declared legacy memory log does not exist"
        if system.get("id") == "module:knowledge_db":
            system["description"] = (
                "Knowledge DB path is declared by the canonical NOEMA path contract."
            )

    unresolved = system_map.setdefault("unresolved_references", [])
    if not isinstance(unresolved, list):
        raise ValueError("unresolved_references must be an array")
    _append_unique(unresolved, _unresolved_record(former_connection))

    canonical_connections = system_map["connections"]
    for connection in canonical_connections:
        if not isinstance(connection, dict):
            raise ValueError("connection must be an object")
        if "weight" not in connection:
            connection["weight"] = None
            connection["weight_status"] = "unavailable"
        elif connection["weight"] is None:
            connection["weight_status"] = "unavailable"
        else:
            connection["weight_status"] = "unverified"
        connection["weight_unit"] = None
        connection["weight_definition"] = None
        connection["weight_source"] = None

    system_ids = {
        system.get("id")
        for system in systems
        if isinstance(system, dict) and isinstance(system.get("id"), str)
    }
    missing = sorted(
        {
            endpoint
            for connection in canonical_connections
            for endpoint in (connection.get("from"), connection.get("to"))
            if isinstance(endpoint, str) and endpoint not in system_ids
        }
    )
    external_nodes = [
        _external_node(endpoint, canonical_connections) for endpoint in missing
    ]
    external_ids = {node["id"] for node in external_nodes}
    unresolved_active = sorted(
        {
            endpoint
            for connection in canonical_connections
            for endpoint in (connection.get("from"), connection.get("to"))
            if endpoint not in system_ids and endpoint not in external_ids
        }
    )
    if unresolved_active:
        raise ValueError(f"unresolved active endpoints: {unresolved_active}")

    system_map["external_nodes"] = external_nodes
    system_map["total_systems"] = len(systems)
    system_map["total_connections"] = len(canonical_connections)
    system_map["total_external_nodes"] = len(external_nodes)
    system_map["total_unresolved_references"] = len(unresolved)
    system_map["edge_weight_contract"] = {
        "schema": "noema.edge-weight/v1",
        "status": "unverified",
        "active_for_scientific_inference": False,
        "unit": None,
        "definition": None,
        "bounds": None,
        "reason": "legacy numeric values have no per-edge source, unit, definition, or bounds",
    }
    system_map["canonicalization"] = {
        "schema": "noema.system-map-canonicalization/v1",
        "policy": "explicit-identities-no-orbital-inference",
        "id_aliases": [
            {"from": old, "to": new} for old, new in sorted(ID_ALIASES.items())
        ],
        "active_graph_excludes_unresolved_references": True,
    }

    serialized = json.dumps(system_map, ensure_ascii=False)
    forbidden = [token for token in ("/tmp/", "New Volume1", "new_volume_rw") if token in serialized]
    if forbidden:
        raise ValueError(f"forbidden path tokens remain in system map: {forbidden}")
    return system_map


def _atomic_replace(path: Path, payload: bytes) -> None:
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
            raise OSError(f"canonicalization receipt collision: {path}")
        return
    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def build_changes() -> tuple[dict[Path, bytes], dict[str, Any]]:
    changes: dict[Path, bytes] = {}
    before_hashes: dict[str, str] = {}

    original_map_bytes = MAP_PATH.read_bytes()
    before_hashes[str(MAP_PATH.relative_to(ROOT))] = _sha256(original_map_bytes)
    original_map = json.loads(original_map_bytes.decode("utf-8"))
    canonical_map = _canonicalize_map(original_map)
    changes[MAP_PATH] = _pretty_bytes(canonical_map)

    for path in sorted(CARDS_ROOT.glob("*.json")):
        original_bytes = path.read_bytes()
        value = json.loads(original_bytes.decode("utf-8"))
        if not isinstance(value, dict):
            continue
        canonical = _canonicalize_card(path, value)
        if canonical != value:
            payload = _pretty_bytes(canonical)
            changes[path] = payload
            before_hashes[str(path.relative_to(ROOT))] = _sha256(original_bytes)

    changed = {
        str(path.relative_to(ROOT)): {
            "before_sha256": before_hashes[str(path.relative_to(ROOT))],
            "after_sha256": _sha256(payload),
        }
        for path, payload in changes.items()
        if payload != path.read_bytes()
    }
    report = {
        "schema": "noema.system-map-canonicalization-receipt/v1",
        "script": str(Path(__file__).resolve()),
        "script_sha256": _sha256(Path(__file__).read_bytes()),
        "changed_files": changed,
        "result_map_sha256": _sha256(changes[MAP_PATH]),
        "inference_used": False,
        "orbital_values_synthesized": False,
    }
    return changes, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)

    changes, report = build_changes()
    pending = [path for path, payload in changes.items() if path.read_bytes() != payload]
    if args.check:
        print(
            json.dumps(
                {
                    "status": "canonical" if not pending else "changes_required",
                    "pending": [str(path.relative_to(ROOT)) for path in pending],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0 if not pending else 1

    for path in pending:
        _atomic_replace(path, changes[path])
    result_hash = report["result_map_sha256"]
    receipt_path = REPORT_ROOT / "receipts" / f"{result_hash}.json"
    if not pending and receipt_path.exists():
        print(
            json.dumps(
                {
                    "status": "already_canonical",
                    "changed": [],
                    "map_sha256": result_hash,
                    "receipt_path": str(receipt_path),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    report["receipt_path"] = str(receipt_path)
    _write_once(receipt_path, _canonical_bytes(report))
    print(
        json.dumps(
            {
                "status": "applied",
                "changed": [str(path.relative_to(ROOT)) for path in pending],
                "map_sha256": result_hash,
                "receipt_path": str(receipt_path),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
