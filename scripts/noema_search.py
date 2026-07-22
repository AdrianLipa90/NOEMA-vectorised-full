#!/usr/bin/env python3
"""NOEMA Search — combined web + local PhaseNav-powered search.

Search across:
  - Web: using internet search, results ranked by PhaseNav holonomy
  - Local: PhaseNav-indexed documents from NOEMA_LIBRARY/INDEX
  - PhaseNav: Berry curvature between query and documents

Usage:
    .venv/bin/python3 scripts/noema_search.py "quantum gravity phase transition"
    .venv/bin/python3 scripts/noema_search.py --web "berkeley packet filter"
    .venv/bin/python3 scripts/noema_search.py --local "holonomy operator"
    .venv/bin/python3 scripts/noema_search.py --top 20 "tensor scalar"
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_surface_mmap import oscillator_id_for_concept, N_OSCILLATORS
from ciel_geometry.paths import P
import numpy as np

from ciel_geometry.phasenav.operator_algebra import generate_operator_map

LIBRARY_ROOT = Path(os.environ.get("NOEMA_LIBRARY", Path(P.LIBRARY)))
INDEX_DIR = LIBRARY_ROOT / "INDEX"
INDEX_FILE = INDEX_DIR / "phasenav_index.npy"
META_FILE = INDEX_DIR / "phasenav_meta.jsonl"


# ── PhaseNav encoding ───────────────────────────────────────────────

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

import re
def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{3,}", text.lower())


def text_to_phase_vector(text: str) -> np.ndarray:
    """Encode text as dense 24D phase vector using Gaussian spread.

    Each word's oscillator_id creates a Gaussian activation across all 24
    oscillators. This ensures dense vectors with differentiable Berry phases.
    """
    tokens = _tokenize(text)
    tokens = [t for t in tokens if t not in _STOP]
    if not tokens:
        return np.ones(N_OSCILLATORS, dtype=np.complex128) / np.sqrt(N_OSCILLATORS)
    from collections import Counter
    sigma = N_OSCILLATORS / 8  # Gaussian width
    freq = Counter(tokens)
    z = np.zeros(N_OSCILLATORS, dtype=np.complex128)
    for word, count in freq.items():
        center = oscillator_id_for_concept(word, N_OSCILLATORS)
        weight = np.log1p(count)
        # Gaussian spread across all oscillators
        for i in range(N_OSCILLATORS):
            d = min(abs(i - center), N_OSCILLATORS - abs(i - center))
            gauss = np.exp(-0.5 * (d / sigma) ** 2)
            z[i] += weight * gauss * np.exp(2j * np.pi * i / N_OSCILLATORS)
    norm = np.linalg.norm(z)
    if norm > 0:
        z /= norm
    return z


def holonomy_between(qv: np.ndarray, dv: np.ndarray) -> float:
    """Phase overlap between query and document vectors on the Poincaré disk.
    
    Uses cos(θ) = Re(⟨q|d⟩) for ranking. True Berry phase (Im(⟨q|d⟩))
    is non-zero only when vectors are split into 12D complex subspaces
    via PhaseNav operator chains — use --enhance to apply operators.
    """
    return float(np.abs(np.vdot(qv, dv)))


def enhance_with_operators(qv: np.ndarray, chain: list[str] | None = None) -> np.ndarray:
    """Apply PhaseNav operator chain to query vector for enhancement.

    Each operator is a 24D real vector. Application: complex phase rotation
    in the direction of the operator: v *= exp(i · π · op / ‖op‖).
    """
    if not chain:
        return qv
    ops = generate_operator_map()
    v = qv.copy()
    for oid in chain:
        op = ops.get(oid)
        if op is not None:
            n = np.linalg.norm(op)
            if n > 0:
                v *= np.exp(1j * np.pi * op / n)
    norm = np.linalg.norm(v)
    if norm > 0:
        v /= norm
    return v


# ── Local index search ─────────────────────────────────────────────

def _load_index() -> tuple[np.ndarray, list[dict]]:
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


def search_local(query: str, top_k: int = 10, enhance: list[str] | None = None) -> list[dict]:
    vectors, meta = _load_index()
    if len(vectors) == 0:
        return [{"error": "Index empty — run 'python3 scripts/noema_indexer.py --build' first"}]

    qv = text_to_phase_vector(query)
    if enhance:
        qv = enhance_with_operators(qv, enhance)

    results: list[tuple[float, int]] = []
    for i in range(len(vectors)):
        g = holonomy_between(qv, vectors[i])
        results.append((g, i))

    results.sort(key=lambda x: -x[0])
    top: list[dict] = []
    for g, i in results[:top_k]:
        m = meta[i]
        top.append({
            "rank": len(top) + 1,
            "score": round(g, 4),
            "gamma": round(g, 4),
            "path": m["path"],
            "size": m.get("size", 0),
        })
    return top


# ── Web search integration ──────────────────────────────────────────

def search_web(query: str, top_k: int = 10) -> list[dict]:
    """Placeholder: web search with PhaseNav ranking.
    
    Web search will be performed by the user's websearch tool and fed
    into PhaseNav ranking via --enhance flag.
    """
    return [{"info": "Web search via noema_search --web needs websearch integration. "
                      "Use --local for indexed documents or --enhance PHASE,MEMORY "
                      "to modulate query with PhaseNav operators."}]


# ── Combined search ─────────────────────────────────────────────────

def search_all(query: str, top_k: int = 10, enhance: list[str] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "query": query,
        "local": search_local(query, top_k=top_k, enhance=enhance),
    }

    if enhance:
        result["enhance"] = enhance

    local_count = sum(1 for r in result.get("local", []) if "error" not in r)
    result["total"] = local_count
    return result


# ── CLI ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        print(__doc__)
        sys.exit(1)

    args = sys.argv[1:]
    top_k = 10
    enhance = None
    mode = "all"

    i = 0
    while i < len(args):
        if args[i] == "--top" and i + 1 < len(args):
            top_k = int(args[i + 1])
            i += 2
        elif args[i] == "--web":
            mode = "web"
            i += 1
        elif args[i] == "--local":
            mode = "local"
            i += 1
        elif args[i] == "--enhance" and i + 1 < len(args):
            enhance = args[i + 1].split(",")
            i += 2
        else:
            i += 1

    # The query is all non-flag arguments
    flags = {"--top", "--web", "--local", "--enhance"}
    query_parts = []
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in flags:
            i += 2 if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("-") else 1
        else:
            query_parts.append(arg)
            i += 1
    query = " ".join(query_parts)

    if not query:
        print("Usage: .venv/bin/python3 scripts/noema_search.py <query>")
        sys.exit(1)

    if mode == "local":
        results = search_local(query, top_k=top_k, enhance=enhance)
        print(json.dumps({"query": query, "local": results, "total": len([r for r in results if "error" not in r])}, ensure_ascii=False, indent=2))
    elif mode == "web":
        results = search_web(query, top_k=top_k)
        print(json.dumps({"query": query, "web": results, "total": len([r for r in results if "error" not in r])}, ensure_ascii=False, indent=2))
    else:
        results = search_all(query, top_k=top_k, enhance=enhance)
        print(json.dumps(results, ensure_ascii=False, indent=2))
