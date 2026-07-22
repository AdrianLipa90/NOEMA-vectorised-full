#!/usr/bin/env python3
"""Run CIELingo HTRI phase-bus report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.htri_phase_bus import phase_bus_report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--query", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--oscillators", type=int, default=120)
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    report = phase_bus_report(
        args.repo_root,
        query=args.query,
        limit=args.limit or None,
        n_oscillators=args.oscillators,
    )
    text = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
