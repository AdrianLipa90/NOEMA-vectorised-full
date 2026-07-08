#!/usr/bin/env python3
"""Build CIELingo tensor-scalar field reports."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.tensor_scalar_field import tensor_scalar_report, write_tensor_scalar_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--query", default="")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    report = tensor_scalar_report(args.repo_root, query=args.query, limit=args.limit)
    if args.out:
        write_tensor_scalar_report(args.out, report)
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
