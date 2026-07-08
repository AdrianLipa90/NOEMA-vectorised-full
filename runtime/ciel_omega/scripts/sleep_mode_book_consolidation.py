#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PKG_PARENT = ROOT.parent
for candidate in (PKG_PARENT, ROOT):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from ciel_omega.memory.sleep_consolidation import analyze_sleep_mode_corpus  # noqa: E402


def _json_default(obj: Any) -> Any:
    try:
        import numpy as np  # noqa: WPS433

        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
    except Exception:
        return str(obj)
    return str(obj)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run idle-time book consolidation for sleep mode")
    parser.add_argument("paths", nargs="*", help="Optional book/pdf paths; defaults to the canonical sleep corpus")
    parser.add_argument("--corpus-label", default="sleep_books")
    parser.add_argument("--report-root", default="", help="Where to write report artifacts")
    parser.add_argument("--idle-threshold", type=float, default=0.35)
    parser.add_argument("--allow-busy", action="store_true", help="Run even if the system is not idle")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument("--no-store", action="store_true", help="Skip MemoryStore writes")
    args = parser.parse_args()

    report = analyze_sleep_mode_corpus(
        args.paths or None,
        corpus_label=args.corpus_label,
        store_memory=not args.no_store,
        report_root=Path(args.report_root) if args.report_root else None,
        idle_threshold=args.idle_threshold,
        allow_busy=args.allow_busy,
    )

    if args.json:
        print(json.dumps(report, ensure_ascii=False, default=_json_default))
    else:
        print(json.dumps(report, ensure_ascii=False, default=_json_default, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
