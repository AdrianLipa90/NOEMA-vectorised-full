"""Repository phase state and synchronisation report builder.

The hot path is expressed as a single PhaseNav-style vector projection: masses
and phases are materialised once, then closure, residual, and Euler observables
are derived from the same NumPy batch. Import and allocation overhead therefore
stay outside repeated report calls and remain independent of GGUF presence.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np


@dataclass(frozen=True)
class RepositoryState:
    key: str
    identity: str
    phi: float
    spin: float
    mass: float
    role: str
    upstream: str


def load_registry(path: str | Path) -> dict[str, RepositoryState]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    repos = data.get("repositories", [])
    out: dict[str, RepositoryState] = {}
    for item in repos:
        state = RepositoryState(
            key=str(item["key"]),
            identity=str(item["identity"]),
            phi=float(item["phi"]),
            spin=float(item["spin"]),
            mass=float(item["mass"]),
            role=str(item["role"]),
            upstream=str(item["upstream"]),
        )
        out[state.key] = state
    return out


def load_couplings(path: str | Path) -> dict[str, dict[str, float]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    raw = data.get("couplings", {})
    return {
        str(key): {str(target): float(value) for target, value in neighbors.items()}
        for key, neighbors in raw.items()
    }


def _phasenav_arrays(states: Iterable[RepositoryState]) -> tuple[list[RepositoryState], np.ndarray, np.ndarray]:
    """Materialise one stable batch for all phase observables."""
    batch = list(states)
    if not batch:
        empty = np.empty(0, dtype=np.float64)
        return batch, empty, empty
    masses = np.fromiter((max(0.0, state.mass) for state in batch), dtype=np.float64, count=len(batch))
    phases = np.fromiter((state.phi for state in batch), dtype=np.float64, count=len(batch))
    return batch, masses, phases


def _phasenav_projection(masses: np.ndarray, phases: np.ndarray) -> complex:
    if masses.size == 0:
        return 0j
    return complex(np.dot(masses, np.exp(1j * phases)))


def weighted_euler_vector(states: Iterable[RepositoryState]) -> complex:
    _, masses, phases = _phasenav_arrays(states)
    return _phasenav_projection(masses, phases)


def weighted_euler_vector_numpy(states: Iterable[RepositoryState]) -> complex:
    """Compatibility name for the native vectorised PhaseNav projection."""
    return weighted_euler_vector(states)


def closure_defect(states: Iterable[RepositoryState]) -> float:
    _, masses, phases = _phasenav_arrays(states)
    total_mass = float(masses.sum())
    if total_mass <= 0.0:
        return 1.0
    vector = _phasenav_projection(masses, phases)
    return float(np.clip(1.0 - abs(vector) / total_mass, 0.0, 1.0))


def euler_residual(states: Iterable[RepositoryState]) -> float:
    """Normalize the Euler closure residual to [0, 1]."""
    batch, masses, phases = _phasenav_arrays(states)
    if not batch:
        return 1.0
    total_mass = float(masses.sum())
    if total_mass <= 0.0:
        return 1.0
    vector = _phasenav_projection(masses, phases)
    return float(np.clip(abs(vector) / total_mass, 0.0, 1.0))


def pairwise_tension(a: RepositoryState, b: RepositoryState, coupling: float) -> float:
    return float(coupling) * (1.0 - math.cos(b.phi - a.phi))


def all_pairwise_tensions(
    states: dict[str, RepositoryState],
    couplings: dict[str, dict[str, float]],
) -> list[dict[str, Any]]:
    """Vectorise each adjacency row while preserving deterministic output order."""
    rows: list[dict[str, Any]] = []
    for source, neighbors in couplings.items():
        source_state = states.get(source)
        if source_state is None:
            continue

        valid = [(target, value) for target, value in neighbors.items() if target in states]
        if not valid:
            continue
        target_names = [target for target, _ in valid]
        target_phases = np.fromiter(
            (states[target].phi for target in target_names),
            dtype=np.float64,
            count=len(target_names),
        )
        coupling_values = np.fromiter(
            (float(value) for _, value in valid),
            dtype=np.float64,
            count=len(valid),
        )
        tensions = coupling_values * (1.0 - np.cos(target_phases - source_state.phi))
        rows.extend(
            {
                "source": source,
                "target": target,
                "coupling": float(coupling),
                "tension": float(tension),
            }
            for target, coupling, tension in zip(target_names, coupling_values, tensions)
        )

    rows.sort(key=lambda row: (row["source"], row["target"]))
    return rows


def pairwise_tension_matrix(
    states: dict[str, RepositoryState],
    couplings: dict[str, dict[str, float]],
) -> list[list[float]]:
    """Build a dense pairwise tension matrix aligned to sorted state keys."""
    keys = sorted(states)
    if not keys:
        return []
    index = {key: position for position, key in enumerate(keys)}
    matrix = np.zeros((len(keys), len(keys)), dtype=np.float64)
    for row in all_pairwise_tensions(states, couplings):
        source_index = index.get(str(row["source"]))
        target_index = index.get(str(row["target"]))
        if source_index is None or target_index is None or source_index == target_index:
            continue
        matrix[source_index, target_index] = float(row["tension"])
    return matrix.tolist()


def j_repo(
    states: Iterable[RepositoryState],
    couplings: dict[str, dict[str, float]] | None = None,
) -> float:
    """Compact repo-level cost functional combining closure and pairwise tension."""
    batch = list(states)
    if not batch:
        return 1.0
    defect = closure_defect(batch)
    if not couplings:
        return float(defect)
    state_map = {state.key: state for state in batch}
    tensions = all_pairwise_tensions(state_map, couplings)
    if not tensions:
        return float(defect)
    values = np.fromiter(
        (float(row["tension"]) for row in tensions),
        dtype=np.float64,
        count=len(tensions),
    )
    score = 0.55 * defect + 0.30 * float(values.mean()) + 0.15 * float(values.max())
    return float(np.clip(score, 0.0, 1.0))


def build_sync_report(
    registry_path: str | Path,
    couplings_path: str | Path,
) -> dict[str, Any]:
    states = load_registry(registry_path)
    couplings = load_couplings(couplings_path)

    batch, masses, phases = _phasenav_arrays(states.values())
    total_mass = float(masses.sum())
    vector = _phasenav_projection(masses, phases)
    if total_mass <= 0.0:
        defect = 1.0
        residual = 1.0
    else:
        normalized = abs(vector) / total_mass
        defect = float(np.clip(1.0 - normalized, 0.0, 1.0))
        residual = float(np.clip(normalized, 0.0, 1.0))

    tensions = all_pairwise_tensions(states, couplings)
    tension_values = np.fromiter(
        (float(row["tension"]) for row in tensions),
        dtype=np.float64,
        count=len(tensions),
    ) if tensions else np.empty(0, dtype=np.float64)

    if tension_values.size:
        j_value = float(np.clip(
            0.55 * defect
            + 0.30 * float(tension_values.mean())
            + 0.15 * float(tension_values.max()),
            0.0,
            1.0,
        ))
    else:
        j_value = defect

    return {
        "repository_count": len(batch),
        "weighted_euler_vector": {
            "real": vector.real,
            "imag": vector.imag,
            "abs": abs(vector),
        },
        "closure_defect": defect,
        "euler_residual": residual,
        "pairwise_tensions": tensions,
        "mean_pairwise_tension": float(tension_values.mean()) if tension_values.size else 0.0,
        "max_pairwise_tension": float(tension_values.max()) if tension_values.size else 0.0,
        "j_repo": j_value,
        "phase_backend": "phasenav_numpy_vectorized",
    }
