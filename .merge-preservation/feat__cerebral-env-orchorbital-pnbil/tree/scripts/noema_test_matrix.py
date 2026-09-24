#!/usr/bin/env python3
"""Run pytest through the NOEMA test matrix surface."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from noema_holonomic_doctor.test_matrix import discover_tests, run_one, write_reports


def main() -> int:
    parser = argparse.ArgumentParser(description="Run NOEMA pytest matrix.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--kind", default="", help="Optional kind filter, e.g. noema_subsystem")
    parser.add_argument("--include-e2e", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    entries = discover_tests(root)
    if args.kind:
        entries = [e for e in entries if e.kind == args.kind]
    if not args.include_e2e:
        entries = [e for e in entries if e.kind != "e2e_gate"]
    if args.limit > 0:
        entries = entries[: args.limit]

    results = [run_one(root, entry, timeout_s=args.timeout) for entry in entries]
    report = write_reports(root, results)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 0 if report["summary"]["by_status"].get("FAIL", 0) == 0 and report["summary"]["by_status"].get("TIMEOUT", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
