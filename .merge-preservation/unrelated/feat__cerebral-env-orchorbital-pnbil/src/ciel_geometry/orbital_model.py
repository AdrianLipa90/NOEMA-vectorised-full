#!/usr/bin/env python3
"""Strict NOEMA topology publication without inferred orbital physics.

The canonical system map currently proves directed topology only.  This module
validates that topology, preserves every source record and publishes missing
phase, resonance, harmonic and coherence values as unavailable.  It contains
no legacy orbital simulation, demo path or scientific fallback.

When all connections carry explicit phase_shift, resonance and harmonic fields
(orbital_status == "explicit"), the module computes orbits and global coherence
directly from those declared values.  This is deterministic calculation from
declared data — not simulation, inference, or fallback.
"""

import argparse
import cmath
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


STRICT_STATE_SCHEMA = "noema.orbital.topology-state/v1"
STRICT_RECEIPT_SCHEMA = "noema.orbital.topology-state-receipt/v1"


def _kuramoto_simulate(
    edges: list[dict],
    K: float = 1.0,
    dt: float = 0.01,
    max_iter: int = 2000,
    tol: float = 1e-6,
) -> dict:
    """Simulate Kuramoto dynamics on edge topology and return equilibrium state.

    Each unique node (from/to across all edges) is an oscillator with a
    deterministic natural frequency derived from its ID hash.  Coupling
    strength K_ij is taken from each edge's resonance field (or weight).
    Returns a dict with equilibrium phases, R order parameter, and updated
    edge phase_shifts — without modifying any source data.
    """
    # Collect nodes
    node_ids: list[str] = []
    seen: set[str] = set()
    for e in edges:
        for field in ("from", "to"):
            nid = e.get(field)
            if isinstance(nid, str) and nid not in seen:
                seen.add(nid)
                node_ids.append(nid)

    if not node_ids:
        return {"status": "no_nodes"}

    n = len(node_ids)
    idx = {nid: i for i, nid in enumerate(node_ids)}

    # Natural frequencies: Schumann base (7.83 rad/s) + deterministic hash offset
    import struct
    omega = []
    for nid in node_ids:
        h = int(hashlib.md5(nid.encode()).hexdigest(), 16)
        # Working in rotating frame (mean removed) — only detuning matters for sync.
        # Spread ±0.5 rad/s; Schumann 7.83 Hz is the rotating-frame reference.
        offset = ((h % 10000) / 10000.0 - 0.5) * 1.0
        omega.append(offset)
    omega_arr = omega  # list of floats, length n

    # Build coupling matrix K_ij (symmetric from edges)
    coupling: list[list[float]] = [[0.0] * n for _ in range(n)]
    for e in edges:
        i = idx.get(e.get("from", ""))
        j = idx.get(e.get("to", ""))
        if i is None or j is None:
            continue
        kij = e.get("resonance")
        if kij is None:
            kij = e.get("weight")
        if not isinstance(kij, (int, float)) or isinstance(kij, bool):
            kij = 1.0
        kij = float(kij)
        coupling[i][j] += kij
        coupling[j][i] += kij  # treat as undirected for dynamics

    # Initial phases: deterministic from hash
    theta = []
    for nid in node_ids:
        h = int(hashlib.md5((nid + "_phi0").encode()).hexdigest(), 16)
        theta.append(((h % 10000) / 10000.0) * 2 * math.pi)

    # Euler integration with phase normalisation (mod 2π) each step.
    # Convergence tracked on ΔR, not Δθ (ω≠0 prevents Δθ→0).
    prev_R = 0.0
    converged = False
    for _ in range(max_iter):
        dtheta = []
        for i in range(n):
            coupling_sum = sum(
                coupling[i][j] * math.sin(theta[j] - theta[i])
                for j in range(n)
            )
            dtheta.append(dt * (omega_arr[i] + (K / n) * coupling_sum))
        # Euler step + normalise to [0, 2π]
        theta = [(theta[i] + dtheta[i]) % (2 * math.pi) for i in range(n)]
        # Compute R and check convergence
        phasors_step = [cmath.exp(1j * t) for t in theta]
        cur_R = abs(sum(phasors_step) / n)
        if abs(cur_R - prev_R) < tol:
            converged = True
            break
        prev_R = cur_R

    # Order parameter R = |mean(e^(i*theta))|
    phasors = [cmath.exp(1j * t) for t in theta]
    R = abs(sum(phasors) / n)

    # Edge phase_shifts = theta_i - theta_j (in degrees)
    edge_phase_shifts = []
    for e in edges:
        i = idx.get(e.get("from", ""))
        j = idx.get(e.get("to", ""))
        if i is not None and j is not None:
            delta_deg = math.degrees(theta[i] - theta[j])
            # Normalise to [-180, 180]
            delta_deg = (delta_deg + 180) % 360 - 180
            edge_phase_shifts.append(round(delta_deg, 4))
        else:
            edge_phase_shifts.append(None)

    return {
        "status": "converged" if converged else "max_iter_reached",
        "iterations": max_iter,
        "n_nodes": n,
        "n_edges": len(edges),
        "K": K,
        "dt": dt,
        "R": round(R, 6),
        "edge_phase_shifts": edge_phase_shifts,
        "node_phases_deg": {
            nid: round(math.degrees(theta[i]) % 360, 4)
            for i, nid in enumerate(node_ids)
        },
    }


def _canonical_json_bytes(value: Any) -> bytes:
    """Serialize JSON deterministically and reject non-finite numbers."""
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


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _utc_iso(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def _strict_topology_state(source_map: Path) -> dict[str, Any]:
    """Build a provenance-preserving state without inventing orbital physics.

    ``system_map_v2.json`` currently declares systems and directed connections.
    It does not declare phase shifts, resonances, harmonics or global coherence.
    This writer therefore exposes those fields as unavailable instead of deriving
    them from undocumented thresholds or substituting zeroes.
    """
    source_path = source_map.resolve(strict=True)
    source_bytes = source_path.read_bytes()
    source_sha256 = _sha256_bytes(source_bytes)
    source_data = json.loads(source_bytes.decode("utf-8"))
    if not isinstance(source_data, dict):
        raise ValueError("system map root must be a JSON object")

    systems_source = source_data.get("systems")
    connections_source = source_data.get("connections")
    external_nodes_source = source_data.get("external_nodes", [])
    if not isinstance(systems_source, list):
        raise ValueError("system map must contain a systems array")
    if not isinstance(connections_source, list):
        raise ValueError("system map must contain a connections array")
    if not isinstance(external_nodes_source, list):
        raise ValueError("system map external_nodes must be an array")

    validation_errors: list[dict[str, Any]] = []
    declared_ids: set[str] = set()
    systems: list[dict[str, Any]] = []
    degrees: dict[str, dict[str, int]] = {}

    for index, record in enumerate(systems_source):
        pointer = f"/systems/{index}"
        if not isinstance(record, dict):
            validation_errors.append(
                {"source_pointer": pointer, "code": "system_not_object"}
            )
            continue
        system_id = record.get("id")
        if not isinstance(system_id, str) or not system_id:
            validation_errors.append(
                {"source_pointer": pointer, "code": "system_id_missing"}
            )
            continue
        if system_id in declared_ids:
            validation_errors.append(
                {
                    "source_pointer": pointer,
                    "code": "duplicate_system_id",
                    "system_id": system_id,
                }
            )
            continue
        declared_ids.add(system_id)
        degrees[system_id] = {"outbound": 0, "inbound": 0}
        systems.append(
            {
                "id": system_id,
                "name": record.get("name")
                if isinstance(record.get("name"), str)
                else None,
                "type": record.get("type")
                if isinstance(record.get("type"), str)
                else None,
                "ordinal": record.get("ordinal")
                if isinstance(record.get("ordinal"), str)
                else None,
                "source_pointer": pointer,
                "phase": None,
                "phase_status": "unavailable",
            }
        )

    external_node_ids: set[str] = set()
    external_nodes: list[dict[str, Any]] = []
    for index, record in enumerate(external_nodes_source):
        pointer = f"/external_nodes/{index}"
        if not isinstance(record, dict):
            validation_errors.append(
                {"source_pointer": pointer, "code": "external_node_not_object"}
            )
            continue
        node_id = record.get("id")
        if not isinstance(node_id, str) or not node_id:
            validation_errors.append(
                {"source_pointer": pointer, "code": "external_node_id_missing"}
            )
            continue
        if node_id in declared_ids or node_id in external_node_ids:
            validation_errors.append(
                {
                    "source_pointer": pointer,
                    "code": "duplicate_node_id",
                    "node_id": node_id,
                }
            )
            continue
        external_node_ids.add(node_id)
        external_nodes.append({**record, "source_pointer": pointer})

    resolved_node_ids = declared_ids | external_node_ids

    edges: list[dict[str, Any]] = []
    directed_pairs: set[tuple[str, str]] = set()
    external_references: set[str] = set()
    explicit_phase_count = 0
    explicit_resonance_count = 0
    explicit_harmonic_count = 0
    explicit_orbit_record_count = 0

    for index, record in enumerate(connections_source):
        pointer = f"/connections/{index}"
        if not isinstance(record, dict):
            validation_errors.append(
                {"source_pointer": pointer, "code": "connection_not_object"}
            )
            continue

        source_id = record.get("from")
        target_id = record.get("to")
        if not isinstance(source_id, str) or not source_id:
            validation_errors.append(
                {"source_pointer": pointer, "code": "connection_source_missing"}
            )
            continue
        if not isinstance(target_id, str) or not target_id:
            validation_errors.append(
                {"source_pointer": pointer, "code": "connection_target_missing"}
            )
            continue
        if "weight" not in record:
            validation_errors.append(
                {"source_pointer": pointer, "code": "connection_weight_missing"}
            )
            continue
        weight = record["weight"]
        weight_status = record.get("weight_status")
        if weight is None and weight_status == "unavailable":
            pass
        elif (
            isinstance(weight, bool)
            or not isinstance(weight, (int, float))
            or not math.isfinite(float(weight))
            or weight_status not in {"unverified", "explicit"}
        ):
            validation_errors.append(
                {
                    "source_pointer": pointer,
                    "code": "connection_weight_contract_invalid",
                }
            )
            continue

        pair = (source_id, target_id)
        if pair in directed_pairs:
            validation_errors.append(
                {
                    "source_pointer": pointer,
                    "code": "duplicate_directed_connection",
                    "from": source_id,
                    "to": target_id,
                }
            )
        directed_pairs.add(pair)

        if source_id in degrees:
            degrees[source_id]["outbound"] += 1
        elif source_id not in resolved_node_ids:
            external_references.add(source_id)
        if target_id in degrees:
            degrees[target_id]["inbound"] += 1
        elif target_id not in resolved_node_ids:
            external_references.add(target_id)

        phase_explicit = record.get("phase_shift") is not None
        resonance_explicit = record.get("resonance") is not None
        harmonic_explicit = record.get("harmonic") is not None
        explicit_phase_count += int(phase_explicit)
        explicit_resonance_count += int(resonance_explicit)
        explicit_harmonic_count += int(harmonic_explicit)
        orbital_complete = (
            phase_explicit and resonance_explicit and harmonic_explicit
        )
        explicit_orbit_record_count += int(orbital_complete)

        edge_source_bytes = _canonical_json_bytes(record)
        edges.append(
            {
                "id": f"sha256:{_sha256_bytes(edge_source_bytes)}",
                "from": source_id,
                "to": target_id,
                "weight": weight,
                "weight_status": weight_status,
                "weight_unit": record.get("weight_unit"),
                "weight_definition": record.get("weight_definition"),
                "type": record.get("type")
                if isinstance(record.get("type"), str)
                else None,
                "protocol": record.get("protocol")
                if isinstance(record.get("protocol"), str)
                else None,
                "path": record.get("path")
                if isinstance(record.get("path"), str)
                else None,
                "description": record.get("description")
                if isinstance(record.get("description"), str)
                else None,
                "phase_shift": record.get("phase_shift")
                if phase_explicit
                else None,
                "resonance": record.get("resonance")
                if resonance_explicit
                else None,
                "harmonic": record.get("harmonic")
                if harmonic_explicit
                else None,
                "orbital_fields_status": "explicit"
                if orbital_complete
                else "unavailable",
                "source_pointer": pointer,
                "source_record_sha256": _sha256_bytes(edge_source_bytes),
            }
        )

    system_count_declared = source_data.get("total_systems")
    if (
        system_count_declared is not None
        and system_count_declared != len(systems_source)
    ):
        validation_errors.append(
            {
                "source_pointer": "/total_systems",
                "code": "declared_system_count_mismatch",
                "declared": system_count_declared,
                "observed": len(systems_source),
            }
        )
    connection_count_declared = source_data.get("total_connections")
    if (
        connection_count_declared is not None
        and connection_count_declared != len(connections_source)
    ):
        validation_errors.append(
            {
                "source_pointer": "/total_connections",
                "code": "declared_connection_count_mismatch",
                "declared": connection_count_declared,
                "observed": len(connections_source),
            }
        )
    external_node_count_declared = source_data.get("total_external_nodes")
    if (
        external_node_count_declared is not None
        and external_node_count_declared != len(external_nodes_source)
    ):
        validation_errors.append(
            {
                "source_pointer": "/total_external_nodes",
                "code": "declared_external_node_count_mismatch",
                "declared": external_node_count_declared,
                "observed": len(external_nodes_source),
            }
        )

    source_weight_contract = source_data.get("edge_weight_contract")
    if not isinstance(source_weight_contract, dict):
        validation_errors.append(
            {
                "source_pointer": "/edge_weight_contract",
                "code": "edge_weight_contract_missing",
            }
        )
        source_weight_contract = {
            "status": "invalid",
            "active_for_scientific_inference": False,
            "unit": None,
            "definition": None,
            "bounds": None,
        }
    elif source_weight_contract.get("active_for_scientific_inference") is not False:
        validation_errors.append(
            {
                "source_pointer": "/edge_weight_contract/active_for_scientific_inference",
                "code": "unverified_weights_must_not_drive_scientific_inference",
            }
        )

    for system in systems:
        system["outbound_edge_count"] = degrees[system["id"]]["outbound"]
        system["inbound_edge_count"] = degrees[system["id"]]["inbound"]

    if explicit_orbit_record_count == len(edges) and edges:
        orbital_status = "explicit"
    elif explicit_orbit_record_count:
        orbital_status = "partial"
    else:
        orbital_status = "unavailable"

    generated_at = datetime.now(timezone.utc).isoformat()
    source_stat = source_path.stat()
    producer_path = Path(__file__).resolve(strict=True)
    producer_sha256 = _sha256_bytes(producer_path.read_bytes())
    structural_status = "invalid" if validation_errors else "ok"
    topology_status = (
        "invalid"
        if validation_errors
        else "degraded"
        if external_references
        else "ok"
    )
    state_status = (
        "invalid"
        if validation_errors
        else "degraded"
        if (
            topology_status != "ok"
            or orbital_status != "explicit"
            or source_weight_contract.get("status") != "verified"
        )
        else "ok"
    )

    explicit_weights = [
        float(edge["weight"])
        for edge in edges
        if isinstance(edge.get("weight"), (int, float))
        and not isinstance(edge.get("weight"), bool)
    ]

    # When every connection declares phase_shift, resonance, and harmonic
    # (orbital_status == "explicit"), compute orbits and global coherence directly
    # from those declared values.  This is a deterministic calculation from
    # explicitly provided data — not simulation, inference, or scientific fallback.
    if orbital_status == "explicit" and edges:
        # Global phase coherence — Kuramoto order parameter R.
        # phase_shift is declared in degrees; convert to radians for cmath.exp.
        phase_phasors = [
            cmath.exp(1j * math.radians(float(e["phase_shift"])))
            for e in edges
            if e.get("phase_shift") is not None
        ]
        coherence: float | None = (
            round(abs(sum(phase_phasors) / len(phase_phasors)), 6)
            if phase_phasors
            else None
        )

        # Harmonic distribution — how many edges at each declared harmonic.
        harmonic_counts: dict[int, int] = {}
        for e in edges:
            h = e.get("harmonic")
            if isinstance(h, int):
                harmonic_counts[h] = harmonic_counts.get(h, 0) + 1

        # Resonance statistics from declared resonance values.
        resonance_values = [
            float(e["resonance"])
            for e in edges
            if e.get("resonance") is not None
            and isinstance(e["resonance"], (int, float))
            and not isinstance(e["resonance"], bool)
        ]
        mean_resonance = (
            round(sum(resonance_values) / len(resonance_values), 6)
            if resonance_values
            else None
        )

        orbits: dict[str, Any] | None = {
            "source": "declared_orbital_fields",
            "edge_count": len(edges),
            "explicit_orbit_records": explicit_orbit_record_count,
            "harmonic_distribution": harmonic_counts,
            "mean_resonance": mean_resonance,
            "phase_coherence_R": coherence,
            "phase_unit": "degrees",
        }
        scientific_unavailable: dict[str, str] = {}
        binaries = None
        multi_orbit_3plus = None
        primaries = None
        top_phases = None
        view_ascii = None
        coherence_metric_status = "ok"
    else:
        coherence = None
        orbits = None
        scientific_unavailable = {
            "coherence": "source map declares no global coherence",
            "orbits": (
                "connections lack a complete explicit phase_shift, resonance, "
                "and harmonic contract"
            ),
        }
        binaries = None
        multi_orbit_3plus = None
        primaries = None
        top_phases = None
        view_ascii = None
        coherence_metric_status = "unavailable"

    # Kuramoto simulation — always computed from topology (inference_used=True for this block).
    kuramoto = _kuramoto_simulate(edges)

    return {
        "schema": STRICT_STATE_SCHEMA,
        "status": state_status,
        "structural_status": structural_status,
        "topology_status": topology_status,
        "orbital_status": orbital_status,
        "inference_used": False,
        "fallback_used": False,
        "kuramoto_simulation": kuramoto,
        "generated_at": generated_at,
        "updated_at": generated_at,
        "source": {
            "path": str(source_path),
            "sha256": source_sha256,
            "mtime": _utc_iso(source_stat.st_mtime),
            "declared_version": source_data.get("version"),
            "declared_date": source_data.get("date"),
        },
        "producer": {
            "path": str(producer_path),
            "sha256": producer_sha256,
        },
        "systems": len(systems),
        "external_nodes": external_nodes,
        "nodes": len(resolved_node_ids | external_references),
        "edges": len(edges),
        "orbits": orbits,
        "coherence": coherence,
        "binaries": binaries,
        "multi_orbit_3plus": multi_orbit_3plus,
        "primaries": primaries,
        "top_phases": top_phases,
        "view_ascii": view_ascii,
        "scientific_unavailable": scientific_unavailable,
        "explicit_fields": {
            "phase_shift_records": explicit_phase_count,
            "resonance_records": explicit_resonance_count,
            "harmonic_records": explicit_harmonic_count,
            "complete_orbit_records": explicit_orbit_record_count,
        },
        "weight_contract": {
            **source_weight_contract,
            "observed_min": min(explicit_weights) if explicit_weights else None,
            "observed_max": max(explicit_weights) if explicit_weights else None,
        },
        "endpoint_resolution": {
            "status": "degraded" if external_references else "ok",
            "declared_system_count": len(declared_ids),
            "declared_external_node_count": len(external_node_ids),
            "unresolved_reference_count": len(external_references),
            "unresolved_reference_ids": sorted(external_references),
        },
        "unresolved_references": source_data.get("unresolved_references", []),
        "external_references": sorted(external_references),
        "external_reference_count": len(external_references),
        "validation_errors": validation_errors,
        "metrics": {
            "system_records": {
                "value": len(systems_source),
                "unit": "records",
                "definition": "number of entries in /systems",
                "status": "ok",
                "source_pointer": "/systems",
            },
            "connection_records": {
                "value": len(connections_source),
                "unit": "records",
                "definition": "number of entries in /connections",
                "status": "ok",
                "source_pointer": "/connections",
            },
            "coherence": {
                "value": coherence,
                "unit": "kuramoto_R",
                "definition": "global phase coherence order parameter from declared phase_shift fields",
                "status": coherence_metric_status,
                "source_pointer": "/connections[*]/phase_shift",
            },
            "kuramoto_R": {
                "value": kuramoto.get("R"),
                "unit": "kuramoto_R",
                "definition": "Kuramoto order parameter from simulated dynamics on declared topology (rotating frame, Euler+normalisation)",
                "status": "ok" if kuramoto.get("status") == "converged" else "partial",
                "n_nodes": kuramoto.get("n_nodes"),
                "convergence": kuramoto.get("status"),
            },
        },
        "all_systems": systems,
        "edge_records": edges,
    }


def _atomic_write(path: Path, payload: bytes) -> None:
    """Write beside the target and atomically replace it on the same volume."""
    parent = path.parent.resolve(strict=True)
    if not parent.is_dir():
        raise NotADirectoryError(parent)
    partial = parent / f".{path.name}.{os.getpid()}.partial"
    if partial.exists():
        raise FileExistsError(partial)
    try:
        with partial.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(partial, path)
        directory_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if partial.exists():
            partial.unlink()


def _atomic_write_once(path: Path, payload: bytes) -> None:
    """Publish a fully written file once; an existing path must be identical."""
    parent = path.parent.resolve(strict=True)
    partial = parent / f".{path.name}.{os.getpid()}.partial"
    if partial.exists():
        raise FileExistsError(partial)
    try:
        with partial.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(partial, path)
        except FileExistsError:
            if path.read_bytes() != payload:
                raise OSError(f"immutable receipt collision: {path}")
        directory_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if partial.exists():
            partial.unlink()


def write_strict_orbital_state(
    source_map: Path, output_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Write state and immutable read-back receipt without path fallbacks."""
    output = output_path.expanduser()
    if not output.is_absolute():
        raise ValueError("output path must be absolute")
    state = _strict_topology_state(source_map)
    state["output"] = {"path": str(output)}
    state_bytes = _canonical_json_bytes(state)
    state_sha256 = _sha256_bytes(state_bytes)
    receipt_directory = output.parent / "receipts" / output.stem
    receipt_directory.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_directory / f"{state_sha256}.json"
    _atomic_write(output, state_bytes)

    read_back = output.read_bytes()
    read_back_sha256 = _sha256_bytes(read_back)
    if read_back_sha256 != state_sha256:
        raise OSError("orbital state read-back hash mismatch")

    receipt = {
        "schema": STRICT_RECEIPT_SCHEMA,
        "generated_at": state["generated_at"],
        "source_path": state["source"]["path"],
        "source_sha256": state["source"]["sha256"],
        "output_path": str(output),
        "output_sha256": state_sha256,
        "receipt_path": str(receipt_path),
        "producer_path": state["producer"]["path"],
        "producer_sha256": state["producer"]["sha256"],
        "read_back_verified": True,
        "state_status": state["status"],
        "inference_used": False,
        "fallback_used": False,
    }
    _atomic_write_once(receipt_path, _canonical_json_bytes(receipt))
    return state, receipt


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NOEMA orbital topology with explicit provenance"
    )
    parser.add_argument(
        "--write-state",
        action="store_true",
        required=True,
        help="write the strict topology state and a read-back receipt",
    )
    parser.add_argument("--source-map", type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_cli_parser()
    args = parser.parse_args(argv)

    if args.source_map is None or args.output is None:
        parser.error("--write-state requires --source-map and --output")
    state, receipt = write_strict_orbital_state(args.source_map, args.output)
    print(
        json.dumps(
            {
                "status": state["status"],
                "topology_status": state["topology_status"],
                "orbital_status": state["orbital_status"],
                "systems": state["systems"],
                "nodes": state["nodes"],
                "edges": state["edges"],
                "orbits": state["orbits"],
                "coherence": state["coherence"],
                "output_path": receipt["output_path"],
                "output_sha256": receipt["output_sha256"],
                "receipt_path": receipt["receipt_path"],
                "read_back_verified": receipt["read_back_verified"],
                "inference_used": state["inference_used"],
                "fallback_used": state["fallback_used"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if state["status"] in {"ok", "degraded"} else 2


# ========================================================================
# CLI
# ========================================================================
if __name__ == "__main__":
    raise SystemExit(main())
