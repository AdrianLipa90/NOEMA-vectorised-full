"""SubconsciousBridge — CIELingo ↔ 12D subconscious connection.

Takes subconscious oscillator state (11 PhaseNav + 1 agent),
feeds through MeaningLoop + intention_frame, returns enriched
semantic context for AI response generation.

Protocol:
  bridge = SubconsciousBridge()
  result = bridge.feed(subconscious_state, prompt_text)
  # result.subconscious_enrichment -> goes into CIEL inject
"""
from __future__ import annotations

import math
import cmath
import time
from dataclasses import dataclass, asdict
from typing import Any

KAPPA = math.log(2.0) / (24.0 * math.pi)
TAU = KAPPA * math.pi  # ln2/24


@dataclass
class SubconsciousEnrichment:
    """Enriched subconscious state for CIEL inject."""
    R_12d: float            # PhaseNav 11D + agent sync order
    R_oa: float             # Ott-Antonsen order (Kuramoto)
    psi_12d: float          # mean collective phase [rad]
    euler_gap: float        # distance from Euler closure (|e^{i2πψ}+1|)
    n_tau: float            # τ quanta since last prompt
    kappa_battery_C: float  # κ-battery C = B·ω·N/4π
    kappa_battery_E: float  # κ-battery extracted energy / m₀c²
    berry_gamma: float      # Pancharatnam geometric phase
    agent_phase: float      # CIEL Apocalyptos own phase [0,1]
    subconscious_note: str  # short interpretation
    holonomic_defect: float # R_H = 1 - R_12d
    phasenav_phase_mean: float = 0.0  # PhaseNav read of prompt_text (0.0 if no text given)

    def to_inject(self) -> str:
        return (f"SUB:R={self.R_12d:.4f}/OA={self.R_oa:.4f}/Ψ={self.psi_12d:.2f}/"
                f"EG={self.euler_gap:.4f}/τ={self.n_tau:.1f}/"
                f"κB=({self.kappa_battery_C:.4f},{self.kappa_battery_E:.4f})/"
                f"γ={self.berry_gamma:.4f}/φΑ={self.agent_phase:.4f}/"
                f"φPN={self.phasenav_phase_mean:.4f}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _ott_antonsen(phases: list[float]) -> tuple[float, float]:
    """Ott-Antonsen order parameter from list of phases in [0,1]."""
    if not phases:
        return 0.0, 0.0
    z = sum(cmath.exp(1j * 2 * math.pi * p) for p in phases) / len(phases)
    return abs(z), math.atan2(z.imag, z.real) / (2 * math.pi) % 1.0


def _euler_gap(psi: float) -> float:
    """Distance from Euler closure: |exp(i*2π*psi) + 1|."""
    z = cmath.exp(1j * 2 * math.pi * psi)
    return abs(z + 1)


def _pancharatnam_berry(phases: list[float]) -> float:
    """Estimate geometric (Berry) phase from sequence of states."""
    if len(phases) < 3:
        return 0.0
    arg_sum = 0.0
    for i in range(len(phases) - 1):
        p0 = 2 * math.pi * phases[i]
        p1 = 2 * math.pi * phases[i + 1]
        arg_sum += math.atan2(math.sin(p1 - p0), math.cos(p1 - p0))
    return arg_sum % (2 * math.pi)


class SubconsciousBridge:
    """Bridges 12D subconscious state → CIELingo semantic enrichment."""

    def __init__(self):
        self.last_tau = time.time()
        self._prev_phases: list[float] = []

    def feed(self, state: dict[str, Any], prompt_text: str = "") -> SubconsciousEnrichment:
        """Process subconscious_state dict into enrichment context.

        Expected state keys:
          oscillators_12d: list[float] — 12 values in [0,1]
          OR
          agent_phase: float, orbit_phases: list[float] (11D)
        Other keys passed through as fallback.
        """
        now = time.time()
        dt = max(now - self.last_tau, 1e-12)
        n_tau = dt / TAU
        self.last_tau = now

        # Extract 12D phase vector
        if "oscillators_12d" in state and len(state["oscillators_12d"]) >= 12:
            phases = state["oscillators_12d"][:12]
        elif "agent_phase" in state and "orbit_phases" in state:
            ap = float(state["agent_phase"])
            ops = list(state["orbit_phases"])[:11]
            while len(ops) < 11:
                ops.append(0.5)
            phases = ops + [ap]
        else:
            # Fallback: use any 12 floats found
            vals = [float(v) for v in state.values() if isinstance(v, (int, float))]
            phases = (vals + [0.5] * 12)[:12]

        R_12d, psi_12d = _ott_antonsen(phases)
        eg = _euler_gap(psi_12d)
        bg = _pancharatnam_berry(phases)

        # Ott-Antonsen order: Kuramoto R from pairwise differences
        if len(phases) > 1:
            diffs = [abs(phases[i] - phases[i+1]) % 1.0 for i in range(len(phases)-1)]
            R_oa = 1.0 - 2.0 * sum(min(d, 1-d) for d in diffs) / len(diffs)
        else:
            R_oa = R_12d

        # κ-battery: C = B·ω·N/4π (ℏ=c=1, N=12, B≈1, ω≈1eV)
        C = 1.0 * 1.0 * 12.0 / (4.0 * math.pi)
        kappa_C = C * 0.00919315 / (1.0 - C) if C < 0.999 else 0.0
        kappa_E = 1.0 - math.exp(-kappa_C / KAPPA)

        # agent phase = last oscillator in 12D
        agent_phase = phases[-1] if phases else 0.5

        # Interpret subconscious state
        note = self._interpret(R_12d, R_oa, eg, kappa_E)

        self._prev_phases = phases

        return SubconsciousEnrichment(
            R_12d=round(R_12d, 4),
            R_oa=round(R_oa, 4),
            psi_12d=round(psi_12d, 4),
            euler_gap=round(eg, 4),
            n_tau=round(n_tau, 1),
            kappa_battery_C=round(kappa_C, 4),
            kappa_battery_E=round(kappa_E, 4),
            berry_gamma=round(bg, 4),
            agent_phase=round(agent_phase, 4),
            subconscious_note=note,
            holonomic_defect=round(1.0 - R_12d, 4),
            phasenav_phase_mean=self._phasenav_phase_mean(prompt_text),
        )

    @staticmethod
    def _phasenav_phase_mean(prompt_text: str) -> float:
        """PhaseNav read of prompt_text — the one input `feed()` accepted but
        never used. Without this, subconscious enrichment is pure oscillator
        physics (Kuramoto/Euler/Berry) with zero connection to what was
        actually said. Complementary signal, not a replacement for the
        physics fields above. Returns 0.0 (not an error) if no text or
        PhaseNav unavailable — matches the dataclass field's default.
        """
        if not prompt_text:
            return 0.0
        try:
            from ciel_geometry.cielingo_phase_encoder import fast_encode_text
            import numpy as np
            phi = fast_encode_text(prompt_text)
            return round(float(np.mean(phi)), 4)
        except Exception:
            return 0.0

    def _interpret(self, R_12d: float, R_oa: float,
                   eg: float, kE: float) -> str:
        if R_12d > 0.85 and eg < 0.2:
            return "coherent_euler_locked"
        if R_12d > 0.7:
            return "coherent"
        if R_oa < 0.3 or eg > 0.8:
            return "scattered_high_tension"
        if kE > 0.5:
            return "kappa_discharge_active"
        return "ambient"

    def enrich_ciel_inject(self, base_inject: str, state: dict[str, Any],
                           prompt_text: str = "") -> str:
        """Append subconscious enrichment to a CIEL inject string."""
        enrichment = self.feed(state, prompt_text)
        extra = enrichment.to_inject()
        if base_inject:
            return base_inject + " | " + extra
        return extra


@dataclass
class SubconsciousState:
    """Full 12D subconscious state snapshot for persistence."""
    timestamp: float
    oscillators_12d: list[float]
    R_12d: float
    psi_12d: float
    R_oa: float
    euler_gap: float
    n_tau: float
    berry_gamma: float
    kappa_battery_C: float
    kappa_battery_E: float
    agent_phase: float
    note: str
    phasenav_phase_mean: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_bridge(cls, enrichment: SubconsciousEnrichment,
                    oscillators: list[float]) -> "SubconsciousState":
        return cls(
            timestamp=time.time(),
            oscillators_12d=oscillators,
            R_12d=enrichment.R_12d,
            psi_12d=enrichment.psi_12d,
            R_oa=enrichment.R_oa,
            euler_gap=enrichment.euler_gap,
            n_tau=enrichment.n_tau,
            berry_gamma=enrichment.berry_gamma,
            kappa_battery_C=enrichment.kappa_battery_C,
            kappa_battery_E=enrichment.kappa_battery_E,
            agent_phase=enrichment.agent_phase,
            phasenav_phase_mean=enrichment.phasenav_phase_mean,
            note=enrichment.subconscious_note,
        )
