from __future__ import annotations

import fnmatch
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .compare import compare_artifacts
from .immune import analyse_artifact
from .memory import ImmuneMemory, utc_now_iso
from .phasenav import normalised_distance
from .policy import ImmunePolicy
from .schema import FeatureSummary, PhaseVectorRecord
from .structure import structure_summary

DEFAULT_EXCLUDES = [
    ".git/**",
    "**/__pycache__/**",
    "**/.pytest_cache/**",
    "**/*.pyc",
    "**/.DS_Store",
]


@dataclass(frozen=True)
class BaselineEntry:
    relative_path: str
    size_bytes: int
    sha256: str
    base64_sha256: str
    structure_kind: str
    phase_vector_digest: str
    phase_vector: list[float]
    feature_summary: dict[str, float]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BaselineSnapshot:
    schema: str
    created_at_utc: str
    root: str
    safety_boundary: str
    excludes: list[str]
    entries: list[BaselineEntry]
    tree_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["entries"] = [entry.to_dict() for entry in self.entries]
        return payload


def _stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _matches_exclude(relative: str, patterns: list[str]) -> bool:
    rel = relative.replace("\\", "/")
    return any(fnmatch.fnmatch(rel, pattern) for pattern in patterns)


def iter_artifacts(root: str | Path, recursive: bool = True, max_files: int = 10000, excludes: list[str] | None = None) -> Iterable[Path]:
    root_path = Path(root).resolve()
    patterns = list(DEFAULT_EXCLUDES)
    if excludes:
        patterns.extend(excludes)
    iterator = root_path.rglob("*") if recursive else root_path.iterdir()
    count = 0
    for item in sorted(iterator, key=lambda p: str(p)):
        if not item.is_file():
            continue
        relative = item.relative_to(root_path).as_posix()
        if _matches_exclude(relative, patterns):
            continue
        count += 1
        if count > max_files:
            raise ValueError(f"max_files cap exceeded: {max_files}")
        yield item


def _feature_summary(features: FeatureSummary) -> dict[str, float]:
    return {
        "byte_entropy_norm": features.byte_entropy_norm,
        "base64_entropy_norm": features.base64_entropy_norm,
        "chunk_entropy_mean": features.chunk_entropy_mean,
        "chunk_entropy_std": features.chunk_entropy_std,
        "chunk_entropy_max_delta": features.chunk_entropy_max_delta,
        "byte_zero_ratio": features.byte_zero_ratio,
        "byte_printable_ratio": features.byte_printable_ratio,
        "byte_high_ratio": features.byte_high_ratio,
    }


def entry_for_path(root: str | Path, path: str | Path) -> BaselineEntry:
    root_path = Path(root).resolve()
    p = Path(path).resolve()
    artifact, features, phase_vector = analyse_artifact(str(p))
    data = p.read_bytes()
    structure = structure_summary(data, p)
    return BaselineEntry(
        relative_path=p.relative_to(root_path).as_posix(),
        size_bytes=artifact.size_bytes,
        sha256=artifact.sha256,
        base64_sha256=artifact.base64_sha256,
        structure_kind=structure.kind,
        phase_vector_digest=phase_vector.digest,
        phase_vector=phase_vector.vector,
        feature_summary=_feature_summary(features),
        notes=structure.structural_notes,
    )


def tree_digest(entries: list[BaselineEntry]) -> str:
    digest_payload = [
        {
            "relative_path": entry.relative_path,
            "sha256": entry.sha256,
            "phase_vector_digest": entry.phase_vector_digest,
            "structure_kind": entry.structure_kind,
        }
        for entry in sorted(entries, key=lambda e: e.relative_path)
    ]
    return hashlib.sha256(_stable_json(digest_payload).encode("utf-8")).hexdigest()


def build_baseline(
    root: str | Path,
    recursive: bool = True,
    max_files: int = 10000,
    excludes: list[str] | None = None,
) -> BaselineSnapshot:
    root_path = Path(root).resolve()
    exclude_patterns = list(DEFAULT_EXCLUDES)
    if excludes:
        exclude_patterns.extend(excludes)
    entries = [entry_for_path(root_path, p) for p in iter_artifacts(root_path, recursive, max_files, excludes)]
    digest = tree_digest(entries)
    return BaselineSnapshot(
        schema="pn-bis-baseline-v0.3",
        created_at_utc=utc_now_iso(),
        root=str(root_path),
        safety_boundary="static-analysis-only; baseline captures trust state without executing artefacts",
        excludes=exclude_patterns,
        entries=entries,
        tree_digest=digest,
    )


def write_baseline(snapshot: BaselineSnapshot, output: str | Path) -> None:
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def load_baseline(path: str | Path) -> BaselineSnapshot:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = [BaselineEntry(**item) for item in raw.get("entries", [])]
    return BaselineSnapshot(
        schema=raw.get("schema", "pn-bis-baseline-unknown"),
        created_at_utc=raw.get("created_at_utc", ""),
        root=raw.get("root", ""),
        safety_boundary=raw.get("safety_boundary", ""),
        excludes=list(raw.get("excludes", DEFAULT_EXCLUDES)),
        entries=entries,
        tree_digest=raw.get("tree_digest", tree_digest(entries)),
    )


def enroll_baseline(snapshot: BaselineSnapshot, memory_path: str | Path, label_prefix: str = "baseline") -> dict[str, Any]:
    memory = ImmuneMemory(memory_path)
    enrolled = 0
    for entry in snapshot.entries:
        # Store a compact profile from the baseline without re-reading files. This is useful
        # when the baseline is the authoritative known-good release artifact.
        profile = {
            "label": f"{label_prefix}:{entry.relative_path}",
            "artifact": {
                "path": entry.relative_path,
                "size_bytes": entry.size_bytes,
                "sha256": entry.sha256,
                "base64_sha256": entry.base64_sha256,
                "base64_length": None,
                "sample_base64_prefix": "",
                "structure_kind": entry.structure_kind,
            },
            "phase_vector": {
                "vector": entry.phase_vector,
                "digest": entry.phase_vector_digest,
                "semantic_type": "binary_artifact",
                "source": "pn-bis-baseline-v0.3",
                "operator": "pn_bis_baseline_enroll_v0_3",
                "route": {},
                "metric_state": {},
                "projection": "baseline-self-profile",
                "confidence": 1.0,
                "canon_status": "baseline",
            },
            "features": entry.feature_summary,
            "enrolled_at_utc": utc_now_iso(),
            "notes": "enrolled from baseline snapshot",
        }
        # Avoid duplicate SHA profiles from repeated baseline enrollment.
        if memory.by_sha256(entry.sha256) is None:
            from .schema import ImmuneProfile

            memory.profiles.append(ImmuneProfile(**profile))
            enrolled += 1
    memory.save()
    return {"schema": "pn-bis-baseline-enroll-v0.3", "memory": str(memory_path), "enrolled": enrolled, "total_profiles": len(memory.profiles)}


def compare_to_baseline(
    baseline_path: str | Path,
    root: str | Path,
    policy: ImmunePolicy | None = None,
    recursive: bool = True,
    max_files: int = 10000,
    excludes: list[str] | None = None,
) -> dict[str, Any]:
    policy = policy or ImmunePolicy()
    baseline = load_baseline(baseline_path)
    root_path = Path(root).resolve()
    baseline_by_path = {entry.relative_path: entry for entry in baseline.entries}
    current_entries = {entry.relative_path: entry for entry in build_baseline(root_path, recursive, max_files, excludes).entries}

    changes: list[dict[str, Any]] = []
    counts = {"unchanged": 0, "low_drift": 0, "warn_drift": 0, "review_drift": 0, "quarantine_drift": 0, "added": 0, "missing": 0}

    for rel, base in sorted(baseline_by_path.items()):
        cur = current_entries.get(rel)
        if cur is None:
            counts["missing"] += 1
            changes.append({"relative_path": rel, "status": "MISSING", "action": "REVIEW", "reason": "baseline artefact is absent"})
            continue
        if cur.sha256 == base.sha256:
            counts["unchanged"] += 1
            continue
        distance = normalised_distance(base.phase_vector, cur.phase_vector)
        if distance <= policy.allow_distance:
            status = "LOW_DRIFT"
            action = "ALLOW"
            counts["low_drift"] += 1
        elif distance <= policy.warn_distance:
            status = "WARN_DRIFT"
            action = "WARN"
            counts["warn_drift"] += 1
        elif distance <= policy.review_distance:
            status = "REVIEW_DRIFT"
            action = "REVIEW"
            counts["review_drift"] += 1
        else:
            status = "QUARANTINE_DRIFT"
            action = "QUARANTINE"
            counts["quarantine_drift"] += 1
        changes.append(
            {
                "relative_path": rel,
                "status": status,
                "action": action,
                "phase_vector_distance": distance,
                "baseline_sha256": base.sha256,
                "current_sha256": cur.sha256,
                "baseline_vector_digest": base.phase_vector_digest,
                "current_vector_digest": cur.phase_vector_digest,
                "structure_kind_changed": base.structure_kind != cur.structure_kind,
                "baseline_structure_kind": base.structure_kind,
                "current_structure_kind": cur.structure_kind,
            }
        )

    for rel, cur in sorted(current_entries.items()):
        if rel not in baseline_by_path:
            counts["added"] += 1
            changes.append(
                {
                    "relative_path": rel,
                    "status": "ADDED",
                    "action": "REVIEW",
                    "reason": "new artefact is not present in baseline",
                    "current_sha256": cur.sha256,
                    "current_vector_digest": cur.phase_vector_digest,
                    "current_structure_kind": cur.structure_kind,
                }
            )

    changed_digest_payload = {"baseline_tree_digest": baseline.tree_digest, "changes": changes}
    change_digest = hashlib.sha256(_stable_json(changed_digest_payload).encode("utf-8")).hexdigest()
    high_risk = counts["quarantine_drift"] + counts["missing"]
    overall = "PASS" if not changes else ("FAIL" if high_risk else "REVIEW")
    return {
        "schema": "pn-bis-baseline-diff-v0.3",
        "created_at_utc": utc_now_iso(),
        "baseline_path": str(baseline_path),
        "root": str(root_path),
        "baseline_tree_digest": baseline.tree_digest,
        "change_digest": change_digest,
        "overall": overall,
        "counts": counts,
        "changes": changes,
        "safety_boundary": "static-analysis-only; no execution, unpacking, detonation, or exploit activity",
    }
