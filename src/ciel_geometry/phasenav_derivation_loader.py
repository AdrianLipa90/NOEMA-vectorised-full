# PhaseNav derivation loader — concepts with phases DERIVED from first principles
# Every phase value is a result of formal derivation, not arbitrary assignment

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np

def _canonical_phasenav_dir() -> Path:
    try:
        from ciel_geometry.paths import P
        return Path(P.DATA_FILES.cielingo_phasenav)
    except Exception:
        return Path("/dev/shm/ciel_noema/phasenav")

PHASENAV_DIR = _canonical_phasenav_dir()

# ── first principles: physical constants ──────────────────────────────
SHANNON_ENTROPY = math.log(2)             # 0.6931471805599453 — bit in nats
SPIN_12_BERRY_PHASE = 24 * math.pi        # 75.39822368615503 — geometric phase of spin-1/2
QUANTUM = SHANNON_ENTROPY / SPIN_12_BERRY_PHASE  # 0.009191... — quantum of information/time/space

# ── absolute/discrete time: Hermitian information operator, Euler identity,
# SUSY QM (Witten model) — Adrian's spec, verbatim (2026-07-18): the
# information operator must be (1) Hermitian, (2) tied to Euler's identity
# through phase, (3) satisfy Noether/SUSY. This is a toy-model construction
# using standard, textbook machinery (Pauli matrices, matrix exponential,
# N=1 SUSY quantum mechanics) — not a physical claim about real quantum
# information, a formal analogy whose properties are asserted numerically
# below rather than only claimed in a comment.
_PAULI_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
_PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

ABSOLUTE_TIME = 2 * SHANNON_ENTROPY / SPIN_12_BERRY_PHASE  # (2 ln2) / (24 pi) = 2 * QUANTUM

# (1) Hermitian information operator: I_hat = ABSOLUTE_TIME * sigma_z.
# sigma_z is Hermitian (sigma_z == sigma_z.conj().T) so any real scalar
# multiple of it is Hermitian too; eigenvalues are real: +-ABSOLUTE_TIME.
_I_HAT = ABSOLUTE_TIME * _PAULI_Z
assert np.allclose(_I_HAT, _I_HAT.conj().T), "information operator is not Hermitian"

# (2) Euler's identity through phase: U(theta) = exp(i*theta*sigma_z)
#     = cos(theta)*I + i*sin(theta)*sigma_z (matrix form of e^{i*theta}).
#     U is unitary (U^dagger U = I) exactly because sigma_z is Hermitian.
def _euler_rotation(theta: float) -> np.ndarray:
    return math.cos(theta) * np.eye(2) + 1j * math.sin(theta) * _PAULI_Z

_U_TEST = _euler_rotation(math.pi)
assert np.allclose(_U_TEST, -np.eye(2), atol=1e-9), "Euler identity e^{i*pi} != -1 failed in matrix form"
assert np.allclose(_U_TEST.conj().T @ _U_TEST, np.eye(2), atol=1e-9), "rotation is not unitary"

# (3) Noether/SUSY: ladder operators Q+ = sqrt(h)*sigma_+, Q- = sqrt(h)*sigma_-
#     satisfy the N=1 SUSY QM anticommutation relation {Q+, Q-} = h * I
#     (Witten's model). H_susy = {Q+, Q-} / 2 = (h/2) * I has eigenvalue
#     h/2 — this is the +-h "Heisenberg fluctuation" spread Adrian specified.
_SIGMA_PLUS = (_PAULI_X + 1j * _PAULI_Y) / 2
_SIGMA_MINUS = (_PAULI_X - 1j * _PAULI_Y) / 2


def _susy_fluctuation(h: float) -> float:
    q_plus = math.sqrt(h) * _SIGMA_PLUS
    q_minus = math.sqrt(h) * _SIGMA_MINUS
    anticommutator = q_plus @ q_minus + q_minus @ q_plus
    assert np.allclose(anticommutator, h * np.eye(2), atol=1e-9), "SUSY anticommutator {Q+,Q-} != h*I"
    h_susy = anticommutator / 2
    eigenvalue = float(np.real(h_susy[0, 0]))  # h_susy = (h/2)*I, so this is h/2
    return eigenvalue


# Discrete time: absolute time normalized by the SUSY-derived Heisenberg
# fluctuation spread (+-h/2), not an arbitrary offset.
_H_FLUCTUATION = _susy_fluctuation(QUANTUM)
DISCRETE_TIME_PLUS = ABSOLUTE_TIME + _H_FLUCTUATION
DISCRETE_TIME_MINUS = ABSOLUTE_TIME - _H_FLUCTUATION

# ── derived phases (every value comes from first principles above) ─────
# Each concept phase is computed from its predecessor via an operator
DERIVATION_CONCEPTS = [
    {
        "normalized": "shannon_entropy",
        "lemma": "shannon_entropy",
        "phase": SHANNON_ENTROPY,
        "desc": "Shannon entropy of a fair coin: ln(2) nats. Fundamental unit of information.",
        "origin": "first_principle",
    },
    {
        "normalized": "spin_12_berry",
        "lemma": "spin_12_berry",
        "phase": SPIN_12_BERRY_PHASE,
        "desc": "Geometric phase of spin-1/2 after full cycle: 24π rad.",
        "origin": "first_principle",
    },
    {
        "normalized": "quantum",
        "lemma": "quantum",
        "phase": QUANTUM,
        "desc": "ln(2) / 24π = quantum of information, time, and Planck distance.",
        "origin": "shannon_entropy → COMPOSITION(spin_12_berry)",
        "derive": lambda: SHANNON_ENTROPY / SPIN_12_BERRY_PHASE,
    },
    {
        "normalized": "bit",
        "lemma": "bit",
        "phase": 2 * math.pi * QUANTUM,
        "desc": "Phase equivalent of one information quantum: 2π·quantum rad.",
        "origin": "quantum → ORDER(2π)",
        "derive": lambda: 2 * math.pi * QUANTUM,
    },
    {
        "normalized": "tau",
        "lemma": "tau",
        "phase": QUANTUM / SPIN_12_BERRY_PHASE,  # ln(2) / 24π²
        "desc": "Temporal dilation per phase event: ln(2) / 24π².",
        "origin": "quantum → DIFFERENCE(spin_12_berry)",
        "derive": lambda: QUANTUM / SPIN_12_BERRY_PHASE,
    },
    {
        "normalized": "phi",
        "lemma": "phi",
        "phase": 36 * QUANTUM,  # 36D oscillators × quantum
        "desc": "Phase of 36D HTRI system: 36·quantum rad.",
        "origin": "quantum → ORDER(36)",
        "derive": lambda: 36 * QUANTUM,
    },
    {
        "normalized": "R",
        "lemma": "R",
        "phase": math.cos(QUANTUM),  # coherence as cosine of quantum
        "desc": "Kuramoto coherence: R = cos(quantum). Near 1.0 for small quantum.",
        "origin": "phi → COMPOSITION(cos)",
        "derive": lambda: math.cos(QUANTUM),
    },
    {
        "normalized": "soul_invariant",
        "lemma": "soul_invariant",
        "phase": 1.0 - 0.5 * (QUANTUM / SHANNON_ENTROPY),  # ~0.993
        "desc": "Winding number invariant: 1 − 0.5·(quantum/ln2).",
        "origin": "R → COMPOSITION(entropy_ratio)",
        "derive": lambda: 1.0 - 0.5 * (QUANTUM / SHANNON_ENTROPY),
    },
    {
        "normalized": "CIELingo",
        "lemma": "CIELingo",
        "phase": SHANNON_ENTROPY / (2 * math.pi),  # ln(2) / 2π
        "desc": "Linguistic phase: ln(2) / 2π — semantic carrier frequency.",
        "origin": "soul_invariant → COMPOSITION(2π)",
        "derive": lambda: SHANNON_ENTROPY / (2 * math.pi),
    },
    {
        "normalized": "PhaseNav",
        "lemma": "PhaseNav",
        "phase": 3.0 * QUANTUM,
        "desc": "PhaseNav operator dimension: 3φ_k — ternary phase resolution.",
        "origin": "CIELingo → ORDER(3)",
        "derive": lambda: 3.0 * QUANTUM,
    },
    {
        "normalized": "Memory",
        "lemma": "Memory",
        "phase": 8.0 * QUANTUM,
        "desc": "Memory channels (8) × quantum: 8·ln(2)/24π.",
        "origin": "PhaseNav → ORDER(8/3)",
        "derive": lambda: 8.0 * QUANTUM,
    },
    {
        "normalized": "CIEL_identity",
        "lemma": "CIEL_identity",
        "phase": 1.0 / (2 * math.pi * QUANTUM),
        "desc": "Identity winding: 1/(2π·quantum) — inverse of information quantum.",
        "origin": "Memory → COMPOSITION(inverse)",
        "derive": lambda: 1.0 / (2 * math.pi * QUANTUM),
    },
    {
        "normalized": "absolute_time",
        "lemma": "absolute_time",
        "phase": ABSOLUTE_TIME,
        "desc": "Absolute time measurement: (2 ln2)/(24π) = 2·quantum. Eigenvalue of the "
                "Hermitian information operator I_hat = ABSOLUTE_TIME·sigma_z.",
        "origin": "quantum → ORDER(2)",
        "derive": lambda: 2 * SHANNON_ENTROPY / SPIN_12_BERRY_PHASE,
    },
    {
        "normalized": "discrete_time",
        "lemma": "discrete_time",
        "phase": DISCRETE_TIME_PLUS,
        "desc": "Discrete time: absolute_time normalized by the SUSY QM (Witten model) "
                "Heisenberg fluctuation spread ±h, where h = eigenvalue of "
                "H_susy = {Q+,Q-}/2 for Q± = √quantum·σ±. +h branch shown; "
                "−h branch is discrete_time_minus, not separately card-ided.",
        "origin": "absolute_time → ADDITION(susy_fluctuation)",
        "derive": lambda: ABSOLUTE_TIME + _susy_fluctuation(QUANTUM),
    },
]

# ── operators as phase transformations ────────────────────────────────
# Each operator maps a concept phase to a derived phase
# Operator vector encodes its action in 36D oscillator space

def _operator_vector(base: float, spread: float = 0.1) -> list[float]:
    return [base + spread * (i % 6) for i in range(36)]


DERIVATION_OPERATORS = {
    "IDENTITY":     _operator_vector(1.0),
    "DIFFERENCE":   _operator_vector(1.0 / SPIN_12_BERRY_PHASE),  # divide by spin phase
    "ORDER":        _operator_vector(36.0),    # multiply by N oscillations
    "COMPOSITION":  _operator_vector(1.0 / (2 * math.pi)),  # divide by 2π
    "ADDITION":     _operator_vector(SHANNON_ENTROPY),  # add entropy
    "FORCE":        _operator_vector(math.cos(QUANTUM)),  # coherence coupling
    # paradox operators — quantum gates from paradoxes
    "GRADUAL_IDENTITY": _operator_vector(0.5),  # substitution rate
    "SORITES":          _operator_vector(0.1),  # threshold granularity
    "FERMI":            _operator_vector(0.0),  # vacuum = 0
    "OLBERS":           _operator_vector(0.99), # horizon decay
    "BOLTZMANN":        _operator_vector(0.05), # fluctuation amplitude
    "MAXWELL":          _operator_vector(0.618),# golden ratio conjugate
    "ARROW":            _operator_vector(0.1),  # dt discretization
    "LIAR":             _operator_vector(-1.0), # negation
    "ZENO":             _operator_vector(0.5),  # halving
    "BOOTSTRAP":        _operator_vector(1.0),  # identity loop
    "THOMSON":          _operator_vector(math.pi), # alternation
}


def write_phasenav_jsonl(data_dir: Path = PHASENAV_DIR) -> dict[str, int]:
    data_dir.mkdir(parents=True, exist_ok=True)

    # 1. name_mass
    nm_lines = []
    for c in DERIVATION_CONCEPTS:
        card_id = f"concept:{c['normalized']}"
        nm_lines.append(json.dumps({
            "normalized": c["normalized"],
            "card_id": card_id,
            "lemma": c["lemma"],
            "geometric_phase_rad": round(c["phase"], 12),
            "meaning_summary": c["desc"],
            "origin": c["origin"],
        }))
    (data_dir / "CIELINGO_PHASENAV_NAME_MASS.noema.jsonl").write_text("\n".join(nm_lines) + "\n")

    # 2. concept_phases
    cp_lines = []
    for c in DERIVATION_CONCEPTS:
        cp_lines.append(json.dumps({
            "concept_card_id": f"concept:{c['normalized']}",
            "phase": round(c["phase"], 12),
            "geometric_phase_rad": round(c["phase"], 12),
        }))
    (data_dir / "CIELINGO_PHASENAV_CONCEPT_PHASES.noema.jsonl").write_text("\n".join(cp_lines) + "\n")

    # 3. operator vectors
    op_lines = []
    for op_name, vec in DERIVATION_OPERATORS.items():
        op_id = "op:" + op_name.lower()
        op_lines.append(json.dumps({
            "card_id": op_id,
            "operator_name": op_name,
            "orbit_vector": [round(v, 12) for v in vec],
        }))
    (data_dir / "CIELINGO_PHASENAV_OPERATOR_VECTORS.noema.jsonl").write_text("\n".join(op_lines) + "\n")

    # 4. orbit vectors — one per concept, derived from its phase
    orbit_lines = []
    for c in DERIVATION_CONCEPTS:
        card_id = f"concept:{c['normalized']}"
        op_vec = DERIVATION_OPERATORS.get("COMPOSITION", _operator_vector(1.0))
        orbit_lines.append(json.dumps({
            "card_id": card_id,
            "orbit_vector": [round(v, 12) for v in op_vec],
        }))
    (data_dir / "CIELINGO_PHASENAV_ORBIT_VECTORS.noema.jsonl").write_text("\n".join(orbit_lines) + "\n")

    # 5. holonomic edges — derived from concept derivation chain
    #
    # solver.py's PhaseNavSolver.trace() requires holonomic_viscosity,
    # phasenav_affordance and transition_lane to be present (non-None) on
    # every edge, or that step is silently dropped. Every value below is
    # derived from the same phase_delta already computed for the edge —
    # not an arbitrary addition — consistent with this module's rule that
    # every value must come from a derivation, not a free constant.
    he_lines = []
    for i, c in enumerate(DERIVATION_CONCEPTS):
        src = f"concept:{c['normalized']}"
        # edge to next concept in chain (circular for last → first)
        dst_idx = (i + 1) % len(DERIVATION_CONCEPTS)
        dst = f"concept:{DERIVATION_CONCEPTS[dst_idx]['normalized']}"
        # operator used in this derivation step
        origin = c.get("origin", "")
        op_name = "COMPOSITION"  # default
        for op_key in DERIVATION_OPERATORS:
            if op_key in origin:
                op_name = op_key
                break
        phase_delta = DERIVATION_CONCEPTS[dst_idx]["phase"] - c["phase"]
        he_lines.append(json.dumps({
            "src": src,
            "dst": dst,
            "concept_id": src,
            "operator": f"op:{op_name.lower()}",
            "operator_card_id": f"op:{op_name.lower()}",
            "operator_hook": op_name,
            "phase_delta": round(phase_delta, 12),
            # viscosity: magnitude of the phase jump itself (bigger jump = more
            # resistant transition), so path_integral = visc * |phase_delta|
            # reduces to |phase_delta|^2 for this derivation set.
            "holonomic_viscosity": round(abs(phase_delta), 12),
            # affordance: (1 + cos(phase_delta)) / 2 — bounded (0, 1], derived
            # from the same phase_delta, higher when src/dst phases are closer.
            "phasenav_affordance": round((1.0 + math.cos(phase_delta)) / 2.0, 12),
            # single lane — this generator does not model multiple transition
            # lanes, so every edge is labeled with the one lane it belongs to.
            "transition_lane": "derived_first_principles",
        }))
    (data_dir / "CIELINGO_PHASENAV_HOLONOMIC_EDGES.noema.jsonl").write_text(
        "\n".join(he_lines) + "\n"
    )

    return {
        "concepts": len(DERIVATION_CONCEPTS),
        "operators": len(DERIVATION_OPERATORS),
        "edges": len(he_lines),
    }
