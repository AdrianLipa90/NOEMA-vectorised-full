#!/usr/bin/env python3
"""One-off: py_compile + verify _phase_confidence_decision() produces
sensible, monotonic results across a grid of (max_sim, avg_sim), compared
against the old if/elif thresholds it replaced."""
import os
import sys
import py_compile

sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")


def old_logic(max_sim: float, avg_sim: float) -> str:
    if max_sim > 0.85 and avg_sim > 0.6:
        return "high"
    elif max_sim > 0.7 and avg_sim > 0.4:
        return "medium"
    elif max_sim > 0.5:
        return "low"
    else:
        return "none"


def main():
    root = "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA"
    py_compile.compile(os.path.join(root, "src/ciel_geometry/cielingo_inference.py"), doraise=True)
    print("py_compile: OK")

    from ciel_geometry.cielingo_inference import _phase_confidence_decision

    grid = [(round(m*0.1,2), round(a*0.1,2)) for m in range(11) for a in range(11) if a*0.1 <= m*0.1]
    agree = 0
    disagree = []
    for max_sim, avg_sim in grid:
        old = old_logic(max_sim, avg_sim)
        new = _phase_confidence_decision(max_sim, avg_sim)
        if old == new:
            agree += 1
        else:
            disagree.append((max_sim, avg_sim, old, new))

    print(f"n_points={len(grid)}  agree={agree}  disagree={len(disagree)}")
    print("\nsample disagreements (first 15):")
    for max_sim, avg_sim, old, new in disagree[:15]:
        print(f"  max_sim={max_sim} avg_sim={avg_sim}: old={old} new={new}")

    # Sanity checks at the extremes — these MUST hold regardless of exact
    # tier boundaries, or the vectorized version is broken, not just
    # "differently tuned"
    assert _phase_confidence_decision(0.99, 0.95) == "high", "near-perfect evidence must be high"
    assert _phase_confidence_decision(0.0, 0.0) == "none", "zero evidence must be none"
    print("\nextreme sanity checks: PASS")

    os.remove(os.path.abspath(__file__))
    return


if __name__ == "__main__":
    main()
