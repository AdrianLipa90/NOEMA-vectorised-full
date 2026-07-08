#!/usr/bin/env python3
"""Record unresolved CIELingo words in real time."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.unresolved_realtime import daily_unresolved_rollup, record_realtime_unresolved


def main() -> int:
    parser = argparse.ArgumentParser(description="CIELingo realtime unresolved-word checker")
    parser.add_argument("--repo-root", default=str(ROOT), help="Repository root")
    parser.add_argument("--text", default=None, help="Text sample to check. If omitted, stdin is used.")
    parser.add_argument("--language", default="pl", help="Language hint")
    parser.add_argument("--source-role", default="runtime_text_sample", help="Observation source role")
    parser.add_argument("--no-candidates", action="store_true", help="Record unresolved only; do not create candidate cards")
    parser.add_argument("--daily-rollup", action="store_true", help="Also emit the daily rollup after recording")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    report = record_realtime_unresolved(
        text,
        args.repo_root,
        language_hint=args.language,
        source_role=args.source_role,
        create_candidates=not args.no_candidates,
    )
    if args.daily_rollup:
        report = {"realtime": report, "daily_rollup": daily_unresolved_rollup(args.repo_root)}
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
