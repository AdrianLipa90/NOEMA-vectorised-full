"""CIEL/Ω Memory Architecture - Base Infrastructure

Phase-based memory system foundation. All memory channels M0-M7 share
common phase state representation and dynamics.

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from abc import ABC, abstractmethod
import numpy as np


@dataclass
class PhaseState:
    """Common phase state for memory channels M0-M7.
    
    All memory channels (except M8 audit) are phase oscillators with:
    - amplitude: significance/strength
    - phase: position in cycle [0, 2π)
    - inertia: resistance to change
    - damping: energy dissipation
    - reliability: coherence/trustworthiness
    
    State evolves according to coupled dynamics with identity attractor.
    """
    
    amplitude: float      # a_k - significance
    phase: float         # γ_k - phase angle [0, 2π)
    inertia: float       # μ_k - resistance to change
    damping: float       # η_k - energy dissipation  
    reliability: float   # ρ_k - coherence
    
    def __post_init__(self):
        """Normalize phase to [0, 2π)"""
        self.phase = self.phase % (2 * np.pi)
        
    def phasor(self) -> complex:
        """Returns phasor representation a_k * e^(iγ_k)"""
        return self.amplitude * np.exp(1j * self.phase)
    
    def distance_to(self, other: PhaseState) -> float:
        """Phase distance to another state (geometric on circle)"""
        delta = abs(self.phase - other.phase)
        return min(delta, 2 * np.pi - delta)
    
    def coherence_with(self, other: PhaseState) -> float:
        """Coherence measure: cos(γ_k - γ_j) weighted by amplitudes"""
        delta = self.phase - other.phase
        return (self.amplitude * other.amplitude * 
                np.cos(delta) / (self.amplitude + other.amplitude + 1e-10))
    
    def evolve_first_order(self, force: float, dt: float) -> PhaseState:
        """First-order evolution: dγ/dt = F
        
        Used for fast channels: M0, M1, M5
        """
        new_phase = (self.phase + force * dt) % (2 * np.pi)
        return PhaseState(
            amplitude=self.amplitude,
            phase=new_phase,
            inertia=self.inertia,
            damping=self.damping,
            reliability=self.reliability
        )
    
    def evolve_second_order(self, force: float, velocity: float, dt: float) -> tuple[PhaseState, float]:
        """Second-order evolution: μ d²γ/dt² = F - η dγ/dt
        
        Used for slow channels: M2, M3, M4, M6, M7
        Returns (new_state, new_velocity)
        """
        acceleration = (force - self.damping * velocity) / self.inertia
        new_velocity = velocity + acceleration * dt
        new_phase = (self.phase + new_velocity * dt) % (2 * np.pi)
        
        return (PhaseState(
            amplitude=self.amplitude,
            phase=new_phase,
            inertia=self.inertia,
            damping=self.damping,
            reliability=self.reliability
        ), new_velocity)


@dataclass
class MemoryChannelParams:
    """Parameters defining a memory channel's behavior.
    
    Based on disk-radial model:
    - Inner channels (small r) are slow, stable, tightly coupled to identity
    - Outer channels (large r) are fast, plastic, weakly coupled
    """
    
    channel_id: int           # 0-7 for M0-M7
    name: str                 # Descriptive name
    radius: float            # r_k - distance from identity attractor [0,1]
    tau: float               # τ_k - relaxation time scale
    coupling_strength: float  # g_k - coupling to identity [0,1]
    max_drift: float         # δ_max - maximum allowed phase drift [radians]
    alignment_cost: float    # α_k - cost of misalignment with identity
    order: int               # 1 or 2 - evolution order
    
    def __post_init__(self):
        """Validate parameters"""
        assert 0 <= self.radius <= 1, f"Radius must be in [0,1], got {self.radius}"
        assert 0 <= self.coupling_strength <= 1, f"Coupling must be in [0,1]"
        assert self.tau > 0, f"Tau must be positive, got {self.tau}"
        assert self.order in [1, 2], f"Order must be 1 or 2, got {self.order}"


# Standard channel parameters — emergentne z concept registry zamiast hardcoded
def _build_channel_params() -> Dict[int, MemoryChannelParams]:
    """Φ emergencja: parametry kanałów z MEMORY_CHANNELS domain w registry."""
    from ciel_geometry.arbitrariness_resolver import Φ_channel_params
    raw = Φ_channel_params()
    result = {}
    for cid in range(8):
        p = raw.get(cid, {})
        result[cid] = MemoryChannelParams(
            channel_id=cid,
            name=p.get("name", f"M{cid}"),
            radius=p.get("radius", 0.5),
            tau=p.get("tau", 10.0),
            coupling_strength=p.get("coupling_strength", 0.5),
            max_drift=p.get("max_drift", 0.5),
            alignment_cost=p.get("alignment_cost", 0.5),
            order=p.get("order", 2),
        )
    return result


CHANNEL_PARAMS = _build_channel_params()


class BaseMemoryChannel(ABC):
    """Abstract base for all memory channels M0-M7.
    
    Each channel maintains phase state and evolves according to
    coupled dynamics with other channels and identity field.
    """
    
    def __init__(self, params: MemoryChannelParams, initial_state: Optional[PhaseState] = None):
        self.params = params
        self.state = initial_state or PhaseState(
            amplitude=0.1,
            phase=0.0,
            inertia=params.tau,
            damping=0.1 * params.tau,  # 10% critical damping
            reliability=0.5
        )
        self.velocity = 0.0  # For second-order channels
        self.anchor_phase = self.state.phase  # For drift calculation
        
    @abstractmethod
    def compute_input_force(self, input_data: Any) -> float:
        """Compute force from external input.
        
        Different channels process input differently:
        - M0: direct sensory mapping
        - M1: context integration
        - M2: episode formation
        - etc.
        """
        pass
    
    @abstractmethod
    def store(self, content: Any, metadata: Optional[Dict] = None) -> None:
        """Store content in channel-specific format"""
        pass
    
    @abstractmethod
    def retrieve(self, query: Any) -> Any:
        """Retrieve content from channel"""
        pass
    
    def evolve(self, total_force: float, dt: float) -> None:
        """Evolve channel state by timestep dt.
        
        Uses first or second order dynamics depending on channel parameters.
        """
        if self.params.order == 1:
            self.state = self.state.evolve_first_order(total_force, dt)
        else:
            self.state, self.velocity = self.state.evolve_second_order(
                total_force, self.velocity, dt
            )
    
    def get_drift_from_anchor(self) -> float:
        """Calculate phase drift from anchor point"""
        delta = abs(self.state.phase - self.anchor_phase)
        return min(delta, 2 * np.pi - delta)
    
    def update_anchor(self) -> None:
        """Update anchor to current phase (after consolidation)"""
        self.anchor_phase = self.state.phase
    
    def check_stability(self) -> bool:
        """Check if drift is within allowed bounds"""
        return self.get_drift_from_anchor() <= self.params.max_drift


class IdentityField:
    """Identity attractor at center of memory disk.

    This is not a memory channel itself, but the organizing center
    around which all memories orbit. Defined by anchors, commitments,
    and stable phase.

    attractor_vector: 3D point in Bloch sphere space that IS the identity
    center — the origin around which WΩ sector centroids are defined.
    It is NOT a state on the surface (norm != 1), but the gravitational
    center inside the sphere. Starts at (0,0,0) and accumulates drift
    from session history via pull_toward_attractor().
    """

    def __init__(self, initial_phase: float = 0.0,
                 attractor_vector: Optional[np.ndarray] = None):
        self.phase = initial_phase  # γ_I
        self.anchors: list[str] = []
        self.commitments: Dict[str, float] = {}
        self.epistemic_rules: Dict[str, Any] = {}
        # 3D identity attractor — geometric center, NOT a surface state
        self.attractor_vector: np.ndarray = (
            attractor_vector.astype(np.float32)
            if attractor_vector is not None
            else np.zeros(3, dtype=np.float32)
        )

    def alignment_force(self, channel_phase: float, coupling_strength: float) -> float:
        """Compute force pulling channel toward identity phase.

        F_align = g_k * sin(γ_I - γ_k)
        """
        delta = self.phase - channel_phase
        return coupling_strength * np.sin(delta)

    def pull_toward_attractor(self, bloch_vec: np.ndarray, lr: float = 0.01) -> None:
        """Update attractor_vector toward a new Bloch surface point.

        Called when identity-sector memory is encoded. The attractor
        accumulates the weighted history of identity-tagged states.
        lr is intentionally small — identity center moves very slowly.
        """
        self.attractor_vector += lr * (bloch_vec.astype(np.float32) - self.attractor_vector)

    def attractor_pull_force(self, bloch_vec: np.ndarray) -> float:
        """Scalar gravitational pull: how strongly bloch_vec is drawn to center.

        Returns value in [0, 1]: 1 = bloch_vec is at attractor, 0 = orthogonal.
        Used to weight sector assignments — states near the attractor belong
        more to 'identity' sector regardless of WΩ cosine similarity.
        """
        norm_ia = float(np.linalg.norm(self.attractor_vector))
        if norm_ia < 1e-9:
            return 0.0  # attractor not yet initialized
        ia_dir = self.attractor_vector / norm_ia
        dot = float(np.dot(ia_dir, bloch_vec.astype(np.float32)))
        return max(0.0, dot)

    def update_phase(self, new_phase: float) -> None:
        """Update identity phase (very slow process)"""
        self.phase = new_phase % (2 * np.pi)


__all__ = [
    'PhaseState',
    'MemoryChannelParams', 
    'CHANNEL_PARAMS',
    'BaseMemoryChannel',
    'IdentityField',
]
