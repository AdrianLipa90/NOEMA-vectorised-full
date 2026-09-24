#!/usr/bin/env python3
"""NOEMA PhaseNav Indexer — build search index from documents to phase vectors.

Indexes documents (PDF, txt, md, jsonl) into N_OSCILLATORS (36) phase vectors stored as
binary mmap files in the INDEX library. Each document gets:
  - N_OSCILLATORS-D phase vector (normalized sum of term→oscillator projections)
  - metadata (path, size, term count, dominant oscillator)

Search: encode query as N_OSCILLATORS-D phase vector → compute holonomy with each doc →
rank by Berry phase magnitude.

Usage:
    .venv/bin/python3 scripts/noema_indexer.py --build    # build/rebuild index
    .venv/bin/python3 scripts/noema_indexer.py --search "query"
    .venv/bin/python3 scripts/noema_indexer.py --probe    # index stats
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_surface_mmap import oscillator_id_for_concept, N_OSCILLATORS

LIBRARY_ROOT = Path(os.environ.get(
    "NOEMA_LIBRARY",
    "/media/adrian/New Volume/NOEMA_LIBRARY",
))
INDEX_DIR = LIBRARY_ROOT / "INDEX"
PDF_DIR = LIBRARY_ROOT / "PDF"
DOC_DIR = LIBRARY_ROOT / "DOCUMENTS"

# Stop words
_STOP = {
    "the", "a", "an", "is", "was", "are", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "out", "off", "over",
    "under", "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "just", "because", "and", "but",
    "or", "if", "while", "about", "up", "it", "its", "this", "that",
    "these", "those", "i", "me", "my", "myself", "we", "our", "ours",
    "you", "your", "yours", "he", "him", "his", "she", "her", "hers",
    "they", "them", "their", "theirs", "what", "which", "who", "whom",
    "się", "nie", "na", "to", "w", "i", "z", "że", "jak", "do", "o",
    "a", "po", "co", "za", "od", "przez", "dla", "ma", "czy", "ale",
    "tym", "tego", "tych", "tak", "jest", "być", "był", "była", "było",
    "który", "która", "które", "jako", "przy", "pod", "nad", "bez",
    "oraz", "już", "bardzo", "więc", "bo", "gdy", "gdzie", "kiedy",
    "może", "mój", "twój", "jego", "jej", "nasz", "wasz", "ich",
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{3,}", text.lower())


def text_to_phase_vector(text: str) -> np.ndarray:
    """Encode text as dense N_OSCILLATORS-D phase vector using Gaussian spread across oscillators.

    Each word's oscillator_id creates a Gaussian activation across all N_OSCILLATORS
    oscillators. This ensures dense vectors with differentiable Berry phases.
    """
    tokens = _tokenize(text)
    tokens = [t for t in tokens if t not in _STOP]
    if not tokens:
        return np.ones(N_OSCILLATORS, dtype=np.complex128) / np.sqrt(N_OSCILLATORS)

    sigma = N_OSCILLATORS / 8  # Gaussian width
    freq = Counter(tokens)
    z = np.zeros(N_OSCILLATORS, dtype=np.complex128)

    for word, count in freq.items():
        center = oscillator_id_for_concept(word, N_OSCILLATORS)
        weight = np.log1p(count)
        for i in range(N_OSCILLATORS):
            d = min(abs(i - center), N_OSCILLATORS - abs(i - center))
            gauss = np.exp(-0.5 * (d / sigma) ** 2)
            z[i] += weight * gauss * np.exp(2j * np.pi * i / N_OSCILLATORS)

    norm = np.linalg.norm(z)
    if norm > 0:
        z /= norm
    return z


def phase_vector_to_disk(z: np.ndarray) -> np.ndarray:
    """Convert complex phase vector to real Poincaré disk coordinates.
    Returns 48D real vector: [real_0, imag_0, real_1, imag_1, ...]
    """
    return np.ascontiguousarray(np.column_stack([z.real, z.imag]).ravel())


def holonomy_between(query: np.ndarray, doc: np.ndarray) -> float:
    """Berry phase between query and document phase vectors.
    γ = Im(log(〈q|d〉))  — geometric phase from inner product.
    """
    overlap = np.vdot(query, doc)
    return float(np.abs(np.angle(overlap)))


# ── Persistence ─────────────────────────────────────────────────────

INDEX_FILE = INDEX_DIR / "phasenav_index.npy"
META_FILE = INDEX_DIR / "phasenav_meta.jsonl"


def _collect_documents() -> list[Path]:
    """Collect all indexable documents from library directories."""
    files: list[Path] = []
    for base in [PDF_DIR, DOC_DIR]:
        if not base.exists():
            continue
        for ext in ("*.txt", "*.md", "*.jsonl", "*.py", "*.html", "*.csv", "*.json"):
            files.extend(base.rglob(ext))
    return sorted(set(files))


def _read_text(path: Path, max_chars: int = 50000) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if path.suffix == ".jsonl":
            lines = [l for l in text.splitlines() if l.strip()][-50:]
            text = "\n".join(lines)
        return text[:max_chars]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_indexer.py:139 quiet except scope=_read_text reason=return \"\"")
        raise
        return ""


def build_index(force: bool = False) -> dict[str, Any]:
    """Scan library directories and build PhaseNav index."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    files = _collect_documents()
    if not files:
        return {"status": "no documents", "count": 0}

    vectors: list[np.ndarray] = []
    meta: list[dict] = []

    t0 = time.time()
    for i, path in enumerate(files):
        rel = path.relative_to(LIBRARY_ROOT)
        text = _read_text(path)
        z = text_to_phase_vector(text)
        vectors.append(z)
        meta.append({
            "path": str(rel),
            "size": path.stat().st_size,
            "terms": len(_tokenize(text)),
            "idx": i,
        })
        if (i + 1) % 100 == 0:
            print(f"  [{i+1}/{len(files)}] {rel.parent}")

    # Save vectors as 2D complex array
    arr = np.array(vectors, dtype=np.complex128)
    np.save(str(INDEX_FILE), arr)

    # Save metadata
    with open(META_FILE, "w") as f:
        for m in meta:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    elapsed = time.time() - t0
    return {
        "status": "ok",
        "count": len(files),
        "elapsed_s": round(elapsed, 2),
        "docs_per_sec": round(len(files) / elapsed, 1),
    }


def load_index() -> tuple[np.ndarray, list[dict]]:
    if not INDEX_FILE.exists():
        return np.array([]), []
    vectors = np.load(str(INDEX_FILE))
    meta: list[dict] = []
    if META_FILE.exists():
        with open(META_FILE) as f:
            for line in f:
                if line.strip():
                    meta.append(json.loads(line))
    return vectors, meta


def search(query: str, top_k: int = 10) -> list[dict[str, Any]]:
    """Search index by PhaseNav holonomy ranking."""
    vectors, meta = load_index()
    if len(vectors) == 0:
        return [{"error": "index empty — run --build first"}]

    qv = text_to_phase_vector(query)
    results: list[tuple[float, int]] = []
    for i in range(len(vectors)):
        g = holonomy_between(qv, vectors[i])
        results.append((g, i))

    results.sort(key=lambda x: -x[0])
    top: list[dict[str, Any]] = []
    for g, i in results[:top_k]:
        m = meta[i]
        top.append({
            "rank": len(top) + 1,
            "gamma": round(g, 4),
            "path": m["path"],
            "size": m["size"],
        })
    return top


def probe_index() -> dict[str, Any]:
    vectors, meta = load_index()
    if len(vectors) == 0:
        return {"status": "empty", "count": 0}
    return {
        "status": "ok",
        "count": len(vectors),
        "dim": vectors.shape[1],
        "dtype": str(vectors.dtype),
        "mean_norm": float(np.mean(np.abs(vectors))),
        "memory_mb": round(vectors.nbytes / 1e6, 2),
    }


# ── CLI ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--build" in sys.argv:
        result = build_index()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--search" in sys.argv:
        idx = sys.argv.index("--search")
        query = " ".join(sys.argv[idx + 1:]) if idx + 1 < len(sys.argv) else ""
        if not query:
            print("Usage: --search \"query terms\"")
        else:
            results = search(query)
            print(json.dumps(results, ensure_ascii=False, indent=2))
    elif "--probe" in sys.argv:
        print(json.dumps(probe_index(), ensure_ascii=False, indent=2))
    else:
        print(__doc__)
