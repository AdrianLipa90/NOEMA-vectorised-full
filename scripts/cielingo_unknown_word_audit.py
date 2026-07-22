#!/usr/bin/env python3
"""Run CIELingo unknown-word audit over meaning-debt candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.unknown_word_audit import audit_unknown_words  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    report = audit_unknown_words(args.repo_root, batch_size=args.batch_size, output_dir=args.output_dir)
    print(json.dumps(report.__dict__, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
