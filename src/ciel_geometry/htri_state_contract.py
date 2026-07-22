"""Strict publication and verified-read contract for HTRI runtime state.

The runtime probe proves hardware/backend capability only.  It does not prove
that an HTRI computation is currently executing and it cannot supply HTRI
scientific metrics.  Those fields therefore remain explicitly unavailable in
probe-only publications.
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


STATE_SCHEMA = "noema.htri.runtime-state/v1"
RECEIPT_SCHEMA = "noema.htri.runtime-state-receipt/v1"
OBSERVATION_KIND = "runtime_probe"
_FORBIDDEN_PERSISTENT_PATH_FRAGMENTS = ("/tmp/", "New Volume1", "new_volume_rw")
_CANONICAL_VOLUME = Path("/media/adrian/New Volume").resolve()
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_CANONICAL_PRODUCER = (
    _PROJECT_ROOT / "scripts" / "publish_htri_runtime_state.py"
).resolve(strict=True)
_CANONICAL_PROBE_SOURCE = (
    _PROJECT_ROOT
    / "src"
    / "CIEL_OMEGA_COMPLETE_SYSTEM"
    / "ciel_omega"
    / "htri"
    / "gpu_driver.py"
).resolve(strict=True)
_CANONICAL_CONTRACT = Path(__file__).resolve(strict=True)


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("HTRI observation timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def _absolute_existing_file(path: Path, label: str) -> Path:
    expanded = path.expanduser()
    if not expanded.is_absolute():
        raise ValueError(f"{label} path must be absolute")
    resolved = expanded.resolve(strict=True)
    if _CANONICAL_VOLUME not in resolved.parents:
        raise ValueError(f"{label} path is outside the canonical New Volume")
    return resolved


def _validate_persistent_path(path: Path, label: str) -> Path:
    expanded = path.expanduser()
    if not expanded.is_absolute():
        raise ValueError(f"{label} path must be absolute")
    rendered = str(expanded)
    forbidden = [
        fragment
        for fragment in _FORBIDDEN_PERSISTENT_PATH_FRAGMENTS
        if fragment in rendered
    ]
    if forbidden:
        raise ValueError(
            f"{label} path contains forbidden legacy/transient fragment: "
            f"{', '.join(forbidden)}"
        )
    resolved = expanded.resolve()
    if _CANONICAL_VOLUME not in resolved.parents:
        raise ValueError(f"{label} path is outside the canonical New Volume")
    return resolved


def _optional_text(value: Any, label: str) -> str | None:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string or null")
    return value


def _normalize_runtime_probe(probe: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the direct GPU runtime observation without selecting a mode."""
    required_bools = (
        "runtime_available",
        "cupy_available",
        "nvidia_smi_available",
    )
    normalized: dict[str, Any] = {}
    for key in required_bools:
        value = probe.get(key)
        if not isinstance(value, bool):
            raise ValueError(f"HTRI runtime probe field {key!r} must be boolean")
        normalized[key] = value

    device_count = probe.get("device_count")
    if isinstance(device_count, bool) or not isinstance(device_count, int):
        raise ValueError("HTRI runtime probe device_count must be an integer")
    if device_count < 0:
        raise ValueError("HTRI runtime probe device_count cannot be negative")
    normalized["device_count"] = device_count

    raw_backend = probe.get("backend")
    observed_backend = probe.get("observed_backend")
    if (
        raw_backend is not None
        and observed_backend is not None
        and raw_backend != observed_backend
    ):
        raise ValueError("HTRI runtime probe observed backend fields contradict")
    backend = raw_backend if raw_backend is not None else observed_backend
    canonical_backend = probe.get("backend_capability")
    if (
        normalized["runtime_available"]
        and canonical_backend is not None
        and canonical_backend != "cupy_dense"
    ):
        raise ValueError("HTRI CUDA backend capability contradicts availability")
    if backend not in {"cupy_dense", "numpy_dense"}:
        raise ValueError("HTRI runtime probe backend is unsupported")
    normalized["observed_backend"] = backend
    normalized["device_name"] = _optional_text(
        probe.get("device_name"), "device_name"
    )
    normalized["nvidia_smi"] = _optional_text(
        probe.get("nvidia_smi"), "nvidia_smi"
    )

    reasons = probe.get("reason")
    if not isinstance(reasons, list) or not all(
        isinstance(reason, str) for reason in reasons
    ):
        raise ValueError("HTRI runtime probe reason must be a list of strings")
    normalized["reason"] = list(reasons)

    expected_runtime_available = bool(
        normalized["cupy_available"]
        and normalized["device_count"] > 0
        and backend == "cupy_dense"
    )
    if normalized["runtime_available"] != expected_runtime_available:
        raise ValueError(
            "HTRI runtime probe availability contradicts backend evidence"
        )
    expected_backend_capability = (
        "cupy_dense" if normalized["runtime_available"] else None
    )
    if (
        canonical_backend is not None
        and canonical_backend != expected_backend_capability
    ):
        raise ValueError("HTRI CUDA backend capability contradicts runtime evidence")
    normalized["backend_capability"] = expected_backend_capability
    if normalized["nvidia_smi_available"] != bool(normalized["nvidia_smi"]):
        raise ValueError(
            "HTRI runtime probe nvidia-smi availability contradicts its path"
        )
    if normalized["runtime_available"] and normalized["device_name"] is None:
        raise ValueError("available HTRI runtime probe has no device name")
    if not normalized["runtime_available"] and (
        not normalized["reason"] or normalized["reason"] == ["ok"]
    ):
        raise ValueError("unavailable HTRI runtime probe must include a reason")
    return normalized


def _unavailable_metrics() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "value": None,
            "unit": None,
            "definition": None,
            "status": "unavailable",
            "source_pointer": None,
        }
        for name in (
            "coherence",
            "soul_invariant",
            "spectral_radius",
            "potential",
            "oscillator_count",
            "optimal_thread_count",
        )
    }


def _probe_only_computation() -> dict[str, Any]:
    return {
        "status": "not_run",
        "active": None,
        "active_backend": None,
        "started_at": None,
        "completed_at": None,
        "source": None,
    }


def build_htri_runtime_probe_state(
    probe: Mapping[str, Any],
    *,
    output_path: Path,
    producer_path: Path,
    probe_source_path: Path,
    observed_at: str | None = None,
) -> dict[str, Any]:
    """Build a probe-only state; no computation metrics may enter this path."""
    output = _validate_persistent_path(output_path, "output")
    producer = _absolute_existing_file(producer_path, "producer")
    probe_source = _absolute_existing_file(probe_source_path, "probe source")
    if producer != _CANONICAL_PRODUCER:
        raise ValueError(f"producer must be the canonical publisher: {_CANONICAL_PRODUCER}")
    if probe_source != _CANONICAL_PROBE_SOURCE:
        raise ValueError(
            f"probe source must be the canonical HTRI GPU probe: "
            f"{_CANONICAL_PROBE_SOURCE}"
        )
    normalized_probe = _normalize_runtime_probe(probe)
    timestamp = observed_at or _utc_now()
    _parse_utc(timestamp)
    source_bytes = _canonical_json_bytes(normalized_probe)
    contract_path = _CANONICAL_CONTRACT

    runtime_status = (
        "available" if normalized_probe["runtime_available"] else "unavailable"
    )
    return {
        "schema": STATE_SCHEMA,
        "generated_at": timestamp,
        "status": "degraded",
        "observation": {
            "kind": OBSERVATION_KIND,
            "observed_at": timestamp,
            "freshness_policy_seconds": None,
            "freshness_status": "not_evaluated",
        },
        "runtime_capability": {
            "status": runtime_status,
            "cuda_runtime_available": normalized_probe["runtime_available"],
            "backend_capability": normalized_probe["backend_capability"],
            "device_count": normalized_probe["device_count"],
            "device_name": normalized_probe["device_name"],
            "cupy_available": normalized_probe["cupy_available"],
            "nvidia_smi_available": normalized_probe["nvidia_smi_available"],
            "nvidia_smi": normalized_probe["nvidia_smi"],
            "reason": normalized_probe["reason"],
        },
        "computation": _probe_only_computation(),
        "metrics": _unavailable_metrics(),
        "source": {
            "kind": OBSERVATION_KIND,
            "probe": normalized_probe,
            "sha256": _sha256_bytes(source_bytes),
        },
        "producer": {
            "path": str(producer),
            "sha256": _sha256_file(producer),
        },
        "probe_source": {
            "path": str(probe_source),
            "sha256": _sha256_file(probe_source),
        },
        "contract": {
            "path": str(contract_path),
            "sha256": _sha256_file(contract_path),
        },
        "python": {
            "executable": str(Path(sys.executable).resolve(strict=True)),
        },
        "output": {"path": str(output)},
        "inference_used": False,
        "fallback_used": False,
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
    """Publish immutable content once; collisions must be byte-identical."""
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
                raise OSError(f"immutable HTRI receipt collision: {path}")
        directory_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if partial.exists():
            partial.unlink()


def publish_htri_runtime_probe(
    probe: Mapping[str, Any],
    *,
    output_path: Path,
    producer_path: Path,
    probe_source_path: Path,
    observed_at: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Atomically publish a probe state and its content-addressed receipt."""
    state = build_htri_runtime_probe_state(
        probe,
        output_path=output_path,
        producer_path=producer_path,
        probe_source_path=probe_source_path,
        observed_at=observed_at,
    )
    output = Path(state["output"]["path"])
    state_bytes = _canonical_json_bytes(state)
    state_sha256 = _sha256_bytes(state_bytes)
    receipt_directory = output.parent / "receipts" / output.stem
    receipt_directory.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_directory / f"{state_sha256}.json"

    _atomic_write(output, state_bytes)
    read_back = output.read_bytes()
    if _sha256_bytes(read_back) != state_sha256:
        raise OSError("HTRI state read-back hash mismatch")

    receipt = {
        "schema": RECEIPT_SCHEMA,
        "generated_at": state["generated_at"],
        "observation_kind": OBSERVATION_KIND,
        "output_path": str(output),
        "output_sha256": state_sha256,
        "receipt_path": str(receipt_path),
        "source_sha256": state["source"]["sha256"],
        "producer_path": state["producer"]["path"],
        "producer_sha256": state["producer"]["sha256"],
        "probe_source_path": state["probe_source"]["path"],
        "probe_source_sha256": state["probe_source"]["sha256"],
        "contract_path": state["contract"]["path"],
        "contract_sha256": state["contract"]["sha256"],
        "runtime_capability_status": state["runtime_capability"]["status"],
        "computation_status": "not_run",
        "state_status": state["status"],
        "metrics_available": False,
        "read_back_verified": True,
        "inference_used": False,
        "fallback_used": False,
    }
    _atomic_write_once(receipt_path, _canonical_json_bytes(receipt))
    return state, receipt


def load_verified_htri_state(
    path: Path,
    *,
    max_age_seconds: float | None = None,
    now: datetime | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load state only after verifying its receipt and explicit freshness policy."""
    state_path = _validate_persistent_path(path, "state").resolve(strict=True)
    state_bytes = state_path.read_bytes()
    state_sha256 = _sha256_bytes(state_bytes)
    state = json.loads(state_bytes.decode("utf-8"))
    if not isinstance(state, dict) or state.get("schema") != STATE_SCHEMA:
        raise ValueError("unsupported or missing HTRI state schema")
    if state.get("inference_used") is not False:
        raise ValueError("HTRI state contains inferred values")
    if state.get("fallback_used") is not False:
        raise ValueError("HTRI state contains fallback values")
    if state.get("status") != "degraded":
        raise ValueError("probe-only HTRI state must be degraded")
    generated_at = state.get("generated_at")
    if not isinstance(generated_at, str):
        raise ValueError("HTRI state generated_at is missing")
    expected_observation = {
        "kind": OBSERVATION_KIND,
        "observed_at": generated_at,
        "freshness_policy_seconds": None,
        "freshness_status": "not_evaluated",
    }
    if state.get("observation") != expected_observation:
        raise ValueError("HTRI observation contract or timestamps do not match")
    if state.get("computation") != _probe_only_computation():
        raise ValueError("probe-only HTRI computation contract is not exact")

    normalized_probe = _normalize_runtime_probe(state.get("source", {}).get("probe", {}))
    expected_source_sha = _sha256_bytes(_canonical_json_bytes(normalized_probe))
    expected_source = {
        "kind": OBSERVATION_KIND,
        "probe": normalized_probe,
        "sha256": expected_source_sha,
    }
    if state.get("source") != expected_source:
        raise ValueError("HTRI state source provenance is not exact")
    expected_runtime_capability = {
        "status": (
            "available" if normalized_probe["runtime_available"] else "unavailable"
        ),
        "cuda_runtime_available": normalized_probe["runtime_available"],
        "backend_capability": normalized_probe["backend_capability"],
        "device_count": normalized_probe["device_count"],
        "device_name": normalized_probe["device_name"],
        "cupy_available": normalized_probe["cupy_available"],
        "nvidia_smi_available": normalized_probe["nvidia_smi_available"],
        "nvidia_smi": normalized_probe["nvidia_smi"],
        "reason": normalized_probe["reason"],
    }
    if state.get("runtime_capability") != expected_runtime_capability:
        raise ValueError("HTRI runtime capability contradicts source probe")
    if state.get("metrics") != _unavailable_metrics():
        raise ValueError("probe-only HTRI metrics registry is not exact")

    expected_producer = {
        "path": str(_CANONICAL_PRODUCER),
        "sha256": _sha256_file(_CANONICAL_PRODUCER),
    }
    if state.get("producer") != expected_producer:
        raise ValueError("HTRI producer provenance is not exact or current")
    expected_probe_source = {
        "path": str(_CANONICAL_PROBE_SOURCE),
        "sha256": _sha256_file(_CANONICAL_PROBE_SOURCE),
    }
    if state.get("probe_source") != expected_probe_source:
        raise ValueError("HTRI probe source provenance is not exact or current")
    expected_contract = {
        "path": str(_CANONICAL_CONTRACT),
        "sha256": _sha256_file(_CANONICAL_CONTRACT),
    }
    if state.get("contract") != expected_contract:
        raise ValueError("HTRI contract provenance is not exact or current")

    recorded_producer = _CANONICAL_PRODUCER
    recorded_probe_source = _CANONICAL_PROBE_SOURCE
    recorded_contract = _CANONICAL_CONTRACT
    current_contract = _CANONICAL_CONTRACT

    receipt_path = (
        state_path.parent / "receipts" / state_path.stem / f"{state_sha256}.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict) or receipt.get("schema") != RECEIPT_SCHEMA:
        raise ValueError("unsupported or missing HTRI receipt schema")
    checks = {
        "output_sha256": receipt.get("output_sha256") == state_sha256,
        "output_path": Path(str(receipt.get("output_path"))).resolve() == state_path,
        "state_output_path": Path(str(state.get("output", {}).get("path"))).resolve()
        == state_path,
        "receipt_path": Path(str(receipt.get("receipt_path"))).resolve()
        == receipt_path.resolve(),
        "source_sha256": receipt.get("source_sha256") == expected_source_sha,
        "producer_path": receipt.get("producer_path")
        == state.get("producer", {}).get("path"),
        "producer_sha256": receipt.get("producer_sha256")
        == state.get("producer", {}).get("sha256"),
        "producer_current_path": str(recorded_producer)
        == state.get("producer", {}).get("path"),
        "producer_current_sha256": _sha256_file(recorded_producer)
        == state.get("producer", {}).get("sha256"),
        "probe_source_path": receipt.get("probe_source_path")
        == state.get("probe_source", {}).get("path"),
        "probe_source_sha256": receipt.get("probe_source_sha256")
        == state.get("probe_source", {}).get("sha256"),
        "probe_source_current_path": str(recorded_probe_source)
        == state.get("probe_source", {}).get("path"),
        "probe_source_current_sha256": _sha256_file(recorded_probe_source)
        == state.get("probe_source", {}).get("sha256"),
        "contract_path": receipt.get("contract_path")
        == state.get("contract", {}).get("path"),
        "contract_sha256": receipt.get("contract_sha256")
        == state.get("contract", {}).get("sha256"),
        "contract_current_path": recorded_contract == current_contract,
        "contract_current_sha256": _sha256_file(recorded_contract)
        == state.get("contract", {}).get("sha256"),
        "generated_at": receipt.get("generated_at") == generated_at,
        "observation_kind": receipt.get("observation_kind")
        == state.get("observation", {}).get("kind"),
        "runtime_capability_status": receipt.get("runtime_capability_status")
        == state.get("runtime_capability", {}).get("status"),
        "computation_status": receipt.get("computation_status")
        == state.get("computation", {}).get("status"),
        "state_status": receipt.get("state_status") == state.get("status"),
        "read_back_verified": receipt.get("read_back_verified") is True,
        "metrics_available": receipt.get("metrics_available") is False,
        "inference_used": receipt.get("inference_used") is False,
        "fallback_used": receipt.get("fallback_used") is False,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError(f"HTRI receipt verification failed: {', '.join(failed)}")

    observed_at = _parse_utc(generated_at)
    reference_now_raw = now or datetime.now(timezone.utc)
    if reference_now_raw.tzinfo is None:
        raise ValueError("HTRI freshness reference time must include a timezone")
    reference_now = reference_now_raw.astimezone(timezone.utc)
    age_seconds = (reference_now - observed_at).total_seconds()
    if age_seconds < 0:
        raise ValueError("HTRI observation timestamp is in the future")
    if max_age_seconds is None:
        freshness_status = "not_evaluated"
        stale: bool | None = None
    else:
        if isinstance(max_age_seconds, bool) or not isinstance(
            max_age_seconds, (int, float)
        ):
            raise ValueError("HTRI max_age_seconds must be numeric")
        if not math.isfinite(float(max_age_seconds)) or max_age_seconds < 0:
            raise ValueError("HTRI max_age_seconds must be finite and non-negative")
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
    return state, publication


def summarize_verified_htri_state(
    path: Path,
    *,
    max_age_seconds: float | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Return a compact projection without converting unavailable data to zero."""
    state, publication = load_verified_htri_state(
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
    "OBSERVATION_KIND",
    "RECEIPT_SCHEMA",
    "STATE_SCHEMA",
    "build_htri_runtime_probe_state",
    "load_verified_htri_state",
    "publish_htri_runtime_probe",
    "summarize_verified_htri_state",
]
