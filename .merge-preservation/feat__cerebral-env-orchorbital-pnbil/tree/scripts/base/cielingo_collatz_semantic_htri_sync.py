#!/usr/bin/env python3
"""Generate CIELingo Collatz⇄semantic⇄HTRI sync report."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.collatz_semantic_htri_sync import synchronization_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--query", default="język słowo znaczenie semantic language word Collatz HTRI")
    parser.add_argument("--limit", type=int, default=24)
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    result = synchronization_report(args.repo_root, query=args.query, limit=args.limit)
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
