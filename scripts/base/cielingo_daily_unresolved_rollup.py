#!/usr/bin/env python3
"""Emit daily unresolved rollup for CIELingo."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.unresolved_realtime import daily_unresolved_rollup


def main() -> int:
    parser = argparse.ArgumentParser(description="CIELingo daily unresolved rollup")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--date", default=None, help="UTC date YYYY-MM-DD; defaults to today")
    args = parser.parse_args()
    print(json.dumps(daily_unresolved_rollup(args.repo_root, date=args.date), indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
