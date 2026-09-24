#!/usr/bin/env python3
"""Run CIELingo word -> phase-sense parser."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.phase_sense_parser import parse_text_to_phase_sense, write_phase_sense_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--text", required=True)
    parser.add_argument("--language", default="pl")
    parser.add_argument("--out", default="integration/reports/cielingo_phase_sense_parser.report.json")
    args = parser.parse_args()
    report = parse_text_to_phase_sense(args.text, args.repo_root, language_hint=args.language)
    write_phase_sense_report(args.out, report)
    print(json.dumps({
        "status": "PASS",
        "schema": report["schema"],
        "token_count": report["token_count"],
        "matched_token_count": report["matched_token_count"],
        "unknown_token_count": report["unknown_token_count"],
        "phase_sense_digest": report["phase_sense_digest"],
        "out": args.out,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
