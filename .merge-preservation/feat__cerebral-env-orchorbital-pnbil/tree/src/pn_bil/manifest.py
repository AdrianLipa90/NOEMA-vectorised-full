from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .immune import analyse_artifact
from .memory import utc_now_iso
from .phasenav import vector_with_labels
from .structure import structure_summary


def build_manifest(path: str | Path) -> dict[str, Any]:
    artifact, features, phase_vector = analyse_artifact(str(path))
    data = Path(path).read_bytes()
    structure = structure_summary(data, path)
    return {
        "schema": "pn-bis-artifact-manifest-v0.2",
        "created_at_utc": utc_now_iso(),
        "safety_boundary": "static-analysis-only; no execution, unpacking, detonation, or exploit activity",
        "artifact": artifact.to_dict(),
        "structure": structure.to_dict(),
        "features": features.to_dict(),
        "phase_vector": phase_vector.to_dict(),
        "vector_labeled": vector_with_labels(phase_vector.vector),
    }


def write_manifest(path: str | Path, output: str | Path) -> dict[str, Any]:
    payload = build_manifest(path)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload
