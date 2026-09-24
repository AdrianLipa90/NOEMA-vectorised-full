from __future__ import annotations

from pathlib import Path
from typing import Any

from .immune import analyse_artifact
from .phasenav import normalised_distance, vector_with_labels
from .structure import structure_summary


def compare_artifacts(left: str | Path, right: str | Path) -> dict[str, Any]:
    la, lf, lv = analyse_artifact(str(left))
    ra, rf, rv = analyse_artifact(str(right))
    ldata = Path(left).read_bytes()
    rdata = Path(right).read_bytes()
    distance = normalised_distance(lv.vector, rv.vector)

    component_delta = {
        name: abs(vector_with_labels(lv.vector)[name] - vector_with_labels(rv.vector)[name])
        for name in vector_with_labels(lv.vector)
    }
    top_delta = sorted(component_delta.items(), key=lambda kv: kv[1], reverse=True)[:8]

    return {
        "schema": "pn-bis-comparison-v0.2",
        "left": {"artifact": la.to_dict(), "structure": structure_summary(ldata, left).to_dict()},
        "right": {"artifact": ra.to_dict(), "structure": structure_summary(rdata, right).to_dict()},
        "exact_sha256_match": la.sha256 == ra.sha256,
        "phase_vector_distance": distance,
        "left_vector_digest": lv.digest,
        "right_vector_digest": rv.digest,
        "top_component_deltas": [{"component": k, "delta": v} for k, v in top_delta],
        "entropy_delta": {
            "byte_entropy_norm": abs(lf.byte_entropy_norm - rf.byte_entropy_norm),
            "base64_entropy_norm": abs(lf.base64_entropy_norm - rf.base64_entropy_norm),
            "chunk_entropy_mean": abs(lf.chunk_entropy_mean - rf.chunk_entropy_mean),
            "chunk_entropy_max_delta": abs(lf.chunk_entropy_max_delta - rf.chunk_entropy_max_delta),
        },
    }
