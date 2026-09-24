#!/usr/bin/env python3
"""CIELingo PhaseNav Indexer — indeksuje CIELINGO_CANON wektorami fazowymi.

Wektoryzowana wersja: żadnej pętli po N_OSCILLATORS (numpy broadcasting).
Po --build każde zapytanie o oś/moduł = holonomy lookup, nie grep po drzewie.

Usage:
    scripts/cielingo_phase_index.py --build
    scripts/cielingo_phase_index.py --query "language_detection_axis"
    scripts/cielingo_phase_index.py --find-axis language_detection_axis
    scripts/cielingo_phase_index.py --probe
"""
from __future__ import annotations
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

CIELINGO_ROOT = Path("/media/adrian/REPOZYTORIA_GIT1/New_Volume/CIEL_PROJECT_CANON/CIELINGO_CANON")

_ICFG: dict = {}
try:
    _cfg_path = Path(os.environ.get("NOEMA_CONFIG", str(ROOT / "noema_config.json")))
    if _cfg_path.exists():
        _ICFG = json.loads(_cfg_path.read_text()).get("indexer", {})
except Exception:
    pass

INDEX_DIR = Path(_ICFG.get("library_root", "/home/adrian/new_volume_rw/NOEMA_LIBRARY")) / "INDEX"
INDEX_FILE = INDEX_DIR / "cielingo_phase_index.npy"
META_FILE  = INDEX_DIR / "cielingo_phase_meta.jsonl"

_EXTENSIONS = (".py", ".json", ".jsonl", ".md")
_MAX_CHARS  = 40_000

_STOP = {
    "the","a","an","is","was","are","be","been","have","has","do","does","did",
    "to","of","in","for","on","with","at","by","from","as","if","and","or","not",
    "się","nie","na","to","w","i","z","że","jak","do","o","a","po","co","za",
    "od","przez","dla","ma","czy","ale","tym","tego","tak","jest","być",
    "import","from","return","def","class","self","pass","true","false","none",
    "str","int","float","list","dict","set","bool","any","optional",
}

_II = np.arange(N_OSCILLATORS)
_PHASE_BASES = np.exp(2j * np.pi * _II / N_OSCILLATORS)
_SIGMA = N_OSCILLATORS / 8


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ_]{3,}", text.lower())


def text_to_phase_vector(text: str) -> np.ndarray:
    """Wektoryzowane kodowanie — brak pętli po N_OSCILLATORS."""
    tokens = [t for t in _tokenize(text) if t not in _STOP]
    if not tokens:
        return np.ones(N_OSCILLATORS, dtype=np.complex128) / np.sqrt(N_OSCILLATORS)

    freq = Counter(tokens)
    z = np.zeros(N_OSCILLATORS, dtype=np.complex128)

    for word, count in freq.items():
        center = oscillator_id_for_concept(word, N_OSCILLATORS)
        weight = np.log1p(count)
        d = np.minimum(np.abs(_II - center), N_OSCILLATORS - np.abs(_II - center))
        gauss = np.exp(-0.5 * (d / _SIGMA) ** 2)
        z += weight * gauss * _PHASE_BASES

    norm = np.linalg.norm(z)
    if norm > 0:
        z /= norm
    return z


def holonomy(q: np.ndarray, d: np.ndarray) -> float:
    return float(np.abs(np.angle(np.vdot(q, d))))


def _extract_symbols(text: str, path: Path) -> list[str]:
    """Wyciąga nazwy funkcji, klas i zmiennych z pliku .py."""
    if path.suffix != ".py":
        return []
    return re.findall(r"(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", text)


def _collect() -> list[Path]:
    files: list[Path] = []
    for ext in _EXTENSIONS:
        files.extend(CIELINGO_ROOT.rglob(f"*{ext}"))
    return sorted(set(files))


def _read(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if path.suffix == ".jsonl":
            lines = [l for l in text.splitlines() if l.strip()][-30:]
            text = "\n".join(lines)
        return text[:_MAX_CHARS]
    except Exception:
        return ""


def build_index() -> dict[str, Any]:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    files = _collect()
    if not files:
        return {"status": "no_files", "count": 0}

    vectors: list[np.ndarray] = []
    meta: list[dict] = []
    t0 = time.time()

    for i, path in enumerate(files):
        text = _read(path)
        z = text_to_phase_vector(text)
        symbols = _extract_symbols(text, path)
        vectors.append(z)
        meta.append({
            "path": str(path.relative_to(CIELINGO_ROOT)),
            "abs": str(path),
            "size": path.stat().st_size,
            "suffix": path.suffix,
            "symbols": symbols[:40],
            "idx": i,
        })
        if (i + 1) % 50 == 0:
            print(f"  [{i+1}/{len(files)}] indexed")

    arr = np.array(vectors, dtype=np.complex128)
    np.save(str(INDEX_FILE), arr)
    with open(META_FILE, "w") as f:
        for m in meta:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    elapsed = time.time() - t0
    return {
        "status": "ok",
        "count": len(files),
        "elapsed_s": round(elapsed, 2),
        "docs_per_sec": round(len(files) / max(elapsed, 0.001), 1),
        "index_file": str(INDEX_FILE),
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


def query(q: str, top_k: int = 10) -> list[dict[str, Any]]:
    vectors, meta = load_index()
    if len(vectors) == 0:
        return [{"error": "empty — run --build first"}]
    qv = text_to_phase_vector(q)
    gammas = np.array([holonomy(qv, vectors[i]) for i in range(len(vectors))])
    top_idx = np.argsort(-gammas)[:top_k]
    return [
        {"rank": r+1, "gamma": round(float(gammas[i]), 4),
         "path": meta[i]["path"], "symbols": meta[i].get("symbols", [])}
        for r, i in enumerate(top_idx)
    ]


def find_axis(axis_name: str) -> dict[str, Any]:
    """Sprawdza czy oś istnieje — exact symbol match + holonomy fallback."""
    vectors, meta = load_index()
    if len(vectors) == 0:
        return {"error": "empty — run --build first"}

    # 1. Exact: szukaj nazwy w symbolach
    exact = [m for m in meta if axis_name in m.get("symbols", []) or
             axis_name in m["path"]]
    if exact:
        return {"found": True, "match": "exact", "files": [m["path"] for m in exact]}

    # 2. Holonomy fallback: top-5 najbliższych
    qv = text_to_phase_vector(axis_name)
    gammas = np.array([holonomy(qv, vectors[i]) for i in range(len(vectors))])
    top_idx = np.argsort(-gammas)[:5]
    candidates = [{"path": meta[i]["path"], "gamma": round(float(gammas[i]), 4)}
                  for i in top_idx]
    return {"found": False, "match": "holonomy_candidates", "candidates": candidates}


def probe() -> dict[str, Any]:
    vectors, meta = load_index()
    if len(vectors) == 0:
        return {"status": "empty"}
    suffixes = Counter(m["suffix"] for m in meta)
    return {
        "status": "ok", "count": len(vectors),
        "dim": vectors.shape[1],
        "memory_mb": round(vectors.nbytes / 1e6, 2),
        "by_suffix": dict(suffixes),
        "index_file": str(INDEX_FILE),
    }


if __name__ == "__main__":
    if "--build" in sys.argv:
        print(json.dumps(build_index(), ensure_ascii=False, indent=2))
    elif "--query" in sys.argv:
        idx = sys.argv.index("--query")
        q = " ".join(sys.argv[idx+1:]) if idx+1 < len(sys.argv) else ""
        print(json.dumps(query(q), ensure_ascii=False, indent=2))
    elif "--find-axis" in sys.argv:
        idx = sys.argv.index("--find-axis")
        axis = sys.argv[idx+1] if idx+1 < len(sys.argv) else ""
        print(json.dumps(find_axis(axis), ensure_ascii=False, indent=2))
    elif "--probe" in sys.argv:
        print(json.dumps(probe(), ensure_ascii=False, indent=2))
    else:
        print(__doc__)
