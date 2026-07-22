"""Content-addressed publication contract for real HTRI computation.

The runtime probe and a scientific computation are different observations.  The
probe-only contract therefore remains strict and degraded.  This module accepts
only a report produced by ``LocalHTRI`` on the verified CUDA backend and keeps
the measured report inside the signed-by-hash state so consumers never need to
invent values or read an unverified side channel.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .htri_state_contract import (
    _CANONICAL_VOLUME,
    _atomic_write,
    _atomic_write_once,
    _canonical_json_bytes,
    _parse_utc,
    _sha256_bytes,
    _sha256_file,
    _validate_persistent_path,
)


COMPUTATION_SCHEMA = "noema.htri.computation-state/v1"
RECEIPT_SCHEMA = "noema.htri.computation-receipt/v1"
OBSERVATION_KIND = "htri_computation"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_CANONICAL_PUBLISHER = (
    _PROJECT_ROOT / "scripts" / "publish_htri_computation_state.py"
).resolve(strict=True)
_CANONICAL_LOCAL_SOURCE = (
    _PROJECT_ROOT
    / "src"
    / "CIEL_OMEGA_COMPLETE_SYSTEM"
    / "ciel_omega"
    / "htri"
    / "htri_local.py"
).resolve(strict=True)
_CANONICAL_GPU_SOURCE = (
    _PROJECT_ROOT
    / "src"
    / "CIEL_OMEGA_COMPLETE_SYSTEM"
    / "ciel_omega"
    / "htri"
    / "gpu_driver.py"
).resolve(strict=True)
_CANONICAL_CONTRACT = Path(__file__).resolve(strict=True)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"HTRI computation {label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"HTRI computation {label} must be finite")
    return result


def _ratio(value: Any, label: str) -> float:
    result = _finite_number(value, label)
    if result < 0.0 or result > 1.0:
        raise ValueError(f"HTRI computation {label} must be within [0, 1]")
    return result


def _count(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"HTRI computation {label} must be a positive integer")
    return value


def _normalize_report(report: Mapping[str, Any]) -> dict[str, Any]:
    """Keep the measured LocalHTRI report and reject CPU/numpy substitution."""
    if report.get("schema") != "ciel/htri-local/v2.0-dense":
        raise ValueError("unsupported HTRI computation report schema")
    hardware = report.get("hardware")
    combined = report.get("combined")
    if not isinstance(hardware, Mapping) or not isinstance(combined, Mapping):
        raise ValueError("HTRI computation report is missing hardware/combined")
    if hardware.get("cuda_active") is not True:
        raise ValueError("HTRI computation requires an active CUDA execution")
    if hardware.get("gpu_backend") != "cupy_dense":
        raise ValueError("HTRI computation backend is not verified cupy_dense")
    device = hardware.get("gpu_device_name")
    if not isinstance(device, str) or not device:
        raise ValueError("HTRI computation has no GPU device provenance")

    total = _count(combined.get("total_oscillators"), "total_oscillators")
    normalized_combined = {
        "coherence": _ratio(combined.get("coherence"), "coherence"),
        "potential": _finite_number(combined.get("potential"), "potential"),
        "soul_invariant": _ratio(
            combined.get("soul_invariant"), "soul_invariant"
        ),
        "spectral_radius": _finite_number(
            combined.get("spectral_radius"), "spectral_radius"
        ),
        "total_oscillators": total,
    }
    normalized_hardware = {
        "cuda_active": True,
        "gpu_backend": "cupy_dense",
        "gpu_device_name": device,
        "cpu": hardware.get("cpu"),
        "gpu": hardware.get("gpu"),
        "ram_total_gb": hardware.get("ram_total_gb"),
    }
    return {
        "schema": report["schema"],
        "hardware": normalized_hardware,
        "combined": normalized_combined,
        "elapsed_s": _finite_number(report.get("elapsed_s"), "elapsed_s"),
    }


def _metrics(report: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    combined = report["combined"]
    return {
        "coherence": {
            "value": combined["coherence"],
            "unit": "ratio",
            "definition": "weighted CPU/GPU HTRI order parameter from LocalHTRI.combined.coherence",
            "status": "observed",
            "source_pointer": "measurement.report.combined.coherence",
        },
        "soul_invariant": {
            "value": combined["soul_invariant"],
            "unit": "ratio",
            "definition": "weighted CPU/GPU phase invariant from LocalHTRI.combined.soul_invariant",
            "status": "observed",
            "source_pointer": "measurement.report.combined.soul_invariant",
        },
        "spectral_radius": {
            "value": combined["spectral_radius"],
            "unit": "phase-space units",
            "definition": "dense phase-network spectral radius from LocalHTRI.combined.spectral_radius",
            "status": "observed",
            "source_pointer": "measurement.report.combined.spectral_radius",
        },
        "potential": {
            "value": combined["potential"],
            "unit": "phase-potential units",
            "definition": "dense phase-network potential from LocalHTRI.combined.potential",
            "status": "observed",
            "source_pointer": "measurement.report.combined.potential",
        },
        "oscillator_count": {
            "value": combined["total_oscillators"],
            "unit": "count",
            "definition": "CPU plus GPU oscillators from LocalHTRI.combined.total_oscillators",
            "status": "observed",
            "source_pointer": "measurement.report.combined.total_oscillators",
        },
        "optimal_thread_count": {
            "value": None,
            "unit": None,
            "definition": None,
            "status": "unavailable",
            "source_pointer": None,
        },
    }


def build_htri_computation_state(
    report: Mapping[str, Any],
    *,
    output_path: Path,
    started_at: str,
    completed_at: str,
) -> dict[str, Any]:
    output = _validate_persistent_path(output_path, "output")
    started = _parse_utc(started_at)
    completed = _parse_utc(completed_at)
    if completed < started:
        raise ValueError("HTRI computation completed_at precedes started_at")
    normalized = _normalize_report(report)
    generated_at = completed_at
    measurement_bytes = _canonical_json_bytes(normalized)
    return {
        "schema": COMPUTATION_SCHEMA,
        "generated_at": generated_at,
        "status": "verified",
        "observation": {
            "kind": OBSERVATION_KIND,
            "observed_at": generated_at,
            "freshness_policy_seconds": 180,
            "freshness_status": "not_evaluated",
        },
        "runtime_capability": {
            "status": "available",
            "cuda_runtime_available": True,
            "backend_capability": "cupy_dense",
            "device_name": normalized["hardware"]["gpu_device_name"],
        },
        "computation": {
            "status": "completed",
            "active": False,
            "active_backend": "cupy_dense",
            "started_at": started_at,
            "completed_at": completed_at,
            "source": "measurement.report",
        },
        "metrics": _metrics(normalized),
        "measurement": {
            "report": normalized,
            "report_sha256": _sha256_bytes(measurement_bytes),
        },
        "producer": {
            "path": str(_CANONICAL_PUBLISHER),
            "sha256": _sha256_file(_CANONICAL_PUBLISHER),
        },
        "local_source": {
            "path": str(_CANONICAL_LOCAL_SOURCE),
            "sha256": _sha256_file(_CANONICAL_LOCAL_SOURCE),
        },
        "gpu_source": {
            "path": str(_CANONICAL_GPU_SOURCE),
            "sha256": _sha256_file(_CANONICAL_GPU_SOURCE),
        },
        "contract": {
            "path": str(_CANONICAL_CONTRACT),
            "sha256": _sha256_file(_CANONICAL_CONTRACT),
        },
        "python": {"executable": str(Path(sys.executable).resolve(strict=True))},
        "output": {"path": str(output)},
        "inference_used": False,
        "fallback_used": False,
    }


def publish_htri_computation(
    report: Mapping[str, Any],
    *,
    output_path: Path,
    started_at: str,
    completed_at: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    state = build_htri_computation_state(
        report,
        output_path=output_path,
        started_at=started_at,
        completed_at=completed_at,
    )
    output = Path(state["output"]["path"])
    state_bytes = _canonical_json_bytes(state)
    state_sha256 = _sha256_bytes(state_bytes)
    receipt_directory = output.parent / "receipts" / output.stem
    receipt_directory.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_directory / f"{state_sha256}.json"
    _atomic_write(output, state_bytes)
    if _sha256_bytes(output.read_bytes()) != state_sha256:
        raise OSError("HTRI computation read-back hash mismatch")
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "generated_at": state["generated_at"],
        "observation_kind": OBSERVATION_KIND,
        "output_path": str(output),
        "output_sha256": state_sha256,
        "receipt_path": str(receipt_path),
        "report_sha256": state["measurement"]["report_sha256"],
        "producer_path": state["producer"]["path"],
        "producer_sha256": state["producer"]["sha256"],
        "local_source_path": state["local_source"]["path"],
        "local_source_sha256": state["local_source"]["sha256"],
        "gpu_source_path": state["gpu_source"]["path"],
        "gpu_source_sha256": state["gpu_source"]["sha256"],
        "contract_path": state["contract"]["path"],
        "contract_sha256": state["contract"]["sha256"],
        "runtime_capability_status": "available",
        "computation_status": "completed",
        "state_status": "verified",
        "metrics_available": True,
        "read_back_verified": True,
        "inference_used": False,
        "fallback_used": False,
    }
    _atomic_write_once(receipt_path, _canonical_json_bytes(receipt))
    return state, receipt


def load_verified_htri_computation(
    path: Path,
    *,
    max_age_seconds: float | None = 180,
    now: datetime | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    state_path = _validate_persistent_path(path, "state").resolve(strict=True)
    state_bytes = state_path.read_bytes()
    state_sha256 = _sha256_bytes(state_bytes)
    state = json.loads(state_bytes.decode("utf-8"))
    if not isinstance(state, dict) or state.get("schema") != COMPUTATION_SCHEMA:
        raise ValueError("unsupported or missing HTRI computation state schema")
    if state.get("status") != "verified":
        raise ValueError("HTRI computation state is not verified")
    if state.get("inference_used") is not False or state.get("fallback_used") is not False:
        raise ValueError("HTRI computation state contains inferred or fallback values")
    measurement = state.get("measurement")
    if not isinstance(measurement, Mapping) or not isinstance(measurement.get("report"), Mapping):
        raise ValueError("HTRI computation measurement is missing")
    normalized = _normalize_report(measurement["report"])
    if measurement.get("report_sha256") != _sha256_bytes(_canonical_json_bytes(normalized)):
        raise ValueError("HTRI computation report hash mismatch")
    if state.get("metrics") != _metrics(normalized):
        raise ValueError("HTRI computation metrics do not match the report")
    generated_at = state.get("generated_at")
    if not isinstance(generated_at, str) or state.get("observation") != {
        "kind": OBSERVATION_KIND,
        "observed_at": generated_at,
        "freshness_policy_seconds": 180,
        "freshness_status": "not_evaluated",
    }:
        raise ValueError("HTRI computation observation contract is not exact")
    expected_sources = {
        "producer": (_CANONICAL_PUBLISHER, state.get("producer")),
        "local_source": (_CANONICAL_LOCAL_SOURCE, state.get("local_source")),
        "gpu_source": (_CANONICAL_GPU_SOURCE, state.get("gpu_source")),
        "contract": (_CANONICAL_CONTRACT, state.get("contract")),
    }
    for label, (current_path, recorded) in expected_sources.items():
        if not isinstance(recorded, Mapping) or recorded.get("path") != str(current_path):
            raise ValueError(f"HTRI computation {label} provenance path is not canonical")
        if recorded.get("sha256") != _sha256_file(current_path):
            raise ValueError(f"HTRI computation {label} provenance hash is stale")
    receipt_path = state_path.parent / "receipts" / state_path.stem / f"{state_sha256}.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict) or receipt.get("schema") != RECEIPT_SCHEMA:
        raise ValueError("unsupported or missing HTRI computation receipt schema")
    checks = {
        "output_sha256": receipt.get("output_sha256") == state_sha256,
        "output_path": Path(str(receipt.get("output_path"))).resolve() == state_path,
        "state_output_path": Path(str(state.get("output", {}).get("path"))).resolve() == state_path,
        "receipt_path": Path(str(receipt.get("receipt_path"))).resolve() == receipt_path.resolve(),
        "report_sha256": receipt.get("report_sha256") == measurement["report_sha256"],
        "metrics_available": receipt.get("metrics_available") is True,
        "read_back_verified": receipt.get("read_back_verified") is True,
        "inference_used": receipt.get("inference_used") is False,
        "fallback_used": receipt.get("fallback_used") is False,
        "state_status": receipt.get("state_status") == "verified",
        "computation_status": receipt.get("computation_status") == "completed",
        "generated_at": receipt.get("generated_at") == generated_at,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError(f"HTRI computation receipt verification failed: {', '.join(failed)}")
    observed_at = _parse_utc(generated_at)
    reference_now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    age_seconds = (reference_now - observed_at).total_seconds()
    if age_seconds < 0:
        raise ValueError("HTRI computation timestamp is in the future")
    if max_age_seconds is None:
        freshness_status, stale = "not_evaluated", None
    else:
        if isinstance(max_age_seconds, bool) or not isinstance(max_age_seconds, (int, float)) or not math.isfinite(float(max_age_seconds)) or max_age_seconds < 0:
            raise ValueError("HTRI computation max_age_seconds must be finite and non-negative")
        stale = age_seconds > float(max_age_seconds)
        freshness_status = "stale" if stale else "current"
    publication = {
        "status": "verified",
        "state_path": str(state_path),
        "state_sha256": state_sha256,
        "receipt_path": str(receipt_path),
        "receipt_checks": checks,
        "age_seconds": age_seconds,
        "freshness_policy_seconds": max_age_seconds,
        "freshness_status": freshness_status,
        "stale": stale,
    }
    if stale:
        raise ValueError("HTRI computation publication is stale")
    return state, publication


def summarize_verified_htri_computation(
    path: Path, *, max_age_seconds: float | None = 180, now: datetime | None = None
) -> dict[str, Any]:
    state, publication = load_verified_htri_computation(
        path, max_age_seconds=max_age_seconds, now=now
    )
    return {
        "schema": state["schema"],
        "status": state["status"],
        "runtime_capability": state["runtime_capability"],
        "computation": state["computation"],
        "metrics": state["metrics"],
        "observation": state["observation"],
        "inference_used": False,
        "fallback_used": False,
        "publication": publication,
    }


__all__ = [
    "COMPUTATION_SCHEMA",
    "RECEIPT_SCHEMA",
    "OBSERVATION_KIND",
    "build_htri_computation_state",
    "load_verified_htri_computation",
    "publish_htri_computation",
    "summarize_verified_htri_computation",
]
