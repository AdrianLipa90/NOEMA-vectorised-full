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

from cielingo.infinitive_merge_audit import generate_infinitive_merge_audit


def main() -> int:
    ap = argparse.ArgumentParser(description="Infinitivize what can and group the rest into owned residual sets.")
    ap.add_argument("--unknown-words", required=True)
    ap.add_argument("--out", default="data/cielingo/infinitive_merge_audit")
    args = ap.parse_args()
    report = generate_infinitive_merge_audit(args.unknown_words, args.out)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
