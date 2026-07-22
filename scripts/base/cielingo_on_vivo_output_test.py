#!/usr/bin/env python3
"""Run local on-vivo style CIELingo output-vector test."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.triadic_output_vector import on_vivo_output_test, write_output_test_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--text", required=True)
    parser.add_argument("--language", default="pl")
    parser.add_argument("--out", default="integration/reports/cielingo_on_vivo_output_test.report.json")
    args = parser.parse_args()
    report = on_vivo_output_test(args.text, args.repo_root, language_hint=args.language)
    write_output_test_report(args.out, report)
    print(json.dumps({
        "status": "PASS",
        "schema": report["schema"],
        "token_count": report["token_count"],
        "matched_token_count": report["matched_token_count"],
        "unknown_token_count": report["unknown_token_count"],
        "vector_dim": report["vector_dim"],
        "output_readiness": report["output_readiness"],
        "phase_lock": report["phase_lock"],
        "semantic_time_resistance": report["semantic_time_resistance"],
        "needs_supervised_grammar_review": report["needs_supervised_grammar_review"],
        "output_digest": report["output_digest"],
        "out": args.out,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
