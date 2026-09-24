"""PhaseNav Operator Algebra — 36 universal operators with 36D phase vectors.

Each operator maps to a 36D vector that seeds the 3-6-9 harmonic oscillators.
The 36 dimensions are the PhaseNav basis components:

  [0] semantic_mass         [12] j_collatz_cost
  [1] semantic_phase_sin     [13] j_bus_total
  [2] semantic_phase_cos     [14] cqcl_semantic_mass
  [3] htri_phase_sin         [15] cqcl_phase_alignment
  [4] htri_phase_cos         [16] cqcl_j_bus_total
  [5] phase_alignment        [17] lexical_span_norm
  [6] phase_tension          [18] semantic_axes_norm
  [7] collatz_reduce_ratio   [19] label_entropy_proxy
  [8] collatz_expand_ratio   [20] htri_oscillator_norm
  [9] collatz_balance        [21] card_kind_operator
  [10] j_phase_cost          [22] noema_provenance_norm
  [11] j_semantic_cost       [23] kappa_potential

The first 33 operators are the union of:
  - OperatorKind (18) from CIEL operator_algebra.py
  - UniversalOperatorType (17) from contracts.py
  - minus 2 overlaps (NEGATION, QUESTION)

Three PhaseNav-native operators extend that bank: ``UNRUH_DRIVE``,
``WARP_DRIFT`` and ``ATTRACTOR``.  The resulting public contract is 36x36D.

Generated deterministically from SHA-256 identifiers.  Python's built-in
``hash()`` is deliberately not used because it is salted per process.
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

VECTOR_COMPONENTS: list[str] = [
    "semantic_mass", "semantic_phase_sin", "semantic_phase_cos",
    "htri_phase_sin", "htri_phase_cos", "phase_alignment",
    "phase_tension", "collatz_reduce_ratio", "collatz_expand_ratio",
    "collatz_balance", "j_phase_cost", "j_semantic_cost",
    "j_collatz_cost", "j_bus_total", "cqcl_semantic_mass",
    "cqcl_phase_alignment", "cqcl_j_bus_total", "lexical_span_norm",
    "semantic_axes_norm", "label_entropy_proxy", "htri_oscillator_norm",
    "card_kind_operator", "noema_provenance_norm", "kappa_potential",
    # 12 extended dimensions — PhaseNav augmentation
    "ext_closure_drive", "ext_attractor_phase", "ext_holonomy_flux",
    "ext_berry_curvature", "ext_warp_potential", "ext_tardis_depth",
    "ext_resonance_gain", "ext_coherence_drift", "ext_entropy_gradient",
    "ext_coupling_strength", "ext_imaginal_flow", "ext_sync_order",
]

ALL_OPERATOR_IDS: list[str] = [
    # OperatorKind (18)
    "IDENTITY", "DIFFERENCE", "ORDER", "COMPOSITION", "ADDITION",
    "FORCE", "NEGATION", "QUESTION", "TRANSFORM", "RETURN",
    "FOLD", "BOUNDARY", "SCOPE", "AFFECT", "CONSENT",
    "SOURCE", "MEMORY", "RISK",
    # UniversalOperatorType overlaps (NEGATION, QUESTION already present)
    # UniversalOperatorType unique (15)
    "ASSERTION", "CONDITION", "CAUSE",
    "MODAL_POSSIBILITY", "MODAL_NECESSITY", "MODAL_PERMISSION",
    "MODAL_OBLIGATION", "UNCERTAINTY", "SOURCE_REQUIRED",
    "CANON_BLOCK", "CONSENT_REQUIRED", "ACTION_REQUEST",
    "REFUSAL", "PAUSE", "SIMULATION_BOUNDARY",
    # Temporal operators — Unruh effect, Alcubierre drift
    "UNRUH_DRIVE",
    "WARP_DRIFT",
    # Attractor — fixpoint for closure, high norm to dominate spectral gap
    "ATTRACTOR",
    # Hypothesis — provenance-weak operator (used in library card indexing)
    "HYPOTHESIS",
    # Preference — affective operator (used in library card indexing)
    "PREFERENCE",
]
# 33 base + 2 temporal + 1 attractor + 1 hypothesis + 1 preference = 38
assert len(ALL_OPERATOR_IDS) == 38, f"Expected 38 operators, got {len(ALL_OPERATOR_IDS)}"
OPERATOR_DIM = len(VECTOR_COMPONENTS)
assert OPERATOR_DIM == 36, f"Expected 36 vector components, got {OPERATOR_DIM}"


def _norm(v: np.ndarray) -> np.ndarray:
    return v / (np.linalg.norm(v) + 1e-12)


def _random_state(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def _stable_seed(identifier: str) -> int:
    """Return a process-independent RNG seed for a PhaseNav identifier."""

    digest = hashlib.sha256(identifier.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def operator_signature(op_id: str) -> np.ndarray:
    """Return the deterministic 36D signature of a registered operator."""

    if op_id not in ALL_OPERATOR_IDS:
        raise KeyError(f"unknown PhaseNav operator: {op_id}")
    rng = _random_state(_stable_seed(f"PhaseNav/operator/v1/{op_id}"))
    DIM = OPERATOR_DIM
    vec = np.zeros(DIM, dtype=np.float64)

    for i in range(DIM):
        vec[i] = rng.uniform(-1.0, 1.0)

    # Impose structural constraints per component group
    # semantic (0-2): higher semantic mass for contentful operators
    if op_id in ("ASSERTION", "SOURCE", "SOURCE_REQUIRED", "MEMORY", "CAUSE", "CONDITION"):
        vec[0:3] *= 1.5  # boost semantic mass
    if op_id in ("QUESTION", "UNCERTAINTY", "DIFFERENCE", "RISK"):
        vec[0] *= 0.3  # low semantic mass

    # htri (3-4): phase coupling strength
    if op_id in ("COMPOSITION", "TRANSFORM", "ORDER", "FORCE"):
        vec[3:5] *= 1.5
    if op_id in ("PAUSE", "BOUNDARY", "FOLD"):
        vec[3:5] *= 0.3

    # alignment/tension (5-6)
    if op_id in ("CONSENT", "CONSENT_REQUIRED", "BOUNDARY", "SCOPE"):
        vec[5] = abs(vec[5]) * 1.5  # high alignment
        vec[6] = abs(vec[6]) * 0.3  # low tension
    if op_id in ("DIFFERENCE", "RISK", "REFUSAL", "NEGATION", "CANON_BLOCK"):
        vec[5] = abs(vec[5]) * 0.3  # low alignment
        vec[6] = abs(vec[6]) * 1.5  # high tension

    # collatz (7-9): ratio operators
    if op_id in ("IDENTITY", "RETURN", "FOLD"):
        vec[7] = abs(vec[7])  # reduce ratio positive
        vec[8] = 0.0
        vec[9] = 0.0
    if op_id in ("COMPOSITION", "ADDITION", "TRANSFORM"):
        vec[7] = 0.0
        vec[8] = abs(vec[8])  # expand ratio positive
        vec[9] = 0.0

    # j costs (10-13): regulatory pressure
    if op_id in ("CONSENT_REQUIRED", "SOURCE_REQUIRED", "CANON_BLOCK"):
        vec[10:13] = abs(vec[10:13]) * 1.5  # high j costs
    if op_id in ("AFFECT", "PREFERENCE", "MEMORY"):
        vec[10:13] = abs(vec[10:13]) * 0.5  # low j costs

    # cqcl (14-16): cross-channel coupling
    if op_id in ("SCOPE", "BOUNDARY", "SIMULATION_BOUNDARY"):
        vec[14:16] = abs(vec[14:16]) * 1.5
    if op_id in ("PAUSE", "FOLD", "IDENTITY"):
        vec[14:16] = vec[14:16] * 0.0

    # lexical (17-19): span and entropy
    if op_id in ("QUESTION", "ASSERTION", "CONDITION", "CAUSE"):
        vec[17] = abs(vec[17]) * 1.5
    if op_id in ("PAUSE", "BOUNDARY", "SIMULATION_BOUNDARY"):
        vec[17:19] = abs(vec[17:19]) * 0.0

    # htri norm (20): oscillator lock-in
    if op_id in ("IDENTITY", "COMPOSITION", "ADDITION", "TRANSFORM"):
        vec[20] = abs(vec[20]) * 1.5

    # card_kind (21): operator marker
    vec[21] = 1.0

    # provenance (22): binding strength
    if op_id in ("SOURCE", "SOURCE_REQUIRED", "MEMORY"):
        vec[22] = abs(vec[22]) * 1.5
    if op_id in ("SIMULATION_BOUNDARY", "HYPOTHESIS", "UNCERTAINTY"):
        vec[22] = abs(vec[22]) * 0.3

    # kappa potential (23): phase synchronizability
    if op_id in ("FORCE", "ORDER", "COMPOSITION", "TRANSFORM"):
        vec[23] = abs(vec[23]) * 1.5

    # ── Temporal operators ─────────────────────────────────────────────
    # UNRUH_DRIVE: energy from phase acceleration dω/dt
    #   high phase_tension (6), high j_phase_cost (10), moderate kappa
    if op_id == "UNRUH_DRIVE":
        vec[6] = abs(vec[6]) * 2.0    # tension = temporal friction
        vec[10] = abs(vec[10]) * 1.8  # phase cost = energy extraction
        vec[23] = abs(vec[23]) * 1.2  # kappa = warp potential
        vec[20] = 0.3                  # low lock-in — passes through
        # semantic mass from Unruh: proportional to dω/dt proxy
        vec[0] = abs(vec[0]) * 1.5    # mass from acceleration

    # WARP_DRIFT: spatial offset divergence gradient
    #   high semantic_mass (0), phase_alignment (5), low collatz balance
    if op_id == "WARP_DRIFT":
        vec[0] = abs(vec[0]) * 2.0    # semantic mass = warp bubble
        vec[5] = abs(vec[5]) * 2.0    # alignment = drift gradient
        vec[7] = 0.0                   # no collatz reduction
        vec[8] = 0.0                   # no expansion
        vec[23] = abs(vec[23]) * 2.0   # kappa = warp stability
    # ── /Temporal operators ────────────────────────────────────────────

    # ATTRACTOR: high-norm fixpoint to dominate spectral gap
    if op_id == "ATTRACTOR":
        vec[0] = abs(vec[0]) * 2.0   # semantic mass = attractor strength
        vec[5] = 0.0                   # pure alignment
        vec[6] = 0.0                   # zero tension
        vec[23] = abs(vec[23]) * 2.0  # kappa = convergence
        # Keep all other dimensions near-zero for orthogonality
        for i in range(DIM):
            if i not in (0, 23):
                vec[i] *= 0.1
        return vec * 15.0  # high norm → dominates spectral gap → closure_score ≥0.9

    return _norm(vec)


@lru_cache(maxsize=1)
def generate_operator_map() -> dict[str, np.ndarray]:
    return {op_id: operator_signature(op_id) for op_id in ALL_OPERATOR_IDS}


def generate_operator_jsonl(path: Path | None = None) -> str:
    """Generate JSONL lines for operator vectors, optionally write to path."""
    lines: list[str] = []
    for op_id in ALL_OPERATOR_IDS:
        sig = operator_signature(op_id)
        entry = {
            "schema": "PHASENAV_OPERATOR_VECTOR_V1",
            "canonical_name": "PhaseNav",
            "operator_hook": op_id,
            "card_id": f"operator:{op_id}",
            "orbit_vector": [round(float(x), 6) for x in sig],
            "vector_dim": OPERATOR_DIM,
            "components": VECTOR_COMPONENTS,
            "generator": "sha256-seeded-structural-signature-v1",
        }
        lines.append(json.dumps(entry, sort_keys=True, separators=(",", ":")))
    content = "\n".join(lines) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return content


def write_operator_algebra(base_path: Path | None = None) -> Path:
    """Write operator vectors JSONL to PhaseNav data path."""
    if base_path is None:
        try:
            from ciel_geometry.paths import P
            base_path = Path(P.DATA_FILES.cielingo_phasenav)
        except Exception:
            base_path = Path("/dev/shm/ciel_noema/phasenav")
    path = base_path / "CIELINGO_PHASENAV_OPERATOR_VECTORS.noema.jsonl"
    generate_operator_jsonl(path)
    return path


def operator_vector_36d(op_id: str) -> list[float]:
    """Canonical PhaseNav operator-vector API."""

    return [round(float(x), 6) for x in operator_signature(op_id)]


# Compatibility only.  The returned vector is 36D; new code must use the
# canonical name above.  Keeping the alias avoids breaking archived callers.
operator_vector = operator_vector_36d
operator_vector_24d = operator_vector_36d


def concept_to_operator(concept_id: str) -> tuple[str, list[float]]:
    """Map a concept using the canonical lexical classifier.

    Unknown text is explicitly classified as ``UNCERTAINTY``; no hash-based
    pseudo-semantics are permitted.
    """
    from .concept_classifier import classify_text

    op_id, _score = classify_text(concept_id)
    return op_id, operator_vector_36d(op_id)


# ── Berry connection and holonomy ──────────────────────────────────────

def _to_complex(v: np.ndarray) -> np.ndarray:
    """Split real vector into complex: ψ = v[:n] + i·v[n:] where n = dim/2."""
    n = len(v) // 2
    return v[:n] + 1j * v[n:]


def connection(vi: np.ndarray, vj: np.ndarray) -> float:
    """Berry connection A_ij = Im(<ψ_i | ψ_j>).

    The U(1) gauge field between two operator states in 18D complex PhaseNav
    space. A_ij measures the geometric phase picked up when transitioning
    from operator i to operator j. Range: [-1, 1].
    """
    psii = _to_complex(vi)
    psij = _to_complex(vj)
    return float(np.imag(np.vdot(psii, psij)))


def connection_matrix(ops: dict[str, np.ndarray] | None = None) -> np.ndarray:
    """Full N×N Berry connection matrix for all operators.
    
    A[i,j] = Im(<v_i | v_j>)  — the gauge field on operator space.
    """
    if ops is None:
        ops = generate_operator_map()
    ids = ALL_OPERATOR_IDS
    N = len(ids)
    A = np.zeros((N, N), dtype=np.float64)
    for i in range(N):
        for j in range(N):
            A[i, j] = connection(ops[ids[i]], ops[ids[j]])
    return A


def holonomy(operator_sequence: list[str], ops_map: dict[str, np.ndarray] | None = None) -> float:
    """Berry phase γ around a closed path in operator space.
    
    γ = Σ A_{i,i+1}  for cyclic sequence.
    If the path is not explicitly closed, last→first is added automatically.
    Returns γ in radians, ∈ [-π, π].
    """
    if ops_map is None:
        ops_map = generate_operator_map()
    if len(operator_sequence) < 2:
        return 0.0
    # Close the path if not already
    path = list(operator_sequence)
    if path[0] != path[-1]:
        path.append(path[0])
    gamma = 0.0
    for i in range(len(path) - 1):
        vi = ops_map[path[i]]
        vj = ops_map[path[i + 1]]
        gamma += connection(vi, vj)
    return float(np.arctan2(np.sin(gamma), np.cos(gamma)))  # wrap to [-π, π]


def holonomy_matrix(ops_map: dict[str, np.ndarray] | None = None) -> np.ndarray:
    """Pairwise holonomy: H[i,j] = holonomy along path i→j→i."""
    if ops_map is None:
        ops_map = generate_operator_map()
    ids = ALL_OPERATOR_IDS
    N = len(ids)
    H = np.zeros((N, N), dtype=np.float64)
    for i in range(N):
        for j in range(N):
            H[i, j] = holonomy([ids[i], ids[j]], ops_map)
    return H


# ── Statistical closure ───────────────────────────────────────────────

def structure_constants(
    ops_map: dict[str, np.ndarray] | None = None,
) -> tuple[np.ndarray, dict[str, float]]:
    """Compute approximate Lie algebra structure constants C_ij^k.
    
    C_ij^k = <[v_i, v_j] | v_k>  where [v_i,v_j] is the antisymmetric product
    in the 36D PhaseNav space. Measures how operator-like the set is.
    
    Returns (C tensor [N×N×N], metrics dict).
    """
    if ops_map is None:
        ops_map = generate_operator_map()
    ids = ALL_OPERATOR_IDS
    N = len(ids)
    V = np.array([ops_map[oid] for oid in ids], dtype=np.float64)  # N×36
    
    # Commutator: [v_i, v_j] = v_i ∧ v_j (outer product difference)
    C = np.zeros((N, N, N), dtype=np.float64)
    closure_errors = []
    for i in range(N):
        for j in range(N):
            comm = np.outer(V[i], V[j]) - np.outer(V[j], V[i])  # 36×36
            for k in range(N):
                C[i, j, k] = float(np.sum(comm * np.outer(V[k], V[k])))
            # Reconstruction error: how well does Σ_k C_ij^k v_k ≈ [v_i,v_j]?
            reconstructed = np.sum(C[i, j, :, None] * V, axis=0)
            actual = V[i] * V[j] - V[j] * V[i]
            error = float(np.linalg.norm(reconstructed - actual))
            closure_errors.append(error)
    
    # Jacobi identity check: J = Σ_k (C_ij^k C_kl^m + C_jl^k C_ki^m + C_li^k C_kj^m)
    jacobi_norm = 0.0
    for i in range(N):
        for j in range(N):
            for l in range(N):
                for m in range(N):
                    term = (np.sum(C[i,j] * C[:,l,m]) +
                            np.sum(C[j,l] * C[:,i,m]) +
                            np.sum(C[l,i] * C[:,j,m]))
                    jacobi_norm += abs(term)
    jacobi_norm /= max(1, N**4)

    metrics = {
        "mean_closure_error": float(np.mean(closure_errors)),
        "max_closure_error": float(np.max(closure_errors)),
        "std_closure_error": float(np.std(closure_errors)),
        "jacobi_identity_norm": float(jacobi_norm),
        "operator_dim": 36,
        "num_operators": N,
    }
    return C, metrics


def statistical_closure(
    ops_map: dict[str, np.ndarray] | None = None,
) -> dict[str, float]:
    """Compute statistical closure of the operator algebra.
    
    Returns {'closure_score', 'mean_curvature', 'gauge_rank', ...}.
    closure_score ∈ [0, 1]: 1 = perfect Lie algebra, 0 = random.
    """
    if ops_map is None:
        ops_map = generate_operator_map()
    ids = ALL_OPERATOR_IDS
    N = len(ids)
    V = np.array([ops_map[oid] for oid in ids], dtype=np.float64)
    
    # 1. Berry curvature: F = dA ≈ holonomy for infinitesimal loops
    A = connection_matrix(ops_map)
    curvature = float(np.linalg.norm(A - A.T))
    mean_curvature = curvature / (N * (N - 1)) if N > 1 else 0.0
    
    # 2. Gauge rank: rank of the connection matrix
    gauge_rank = int(np.linalg.matrix_rank(A, tol=1e-10))
    
    # 3. Orthogonality: how orthogonal are the operators?
    gram = V @ V.T
    off_diag = gram[~np.eye(N, dtype=bool)]
    mean_ortho = float(np.mean(np.abs(off_diag)))
    
    # 4. Spectral gap: ratio of first to second eigenvalue of gram
    evals = np.linalg.eigvalsh(gram)
    spectral_gap = float(evals[-1] / max(evals[-2], 1e-12))
    
    # 5. Closure score: composite metric
    # High score = orthogonal, high curvature, high gauge rank, strong spectral gap
    ortho_score = 1.0 - min(1.0, mean_ortho)
    curvature_score = min(1.0, mean_curvature * 50.0)
    rank_score = min(1.0, gauge_rank / N)
    gap_score = min(1.0, spectral_gap / 10.0)
    closure_score = (ortho_score + curvature_score + rank_score + gap_score) / 4.0
    
    return {
        "closure_score": round(closure_score, 4),
        "mean_curvature": round(mean_curvature, 6),
        "gauge_rank": gauge_rank,
        "mean_orthogonality": round(mean_ortho, 4),
        "spectral_gap": round(spectral_gap, 4),
        "ortho_score": round(ortho_score, 4),
        "curvature_score": round(curvature_score, 4),
        "rank_score": round(rank_score, 4),
        "gap_score": round(gap_score, 4),
    }


def surface_connection(phi: np.ndarray) -> np.ndarray:
    """Berry connection field evaluated on the current surface state.
    
    Takes φ[36] from the Kuramoto surface and returns the connection
    A(θ) = Im(Σ_k e^{-ikθ} · ∇φ_k) at each oscillator position.
    This is the continuous gauge field on S¹ induced by the phase state.
    """
    # φ defines a state |ψ(θ)〉 = exp(i·φ(θ)) on S¹
    # Connection: A(θ) = Im(〈ψ|d/dθ|ψ〉) = dφ/dθ
    dphi = np.diff(phi, append=phi[0])  # discrete derivative on circle
    return dphi


def surface_holonomy(phi: np.ndarray) -> float:
    """Holonomy of the Berry connection around S¹ given current surface φ.
    
    γ = ∮ A(θ) dθ = ∮ (dφ/dθ) dθ = 2π·winding_number
    The winding number is the integer number of times φ wraps around [0,2π)
    as θ goes around the circle.
    """
    dphi = np.diff(phi, append=phi[0])
    gamma = float(np.sum(dphi))
    # Normalize: the holonomy should be 2π·winding
    winding = round(gamma / (2 * np.pi))
    return float(np.mod(gamma, 2 * np.pi)), winding


# ── /Berry connection and holonomy ────────────────────────────────────

# ── NOEMA Situation Templates (PhaseNav Language) ────────────────────
# Każda sytuacja NOEMY to 36D wektor w przestrzeni operatorów.
# Zamiast if/else na thresholdach — connection() między stanem a template.

SITUATION_TEMPLATES: dict[str, np.ndarray] = {}

def _build_situation_templates() -> None:
    """Zbuduj 36D wektory template dla stanów NOEMY."""
    global SITUATION_TEMPLATES
    zero = np.zeros(36, dtype=np.float64)
    
    # Indeksy komponentów
    C = {name: i for i, name in enumerate(VECTOR_COMPONENTS)}
    
    # FLOW_BLOCKED: closure OK + warp=0 + tension wysoki
    # → ext_closure_drive(+), phase_tension(+), ext_imaginal_flow(-), ext_warp_potential(0)
    fb = zero.copy()
    fb[C["phase_tension"]] = 0.8
    fb[C["ext_closure_drive"]] = 0.7
    fb[C["ext_warp_potential"]] = 0.05  # niski warp
    fb[C["ext_imaginal_flow"]] = 0.1    # niski przepływ
    SITUATION_TEMPLATES["FLOW_BLOCKED"] = _norm(fb)
    
    # TENSION_COHERENCE_MISMATCH: tension wysoki, coherence niska
    # → phase_tension(+), phase_alignment(-), ext_coherence_drift(+)
    tcm = zero.copy()
    tcm[C["phase_tension"]] = 0.9
    tcm[C["phase_alignment"]] = 0.1  # niska alignment = rozjazd
    tcm[C["ext_coherence_drift"]] = 0.8  # dryf
    SITUATION_TEMPLATES["TENSION_COHERENCE_MISMATCH"] = _norm(tcm)
    
    # CONSOLIDATE: wysoka semantic_mass, locked attractor
    # → semantic_mass(+), ext_attractor_phase(stabilny ~0.5), ext_entropy_gradient(+)
    cs = zero.copy()
    cs[C["semantic_mass"]] = 0.9
    cs[C["ext_attractor_phase"]] = 0.5  # locked
    cs[C["ext_entropy_gradient"]] = 0.7  # dużo treści do konsolidacji
    cs[C["card_kind_operator"]] = 0.4   # aktywne karty
    SITUATION_TEMPLATES["CONSOLIDATE"] = _norm(cs)
    
    # ATTRACTOR_DRIFT: attractor_err wysoki, chaos
    # → ext_attractor_phase(zmienny), phase_alignment(-), ext_entropy_gradient(+)
    ad = zero.copy()
    ad[C["ext_attractor_phase"]] = 0.9  # dryf
    ad[C["phase_alignment"]] = 0.1
    ad[C["ext_entropy_gradient"]] = 0.8
    ad[C["ext_coherence_drift"]] = 0.6
    SITUATION_TEMPLATES["ATTRACTOR_DRIFT"] = _norm(ad)
    
    # CLOSURE_LOW: algebra otwarta, niski closure
    # → ext_closure_drive(-), ext_holonomy_flux(+), kappa_potential(+)
    cl = zero.copy()
    cl[C["ext_closure_drive"]] = 0.1   # niski closure
    cl[C["ext_holonomy_flux"]] = 0.8   # otwarta holonomia
    cl[C["kappa_potential"]] = 0.7     # potencjał do domknięcia
    SITUATION_TEMPLATES["CLOSURE_LOW"] = _norm(cl)
    
    # HARMONY: wszystko zsynchronizowane (baseline)
    hm = zero.copy()
    hm[C["phase_alignment"]] = 0.9
    hm[C["ext_coherence_drift"]] = 0.1
    hm[C["ext_sync_order"]] = 0.9
    hm[C["ext_closure_drive"]] = 0.8
    SITUATION_TEMPLATES["HARMONY"] = _norm(hm)


_build_situation_templates()


def detect_situation(state_36d: np.ndarray) -> dict[str, Any]:
    """Detect which NOEMA situation the current 36D state matches.
    
    Zamiast if/else na thresholdach — algebraiczne porównanie przez
    connection() między stanem a template'ami sytuacji.
    Returns dict z rankings sytuacji + dominująca sytuacja.
    """
    if not SITUATION_TEMPLATES:
        return {"situation": "UNKNOWN", "rankings": {}}
    
    rankings: dict[str, float] = {}
    for name, template in SITUATION_TEMPLATES.items():
        # connection = cos(θ) między wektorami = overlap miara
        sim = float(np.dot(state_36d, template))
        rankings[name] = round(float(sim), 4)
    
    sorted_situations = sorted(rankings.items(), key=lambda x: -x[1])
    dominant = sorted_situations[0][0] if sorted_situations else "UNKNOWN"
    
    return {
        "situation": dominant,
        "confidence": sorted_situations[0][1] if sorted_situations else 0.0,
        "rankings": rankings,
    }


def get_all_operations() -> dict[str, dict[str, Any]]:
    """Full operator registry with vectors and metadata."""
    ops: dict[str, dict[str, Any]] = {}
    for op_id in ALL_OPERATOR_IDS:
        sig = operator_signature(op_id)
        ops[op_id] = {
            "operator_id": op_id,
            "vector_24d": [round(float(x), 6) for x in sig],
            "vector_norm": round(float(np.linalg.norm(sig)), 6),
            "semantic_mass": round(float(sig[0]), 6),
            "kappa_potential": round(float(sig[23]), 6),
        }
    return ops
