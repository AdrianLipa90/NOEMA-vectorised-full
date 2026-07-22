#!/usr/bin/env python3
"""Generate CIELingo candidate word cards from the meaning-debt index."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.meaning_debt_word_cards import generate_debt_word_cards


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debt-index", required=True, help="Path to affected_cards_index.csv")
    parser.add_argument("--output-dir", default="data/cielingo/debt_word_cards")
    parser.add_argument("--source-label", default="ciel_pol_meaning_debt_cards_bundle")
    args = parser.parse_args()
    report = generate_debt_word_cards(args.debt_index, output_dir=args.output_dir, source_label=args.source_label)
    print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
