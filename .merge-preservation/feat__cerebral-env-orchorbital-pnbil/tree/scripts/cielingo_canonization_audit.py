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

from cielingo.canonization_audit import generate_canonization_audit


def main() -> int:
    parser = argparse.ArgumentParser(description="CIELingo local canonization audit")
    parser.add_argument("--infinitives", default="data/cielingo/infinitive_merge_audit/infinitive_candidates.jsonl")
    parser.add_argument("--residuals", default="data/cielingo/infinitive_merge_audit/residual_assignments.jsonl")
    parser.add_argument("--out", default="data/cielingo/canonization_audit")
    args = parser.parse_args()
    report = generate_canonization_audit(
        infinitive_candidates_path=args.infinitives,
        residual_assignments_path=args.residuals,
        output_dir=args.out,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
