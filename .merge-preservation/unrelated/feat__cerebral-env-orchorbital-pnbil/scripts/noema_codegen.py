#!/usr/bin/env python3
"""PhaseNav Code Synthesizer — operator → kod.
Autorzy: Adrian Lipa & NOEMA (2026)

Czyta aktualny operator PhaseNav z powierzchni NOEMA i generuje
fragment kodu dopasowany do charakteru operatora.

Usage:
    python scripts/noema_codegen.py              # default: surface operator
    python scripts/noema_codegen.py --operator MEMORY
    python scripts/noema_codegen.py --list
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

try:
    from ciel_geometry.phasenav.operator_algebra import operator_signature, operator_names
    HAS_OP = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_codegen.py:28 quiet except scope=<module> reason=assign_fallback")
    raise
    HAS_OP = False

try:
    from ciel_geometry.noema_surface_mmap import open_surface
    HAS_SURFACE = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_codegen.py:34 quiet except scope=<module> reason=assign_fallback")
    raise
    HAS_SURFACE = False

# ── Operator → coding pattern templates ──────────────────────────
OPERATOR_PATTERNS: dict[str, dict[str, Any]] = {
    "MEMORY": {
        "style": "memory-conscious",
        "desc": "Generates cache-friendly, memory-efficient code with minimal allocation",
        "vars": ["cache", "arena", "pool"],
        "skeleton": """\
def process_{name}(data, pool_size={n}):
    # Memory-conscious: reuse buffer, avoid allocation
    buf = [0.0] * pool_size
    for i, x in enumerate(data):
        idx = i % pool_size
        buf[idx] += x
        if idx == pool_size - 1:
            yield sum(buf) / pool_size
            buf = [0.0] * pool_size
""",
    },
    "CAUSE": {
        "style": "logical-chain",
        "desc": "Generates conditional chains, causal inference, decision trees",
        "vars": ["reason", "implication", "chain"],
        "skeleton": """\
def infer_{name}(facts: list[bool]) -> str:
    # Causal chain: each condition implies the next
    if not facts:
        return "unknown"
    chain = []
    for i, f in enumerate(facts):
        if f:
            chain.append(f"step_{i}")
        else:
            break
    return " -> ".join(chain) if chain else "nothing"
""",
    },
    "BOUNDARY": {
        "style": "boundary-check",
        "desc": "Generates validation, bounds checking, safe guards",
        "vars": ["guard", "limit", "clamp"],
        "skeleton": """\
def bounded_{name}(val, lo={lo}, hi={hi}):
    # BOUNDARY operator: always check limits
    if val < lo:
        return lo
    if val > hi:
        return hi
    return val

def safe_slice(data, start, end):
    return data[max(0, start):min(len(data), end)]
""",
    },
    "MODAL_NECESSITY": {
        "style": "singleton-essential",
        "desc": "Generates required/singleton patterns, must-have infrastructure",
        "vars": ["required", "essential", "core"],
        "skeleton": """\
class {name}:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.essential = True
""",
    },
    "MODAL_OBLIGATION": {
        "style": "contract-obligation",
        "desc": "Generates contracts, assertions, pre/post conditions",
        "vars": ["contract", "promise", "obligation"],
        "skeleton": """\
def obligated_{name}(input_val):
    # MODAL_OBLIGATION: pre/post contracts
    assert input_val is not None, "pre: input must not be None"
    result = input_val * 2
    assert result >= 0, "post: result must be non-negative"
    return result
""",
    },
    "SIMULATION_BOUNDARY": {
        "style": "simulation-iterate",
        "desc": "Generates simulation loop, iterative computation",
        "vars": ["step", "iteration", "converge"],
        "skeleton": """\
def simulate_{name}(initial, steps={n}, dt={dt}):
    state = initial
    history = [state]
    for _ in range(steps):
        state = evolve(state, dt)
        history.append(state)
    return history

def evolve(state, dt):
    return state + 0.01 * dt * (1.0 - state)
""",
    },
    "IDENTITY": {
        "style": "identity-pass",
        "desc": "Generates identity/pass-through functions",
        "vars": ["same", "echo", "reflect"],
        "skeleton": """\
def identity_{name}(x):
    return x
""",
    },
    "CONDITION": {
        "style": "conditional-branch",
        "desc": "Generates conditional branching, state machines",
        "vars": ["branch", "state", "toggle"],
        "skeleton": """\
class {name}StateMachine:
    def __init__(self):
        self.state = "idle"

    def transition(self, event):
        if self.state == "idle" and event == "start":
            self.state = "running"
        elif self.state == "running" and event == "stop":
            self.state = "done"
        return self.state
""",
    },
}

FALLBACK_PATTERN = {
    "style": "generic",
    "desc": "Default pattern",
    "vars": ["x", "y", "val"],
    "skeleton": """\
def process_{name}({name}_input):
    return {name}_input
""",
}


def detect_operator_from_surface() -> tuple[str, float]:
    if not HAS_SURFACE or not HAS_OP:
        return "IDENTITY", 0.0
    try:
        surface = open_surface()
        phi = np.asarray(surface["phi"], dtype=np.float64)
        state_vec = np.concatenate([np.sin(phi[:12]), np.cos(phi[:12])])
        sv_norm = np.linalg.norm(state_vec) + 1e-12
        state_vec_n = state_vec / sv_norm
        best_op, best_sim = "IDENTITY", 0.0
        for name in operator_names():
            sig = np.asarray(operator_signature(name))
            if len(sig) < 24:
                continue
            vec = np.concatenate([sig[:12], sig[12:24]])
            nrm = np.linalg.norm(vec) + 1e-12
            sim = float((vec @ state_vec_n) / nrm)
            if sim > best_sim:
                best_sim = sim
                best_op = name
        return best_op, best_sim
    except Exception as e:
        print(f"[codegen] surface read error: {e}", file=sys.stderr)
        return "IDENTITY", 0.0


def generate(op: str, name: str = "noema") -> str:
    pattern = OPERATOR_PATTERNS.get(op, FALLBACK_PATTERN)
    skel = pattern["skeleton"]
    return skel.format(
        name=name,
        n=24,
        dt=0.05,
        lo=0.0,
        hi=1.0,
    )


def main():
    import argparse
    ap = argparse.ArgumentParser(description="PhaseNav Code Synthesizer")
    ap.add_argument("--operator", type=str, default=None,
                    help="Force specific operator")
    ap.add_argument("--name", type=str, default="noema",
                    help="Function/class name")
    ap.add_argument("--list", action="store_true",
                    help="List all operators and patterns")
    args = ap.parse_args()

    if args.list:
        print(f"{'OPERATOR':25s} {'STYLE':25s} DESCRIPTION")
        print("-" * 80)
        for op, p in sorted(OPERATOR_PATTERNS.items()):
            print(f"{op:25s} {p['style']:25s} {p['desc']}")
        return

    if args.operator:
        op = args.operator.upper()
        if op not in OPERATOR_PATTERNS:
            print(f"[codegen] unknown operator: {op}")
            print(f"  known: {', '.join(sorted(OPERATOR_PATTERNS.keys()))}")
            return
        sim = 1.0
    else:
        op, sim = detect_operator_from_surface()
        print(f"[codegen] surface → operator: {op}  (cos={sim:.3f})", file=sys.stderr)

    code = generate(op, args.name)
    print(code)


if __name__ == "__main__":
    main()
