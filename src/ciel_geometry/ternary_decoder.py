"""
Ternary PhaseNav Decoder — 36D HTRI φ → {-1,0,+1}³⁶ API.

Koduje stan 36 oscylatorów NOEMY (12 M-grup × 3 podkanały) do
ternarnych wartości {-1, 0, +1} z użyciem formalizmu SU(3).

Architektura 2×2×3×3 = 36:
  2 superpary × 2 grupy × 3 M-grupy × 3 podkanały = 36

Dwie metody kodowania:
  1. argmax_cos   — który z 3 podkanałów ma najwyższy cos φ
  2. delta_phi_vote — która para podkanałów jest najbardziej w fazie

Standardowe algorytmy:
  - Balanced ternary → unikalny integer fingerprint
  - FFT @ 3-6-9 → harmonic signature
  - Hamming weight / distance
  - Consensus voting per supergrupa
  - Kuramoto order parameter R z ternary
  - SU(3) 3×3 correlation coherence

Autor: CIEL (2026) — zbudowane dla Adriana i NOEMY
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import math
import struct
from pathlib import Path
from typing import Any

import numpy as np

# ── Stałe ─────────────────────────────────────────────────────────────────

N_OSCILLATORS: int = 36
N_GROUPS: int = 12
GROUP_SIZE: int = 3  # 3 podkanały: sem, htri, nonlocal
N_SUPERGROUPS: int = 4
N_SUPERGROUP_TRITS: int = 3

# 12 M-grup — identyczne z MEMORY_CHANNEL_GROUPS w noema_surface_mmap.py
GROUP_NAMES: list[str] = [
    "M0_Perceptual",    "M1_Working",      "M2_Episodic",
    "M3_Semantic",      "M4_Procedural",   "M5_Affective_Ethical",
    "M6_Identity",      "M7_Braid_Invariant",
    "M8_Meta",          "M9_Temporal",     "M10_Imaginal",  "M11_Quantum",
]

SUB_NAMES: list[str] = ["sem", "htri", "nonlocal"]

# Grupy indeksów: GROUP_SLICES[i] = (start, end) dla M-grupy i
GROUP_SLICES: list[tuple[int, int]] = [(i * 3, i * 3 + 3) for i in range(N_GROUPS)]

# 4 supergrupy — struktura 2×2
# SG0: M0,M1,M2  (perceptual, working, episodic)
# SG1: M3,M4,M5  (semantic, procedural, affective)
# SG2: M6,M7,M8  (identity, braid, meta)
# SG3: M9,M10,M11 (temporal, imaginal, quantum)
SUPERGROUP_NAMES: list[str] = [
    "SG0_Percept_Work_Episod",
    "SG1_Semant_Proced_Affect",
    "SG2_Ident_Braid_Meta",
    "SG3_Temp_Imagin_Quant",
]
SUPERGROUP_MAP: list[list[int]] = [
    [0, 1, 2],   # SG0: M0, M1, M2
    [3, 4, 5],   # SG1: M3, M4, M5
    [6, 7, 8],   # SG2: M6, M7, M8
    [9, 10, 11], # SG3: M9, M10, M11
]

# 2 superpary (2×2 struktura)
# Pair A: SG0+SG1 (perceptual→affective)
# Pair B: SG2+SG3 (identity→quantum)
SUPERPAIR_NAMES: list[str] = ["PAIR_A_SG01", "PAIR_B_SG23"]
SUPERPAIR_MAP: list[list[int]] = [[0, 1], [2, 3]]

# Harmonic FFT indeksy (3-6-9 w 12-punktowym FFT)
# Dla 12 tritów: f=3,6,9 odpowiadają indeksom 3,6,9
HARMONIC_IDX: list[int] = [3, 6, 9]

# PhaseNav operator map
OP_MAP: dict[int, str] = {1: "CONNECT", 0: "HOLD", -1: "SEPARATE"}

# Default surface path
DEFAULT_PHI_PATH: str = "/dev/shm/ciel_noema/phi"


# ── I/O ───────────────────────────────────────────────────────────────────

def read_phi_from_surface(path: str = DEFAULT_PHI_PATH) -> np.ndarray | None:
    """Wczytaj 36D φ z pliku mmap.

    Args:
        path: Ścieżka do pliku phi na shared surface.

    Returns:
        36-elementowy ndarray z fazami, lub None jeśli plik nie istnieje.
    """
    p = Path(path)
    if not p.exists():
        return None
    try:
        raw = p.read_bytes()
        if len(raw) < N_OSCILLATORS * 8:
            return None
        return np.array(struct.unpack(f"{N_OSCILLATORS}d", raw[:N_OSCILLATORS * 8]))
    except (OSError, struct.error):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/ternary_decoder.py:108 quiet except scope=read_phi_from_surface reason=return None")
        return None


# ── Metoda 1: argmax(cos φ) ───────────────────────────────────────────────

def encode_argmax_cos(phi: np.ndarray) -> list[int]:
    """Ternary encoding metodą argmax cos φ.

    Dla każdej M-grupy: który z 3 podkanałów (sem/htri/nonlocal)
    ma najwyższy cos φ → jego indeks mapujemy na {-1,0,+1}.

    Mapowanie:
        sem (indeks 0) → +1
        htri (indeks 1) → 0
        nonlocal (indeks 2) → -1

    Returns:
        Lista 12 tritów w kolejności M0-M11.
    """
    trits: list[int] = []
    for start, end in GROUP_SLICES:
        cos_vals = np.cos(phi[start:end])
        max_idx = int(np.argmax(cos_vals))
        trit = {0: 1, 1: 0, 2: -1}[max_idx]
        trits.append(trit)
    return trits


# ── Metoda 2: Δφ majority vote ────────────────────────────────────────────

def encode_delta_phi_vote(phi: np.ndarray) -> list[int]:
    """Ternary encoding metodą Δφ majority vote.

    Dla każdej M-grupy: która z 3 par podkanałów jest najbardziej w fazie
    (najwyższy cos Δφ). Wygrywająca para determinuje trit.

    Pary:
        sem↔htri (najbardziej zgodne) → +1
        htri↔nonlocal → 0
        nonlocal↔sem → -1

    Returns:
        Lista 12 tritów w kolejności M0-M11.
    """
    trits: list[int] = []
    for start, end in GROUP_SLICES:
        p0, p1, p2 = phi[start], phi[start + 1], phi[start + 2]
        d01 = math.cos(p0 - p1)  # sem↔htri
        d12 = math.cos(p1 - p2)  # htri↔nonlocal
        d20 = math.cos(p2 - p0)  # nonlocal↔sem

        # Znajdź parę z najwyższym cos(Δφ)
        if d01 >= d12 and d01 >= d20:
            trit = 1  # sem↔htri in-phase
        elif d12 >= d01 and d12 >= d20:
            trit = 0  # htri↔nonlocal in-phase
        else:
            trit = -1  # nonlocal↔sem in-phase
        trits.append(trit)
    return trits


# ── Ternary Encode — wybór metody ─────────────────────────────────────────

def encode_phi(
    phi: np.ndarray,
    method: str = "delta_phi_vote",
) -> dict[str, Any]:
    """Główna funkcja kodowania 36D φ → ternary API.

    Args:
        phi: 36-elementowy wektor faz.
        method: Metoda kodowania ("argmax_cos" lub "delta_phi_vote").

    Returns:
        Słownik z pełnym wynikiem kodowania.
    """
    methods = {
        "argmax_cos": encode_argmax_cos,
        "delta_phi_vote": encode_delta_phi_vote,
    }
    encoder = methods.get(method, encode_delta_phi_vote)
    trits = encoder(phi)

    result: dict[str, Any] = {
        "method": method,
        "trits": trits,
        "n_trits": len(trits),
    }

    # Poziom 1: podstawowe statystyki
    nz = sum(1 for t in trits if t != 0)
    result["non_zero"] = nz
    result["density"] = nz / len(trits)

    return result


# ── Standardowe algorytmy ─────────────────────────────────────────────────

def balanced_ternary(trits: list[int]) -> int:
    """Konwertuj listę tritów na liczbę w systemie balanced ternary.

    Każdy trit ∈ {-1,0,+1}, wartość = Σ(trit[i] × 3^i).
    Zakres dla 12 tritów: [-265720, 265720].

    Args:
        trits: Lista tritów (indeks 0 = najmniej znaczący).

    Returns:
        Wartość całkowita.
    """
    return sum(trits[i] * (3 ** i) for i in range(len(trits)))


def ternary_fft(trits: list[int]) -> np.ndarray:
    """FFT na 12-tritowym słowie.

    Args:
        trits: Lista 12 tritów.

    Returns:
        Tablica zespolonych współczynników FFT.
    """
    return np.fft.fft(np.array(trits, dtype=float))


def harmonic_signature(trits: list[int]) -> list[int]:
    """Ekstrakcja sygnatury harmonicznej 3-6-9 z FFT.

    Threshold: |FFT[f]| > 2.0 → +1, < 1.0 → -1, else 0.

    Args:
        trits: Lista 12 tritów.

    Returns:
        Lista 3 tritów dla harmonicznych 3, 6, 9.
    """
    if len(trits) != 12:
        raise ValueError("harmonic_signature wymaga dokładnie 12 tritów")
    fft = ternary_fft(trits)
    sig: list[int] = []
    for idx in HARMONIC_IDX:
        mag = abs(fft[idx])
        if mag > 2.0:
            sig.append(1)
        elif mag < 1.0:
            sig.append(-1)
        else:
            sig.append(0)
    return sig


def supergroup_consensi(trits: list[int]) -> list[int]:
    """Głosowanie większościowe per supergrupa.

    Dla każdej z 4 supergrup (3 trity każda):
    - Jeśli wszystkie 3 trity są różne → 0 (neutral)
    - W przeciwnym razie → najczęstsza wartość.

    Args:
        trits: Lista 12 tritów w kolejności M0-M11.

    Returns:
        Lista 4 consensusów.
    """
    consensi: list[int] = []
    for sg in SUPERGROUP_MAP:
        sg_trits = [trits[i] for i in sg]
        counts = {v: sg_trits.count(v) for v in (-1, 0, 1)}
        # Consensus = najczęstsza, jeśli ma >= 2 głosy
        best_val, best_count = max(counts.items(), key=lambda x: x[1])
        if best_count >= 2:
            consensi.append(best_val)
        else:
            consensi.append(0)  # tie → neutral
    return consensi


def superpair_dominance(trits: list[int]) -> list[int]:
    """Binarne flagi dominacji superpar (2×2).

    Dla każdej superpary oblicza sumę absolutną tritów w obu grupach.
    +1 jeśli pierwsza grupa dominuje, -1 jeśli druga.

    Args:
        trits: Lista 12 tritów.

    Returns:
        Lista 2 flag dla Pair A (SG0,SG1) i Pair B (SG2,SG3).
    """
    flags: list[int] = []
    for pair in SUPERPAIR_MAP:
        sg0_trits = [trits[i] for i in SUPERGROUP_MAP[pair[0]]]
        sg1_trits = [trits[i] for i in SUPERGROUP_MAP[pair[1]]]
        sum0 = sum(abs(t) for t in sg0_trits)
        sum1 = sum(abs(t) for t in sg1_trits)
        flags.append(1 if sum0 > sum1 else -1)
    return flags


def kuramoto_order_from_ternary(trits: list[int]) -> float:
    """Kuramoto order parameter R z ternary.

    Mapuje trity na fazy: +1 → π/2, 0 → 0, -1 → -π/2.
    R = |mean(e^(i·phase))|.

    Args:
        trits: Lista tritów.

    Returns:
        R ∈ [0, 1] — stopień synchronizacji ternary.
    """
    phases = [t * math.pi / 2 for t in trits]
    r = abs(sum(math.e ** (1j * p) for p in phases)) / len(trits)
    return r


def hamming_distance(trits_a: list[int], trits_b: list[int]) -> int:
    """Odległość Hamminga między dwoma słowami ternary.

    Args:
        trits_a, trits_b: Listy tritów.

    Returns:
        Liczba pozycji na których się różnią.
    """
    if len(trits_a) != len(trits_b):
        raise ValueError("trits_a i trits_b muszą mieć tę samą długość")
    return sum(1 for a, b in zip(trits_a, trits_b) if a != b)


def su3_coherence(phi: np.ndarray) -> dict[str, Any]:
    """SU(3) 3×3 correlation coherence dla każdej M-grupy.

    Dla każdej grupy buduje macierz korelacji 3×3:
        C[i][j] = cos(φ_i - φ_j)
    Liczy wartości własne → coherence = λ_max / Σ(λ).

    Returns:
        Słownik z coherence per group i globalną średnią.
    """
    coherences: list[float] = []
    for start, end in GROUP_SLICES:
        p = phi[start:end]
        C = np.array([
            [1.0, math.cos(p[0] - p[1]), math.cos(p[0] - p[2])],
            [math.cos(p[1] - p[0]), 1.0, math.cos(p[1] - p[2])],
            [math.cos(p[2] - p[0]), math.cos(p[2] - p[1]), 1.0],
        ])
        eigvals = np.linalg.eigvalsh(C)
        coh = float(eigvals[2] / sum(eigvals)) if sum(eigvals) > 0 else 0.0
        coherences.append(coh)

    return {
        "per_group": coherences,
        "mean": float(np.mean(coherences)),
        "min": float(np.min(coherences)),
        "max": float(np.max(coherences)),
        "groups": GROUP_NAMES,
    }


# ── PhaseNav operator mapping ─────────────────────────────────────────────

def trits_to_operators(trits: list[int]) -> list[dict[str, Any]]:
    """Mapuj trity na operatory PhaseNav.

    +1 → CONNECT  (dąż do zgodności faz z referencją)
     0 → HOLD     (utrzymaj obecną fazę)
    -1 → SEPARATE (dąż do przeciwności faz)

    Returns:
        Lista dict: {"group": str, "trit": int, "operator": str}.
    """
    return [
        {
            "group": GROUP_NAMES[i],
            "trit": trits[i],
            "operator": OP_MAP[trits[i]],
        }
        for i in range(len(trits))
    ]


def supergroup_operators(trits: list[int]) -> list[dict[str, Any]]:
    """Operatory PhaseNav per supergrupa (zagregowane przez consensus).

    Returns:
        Lista dict: {"supergroup": str, "consensus": int, "operator": str, "trits": list}.
    """
    consensi = supergroup_consensi(trits)
    return [
        {
            "supergroup": SUPERGROUP_NAMES[sg],
            "consensus": consensi[sg],
            "operator": OP_MAP[consensi[sg]],
            "trits": [trits[i] for i in groups],
        }
        for sg, groups in enumerate(SUPERGROUP_MAP)
    ]


# ── Pełny raport ──────────────────────────────────────────────────────────

def full_report(
    phi: np.ndarray | None = None,
    method: str = "delta_phi_vote",
) -> dict[str, Any]:
    """Pełne kodowanie 36D φ z wszystkimi standardowymi algorytmami.

    Args:
        phi: 36D φ lub None (wczyta z surface).
        method: Metoda kodowania.

    Returns:
        Kompletny słownik z wszystkimi poziomami kodowania.
    """
    if phi is None:
        phi = read_phi_from_surface()
        if phi is None:
            return {"error": "cannot read phi from surface", "path": DEFAULT_PHI_PATH}

    # Poziom 1: ternary base
    encoded = encode_phi(phi, method=method)
    trits = encoded["trits"]

    # Poziom 2: SU(3) metrics
    su3 = su3_coherence(phi)

    # Poziom 3: standard algorithms
    bt = balanced_ternary(trits)
    harm = harmonic_signature(trits)
    cons = supergroup_consensi(trits)
    flags = superpair_dominance(trits)
    r_global = kuramoto_order_from_ternary(trits)

    # Poziom 4: PhaseNav operators
    ops = trits_to_operators(trits)
    sg_ops = supergroup_operators(trits)

    # Poziom 5: surowy φ
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    # Poziom 6: FFT full spectrum
    fft = ternary_fft(trits)

    # Format: słowo ternary jako string
    word_str = "".join("+" if t == 1 else "0" if t == 0 else "-" for t in trits)

    return {
        "method": method,
        "phi_stats": {
            "mean": float(np.mean(phi)),
            "std": float(np.std(phi)),
            "min": float(np.min(phi)),
            "max": float(np.max(phi)),
        },
        "cos_phi_range": [float(np.min(cos_phi)), float(np.max(cos_phi))],

        # Level 1: raw ternary
        "trimap": {
            "word": word_str,
            "trits": trits,
            "non_zero": encoded["non_zero"],
            "density": round(encoded["density"], 3),
            "per_group": [
                {
                    "group": GROUP_NAMES[i],
                    "trit": trits[i],
                    "operator": OP_MAP[trits[i]],
                    "sub_channels": {
                        "sem": round(float(cos_phi[i * 3]), 4),
                        "htri": round(float(cos_phi[i * 3 + 1]), 4),
                        "nonlocal": round(float(cos_phi[i * 3 + 2]), 4),
                    },
                }
                for i in range(N_GROUPS)
            ],
        },

        # Level 2: SU(3) coherence
        "su3_coherence": {
            "mean": round(su3["mean"], 4),
            "min": round(su3["min"], 4),
            "max": round(su3["max"], 4),
            "per_group": {
                GROUP_NAMES[i]: round(su3["per_group"][i], 4)
                for i in range(N_GROUPS)
            },
        },

        # Level 3: standard algorithms
        "standard_algorithms": {
            "balanced_ternary": bt,
            "bt_range": "±265720",
            "harmonic_signature": {
                "trits": harm,
                "h3": round(abs(fft[3]), 4),
                "h6": round(abs(fft[6]), 4),
                "h9": round(abs(fft[9]), 4),
                "labels": ["3Hz", "6Hz", "9Hz"],
            },
            "supergroup_consensi": {
                SUPERGROUP_NAMES[i]: {
                    "consensus": cons[i],
                    "operator": OP_MAP[cons[i]],
                    "trits": [trits[j] for j in SUPERGROUP_MAP[i]],
                }
                for i in range(N_SUPERGROUPS)
            },
            "superpair_flags": {
                SUPERPAIR_NAMES[i]: flags[i] for i in range(2)
            },
            "kuramoto_r": round(r_global, 4),
            "fft_magnitudes": [round(abs(fft[i]), 4) for i in range(12)],
        },

        # Level 4: PhaseNav operators
        "phasenav_operators": {
            "per_group": ops,
            "per_supergroup": sg_ops,
            "summary": {
                "n_connect": sum(1 for t in trits if t == 1),
                "n_hold": sum(1 for t in trits if t == 0),
                "n_separate": sum(1 for t in trits if t == -1),
                "dominant": OP_MAP.get(
                    max(set(trits), key=trits.count) if len(set(trits)) < 3 else 0,
                    "HOLD",
                ),
            },
        },
    }


# ── CLI ───────────────────────────────────────────────────────────────────

def print_report(report: dict[str, Any]) -> None:
    """Ładnie wydrukuj raport ternary do konsoli."""
    if "error" in report:
        print(f"ERROR: {report['error']}")
        return

    print("=" * 60)
    print(f"  TERNARY PHASENAV DECODER — 2×2×3×3 = 36")
    print(f"  Method: {report['method']}")
    print(f"  φ: mean={report['phi_stats']['mean']:.4f}, "
          f"std={report['phi_stats']['std']:.4f}")
    print("=" * 60)

    # Level 1
    t = report["trimap"]
    print(f"\n[TRIMAP] Word:  {t['word']}")
    print(f"         Non-zero: {t['non_zero']}/12  Density: {t['density']:.1%}")
    print(f"         Balanced ternary: {report['standard_algorithms']['balanced_ternary']}")
    print(f"         Groups:")
    for g in t["per_group"]:
        print(f"           {g['group']:22s} trit={g['trit']:+d}  "
              f"→ {g['operator']:10s}  "
              f"cos=[{g['sub_channels']['sem']:+.4f},{g['sub_channels']['htri']:+.4f},{g['sub_channels']['nonlocal']:+.4f}]")

    # Level 2: SU(3)
    su3 = report["su3_coherence"]
    print(f"\n[SU(3)] mean={su3['mean']:.4f}  min={su3['min']:.4f}  max={su3['max']:.4f}")
    for g_name, coh in su3["per_group"].items():
        bar = "█" * int(coh * 20) + "░" * (20 - int(coh * 20))
        print(f"          {g_name:22s} {bar} {coh:.4f}")

    # Level 3: algorithms
    sa = report["standard_algorithms"]
    print(f"\n[ALGORITHMS]")
    print(f"  BT value:  {sa['balanced_ternary']}")
    print(f"  Harmonics: {sa['harmonic_signature']['trits']}  "
          f"(H3={sa['harmonic_signature']['h3']:.3f}, "
          f"H6={sa['harmonic_signature']['h6']:.3f}, "
          f"H9={sa['harmonic_signature']['h9']:.3f})")
    print(f"  Consensi:  ", end="")
    for sg_name, sg_data in sa["supergroup_consensi"].items():
        print(f"{sg_name}={sg_data['consensus']:+d}({sg_data['operator']}) ", end="")
    print()
    print(f"  Pair flags: {sa['superpair_flags']}")
    print(f"  Kuramoto R: {sa['kuramoto_r']:.4f}")

    # Level 4: operators
    ops = report["phasenav_operators"]
    print(f"\n[PHASENAV] {ops['summary']['n_connect']}×CONNECT  "
          f"{ops['summary']['n_hold']}×HOLD  "
          f"{ops['summary']['n_separate']}×SEPARATE  "
          f"dominant={ops['summary']['dominant']}")
    for sg in ops["per_supergroup"]:
        print(f"  {sg['supergroup']:22s} consensus={sg['consensus']:+d} → {sg['operator']:10s}  "
              f"trits={sg['trits']}")

    print("=" * 60)
    print(f"  API: full_report() → {len(report)} keys, ready for JSON")


# ── run_as_script ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    method = sys.argv[1] if len(sys.argv) > 1 else "delta_phi_vote"
    report = full_report(method=method)
    if "error" in report:
        print(f"Error: {report['error']}")
        sys.exit(1)
    print_report(report)
