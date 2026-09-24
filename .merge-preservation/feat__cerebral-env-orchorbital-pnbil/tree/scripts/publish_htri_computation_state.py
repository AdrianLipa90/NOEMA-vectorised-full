#!/usr/bin/env python3
"""Run one real CUDA HTRI computation and publish its verified read-back."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OMEGA_SRC = SRC / "CIEL_OMEGA_COMPLETE_SYSTEM"
for candidate in (SRC, OMEGA_SRC):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from ciel_geometry.htri_computation_contract import publish_htri_computation
from ciel_omega.htri.htri_local import LocalHTRI


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run LocalHTRI on the verified CUDA backend and publish one "
            "content-addressed computation state. No CPU/numpy fallback is published."
        )
    )
    parser.add_argument("--once", action="store_true", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cpu-steps", type=int, default=64)
    parser.add_argument("--gpu-steps", type=int, default=64)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.cpu_steps < 1 or args.gpu_steps < 1:
        raise SystemExit("HTRI steps must be positive")
    started_at = datetime.now(timezone.utc).isoformat()
    report = LocalHTRI().run(cpu_steps=args.cpu_steps, gpu_steps=args.gpu_steps)
    completed_at = datetime.now(timezone.utc).isoformat()
    state, receipt = publish_htri_computation(
        report,
        output_path=args.output,
        started_at=started_at,
        completed_at=completed_at,
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
