#!/usr/bin/env python3
"""One-shot publisher for verified HTRI runtime capability evidence."""

from __future__ import annotations

import argparse
import inspect
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OMEGA_SRC = SRC / "CIEL_OMEGA_COMPLETE_SYSTEM"
for candidate in (SRC, OMEGA_SRC):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from ciel_geometry.htri_state_contract import publish_htri_runtime_probe
from ciel_omega.htri.gpu_driver import probe_htri_gpu_runtime


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Publish one HTRI runtime capability observation. "
            "This command does not run continuously and does not publish "
            "scientific HTRI metrics."
        )
    )
    parser.add_argument(
        "--publish-runtime-probe",
        action="store_true",
        required=True,
        help="perform exactly one runtime probe and publish its verified state",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="absolute canonical-volume output path",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    probe_source = inspect.getsourcefile(probe_htri_gpu_runtime)
    if not probe_source:
        raise RuntimeError("cannot identify HTRI runtime probe source")
    state, receipt = publish_htri_runtime_probe(
        probe_htri_gpu_runtime(),
        output_path=args.output,
        producer_path=Path(__file__),
        probe_source_path=Path(probe_source),
    )
    print(
        json.dumps(
            {
                "status": "published",
                "runtime_capability": state["runtime_capability"],
                "computation": state["computation"],
                "metrics": state["metrics"],
                "output_path": receipt["output_path"],
                "output_sha256": receipt["output_sha256"],
                "receipt_path": receipt["receipt_path"],
                "read_back_verified": receipt["read_back_verified"],
                "inference_used": receipt["inference_used"],
                "fallback_used": receipt["fallback_used"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
