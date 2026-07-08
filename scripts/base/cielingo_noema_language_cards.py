#!/usr/bin/env python3
"""NOEMA-style inventory/search for CIELingo LNS language cards."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.lns_language_cards import language_card_inventory, search_language_cards


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--query", default="")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    if args.query:
        result = {
            "schema": "cielingo/noema-language-card-search/v0.1",
            "query": args.query,
            "hits": search_language_cards(args.query, args.repo_root, limit=args.limit),
        }
    else:
        result = language_card_inventory(args.repo_root)
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
