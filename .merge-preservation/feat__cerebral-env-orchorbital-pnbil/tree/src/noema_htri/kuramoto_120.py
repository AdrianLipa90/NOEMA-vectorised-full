"""Low-energy Kuramoto 120 oscillator HTRI simulator for NOEMA surface runs.

This is a computational diagnostic model. It does not claim physical nonlocal
coupling. In this repository, "nonlocal" means NOEMA-surface/proxy semantics:
file-packet coupling, manifest hashes, card registry meaning and pipeline reports.

The simulator emits RAW metrics only. Publication into pipeline metrics is gated
by :mod:`noema_htri.validation`.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class KuramotoHTRIConfig:
    n_oscillators: int = 120
    steps: int = 512
    dt: float = 0.002
    base_frequency_hz: float = 7.83
    coupling: float = 7.25
    damping: float = 0.035
    detuning_fraction: float = 0.004
    initial_phase_spread: float = 0.18
    seed: int = 474812


def _seed_from_digest(digest: str, fallback: int) -> int:
    try:
        return int(digest[:16], 16) % (2**32)
    except Exception:
        return fallback


def _order_parameter(theta: np.ndarray) -> complex:
    return complex(np.mean(np.exp(1j * theta)))


def _wrap(theta: np.ndarray) -> np.ndarray:
    return np.angle(np.exp(1j * theta))


def run_kuramoto_htri_120(
    *,
    manifest_digest: str,
    card_registry_digest: str,
    config: KuramotoHTRIConfig | None = None,
) -> dict[str, Any]:
    """Run deterministic HTRI/Kuramoto diagnostic simulation.

    Dynamics are integrated in the co-rotating frame ``phi = theta - omega0*t``.
    This prevents the natural 7.83 Hz carrier rotation from being counted as
    phase-closure error.
    """
    config = config or KuramotoHTRIConfig()
    seed_material = hashlib.sha256((manifest_digest + card_registry_digest).encode("utf-8")).hexdigest()
    rng = np.random.default_rng(_seed_from_digest(seed_material, config.seed))

    n = config.n_oscillators
    omega0 = 2.0 * math.pi * config.base_frequency_hz

    # Ten semantic/card clusters × twelve oscillators each.  Detuning is small
    # relative to the carrier and coupling is in rad/s, so the default model can
    # actually test synchronization rather than always desynchronizing.
    cluster_count = 10
    cluster_ids = np.arange(n) % cluster_count
    cluster_offsets = (cluster_ids - (cluster_count - 1) / 2.0) / cluster_count
    detuning = (
        config.detuning_fraction * omega0 * cluster_offsets
        + rng.normal(0.0, 0.00075 * omega0, size=n)
    )

    # Start near a shared semantic phase with card-cluster offsets.  A fully
    # random initialization remains useful as an adversarial test, but should not
    # be the default for a low-energy HTRI diagnostic run.
    phi = (
        rng.normal(0.0, config.initial_phase_spread, size=n)
        + 0.04 * cluster_offsets
    )
    phi = _wrap(phi)

    r_values: list[float] = []
    phase_values: list[float] = []
    energy_values: list[float] = []
    closure_values: list[float] = []
    drift_values: list[float] = []

    prev_phase = 0.0
    unwrapped_phase = 0.0

    for _ in range(config.steps):
        z = _order_parameter(phi)
        r = abs(z)
        psi = math.atan2(z.imag, z.real)
        coupling_term = config.coupling * r * np.sin(psi - phi)
        phi = phi + config.dt * (detuning + coupling_term - config.damping * np.sin(phi))
        phi = _wrap(phi)

        z2 = _order_parameter(phi)
        phase = math.atan2(z2.imag, z2.real)
        d_phase = math.atan2(math.sin(phase - prev_phase), math.cos(phase - prev_phase))
        unwrapped_phase += d_phase
        prev_phase = phase

        # In the co-rotating frame, closure should remain close to the semantic
        # reference phase, not the carrier angle omega0*t.
        closure = abs(math.atan2(math.sin(phase), math.cos(phase))) / math.pi
        drift = abs(unwrapped_phase) / max(1.0, len(r_values) + 1)
        energy = float(np.mean(detuning**2) + np.var(np.sin(phi)))

        r_values.append(float(abs(z2)))
        phase_values.append(float(phase))
        closure_values.append(float(closure))
        drift_values.append(float(drift))
        energy_values.append(energy)

    r_arr = np.array(r_values)
    c_arr = np.array(closure_values)
    d_arr = np.array(drift_values)
    e_arr = np.array(energy_values)

    final_r = float(r_arr[-1])
    mean_r = float(r_arr.mean())
    closure_final = float(c_arr[-1])
    closure_mean = float(c_arr.mean())
    phase_drift_mean = float(d_arr.mean())
    energy_proxy = float(e_arr.mean())

    # Raw diagnostic score only.  Validation decides whether this may be
    # published to pipeline-facing metrics.
    htri_index = max(
        0.0,
        min(
            1.0,
            0.55 * final_r
            + 0.25 * mean_r
            + 0.15 * (1.0 - closure_final)
            + 0.05 * max(0.0, 1.0 - phase_drift_mean),
        ),
    )
    htri_diagnostic_cost = float((1.0 - htri_index) + closure_mean + 0.001 * energy_proxy)

    return {
        "schema": "noema/htri-kuramoto-120-raw-report/v0.2",
        "epistemic_status": "NOEMA-surface simulation; not direct external/nonlocal sensor proof",
        "publication_status": "raw_unvalidated",
        "config": asdict(config),
        "manifest_digest": manifest_digest,
        "card_registry_digest": card_registry_digest,
        "metrics": {
            "oscillator_count": n,
            "steps": config.steps,
            "base_frequency_hz": config.base_frequency_hz,
            "omega0_rad_s": omega0,
            "order_parameter_final": final_r,
            "order_parameter_mean": mean_r,
            "order_parameter_min": float(r_arr.min()),
            "order_parameter_max": float(r_arr.max()),
            "phase_closure_error_final": closure_final,
            "phase_closure_error_mean": closure_mean,
            "phase_drift_mean_corotating": phase_drift_mean,
            "energy_proxy_mean": energy_proxy,
            "htri_index": htri_index,
            "htri_diagnostic_cost": htri_diagnostic_cost,
            "pipeline_connected_score": None,
        },
    }


__all__ = ["KuramotoHTRIConfig", "run_kuramoto_htri_120"]
