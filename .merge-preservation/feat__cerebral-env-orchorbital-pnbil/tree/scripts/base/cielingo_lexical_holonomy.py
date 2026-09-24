#!/usr/bin/env python3
"""Build CIELingo lexical holonomy relations and word confidence notes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.lexical_holonomy import lexical_holonomy_report, read_language_card_file, write_lexical_holonomy_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--language", default=None)
    parser.add_argument("--query", default="")
    parser.add_argument("--out", default="")
    parser.add_argument("--read-card", default="", help="Read one guarded language-card file path and return preview.")
    parser.add_argument("--preview-bytes", type=int, default=2048)
    args = parser.parse_args()

    if args.read_card:
        text = read_language_card_file(args.read_card, args.repo_root, max_bytes=max(args.preview_bytes, 1_000_000))
        print(text[: args.preview_bytes])
        return 0

    report = lexical_holonomy_report(args.repo_root, language=args.language, query=args.query)
    if args.out:
        write_lexical_holonomy_report(args.out, args.repo_root, language=args.language, query=args.query)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
