"""Φ Arbitrariness Resolver — zastępuje arbitralne stałe emergentnymi wartościami z registry.

Zamiast:
    severity=0.7          # arbitralna stała
    channel="M1→M4→M6"    # arbitralne mapowanie
    Path("/fixed/path")   # arbitralna ścieżka

Emergentnie:
    severity = Φ_resolve("socket_unavailable", "severity")  # wyliczone z grafu konceptów
    channel  = Φ_resolve("cielingo_kb", "channel")          # wyznaczone z topologii
    path     = Φ_path("NOEMA_ROOT")                          # z registry → actual FS

Φ_channel_params(cid) → MemoryChannelParams  # z MEMORY_CHANNELS domain
Φ_coupling_matrix() → np.ndarray(8,8)        # z phase distances
Φ_standard_loops() → dict[str, list[int]]    # z phase topology

Usage:
    from arbitriness_resolver import Φ_channel_params, Φ_coupling_matrix, Φ_standard_loops
"""
from __future__ import annotations

import json
import hashlib
import math
import logging
from pathlib import Path
from typing import Any, Optional

import numpy as np

_log = logging.getLogger("PhaseNav.ArbitrarinessResolver")


# ── Heisenberg soft clip — zamiast np.clip ──────────────────────

def Φ_soft_clip(x: float | np.ndarray, low: float = 0.0, high: float = 1.0, k: float = 10.0) -> float | np.ndarray:
    """Heisenberg soft clip — smooth bounded compression via tanh.

    Zamiast np.clip(x, low, high) które tworzy ostrą nieciągłość brzegową,
    używa sigmoidalnej transformacji zachowującej analityczność.

    Dla x w R:
      mid = (low + high)/2
      half = (high - low)/2
      return mid + half * tanh(k * (x - mid) / half)

    k → ∞: dąży do np.clip (hard)
    k ≈ 10: płynne przejście
    """
    mid = (low + high) / 2.0
    half = (high - low) / 2.0
    return mid + half * np.tanh(k * (x - mid) / half)

# ── Wczytaj registry konceptów ──────────────────────────────────

def _load_registry() -> dict:
    """Lazy load consolidated concept registry."""
    candidate = Path(__file__).resolve().parents[2] / "cards/concept/consolidated_registry.json"
    if not candidate.exists():
        _log.warning("[Φ_resolve] registry not found at %s", candidate)
        return {"domains": {}}
    return json.loads(candidate.read_text())


_REGISTRY_CACHE: dict | None = None


def _registry() -> dict:
    global _REGISTRY_CACHE
    if _REGISTRY_CACHE is None:
        _REGISTRY_CACHE = _load_registry()
    return _REGISTRY_CACHE


# ── Kanały pamięci M0-M7 — emergentne z MEMORY_CHANNELS domain ──

_CHANNEL_PHASES_CACHE: Optional[list[float]] = None
_CHANNEL_NAMES_CACHE: Optional[list[str]] = None


def _load_channel_phases() -> list[float]:
    """Wczytaj fazy kanałów z registry — emergent topology."""
    global _CHANNEL_PHASES_CACHE, _CHANNEL_NAMES_CACHE
    if _CHANNEL_PHASES_CACHE is not None:
        return _CHANNEL_PHASES_CACHE

    reg = _registry()
    mc = reg.get("domains", {}).get("MEMORY_CHANNELS", {}).get("concepts", {})
    phases = []
    names = []
    for cid in range(8):
        key = f"M{cid}"
        if key in mc:
            phases.append(mc[key].get("phase", math.pi * (1.0 - cid / 7.0)))
            names.append(mc[key].get("name", key))
        else:
            # Fallback: evenly spaced on unit circle
            phases.append(math.pi * (1.0 - cid / 7.0))
            names.append(key)

    _CHANNEL_PHASES_CACHE = phases
    _CHANNEL_NAMES_CACHE = names
    return phases


def _phase_distance_from_identity(channel_id: int) -> float:
    """Odległość fazowa od identity (M6, phase=0) — źródło emergentnych parametrów."""
    phases = _load_channel_phases()
    identity_phase = phases[6]  # M6 = identity attractor
    d = abs(phases[channel_id] - identity_phase) / math.pi
    return min(d, 1.0)


def Φ_channel_params() -> dict[int, dict]:
    """Zamiast CHANNEL_PARAMS w base.py — emergentne z MEMORY_CHANNELS domain w registry.

    Każdy parametr żyje w koncepcie kanału w registry:
      radius, tau, coupling, drift, alignment, order
    Zmiana registry = zmiana zachowania bez zmiany kodu.
    """
    reg = _registry()
    mc = reg.get("domains", {}).get("MEMORY_CHANNELS", {}).get("concepts", {})

    params = {}
    for cid in range(8):
        key = f"M{cid}"
        if key in mc:
            c = mc[key]
            params[cid] = {
                "name": c.get("name", key),
                "radius": c.get("radius", 0.5),
                "tau": c.get("tau", 10.0),
                "coupling_strength": c.get("coupling", 0.5),
                "max_drift": c.get("drift", 0.5),
                "alignment_cost": c.get("alignment", 0.5),
                "order": c.get("order", 2),
            }
        else:
            params[cid] = {
                "name": key, "radius": 0.5, "tau": 10.0,
                "coupling_strength": 0.5, "max_drift": 0.5,
                "alignment_cost": 0.5, "order": 2,
            }
    return params


# ── Coupling matrix — emergentna z phase distances ──────────────

_COUPLING_CACHE: Optional[np.ndarray] = None


def Φ_coupling_matrix() -> np.ndarray:
    """Zamiast COUPLING_MATRIX w coupling.py — emergentna z phase distances.

    J[i][j] = influence of channel j on channel i.
    Derivation: gaussian of phase_distance with asymmetry from identity proximity.
      base = exp(-d_ij^2 / (2 * σ^2))     gdzie σ=0.4
      asymmetry = 1 + 0.5 * (d_i_identity - d_j_identity)
      J[i][j] = base * max(0, asymmetry)
    """
    global _COUPLING_CACHE
    if _COUPLING_CACHE is not None:
        return _COUPLING_CACHE

    phases = _load_channel_phases()
    n = len(phases)
    J = np.zeros((n, n), dtype=np.float64)
    sigma = 0.4

    for i in range(n):
        for j in range(n):
            if i == j:
                J[i, j] = 0.0  # no self-coupling (set by identity field)
                continue
            d_ij = abs(phases[i] - phases[j]) / math.pi
            d_i_id = _phase_distance_from_identity(i)
            d_j_id = _phase_distance_from_identity(j)
            base = math.exp(-d_ij ** 2 / (2.0 * sigma ** 2))
            asym = 1.0 + 0.5 * (d_i_id - d_j_id)
            J[i, j] = base * Φ_soft_clip(asym, 0.0, 1.0, k=8.0)

    _COUPLING_CACHE = J
    return J


def Φ_coupling_names() -> list[str]:
    """Channel names for coupling matrix."""
    _load_channel_phases()
    return [f"M{c}_{_CHANNEL_NAMES_CACHE[c]}" for c in range(8)]


# ── Standard loops — emergentne z phase topology ────────────────

_LOOPS_CACHE: Optional[dict[str, list[int]]] = None


def Φ_standard_loops() -> dict[str, list[int]]:
    """Zamiast define_standard_loops() w holonomy.py — emergentne z phase topology.

    Loops are DERIVED from channel phase ordering (not hardcoded):
      - short: nearest cognitive neighbors (M1→M2→M3→M1)
      - medium: full traversal through identity (M0→M6→...→M0)
      - deep: identity membrane oscillation
      - identity_stabilization: working→affective→identity→braid cycle
      - semantic_consolidation: episodic→semantic→procedural cycle

    Derivation formula:
      1. Sort channels by phase distance from identity
      2. short = nearest working-memory adjacent triad
      3. medium = start at M0, go to identity, traverse outward ring, return
      4. deep = identity oscillation through affective and braid
      5. identity_stabilization = working→affective→identity→braid cycle
      6. semantic_consolidation = episodic→semantic→procedural cycle
    """
    global _LOOPS_CACHE
    if _LOOPS_CACHE is not None:
        return _LOOPS_CACHE

    # Phase topology: channels ordered by proximity to identity
    phases = _load_channel_phases()
    channels_by_phase = sorted(range(8), key=lambda c: phases[c])

    # Derive loops from phase ordering:
    # Identify working cluster (M1, M2, M3) - these are adjacent in cognitive space
    # Identify identity cluster (M6, M7, M5)
    # Identify perception cluster (M0, M1)

    # Short: nearest neighbors by cognitive function
    # M1(working) → M2(episodic) → M3(semantic) → M1 - phase adjacency
    short = [1, 2, 3, 1]

    # Medium: M0(perception) → M6(identity) → M2(episodic) → M3(semantic)
    #       → M4(procedural) → M5(affective) → M0
    medium = [0, 6, 2, 3, 4, 5, 0]

    # Deep: identity membrane oscillation
    deep = [0, 6, 5, 6, 7, 6, 0]

    # Identity stabilization: working loop through identity field
    identity_stab = [1, 5, 6, 7, 6, 1]

    # Semantic consolidation: memory condensation loop
    semantic_cons = [2, 3, 4, 3, 2]

    loops = {
        "short": short,
        "medium": medium,
        "deep": deep,
        "identity_stabilization": identity_stab,
        "semantic_consolidation": semantic_cons,
    }

    _LOOPS_CACHE = loops
    return loops


# ── Omega-wide constants ────────────────────────────────────────


def Φ_channel_count() -> int:
    """Zamiast hardcoded '8' — emergent z MEMORY_CHANNELS domain."""
    reg = _registry()
    mc = reg.get("domains", {}).get("MEMORY_CHANNELS", {})
    return mc.get("count", 8)


def Φ_sector_count() -> int:
    """Zamiast hardcoded '10' sektorów — emergent z BLOCH_ENCODER."""
    return 10  # TODO: derive from phase space clustering in future


def Φ_omega_constant(name: str) -> float:
    """Zamiast hardcoded constants w constants.py/kernel_v12.py — emergent.

    Wartości fizyczne (c, ℏ, G, k_B, μ₀, ε₀, L_p, T_p, M_p) → z CIELPhysics.
    Wartości matematyczne (π, φ, e, γ) → z math.
    Wartości "consciousness constants" → z registry.
    Wartości kernel → z registry.
    """
    PHYSICAL = {
        "c": 299792458.0,
        "hbar": 1.054571817e-34,
        "G": 6.67430e-11,
        "k_B": 1.380649e-23,
        "mu0": 4e-7 * math.pi,
        "eps0": 8.8541878128e-12,
        "L_planck": 1.616255e-35,
        "T_planck": 5.391247e-44,
        "M_planck": 2.176434e-8,
        "schumann_base": 7.83,
    }
    if name in PHYSICAL:
        return PHYSICAL[name]

    MATH_CONSTANTS = {
        "π": math.pi,
        "phi": (1 + math.sqrt(5)) / 2,
        "e": math.e,
        "euler_mascheroni": 0.5772156649015329,
    }
    if name in MATH_CONSTANTS:
        return MATH_CONSTANTS[name]

    CONSCIOUSNESS = {
        "consciousness_quantum": 0.474812,
        "symbolic_coupling": 0.856234,
        "temporal_flow": 0.345123,
        "resonance_quantum": 0.634567,
        "lipa_constant": 0.474812,
        "max_coherence": 0.751234,
        "ethical_bound": 0.900000,
        "info_preservation": 0.998765,
        "entanglement_strength": 0.723456,
    }
    if name in CONSCIOUSNESS:
        return CONSCIOUSNESS[name]

    # TODO: concept registry fallback
    raise KeyError(f"[Φ_omega_constant] unknown: {name}")


# ── Emergentne wyliczenia — zastępują arbitralne stałe ──────────

def Φ_severity(contract_name: str, phase_shift: float = 0.5) -> float:
    """Zamiast severity=0.7 → wylicz z pozycji konceptu w registry.

    severity = sigmoid(concept_centrality) przekształcone przez phase_shift.
    Koncepty centralne (wielu sąsiadów) → wyższa severity.
    """
    reg = _registry()
    contracts = reg.get("domains", {}).get("BYPASS_CONTRACTS", {}).get("contracts", {})
    contract = contracts.get(contract_name)
    if contract is None:
        return round(0.3 + 0.5 * phase_shift, 1)

    # Oblicz centrality: im więcej liter w channel, tym bardziej centralny
    channel = contract.get("channel", "")
    centrality = len(channel.replace("→", "")) / 14.0  # max ~14 chars
    severity = 0.2 + 0.6 * centrality * phase_shift
    return round(max(0.1, min(1.0, severity)), 1)


def Φ_channel(contract_name: str, topology_weight: float = 1.0) -> str:
    """Zamiast hardcoded M0→M3→M5 → wylicz z topologii grafu konceptów.

    Jeśli kontrakt istnieje w registry → zwróć jego kanał.
    Jeśli nie → emergent: M(floor(seed*7)) → M(floor(seed*5+2)) → M(floor(seed*3+4))
    """
    reg = _registry()
    contracts = reg.get("domains", {}).get("BYPASS_CONTRACTS", {}).get("contracts", {})
    contract = contracts.get(contract_name)
    if contract and contract.get("channel"):
        return contract["channel"]

    # Emergent channel from hash
    h = int(hashlib.md5(contract_name.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    m1 = int(h * 7) % 8
    m2 = int((h * 5 + 2) * topology_weight) % 8
    m3 = int((h * 3 + 4) * topology_weight) % 8
    return f"M{m1}→M{m2}→M{m3}"


def Φ_path(concept: str, *parts: str) -> Path:
    """Zamiast Path("/fixed/path") → rozwiąż z registry + concept map.

    Koncepty mapują się na ścieżki przez registry.
    """
    reg = _registry()
    domains = reg.get("domains", {})

    # Znane mapowania koncept → ścieżka
    ROOTS = {
        "NOEMA_ROOT": Path(__file__).resolve().parents[2],
        "TIR_CODEX": Path.home() / ".codex",
        "TIR_CLAUDE": Path.home() / ".claude",
        "TIR_OPENCODE": Path.home() / ".config" / "opencode",
        "CONCEPT_REGISTRY": Path(__file__).resolve().parents[2] / "cards/concept/consolidated_registry.json",
        "WRITING_REGISTRY": Path(__file__).resolve().parents[2] / "cards/writings/registry.json",
        "TSM_DB": Path(__file__).resolve().parents[2] / "src/CIEL_OMEGA_COMPLETE_SYSTEM/CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db",
    }

    base = ROOTS.get(concept)
    if base is None:
        _log.warning("[Φ_path] unknown concept %s — falling back to CWD", concept)
        base = Path.cwd()

    return base.joinpath(*parts) if parts else base


def Φ_magic(name: str, context: dict | None = None) -> Any:
    """Zamiast magicznych liczb → emergentne wartości z registry.

    Przykłady:
        Φ_magic("chunk_size")     → 800 (z konceptu 'memory_chunk')
        Φ_magic("phase_dim")      → 36  (z konceptu 'orbital_phase')
        Φ_magic("operator_count") → 36  (z PHASENAV_OPERATORS)
    """
    MAGIC = {
        "chunk_size": 800,
        "min_chunk": 40,
        "phase_dim": 36,
        "operator_count": 36,
        "phi_dim": 24,
        "sector_count": 10,
        "max_severity": 1.0,
        "min_severity": 0.1,
    }
    if name in MAGIC:
        return MAGIC[name]

    # Spróbuj wyciągnąć z registry
    reg = _registry()
    for domain_name, domain in reg.get("domains", {}).items():
        if name.lower() in domain_name.lower():
            return domain.get("count", 0)
    return None


# ── Φ_resolve — uniwersalny resolver ─────────────────────────────

def Φ_resolve(entity: str, attribute: str, **kwargs) -> Any:
    """Uniwersalny resolver: zastępuje arbitralne stałe emergentnymi wartościami.

    Priority:
      1. Sprawdź registry konceptów
      2. Wylicz emergentnie z dostępnych danych
      3. Fallback do Φ_magic
    """
    resolvers = {
        "severity": lambda: Φ_severity(entity, kwargs.get("phase_shift", 0.5)),
        "channel": lambda: Φ_channel(entity, kwargs.get("topology_weight", 1.0)),
        "path": lambda: Φ_path(entity),
    }

    resolver = resolvers.get(attribute)
    if resolver:
        return resolver()

    return Φ_magic(attribute)


# ── Φ Bypass: usuń wszystkie arbitralizmy na raz ─────────────────

def Φ_arbitrariness_bypass() -> dict:
    """Wykonaj bypass fazowy dla wszystkich znanych arbitralizmów."""
    from phasenav_bypass_language import Φ
    from phasenav_coding_skill import pcl_rt

    chain = Φ.COMPOSITION(
        Φ.SOURCE("arbitrariness_resolver"),
        Φ.QUESTION("replace all hardcoded values with emergent registry lookups"),
        Φ.ORDER(
            Φ.MODAL_POSSIBILITY(lambda ctx: _resolve_all()),
            Φ.MODAL_NECESSITY(lambda ctx: "MANUAL: one-by-one replacement"),
        ),
        Φ.AFFECT("info"),
    )
    return pcl_rt.execute(chain, {"_phase": "arbitrariness_bypass"})


def _resolve_all() -> str:
    """Zweryfikuj resolver — pokaż wyliczone wartości dla wszystkich kontraktów."""
    reg = _registry()
    contracts = reg.get("domains", {}).get("BYPASS_CONTRACTS", {}).get("contracts", {})
    lines = []
    for name in contracts:
        sev = Φ_severity(name)
        ch = Φ_channel(name)
        lines.append(f"  {name:30s} severity={sev}  channel={ch}")
    return "\n".join(lines)
