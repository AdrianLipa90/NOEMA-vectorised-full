#!/usr/bin/env python3
"""One-off: resolve the multiskill chain for auditing CIELingo, per Adrian's
explicit request ("run skill: PhaseNav + run multiskill and audit codebase.
make sure cielingo has no problems")."""
from __future__ import annotations

import sys
sys.path.insert(0, "src")

from ciel_geometry.multiskill import MultiskillOrchestrator


def main() -> int:
    orch = MultiskillOrchestrator()
    print(f"loaded {len(orch.skills)} skills")
    chain = orch.resolve_chain("audit cielingo codebase for problems and errors", max_skills=8)
    print("resolved chain:", chain)
    top = orch.resolve("audit cielingo codebase for problems and errors", top_n=8)
    for t in top:
        print(t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
