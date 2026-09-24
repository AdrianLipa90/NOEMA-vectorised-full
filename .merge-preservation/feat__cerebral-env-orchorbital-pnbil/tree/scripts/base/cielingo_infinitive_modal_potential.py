#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.infinitive_modal_potential import infinitive_modal_report, write_report


def main() -> int:
    ap = argparse.ArgumentParser(description="Build CIELingo infinitive -> modality potential report.")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--out", default="integration/reports/cielingo_infinitive_modal_potential_20260529.json")
    args = ap.parse_args()
    report = write_report(args.out, args.repo_root)
    print(json.dumps({
        "schema": report["schema"],
        "infinitive_count": report["infinitive_count"],
        "modality_count": report["modality_count"],
        "mapping_count": report["mapping_count"],
        "lane_counts": report["lane_counts"],
        "out": args.out,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
