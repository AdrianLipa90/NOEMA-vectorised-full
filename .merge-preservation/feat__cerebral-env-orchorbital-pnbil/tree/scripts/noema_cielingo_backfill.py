#!/usr/bin/env python3
"""Backfill CIELingo's learning gate against the pre-existing Knowledge DB
document backlog — separate from "digest" (TF-IDF indexing into
doc_analysis, which every doc already went through) vs "learning" (phase-
vector encoding + confidence-gated admission into PhaseMemory, which only
NEW rows after cielingo-sync's startup watermark ever received). Adrian's
framing (2026-07-10): "digest to jedno, nauka mówienia na nich to inna
sprawa" — this closes that gap for a chosen priority subset, not the whole
16581-row backlog (source_type='library_scan' dominates that with NOEMA's
own internal card/config files, not prose worth learning language from).

Priority filter (Adrian: "tylko część, priorytet"): source_type IN
('pdf', 'academic_paper') OR filename contains PUBLICATIONS/monograph —
real written documents, not NOEMA's own structural cards.

Resumable: writes progress (last processed idx) to a checkpoint file so a
Ctrl-C / restart doesn't lose place or reprocess. Throttled (SLEEP_S
between docs) to stay well under the disk/CPU pressure from earlier today.

Usage:
    .venv/bin/python3 scripts/noema_cielingo_backfill.py [--limit N] [--dry-run]
"""
from __future__ import annotations
import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
from ciel_geometry.paths import P  # noqa: E402
from ciel_geometry.cielingo_inference import CIELingoInference  # noqa: E402
from ciel_sot_agent.phasenav_learning_gate import learn_with_confidence  # noqa: E402

CHECKPOINT_PATH = Path(P.MEMORY) / "state" / "cielingo_backfill_checkpoint.json"
SLEEP_S = 0.5
PRIORITY_FILTER = """
    source_type IN ('pdf', 'academic_paper')
    OR filename LIKE '%PUBLICATIONS%'
    OR filename LIKE '%monograph%'
"""


def _load_checkpoint() -> int:
    if CHECKPOINT_PATH.exists():
        try:
            return json.loads(CHECKPOINT_PATH.read_text()).get("last_idx", 0)
        except (OSError, json.JSONDecodeError):
            return 0
    return 0


def _save_checkpoint(last_idx: int, processed: int) -> None:
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_PATH.write_text(json.dumps({
        "last_idx": last_idx, "processed_total": processed,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }))


def euler_target_phases(phi: np.ndarray) -> np.ndarray:
    mean_phase = np.angle(np.mean(np.exp(1j * phi)))
    return np.full_like(phi, mean_phase)


def apply_euler_sync(phi: np.ndarray, mix: float = 0.3) -> np.ndarray:
    phi_target = euler_target_phases(phi)
    delta = np.angle(np.exp(1j * (phi_target - phi)))
    return phi + mix * delta


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50, help="max docs to process this run")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    last_idx = _load_checkpoint()
    conn = sqlite3.connect(str(P.DB.KNOWLEDGE))
    rows = conn.execute(
        f"SELECT idx, essence, filename, source_type FROM doc_analysis "
        f"WHERE idx > ? AND ({PRIORITY_FILTER}) ORDER BY idx ASC LIMIT ?",
        (last_idx, args.limit),
    ).fetchall()
    conn.close()

    if not rows:
        print(f"nothing new to backfill past idx={last_idx}")
        return 0

    engine = CIELingoInference()
    processed = 0
    for row_idx, essence, filename, source_type in rows:
        text = (essence or filename or "").strip()
        if not text:
            last_idx = row_idx
            continue
        try:
            phi = engine.encode(text)
            phi_synced = apply_euler_sync(phi, mix=0.3)
        except Exception as e:
            print(f"  idx={row_idx} encode failed: {e}")
            last_idx = row_idx
            continue

        result = learn_with_confidence(
            engine, text, source="backfill", source_type=(source_type or "unknown"),
            metadata={"knowledge_db_idx": row_idx, "filename": filename},
            dry_run=args.dry_run, phi_override=phi_synced,
        )
        decision = result.get("decision", {})
        print(f"  idx={row_idx} conf={decision.get('confidence', '?')} "
              f"horizon={decision.get('horizon_class', '?')} file={str(filename)[:60]}")
        processed += 1
        last_idx = row_idx
        _save_checkpoint(last_idx, processed)
        time.sleep(SLEEP_S)

    print(f"backfill run done: {processed} docs processed, checkpoint at idx={last_idx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
