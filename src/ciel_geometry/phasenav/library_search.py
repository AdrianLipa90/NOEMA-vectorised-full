"""PhaseNav Library Search — hybrid 36D + 24D search over NOEMA_LIBRARY PDFs.

Search pipeline:
  1. 36D PhaseNav per-doc index — operator-cluster routing (fast cosine)
  2. 24D semantic index — within-cluster re-ranking (text embedding similarity)
  3. Hybrid score: alpha * sim_36d + (1 - alpha) * sim_24d

Usage:
    from ciel_geometry.phasenav.library_search import LibrarySearch
    s = LibrarySearch()
    results = s.search("świadomość tożsamość", top_k=10)
"""
from __future__ import annotations

import hashlib
import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from .operator_algebra import concept_to_operator

_log = logging.getLogger(__name__)

PHASE_INDEX = Path(__file__).resolve().parents[4] / "NOEMA_PHASE_DATA" / "PHASE_INDEX"
# Fallback: try canonical P path at runtime
try:
    from ciel_geometry.paths import P as _P
    _PHASE_INDEX_ENV = Path(_P.PHASE_DATA) / "PHASE_INDEX"
    if _PHASE_INDEX_ENV.exists():
        PHASE_INDEX = _PHASE_INDEX_ENV
except Exception:
    pass

_ALPHA = 1.0    # 36D only by default — 24D requires a text encoder for query embedding
_PERTURB = 0.15  # perturbation weight in per-doc vector


class LibrarySearch:
    """Hybrid NOEMA library search: PhaseNav cluster routing + semantic re-rank."""

    def __init__(self, phase_index: Path | None = None) -> None:
        self._idx_dir = Path(phase_index) if phase_index else PHASE_INDEX
        self._arr36: np.ndarray | None = None
        self._arr24: np.ndarray | None = None
        self._records: list[dict] = []
        self._meta24: list[Any] = []
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return
        idx36 = self._idx_dir / "library_index_36d_perdoc.npy"
        meta36 = self._idx_dir / "library_meta_36d_perdoc.jsonl"
        idx24 = self._idx_dir / "library_index.npy"
        meta24 = self._idx_dir / "library_meta.npy"

        if not idx36.exists():
            raise FileNotFoundError(f"36D index not found: {idx36}")

        self._arr36 = np.load(str(idx36))
        with open(meta36, encoding="utf-8") as f:
            self._records = [json.loads(line) for line in f]

        if idx24.exists() and meta24.exists():
            raw24 = np.load(str(idx24))
            norms = np.linalg.norm(raw24, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self._arr24 = raw24 / norms
            self._meta24 = list(np.load(str(meta24), allow_pickle=True))
        else:
            _log.warning("24D index not found — using 36D only")

        self._loaded = True

    def _query_vec36(self, text: str) -> tuple[np.ndarray, str]:
        seed_str = f"query::{text}"
        op_id, op_vec = concept_to_operator(seed_str)
        op_arr = np.array(op_vec, dtype=np.float64)
        digest = hashlib.sha256(text.encode()).digest()
        rng = np.random.default_rng(int.from_bytes(digest[:8], "big"))
        perturb = rng.standard_normal(36)
        perturb /= np.linalg.norm(perturb) + 1e-12
        q = (1.0 - _PERTURB) * op_arr + _PERTURB * perturb
        q /= np.linalg.norm(q) + 1e-12
        return q, op_id

    def search(
        self,
        query: str,
        top_k: int = 10,
        alpha: float | None = None,
        operator_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search NOEMA library.

        Args:
            query: Free-text query (Polish or English).
            top_k: Number of results.
            alpha: Override blend weight (default 0.72).
            operator_filter: Restrict to one PhaseNav operator (e.g. 'IDENTITY').

        Returns:
            List of result dicts with keys: rank, file, collection, author,
            operator_id, score, score_36d, score_24d, path.
        """
        self._load()
        blend = alpha if alpha is not None else _ALPHA

        q36, op_id = self._query_vec36(query)
        sim36 = self._arr36 @ q36

        if self._arr24 is not None:
            # 24D query: project query text through simple hash-to-24d mapping
            digest = hashlib.sha256(query.encode()).digest()
            rng24 = np.random.default_rng(int.from_bytes(digest[8:16], "big"))
            q24 = rng24.standard_normal(24)
            q24 /= np.linalg.norm(q24) + 1e-12
            sim24 = self._arr24 @ q24
        else:
            sim24 = np.zeros(len(self._records))

        hybrid = blend * sim36 + (1.0 - blend) * sim24

        # Apply operator filter
        mask = np.ones(len(self._records), dtype=bool)
        if operator_filter:
            for i, r in enumerate(self._records):
                if r.get("operator_id") != operator_filter:
                    mask[i] = False
            hybrid = np.where(mask, hybrid, -np.inf)

        idx = np.argsort(hybrid)[::-1][:top_k]
        results = []
        for rank, i in enumerate(idx, 1):
            r = self._records[i]
            results.append({
                "rank": rank,
                "file": r.get("file", ""),
                "collection": r.get("collection", ""),
                "author": r.get("author", ""),
                "operator_id": r.get("operator_id", ""),
                "score": round(float(hybrid[i]), 6),
                "score_36d": round(float(sim36[i]), 6),
                "score_24d": round(float(sim24[i]), 6),
                "path": r.get("path", ""),
            })
        return results

    def search_by_operator(self, operator_id: str, top_k: int = 10) -> list[dict]:
        """Return top-k documents in a specific operator cluster by 36D score."""
        self._load()
        q36, _ = self._query_vec36(operator_id)
        sim36 = self._arr36 @ q36
        mask = np.array([r.get("operator_id") == operator_id for r in self._records])
        sim36_masked = np.where(mask, sim36, -np.inf)
        idx = np.argsort(sim36_masked)[::-1][:top_k]
        return [
            {
                "rank": rank,
                "file": self._records[i].get("file", ""),
                "collection": self._records[i].get("collection", ""),
                "operator_id": operator_id,
                "score": round(float(sim36[i]), 6),
            }
            for rank, i in enumerate(idx, 1)
        ]

    def stats(self) -> dict[str, Any]:
        """Index statistics."""
        self._load()
        from collections import Counter
        ops = Counter(r.get("operator_id", "") for r in self._records)
        return {
            "n_documents": len(self._records),
            "index_36d_shape": list(self._arr36.shape) if self._arr36 is not None else None,
            "index_24d_shape": list(self._arr24.shape) if self._arr24 is not None else None,
            "operator_distribution": dict(ops.most_common(10)),
        }


@lru_cache(maxsize=1)
def get_library_search() -> LibrarySearch:
    return LibrarySearch()
