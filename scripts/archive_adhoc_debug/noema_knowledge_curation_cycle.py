#!/usr/bin/env python3
"""Autonomous knowledge-curation arm — chains the three provenance/concept
passes built 2026-07-08 into one periodic, self-contained cycle instead of
requiring a human to run each script by hand after every ingest.

Order matters: confidence backfill must run before flagging (flagging reads
source_type/confidence), concept tagging is independent of both but shares
the same term_index read.

    1. noema_tag_concepts.py    — doc -> PhaseNav operator tags
    2. ciel_confidence_system.backfill — doc -> confidence/source_reliability
    3. noema_flag_ambiguities.py       — unified uncertainty_log queue

Idempotent: re-running is safe (tagging replaces its own table each run,
backfill only touches docs still at the 0.5 default, flagging dedupes by
doc_idx+reason). Meant to run on a timer (see
systemd/noema-knowledge-curation.timer), not continuously — a full pass
over ~8000 docs takes several minutes.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _run(label: str, args: list[str]) -> None:
    print(f"[curation-cycle] === {label} ===", flush=True)
    t0 = time.time()
    result = subprocess.run([sys.executable, *args], cwd=str(ROOT.parent))
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"[curation-cycle] {label} FAILED (exit {result.returncode}) after {elapsed:.1f}s", flush=True)
        raise SystemExit(result.returncode)
    print(f"[curation-cycle] {label} done in {elapsed:.1f}s", flush=True)


def main() -> int:
    _run("concept tagging", [str(ROOT / "noema_tag_concepts.py")])
    _run("confidence backfill", ["-m", "scripts.ciel_confidence_system.backfill"])
    _run("ambiguity flagging", [str(ROOT / "noema_flag_ambiguities.py")])
    print("[curation-cycle] full cycle complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
