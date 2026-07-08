#!/usr/bin/env python3
"""Pełny pipeline: plik → PhaseNav koncept → biblioteka → surface.

Usage:
    .venv/bin/python3 scripts/noema_learn_file.py <ścieżka_do_pliku>

Kroki:
  1. Czyta plik, wyciąga tekst
  2. Przez phasenav_enrich → 24D vector + operator
  3. Dodaje do library_index.npy + library_meta.npy
  4. Rebuild zip_catalog/index.jsonl
  5. Restartuje PhaseNav cold (przez systemd)
  6. Opcjonalnie: pyta agent backend o wygenerowanie kodu
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.phasenav.enrichment import phasenav_enrich
from ciel_geometry.phasenav.operator_algebra import operator_signature

LIBRARY_INDEX = "/media/adrian/New Volume1/NOEMA_PHASE_DATA/PHASE_INDEX/library_index.npy"
LIBRARY_META = "/media/adrian/New Volume1/NOEMA_PHASE_DATA/PHASE_INDEX/library_meta.npy"
ZIP_INDEX = Path("/dev/shm/ciel_noema/zip_catalog/index.jsonl")
AGENT_BACKEND = "http://localhost:18520"

OPERATORS = [
    "ACTION_REQUEST", "ADDITION", "AFFECT", "ASSERTION", "BOUNDARY",
    "CANON_BLOCK", "CAUSE", "COMPOSITION", "CONDITION", "CONSENT",
    "CONSENT_REQUIRED", "DIFFERENCE", "FOLD", "FORCE", "HYPOTHESIS",
    "IDENTITY", "MEMORY", "MODAL_NECESSITY", "MODAL_OBLIGATION",
    "MODAL_PERMISSION", "MODAL_POSSIBILITY", "NEGATION", "ORDER",
    "PAUSE", "PREFERENCE", "QUESTION", "REFUSAL", "RETURN", "RISK",
    "SCOPE", "SIMULATION_BOUNDARY", "SOURCE", "SOURCE_REQUIRED",
    "TRANSFORM", "UNCERTAINTY", "UNRUH_DRIVE", "WARP_DRIFT",
]


def _normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v


def _nearest_operator(vec: np.ndarray) -> tuple[str, float]:
    vn = _normalize(vec)
    best_op = "IDENTITY"
    best_sim = -1.0
    for op in OPERATORS:
        sig = operator_signature(op)
        sim = float(np.dot(vn, _normalize(sig)))
        if sim > best_sim:
            best_sim = sim
            best_op = op
    return best_op, best_sim


def learn_file(filepath: str, *, generate_code: bool = True) -> dict:
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    text = path.read_text(encoding="utf-8", errors="replace")

    # Krok 1: PhaseNav enrichment
    pn = phasenav_enrich(text)
    vec = np.array(pn["operator_vector_24d"], dtype=np.float64)
    op_id = pn["operator_id"]
    fp = pn["harmonic_fingerprint"]

    # Krok 2: Dodaj do biblioteki
    idx = np.load(LIBRARY_INDEX) if Path(LIBRARY_INDEX).exists() else np.zeros((0, 24), dtype=np.float64)
    meta = np.load(LIBRARY_META) if Path(LIBRARY_META).exists() else np.zeros(0, dtype=[('id','U12'),('filename','U200'),('author','U50'),('topic','U100'),('date','U20'),('on_disk','?'),('disk_path','U400')])

    new_id = f"{hash(filepath) % (10**12):012x}"
    new_meta = np.array([(new_id, path.name[:199], "NOEMA_learned", op_id[:99], time.strftime("%Y-%m-%d"), True, str(path.absolute())[:399])], dtype=meta.dtype)

    idx = np.vstack([idx, vec.reshape(1, 24)]) if idx.shape[0] else vec.reshape(1, 24)
    meta = np.concatenate([meta, new_meta]) if meta.shape[0] else new_meta

    np.save(LIBRARY_INDEX, idx)
    np.save(LIBRARY_META, meta)

    # Krok 3: Rebuild zip_catalog/index.jsonl
    ZIP_INDEX.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(ZIP_INDEX, "w") as f:
        for i in range(len(idx)):
            entry = {
                "zip_path": str(meta[i]["disk_path"]) if i < len(meta) else path.name,
                "total_files": 1,
                "phasenav": {
                    "operator_id": str(meta[i]["topic"]) if i < len(meta) else op_id,
                    "operator_vector_24d": idx[i].tolist(),
                },
                "meta": {
                    "id": str(meta[i]["id"]) if i < len(meta) else new_id,
                    "filename": str(meta[i]["filename"]) if i < len(meta) else path.name,
                    "author": str(meta[i]["author"]) if i < len(meta) else "NOEMA",
                    "topic": str(meta[i]["topic"]) if i < len(meta) else op_id,
                },
            }
            f.write(json.dumps(entry) + "\n")
            count += 1

    # Krok 4: Restart PhaseNav cold
    subprocess.run(["systemctl", "--user", "restart", "noema-phasenav.service", "noema-phasenav-hot.service"],
                   capture_output=True, timeout=10)

    result = {
        "file": filepath,
        "operator": op_id,
        "fingerprint": fp,
        "library_size": int(count),
        "new_index": int(len(idx) - 1),
        "status": "learned + seeded on surface",
    }

    # Krok 5 (opcjonalnie): Analiza przez agent backend
    if generate_code:
        try:
            import urllib.request
            import urllib.parse
            payload = json.dumps({"messages": [{"role": "user", "content": f"Analyze this concept and extract themes, essence, and structural patterns:\n\n{text[:3000]}"}]}).encode()
            req = urllib.request.Request(f"{AGENT_BACKEND}/v1/chat/completions", data=payload, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=30)
            agent_result = json.loads(resp.read().decode())
            result["agent_response"] = agent_result
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_learn_file.py:137 quiet except scope=learn_file reason=assign_fallback")
            result["agent_error"] = str(e)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    result = learn_file(sys.argv[1], generate_code="--no-code" not in sys.argv)
    print(json.dumps(result, indent=2, default=str))
