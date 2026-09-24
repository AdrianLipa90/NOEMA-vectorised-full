from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .baseline import build_baseline, compare_to_baseline
from .memory import ImmuneMemory, utc_now_iso
from .phasenav import PHASENAV_24D_COMPONENTS, vector_with_labels

SCHEMA_STATUS = "NOEMA_VECTORISED_STATUS_V0_1"
SCHEMA_STATE = "NOEMA_SOT_STATE_V0_1"
SCHEMA_CANDIDATE = "NOEMA_APPEND_ONLY_UPDATE_CANDIDATE_V0_1"
SCHEMA_RECEIPT = "NOEMA_UPDATE_RECEIPT_V0_1"


def stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stable_sha256(payload: Any) -> str:
    return hashlib.sha256(stable_json(payload).encode("utf-8")).hexdigest()


def _safe_git_commit(repo_root: str | Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            cwd=str(repo_root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=2,
        )
        value = result.stdout.strip()
        return value if result.returncode == 0 and value else None
    except Exception:
        return None


def _safe_git_dirty(repo_root: str | Path) -> bool | None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=2,
        )
        if result.returncode != 0:
            return None
        return bool(result.stdout.strip())
    except Exception:
        return None


def _bool_to_float(value: bool | None) -> float:
    if value is True:
        return 1.0
    if value is False:
        return 0.0
    return 0.5


def _unit_from_digest(hex_digest: str, start: int = 0, length: int = 8) -> float:
    if not hex_digest:
        return 0.0
    part = hex_digest[start : start + length]
    if not part:
        return 0.0
    return int(part, 16) / float(16**len(part) - 1)


def _angle_pair(hex_digest: str, start: int = 0) -> tuple[float, float]:
    angle = 2.0 * math.pi * _unit_from_digest(hex_digest, start=start, length=12)
    return (math.sin(angle) + 1.0) / 2.0, (math.cos(angle) + 1.0) / 2.0


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _normalise_count(value: int, cap: int = 10_000) -> float:
    return _clamp01(math.log2(max(1, value)) / math.log2(cap))


def _vector_from_status_inputs(inputs: dict[str, Any]) -> list[float]:
    tree_digest = inputs.get("tree_digest") or "0" * 64
    status_digest = inputs.get("status_digest_seed") or tree_digest
    tree_sin, tree_cos = _angle_pair(tree_digest, 0)
    status_sin, status_cos = _angle_pair(status_digest, 12)
    total_files = int(inputs.get("total_files") or 0)
    total_bytes = int(inputs.get("total_bytes") or 0)
    profiles = int(inputs.get("profiles") or 0)
    changes = int(inputs.get("changes") or 0)
    gate = inputs.get("release_gate", "UNKNOWN")
    tests = inputs.get("tests", "unknown")
    repo_dirty = inputs.get("repo_dirty")
    has_current = bool(inputs.get("current_state_id"))
    candidate_count = int(inputs.get("candidate_count") or 0)
    receipt_count = int(inputs.get("receipt_count") or 0)

    gate_score = {"PASS": 1.0, "REVIEW": 0.55, "FAIL": 0.0, "UNKNOWN": 0.25}.get(str(gate).upper(), 0.25)
    tests_score = {"pass": 1.0, "fail": 0.0, "unknown": 0.5}.get(str(tests).lower(), 0.5)
    dirty_score = 1.0 - _bool_to_float(repo_dirty) if repo_dirty is not None else 0.5
    change_norm = _normalise_count(changes, cap=2048)
    stability = _clamp01((gate_score + tests_score + dirty_score + (1.0 - change_norm)) / 4.0)
    tension = 1.0 - stability

    vector = [
        _normalise_count(total_files),
        tree_sin,
        tree_cos,
        status_sin,
        status_cos,
        stability,
        tension,
        _normalise_count(profiles, cap=4096),
        _normalise_count(candidate_count, cap=4096),
        _normalise_count(receipt_count, cap=4096),
        1.0 - gate_score,
        1.0 - tests_score,
        1.0 - dirty_score,
        tension,
        _normalise_count(total_bytes, cap=2**32),
        stability,
        tension,
        _normalise_count(total_files * max(1, profiles), cap=1_000_000),
        _unit_from_digest(tree_digest, 24, 8),
        _unit_from_digest(tree_digest, 32, 8),
        _unit_from_digest(status_digest, 40, 8),
        0.75,  # NOEMA/SoT operator lane
        1.0 if has_current else 0.0,
        stability,
    ]
    return [_clamp01(x) for x in vector]


@dataclass(frozen=True)
class CurrentState:
    state_id: str | None
    payload: dict[str, Any] | None
    current_loaded: bool


@dataclass(frozen=True)
class VectorisedStatus:
    payload: dict[str, Any]

    @property
    def digest(self) -> str:
        return str(self.payload["vector_surface"]["digest"])

    @property
    def vector(self) -> list[float]:
        return list(self.payload["vector_surface"]["values"])


class FileSoTClient:
    """Local append-only NOEMA SoT simulator.

    This is deliberately conservative: it can stage candidates, verify receipts,
    and promote CURRENT only through an explicit accept operation. It does not
    claim to be the external NOEMA SoT.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.snaps = self.root / "snaps"
        self.staged = self.root / "staged"
        self.receipts = self.root / "receipts"
        self.current_pointer = self.root / "CURRENT"

    def init(self) -> dict[str, Any]:
        self.snaps.mkdir(parents=True, exist_ok=True)
        self.staged.mkdir(parents=True, exist_ok=True)
        self.receipts.mkdir(parents=True, exist_ok=True)
        if not self.current_pointer.exists():
            self.current_pointer.write_text("", encoding="utf-8")
        return {
            "schema": "NOEMA_FILE_SOT_INIT_V0_1",
            "root": str(self.root),
            "mode": "local_file_sot_simulator",
            "append_only": True,
            "current_pointer": str(self.current_pointer),
        }

    def pull_current(self) -> CurrentState:
        if not self.current_pointer.exists():
            return CurrentState(None, None, False)
        state_id = self.current_pointer.read_text(encoding="utf-8").strip() or None
        if not state_id:
            return CurrentState(None, None, False)
        state_path = self.snaps / f"{state_id}.json"
        if not state_path.exists():
            return CurrentState(state_id, None, False)
        return CurrentState(state_id, json.loads(state_path.read_text(encoding="utf-8")), True)

    def counts(self) -> dict[str, int]:
        self.init()
        return {
            "snaps": len(list(self.snaps.glob("*.json"))),
            "staged": len(list(self.staged.glob("*.json"))),
            "receipts": len(list(self.receipts.glob("*.json"))),
        }

    def stage_update(self, status: VectorisedStatus, message: str = "", promote_current_requested: bool = False) -> dict[str, Any]:
        self.init()
        current = self.pull_current()
        payload = {
            "schema": SCHEMA_CANDIDATE,
            "created_utc": utc_now_iso(),
            "namespace": status.payload.get("namespace", "PN-BIS"),
            "previous_current_state_id": current.state_id,
            "message": message,
            "status_digest": status.digest,
            "status": status.payload,
            "writeback": {
                "append_only": True,
                "promote_current_requested": bool(promote_current_requested),
                "canon_allowed": False,
                "external_noema_sot_claimed": False,
                "mode": "local_file_sot_candidate",
            },
        }
        candidate_id = stable_sha256(payload)
        payload["candidate_id"] = candidate_id
        path = self.staged / f"{candidate_id}.json"
        if path.exists():
            raise FileExistsError(f"candidate already staged: {candidate_id}")
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return payload

    def read_candidate(self, candidate_id: str) -> dict[str, Any]:
        path = self.staged / f"{candidate_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"candidate does not exist: {candidate_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def accept_candidate(self, candidate_id: str, promote_current: bool = False, accepted_by: str = "local-operator") -> dict[str, Any]:
        self.init()
        candidate = self.read_candidate(candidate_id)
        state_payload = {
            "schema": SCHEMA_STATE,
            "created_utc": utc_now_iso(),
            "namespace": candidate.get("namespace", "PN-BIS"),
            "source_candidate_id": candidate_id,
            "previous_current_state_id": self.pull_current().state_id,
            "status_digest": candidate.get("status_digest"),
            "status": candidate.get("status"),
            "append_only": True,
            "canon_allowed": bool(promote_current),
        }
        state_id = stable_sha256(state_payload)
        state_payload["state_id"] = state_id
        snap_path = self.snaps / f"{state_id}.json"
        if snap_path.exists():
            raise FileExistsError(f"state already exists: {state_id}")
        snap_path.write_text(json.dumps(state_payload, indent=2, sort_keys=True), encoding="utf-8")
        if promote_current:
            self.current_pointer.write_text(state_id, encoding="utf-8")
        receipt = {
            "schema": SCHEMA_RECEIPT,
            "created_utc": utc_now_iso(),
            "candidate_id": candidate_id,
            "accepted": True,
            "accepted_by": accepted_by,
            "new_state_id": state_id,
            "current_pointer_updated": bool(promote_current),
            "append_only": True,
            "receipt_hash": None,
        }
        receipt["receipt_hash"] = stable_sha256({k: v for k, v in receipt.items() if k != "receipt_hash"})
        (self.receipts / f"{candidate_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True), encoding="utf-8")
        return receipt

    def verify_receipt(self, candidate_id: str) -> dict[str, Any]:
        receipt_path = self.receipts / f"{candidate_id}.json"
        if not receipt_path.exists():
            return {"ok": False, "candidate_id": candidate_id, "errors": ["receipt does not exist"]}
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        expected = stable_sha256({k: v for k, v in receipt.items() if k != "receipt_hash"})
        errors: list[str] = []
        if receipt.get("receipt_hash") != expected:
            errors.append("receipt_hash mismatch")
        state_id = receipt.get("new_state_id")
        if not state_id or not (self.snaps / f"{state_id}.json").exists():
            errors.append("accepted state snap missing")
        current = self.pull_current()
        if receipt.get("current_pointer_updated") and current.state_id != state_id:
            errors.append("CURRENT pointer does not match receipt new_state_id")
        return {"ok": not errors, "candidate_id": candidate_id, "receipt": receipt, "current_state_id": current.state_id, "errors": errors}


def build_vectorised_status(
    repo_root: str | Path,
    sot: FileSoTClient | None = None,
    baseline_path: str | Path | None = None,
    memory_path: str | Path | None = None,
    tests: str = "unknown",
    release_gate: str | None = None,
    excludes: list[str] | None = None,
    max_files: int = 10000,
) -> VectorisedStatus:
    repo = Path(repo_root).resolve()
    current = sot.pull_current() if sot else CurrentState(None, None, False)
    counts = sot.counts() if sot else {"snaps": 0, "staged": 0, "receipts": 0}
    baseline = build_baseline(repo, recursive=True, max_files=max_files, excludes=excludes)
    diff_payload: dict[str, Any] | None = None
    gate = release_gate or "UNKNOWN"
    change_count = 0
    if baseline_path:
        diff_payload = compare_to_baseline(baseline_path, repo, max_files=max_files, excludes=excludes)
        gate = str(diff_payload.get("overall", gate))
        change_count = len(diff_payload.get("changes", []))
    total_bytes = sum(entry.size_bytes for entry in baseline.entries)
    profile_count = 0
    if memory_path and Path(memory_path).exists():
        profile_count = len(ImmuneMemory(memory_path).profiles)
    repo_dirty = _safe_git_dirty(repo)
    source_commit = _safe_git_commit(repo)
    status_digest_seed = stable_sha256(
        {
            "tree_digest": baseline.tree_digest,
            "current_state_id": current.state_id,
            "source_commit": source_commit,
            "tests": tests,
            "release_gate": gate,
            "changes": change_count,
        }
    )
    vector_inputs = {
        "tree_digest": baseline.tree_digest,
        "status_digest_seed": status_digest_seed,
        "total_files": len(baseline.entries),
        "total_bytes": total_bytes,
        "profiles": profile_count,
        "changes": change_count,
        "release_gate": gate,
        "tests": tests,
        "repo_dirty": repo_dirty,
        "current_state_id": current.state_id,
        "candidate_count": counts.get("staged", 0),
        "receipt_count": counts.get("receipts", 0),
    }
    vector = _vector_from_status_inputs(vector_inputs)
    vector_digest = stable_sha256({"schema": SCHEMA_STATUS, "values": [round(x, 12) for x in vector], "seed": status_digest_seed})
    payload = {
        "schema": SCHEMA_STATUS,
        "namespace": "PN-BIS",
        "created_utc": utc_now_iso(),
        "sot": {
            "sot_available": sot is not None,
            "mode": "local_file_sot_simulator" if sot else "none",
            "current_state_loaded": current.current_loaded,
            "current_state_id": current.state_id,
            "canon_allowed": False,
        },
        "source_commit": source_commit,
        "repo": {
            "root": str(repo),
            "dirty": repo_dirty,
            "state": "dirty" if repo_dirty else ("clean" if repo_dirty is False else "unknown"),
        },
        "artifact_manifest_sha256": baseline.tree_digest,
        "baseline": {
            "schema": baseline.schema,
            "entries": len(baseline.entries),
            "tree_digest": baseline.tree_digest,
            "total_bytes": total_bytes,
        },
        "comparison": diff_payload,
        "status": {
            "repo": "dirty" if repo_dirty else ("clean" if repo_dirty is False else "unknown"),
            "tests": tests,
            "release_gate": gate,
            "immune_decision": "ALLOW" if gate == "PASS" else ("REVIEW" if gate in {"REVIEW", "UNKNOWN"} else "QUARANTINE"),
        },
        "vector_surface": {
            "dim": 24,
            "encoding": "phase_vector_float64",
            "operator": "pn_bis_noema_status_vectorize_v0_4",
            "components": PHASENAV_24D_COMPONENTS,
            "values": vector,
            "labeled": vector_with_labels(vector),
            "digest": vector_digest,
        },
        "writeback": {
            "append_only": True,
            "promote_current_requested": False,
            "canon_allowed": False,
        },
    }
    return VectorisedStatus(payload)


def write_json(payload: dict[str, Any], output: str | Path) -> None:
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
