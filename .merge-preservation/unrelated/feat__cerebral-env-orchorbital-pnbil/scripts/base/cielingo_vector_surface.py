#!/usr/bin/env python3
"""Build the CIELingo 24D vector compatibility surface."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.vector_surface import vector_surface_report, write_vector_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--query", default="")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--oscillators", type=int, default=120)
    parser.add_argument("--out", default="integration/reports/cielingo_vector_surface_20260529.json")
    args = parser.parse_args()

    report = vector_surface_report(
        args.repo_root,
        query=args.query,
        limit=args.limit,
        n_oscillators=args.oscillators,
    )
    out = Path(args.repo_root) / args.out
    write_vector_report(out, report)
    print(json.dumps({
        "schema": report["schema"],
        "card_count": report["card_count"],
        "vector_dim": report["vector_dim"],
        "mean_phase_alignment": report["mean_phase_alignment"],
        "mean_j_bus_total": report["mean_j_bus_total"],
        "registry_digest": report["registry_digest"],
        "out": str(out),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
