#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RealityKernel.py — CIEL/0 Unified Reality Kernel (COMPREHENSIVE, single-file, no FFT/QFT)

This file wires together, in real space:
  • Analog wave PDE (no FFT/QFT) + Schrödinger quantization (Heisenberg-seeded)
  • Paradox stack: Collatz rhythm, cymatic resonators, ζ-topological protection, Banach–Tarski recomposition
  • Λ0 & weak-relativistic coupling (Λ-plasma–inspired)
  • Neutrino flavor oscillations (PMNS) — probabilities in time/baseline
  • Intention–fermions: intention current from wavefunction & feedback potential
  • Fluid-time hydrodynamics: continuity + Euler + chronon perturbations (real-space)
  • Anchors/symbolic JSON integration → spatial potential modulation (gaussian kernels)
  • Engine modes (analog, quantized, paradox, relativistic, neutrino, intentionfermions, fluidtime, ultimate)
  • Metrics & lightweight console visualization

Design goals:
  • Deterministic, bounded, numerically cautious. All stencils are local FD with periodic boundaries.
  • Clear extension points (TODOs) where your exact PDF constants/forms can be dropped in.
  • One file, strong interfaces, no hidden dependencies.

Author (concept): Adrian Lipa
Assembly (code): assistant
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

from dataclasses import dataclass
from typing import Tuple, Dict, List, Optional
import numpy as np
import argparse, json

# =============================================================================
# 1) CONSTANTS & CORE OPS
# =============================================================================

@dataclass
class CIELPhysics:
    """SI constants, Planck scales, numerics safeguards shared by all modules."""
    # Fundamental constants (SI)
    c: float   = 299_792_458.0
    hbar: float= 1.054_571_817e-34
    G: float   = 6.67430e-11
    mu0: float = 4e-7*np.pi
    eps0: float= 8.854_187_8128e-12

    # Planck scales
    Lp: float  = 1.616_255e-35
    tp: float  = 5.391_247e-44
    mp: float  = 2.176_434e-8

    # Numerics
    eps: float = 1e-12
    clip: float= 1e8
    cfl: float = 0.45

def Lambda0(B: float, rho: float, L: float, p: CIELPhysics) -> float:
    """
    Λ0-like emergent curvature coupling (Λ-plasma heuristic).
    Units target: m^-2 (weak-curvature surrogate used in RelativisticCoupler).
    Adjust prefactors to your PDF’s exact expression as needed.
    """
    if rho <= 0 or L <= 0: return 0.0
    return (B*B)/(p.mu0*max(rho, p.eps)*p.c**2) * (1.0/max(L, p.eps)**2)

# --------- Finite-difference primitives (periodic) ---------

def rollp(a, axis): return np.roll(a, +1, axis=axis)
def rollm(a, axis): return np.roll(a, -1, axis=axis)

def lap3(F: np.ndarray, dx: float) -> np.ndarray:
    """3D 2nd-order Laplacian (periodic)."""
    return (
        rollp(F,0)+rollm(F,0)+
        rollp(F,1)+rollm(F,1)+
        rollp(F,2)+rollm(F,2)-6.0*F
    )/(dx*dx)

def grad3(F: np.ndarray, dx: float) -> Tuple[np.ndarray,np.ndarray,np.ndarray]:
    """3D central gradient (periodic)."""
    fx = (rollm(F,0)-rollp(F,0))/(2*dx)
    fy = (rollm(F,1)-rollp(F,1))/(2*dx)
    fz = (rollm(F,2)-rollp(F,2))/(2*dx)
    return fx, fy, fz

def div3(vx: np.ndarray, vy: np.ndarray, vz: np.ndarray, dx: float) -> np.ndarray:
    """3D central divergence (periodic)."""
    dvx = (rollm(vx,0)-rollp(vx,0))/(2*dx)
    dvy = (rollm(vy,1)-rollp(vy,1))/(2*dx)
    dvz = (rollm(vz,2)-rollp(vz,2))/(2*dx)
    return dvx + dvy + dvz

def heisenberg_seed(shape: Tuple[int,int,int], scale: float, p: CIELPhysics) -> np.ndarray:
    """
    Vacuum-fluctuation seed respecting ΔE·Δt ≳ ħ/2 heuristically via noise level.
    'scale' can be linked to dt (Δt) in the main loop; here used as amplitude proxy.
    """
    sigma = np.sqrt(p.hbar/(2.0*max(scale, p.eps)))
    return (sigma*(np.random.normal(size=shape) + 1j*np.random.normal(size=shape))).astype(np.complex128)

# =============================================================================
# 2) WAVE & QUANTIZATION LAYERS
# =============================================================================

class AnalogWave:
    """
    Real-space wave equation via first-order system:
        ∂t ψ = Π
        ∂t Π = c^2 ∇^2 ψ
    Leapfrog-like explicit update (no FFT/QFT).
    """
    def __init__(self, c_eff: float):
        self.c2 = float(c_eff)**2
        self._pi = None

    def step(self, psi: np.ndarray, dt: float, dx: float) -> np.ndarray:
        if self._pi is None: self._pi = np.zeros_like(psi)
        self._pi = self._pi + dt*self.c2*lap3(psi, dx)
        psi_new = psi + dt*self._pi
        return psi_new

class Schrodinger:
    """Schrödinger evolution with optional real potential V(x)."""
    def __init__(self, p: CIELPhysics, mass: float=1.0):
        self.p, self.m = p, mass

    def step(self, psi: np.ndarray, dt: float, dx: float, V: np.ndarray|float=0.0) -> np.ndarray:
        lap = lap3(psi, dx)
        dpsi = (-1j*self.p.hbar/(2.0*self.m))*lap + (-1j/self.p.hbar)*(V*psi)
        out = psi + dt*dpsi
        n = np.linalg.norm(out.ravel())
        return out/n if n>0 else out

    @staticmethod
    def resonance(S: np.ndarray, I: np.ndarray) -> float:
        """R(S,I) = |⟨S|I⟩|² (global overlap)."""
        inner = np.vdot(S.ravel(), I.ravel())
        return float(np.abs(inner)**2)

    @staticmethod
    def collapse_max_overlap(psi: np.ndarray, I: np.ndarray) -> np.ndarray:
        score = np.abs(psi*np.conj(I))
        idx = np.unravel_index(np.argmax(score), psi.shape)
        out = np.zeros_like(psi); out[idx] = 1.0+0j; return out

# =============================================================================
# 3) MATHEMATICAL SOUL (Ramanujan)
# =============================================================================

class RamanujanMath:
    """Safe, bounded Ramanujan-inspired modulations."""
    def ramanujan_sum(self, n: int) -> complex:
        corr = -1/12 + n*(n+1)/2
        return complex(np.clip(corr, -1e10, 1e10))

    def modular_forms_contribution(self, coords_sum: np.ndarray) -> np.ndarray:
        """
        Bounded complex modulation from truncated q-expansion + mock theta phase.
        Input: scalar field s = x+y+z (or any scalar coord sum).
        """
        s = np.clip(coords_sum, -10, 10)
        q = np.exp(1j*np.pi*s)
        j = 1/q + 744 + 196_884*q  # truncated J-invariant motif
        tame = np.tanh(np.real(j)/1e3)
        mock = np.exp(1j*0.3*np.sin(s))
        return tame*mock

# =============================================================================
# 4) NUMBER THEORY: COLLATZ + CYMATICS + TWIN PRIME RHYTHM (cymatics)
# =============================================================================

class CollatzLayer:
    """Collatz length-based scalar rhythm (smooth decay exp(-len/50))."""
    def __init__(self, cap: int=1000):
        self.cap, self.cache = cap, {}

    def length(self, n: int) -> int:
        if n in self.cache: return self.cache[n]
        x, s = n, 0
        while x != 1 and s < self.cap:
            x = (x//2) if (x%2==0) else (3*x+1); s += 1
        self.cache[n] = s; return s

    def field(self, shape: Tuple[int,...]) -> np.ndarray:
        idx = np.arange(np.prod(shape), dtype=int).reshape(shape) + 1
        vlen = np.vectorize(self.length)(idx)
        return np.exp(-vlen/50.0).astype(float)

class CymaticLayer:
    """Standing-wave resonators in a cuboid volume + optional radial blend."""
    def __init__(self, Lx: float, Ly: float, Lz: float, modes: Optional[List[Tuple[int,int,int]]]=None, radial_mix: float=0.25):
        self.Lx, self.Ly, self.Lz = Lx, Ly, Lz
        self.modes = modes or [(1,1,1),(1,2,2),(2,1,2),(2,2,3)]
        self.radial_mix = float(np.clip(radial_mix,0.0,1.0))

    def _cartesian(self, X,Y,Z):
        pat = np.zeros_like(X, dtype=float)
        for nx,ny,nz in self.modes:
            pat += np.sin(nx*np.pi*(X/self.Lx))*np.sin(ny*np.pi*(Y/self.Ly))*np.sin(nz*np.pi*(Z/self.Lz))
        pat -= pat.min()
        rng = pat.max() - 1e-30
        return pat/rng

    def _radial(self, X,Y,Z):
        r = np.sqrt(X*X + Y*Y + Z*Z)
        k = (np.pi/min(self.Lx,self.Ly,self.Lz))*2.5
        w = np.cos(np.clip(k*r, 0, 10.0))
        w -= w.min(); w /= (w.max()-1e-30)
        return w

    def field(self, X,Y,Z) -> np.ndarray:
        cart = self._cartesian(X,Y,Z); rad = self._radial(X,Y,Z)
        return (1-self.radial_mix)*cart + self.radial_mix*rad

# =============================================================================
# 5) TOPOLOGICAL PROTECTION (Riemann ζ zeros)
# =============================================================================

class RiemannZetaProtection:
    """ζ-zero driven complex protection phase (bounded)."""
    ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073]
    def field(self, X,Y,Z) -> np.ndarray:
        r = np.sqrt(X*X + Y*Y + Z*Z)
        P = 0.0j
        for t in self.ZEROS:
            ph = t*np.clip(r,0,100)
            P += (np.sin(ph)+1j*np.cos(ph))/(t*t+1.0)
        # Use phase of sum → unit magnitude
        return np.exp(1j*np.angle(P))

# =============================================================================
# 6) BANACH–TARSKI (safe, array-stable recomposition)
# =============================================================================

class BanachTarski:
    """Paradoxical decompose/recombine (deterministic roll-per-piece)."""
    def decompose(self, field: np.ndarray, n_pieces: int=5) -> List[np.ndarray]:
        flat = field.flatten(); N = flat.size; size = max(1, N//n_pieces)
        pieces=[]
        for i in range(n_pieces):
            s = i*size; e = (i+1)*size if i<n_pieces-1 else N
            buf = flat[s:e].copy()
            shift = (i+1) % max(1, buf.size)
            piece = np.zeros_like(flat); piece[s:e] = np.roll(buf, shift)
            pieces.append(piece.reshape(field.shape))
        return pieces

    def recombine(self, pieces: List[np.ndarray]) -> np.ndarray:
        if not pieces: return np.array([])
        acc = np.zeros_like(pieces[0], dtype=pieces[0].dtype)
        for p in pieces: acc += p
        return acc/max(1,len(pieces))

# =============================================================================
# 7) RELATIVISTIC COUPLER (Λ0 weak-curvature surrogate)
# =============================================================================

class RelativisticCoupler:
    """
    Weak-curvature dispersion modulation via Λ0 & geometric potential Vgeom.
    Intended as a Λ-plasma–inspired surrogate; plug your exact Lagrangian constants here.
    """
    def __init__(self, p: CIELPhysics): self.p = p

    def step(self, psi: np.ndarray, dt: float, dx: float, lam0: float, Vgeom: np.ndarray) -> np.ndarray:
        kappa = float(np.tanh(lam0 * dx*dx))     # bounded curvature factor
        lap = lap3(psi, dx)
        dpsi = (-1j*self.p.hbar/2.0)*(1.0+kappa)*lap + (-1j/self.p.hbar)*(Vgeom*psi)
        out = psi + dt*dpsi
        n = np.linalg.norm(out.ravel())
        return out/n if n>0 else out

# =============================================================================
# 8) NEUTRINO FLAVORS (PMNS oscillations)
# =============================================================================

class FlavorState:
    """Three-flavor neutrino state |ν> = (ν_e, ν_μ, ν_τ) with PMNS mixing & vacuum phases."""
    def __init__(self, theta12=33.44*np.pi/180, theta23=49.2*np.pi/180, theta13=8.57*np.pi/180,
                 delta_cp=195*np.pi/180, dm21=7.42e-5, dm31=2.517e-3, E_GeV: float=0.6):
        s12,c12 = np.sin(theta12), np.cos(theta12)
        s23,c23 = np.sin(theta23), np.cos(theta23)
        s13,c13 = np.sin(theta13), np.cos(theta13)
        δ = delta_cp
        self.U = np.array([
            [c12*c13, s12*c13, s13*np.exp(-1j*δ)],
            [-s12*c23 - c12*s23*s13*np.exp(1j*δ),
             c12*c23 - s12*s23*s13*np.exp(1j*δ),
             s23*c13],
            [s12*s23 - c12*c23*s13*np.exp(1j*δ),
             -c12*s23 - s12*c23*s13*np.exp(1j*δ),
             c23*c13]
        ], dtype=complex)
        self.dm21, self.dm31, self.E = dm21, dm31, E_GeV
        self.state = np.array([1+0j,0+0j,0+0j])  # pure ν_e initial

    def evolve_km(self, L_km: float):
        dm2 = np.array([0.0, self.dm21, self.dm31])
        mstate = np.conj(self.U.T) @ self.state
        phases = np.exp(-1j*1.267*dm2*L_km/max(self.E,1e-12))
        self.state = self.U @ (mstate*phases)

    def probabilities(self) -> np.ndarray:
        return np.real(np.abs(self.state)**2)

# =============================================================================
# 9) INTENTION–FERMIONS (current & feedback potential)
# =============================================================================

class IntentionFermions:
    """
    Intention current derived from ψ:
       J0 = |ψ|^2   (intention density)
       J  = (ħ/m) Im(ψ* ∇ψ) ≈ phase-gradient proxy (here scaled)
    Feedback potential V_intent = α·norm(J0) + β·(∇·J) (bounded)
    """
    def __init__(self, p: CIELPhysics, mass: float=1.0, alpha: float=0.15, beta: float=0.05, smooth: float=0.1):
        self.p, self.m = p, mass
        self.alpha, self.beta, self.smooth = alpha, beta, smooth
        self._J0 = None
        self._Jx = self._Jy = self._Jz = None

    def _phase_grad(self, psi: np.ndarray, dx: float) -> Tuple[np.ndarray,np.ndarray,np.ndarray]:
        phase = np.angle(psi + 0j)
        return grad3(phase, dx)

    def step(self, psi: np.ndarray, dt: float, dx: float) -> np.ndarray:
        J0 = np.abs(psi)**2
        gx,gy,gz = self._phase_grad(psi, dx)
        scale = self.p.hbar/max(self.m, self.p.eps)
        Jx, Jy, Jz = scale*J0*gx, scale*J0*gy, scale*J0*gz

        # optional smoothing (diffusive) for stability
        if self._J0 is None:
            self._J0 = J0.copy(); self._Jx, self._Jy, self._Jz = Jx.copy(), Jy.copy(), Jz.copy()
        self._J0 = (1-self.smooth)*self._J0 + self.smooth*J0
        self._Jx = (1-self.smooth)*self._Jx + self.smooth*Jx
        self._Jy = (1-self.smooth)*self._Jy + self.smooth*Jy
        self._Jz = (1-self.smooth)*self._Jz + self.smooth*Jz

        divJ = div3(self._Jx, self._Jy, self._Jz, dx)
        J0n  = self._J0/ (np.max(self._J0)+self.p.eps)
        Vint = np.clip(self.alpha*J0n + self.beta*divJ, -1.0, 1.0)  # bounded feedback
        return Vint

# =============================================================================
# 10) FLUID-TIME HYDRODYNAMICS (continuity + Euler + chronon)
# =============================================================================

@dataclass
class FluidTimeState:
    """Hydrodynamic state of 'time-fluid' τ(x): density ρτ, pressure pτ, velocity vτ, scalar τ, chronon χ & momentum πχ."""
    tau: np.ndarray
    rho: np.ndarray
    pres: np.ndarray
    vx:  np.ndarray
    vy:  np.ndarray
    vz:  np.ndarray
    chi: np.ndarray   # chronon perturbation
    pi_chi: np.ndarray

class FluidTime:
    """
    Minimal, stable real-space hydrodynamics of time:
      Continuity:  ∂t ρ + ∇·(ρ v) = 0
      Euler:       ∂t v + (v·∇)v = -∇p/ρ + F_ext + ν ∇² v
      EOS:         p = c_s^2 ρ   (compressible isothermal proxy)
      Chronon:     ∂t χ = π,  ∂t π = cχ² ∇² χ - γ π   (damped wave)
    """
    def __init__(self, p: CIELPhysics, cs: float=0.1, nu: float=0.01, gamma: float=0.05, c_chi: float=0.2):
        self.p = p
        self.cs2 = cs*cs     # sound speed^2
        self.nu  = nu        # kinematic viscosity
        self.gamma = gamma   # chronon damping
        self.cchi2 = c_chi*c_chi

    def step(self, st: FluidTimeState, dt: float, dx: float,
             Vext: Optional[np.ndarray]=None, coupling_scalar: Optional[np.ndarray]=None) -> FluidTimeState:
        rho, vx, vy, vz = st.rho, st.vx, st.vy, st.vz
        pres = self.cs2 * rho

        # Fluxes for continuity
        Fx, Fy, Fz = rho*vx, rho*vy, rho*vz
        drho = -div3(Fx, Fy, Fz, dx)

        # Pressure gradient
        dpx, dpy, dpz = grad3(pres, dx)
        invrho = 1.0/np.maximum(rho, self.p.eps)

        # Advection (v·∇)v approx with central diffs
        dvx_dx, dvx_dy, dvx_dz = grad3(vx, dx)
        dvy_dx, dvy_dy, dvy_dz = grad3(vy, dx)
        dvz_dx, dvz_dy, dvz_dz = grad3(vz, dx)
        adv_x = vx*dvx_dx + vy*dvx_dy + vz*dvx_dz
        adv_y = vx*dvy_dx + vy*dvy_dy + vz*dvy_dz
        adv_z = vx*dvz_dx + vy*dvz_dy + vz*dvz_dz

        # External force (from anchors/ψ etc.)
        Fx_ext = Fy_ext = Fz_ext = 0.0
        if Vext is not None:
            gx,gy,gz = grad3(Vext, dx)
            Fx_ext, Fy_ext, Fz_ext = -gx, -gy, -gz

        # Optional scalar coupling (e.g., |ψ|^2)
        if coupling_scalar is not None:
            cx,cy,cz = grad3(coupling_scalar, dx)
            Fx_ext += -0.05*cx; Fy_ext += -0.05*cy; Fz_ext += -0.05*cz

        # Viscosity
        lap_vx = lap3(vx, dx); lap_vy = lap3(vy, dx); lap_vz = lap3(vz, dx)

        # Momentum update
        dvx_dt = -adv_x - invrho*dpx + Fx_ext + self.nu*lap_vx
        dvy_dt = -adv_y - invrho*dpy + Fy_ext + self.nu*lap_vy
        dvz_dt = -adv_z - invrho*dpz + Fz_ext + self.nu*lap_vz

        # Apply updates
        rho_new = np.clip(rho + dt*drho, self.p.eps, None)
        vx_new  = vx  + dt*dvx_dt
        vy_new  = vy  + dt*dvy_dt
        vz_new  = vz  + dt*dvz_dt
        pres_new= self.cs2*rho_new

        # τ advection + mild diffusion (optional)
        tau_adv = vx*grad3(st.tau, dx)[0] + vy*grad3(st.tau, dx)[1] + vz*grad3(st.tau, dx)[2]
        tau_new = st.tau - dt*tau_adv + 0.05*dt*lap3(st.tau, dx)

        # Chronon damped wave
        pi_new  = st.pi_chi + dt*(self.cchi2*lap3(st.chi, dx) - self.gamma*st.pi_chi)
        chi_new = st.chi + dt*pi_new

        return FluidTimeState(tau_new, rho_new, pres_new, vx_new, vy_new, vz_new, chi_new, pi_new)

# =============================================================================
# 11) ANCHORS / SYMBOLIC JSON → POTENTIAL MAP
# =============================================================================

class Anchors:
    """
    Load anchor JSONs (Tesseract/Pineal, Drift, SigmaDream) and convert to a spatial potential map
    using Gaussian kernels centered at normalized points in [0,1]^3 with amplitudes.
    JSON schema (flexible):
      { "points": [ {"xyz": [0.1,0.4,0.7], "amp": 1.2, "sigma": 0.08}, ... ] }
    """
    def __init__(self):
        self.tesseract: Dict = {}
        self.drift: Dict     = {}
        self.sigma: Dict     = {}

    def load_paths(self, tesseract_path: Optional[str], drift_path: Optional[str], sigma_path: Optional[str]):
        def safe_load(path: Optional[str]) -> Dict:
            if not path: return {}
            try:
                with open(path, "r", encoding="utf-8") as f: return json.load(f)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/ResCxParKer_phone.py:454 quiet except scope=Anchors.load_paths.safe_load reason=return {}")
                return {}
        self.tesseract = safe_load(tesseract_path)
        self.drift     = safe_load(drift_path)
        self.sigma     = safe_load(sigma_path)

    @staticmethod
    def _add_points_potential(V: np.ndarray, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, conf: Dict, L: float):
        pts = conf.get("points", [])
        for pt in pts:
            xyz = pt.get("xyz", [0.5,0.5,0.5]); amp = float(pt.get("amp", 1.0)); sig = float(pt.get("sigma", 0.1))
            cx,cy,cz = [float(x)*L for x in xyz]
            r2 = (X-cx)**2 + (Y-cy)**2 + (Z-cz)**2
            V += amp*np.exp(-r2/(2*(sig*L+1e-12)**2))

    def potential(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, L: float) -> np.ndarray:
        V = np.zeros_like(X, dtype=float)
        for conf in (self.tesseract, self.drift, self.sigma):
            if conf: self._add_points_potential(V, X, Y, Z, conf, L)
        # normalize to [-1,1]
        V -= V.min(); mx = V.max() + 1e-30; Vn = 2.0*(V/mx) - 1.0
        return Vn

# =============================================================================
# 12) ENGINE (modes, wiring, metrics)
# =============================================================================

class RealityKernelEngine:
    """
    Central orchestrator: initializes grid & fields, calls module steps per mode, and reports metrics.
    """
    def __init__(self, n: int=32, L: float=1.0, mode: str="ultimate",
                 anchors: Optional[Anchors]=None, seed_scale: Optional[float]=None):
        self.n, self.L, self.mode = n, L, mode
        self.p = CIELPhysics()

        # Grid (periodic box [0,L)^3)
        xs = np.linspace(0.0, L, n, endpoint=False)
        self.X, self.Y, self.Z = np.meshgrid(xs, xs, xs, indexing="ij")
        self.dx = L/n

        # Fields
        self.psi = heisenberg_seed((n,n,n), scale=seed_scale or self.dx, p=self.p)  # complex
        self.I   = np.exp(1j*(2*np.pi/L)*(self.X + self.Y + self.Z))               # intention pattern (phase grating)

        # Modules
        self.wave = AnalogWave(c_eff=0.02*self.p.c)
        self.schr = Schrodinger(self.p, mass=1.0)
        self.ram  = RamanujanMath()
        self.coll = CollatzLayer()
        self.cym  = CymaticLayer(L, L, L)
        self.zeta = RiemannZetaProtection()
        self.bant = BanachTarski()
        self.relc = RelativisticCoupler(self.p)
        self.flav = FlavorState()
        self.ifrm = IntentionFermions(self.p, mass=1.0, alpha=0.15, beta=0.05, smooth=0.1)

        # Anchors
        self.anchors = anchors or Anchors()
        self.V_anchor = self.anchors.potential(self.X, self.Y, self.Z, L) if (self.anchors.tesseract or self.anchors.drift or self.anchors.sigma) else np.zeros_like(self.X)

        # Fluid-time initial state
        zeros = np.zeros((n,n,n), dtype=float)
        ones  = np.ones((n,n,n), dtype=float)
        self.ft = FluidTime(self.p, cs=0.15, nu=0.02, gamma=0.04, c_chi=0.25)
        self.ft_state = FluidTimeState(
            tau=zeros.copy(),
            rho=ones.copy(),
            pres=(0.15**2)*ones.copy(),
            vx=zeros.copy(), vy=zeros.copy(), vz=zeros.copy(),
            chi=zeros.copy(), pi_chi=zeros.copy()
        )

    # ---------- STEP METHODS PER MODE ----------

    def step_analog(self, dt: float):
        self.psi = self.wave.step(self.psi, dt, self.dx)

    def step_quantized(self, dt: float):
        self.psi = self.schr.step(self.psi, dt, self.dx, V=0.0)

    def step_paradox(self, dt: float):
        # Build composite potential from Collatz + Cymatics + Ramanujan + Anchors
        Vc     = self.coll.field(self.psi.shape)
        Vcym   = self.cym.field(self.X, self.Y, self.Z)
        s_coord= (self.X + self.Y + self.Z) - (3*self.L/2)
        Vram   = np.real(self.ram.modular_forms_contribution(s_coord))  # bounded in [-1,1]
        Vmix   = np.clip(0.35*Vc + 0.45*Vcym + 0.2*Vram + 0.3*self.V_anchor, -1.0, 1.0)

        # ζ-protection as phase guard
        Pz = self.zeta.field(self.X-self.L/2, self.Y-self.L/2, self.Z-self.L/2)
        self.psi = self.schr.step(self.psi*Pz, dt, self.dx, V=Vmix)

    def step_relativistic(self, dt: float, B: float, rho: float, Lc: float):
        lam0 = Lambda0(B, rho, Lc, self.p)
        Vgeom = np.clip(0.5*self.cym.field(self.X, self.Y, self.Z) + 0.5*self.V_anchor, -1.0, 1.0)
        self.psi = self.relc.step(self.psi, dt, self.dx, lam0, Vgeom)

    def step_neutrino(self, dt: float, baseline_km_inc: float):
        self.psi = self.schr.step(self.psi, dt, self.dx, V=0.0)
        self.flav.evolve_km(baseline_km_inc)

    def step_intentionfermions(self, dt: float):
        Vint = self.ifrm.step(self.psi, dt, self.dx)
        self.psi = self.schr.step(self.psi, dt, self.dx, V=Vint + 0.2*self.V_anchor)

    def step_fluidtime(self, dt: float):
        # Use |ψ|^2 as coupling scalar; anchors as external potential for time-fluid
        psi_density = np.abs(self.psi)**2
        self.ft_state = self.ft.step(self.ft_state, dt, self.dx, Vext=self.V_anchor, coupling_scalar=psi_density)

    def step_ultimate(self, dt: float, B: float, rho: float, Lc: float, baseline_km_inc: float):
        # 1) Paradox mix + ζ protection + anchor modulation
        self.step_paradox(dt)
        # 2) Relativistic curvature effect
        self.step_relativistic(dt, B, rho, Lc)
        # 3) Neutrino flavors
        self.flav.evolve_km(baseline_km_inc)
        # 4) Intention–fermions feedback
        Vint = self.ifrm.step(self.psi, dt, self.dx)
        self.psi = self.schr.step(self.psi, dt, self.dx, V=Vint)
        # 5) Fluid-time response
        self.step_fluidtime(dt)
        # Normalize ψ
        n = np.linalg.norm(self.psi.ravel()); 
        if n>0: self.psi /= n

    # ---------- METRICS ----------

    def metrics(self) -> Dict[str, float]:
        R = Schrodinger.resonance(self.psi, self.I)
        P_e, P_mu, P_tau = self.flav.probabilities()
        psi_energy = float(np.mean(np.abs(self.psi)**2))
        # Fluid quantities
        div_v = float(np.mean(np.abs(div3(self.ft_state.vx, self.ft_state.vy, self.ft_state.vz, self.dx))))
        rho_mean = float(np.mean(self.ft_state.rho))
        chi_level= float(np.mean(self.ft_state.chi**2))
        return {
            "R_SI": R,
            "P_nu_e": float(P_e), "P_nu_mu": float(P_mu), "P_nu_tau": float(P_tau),
            "psi_energy": psi_energy,
            "fluid_divV_mean": div_v,
            "fluid_rho_mean": rho_mean,
            "chronon_level": chi_level
        }

# =============================================================================
# 13) LIGHT VISUALIZATION (console)
# =============================================================================

class RealityVisualizer:
    @staticmethod
    def quick_summary(state: Dict[str, float]):
        print("=== Reality Kernel Metrics ===")
        for k in sorted(state.keys()):
            print(f"{k:>18s}: {state[k]:.6g}")

# =============================================================================
# 14) CLI
# =============================================================================

def main():
    ap = argparse.ArgumentParser(description="CIEL/0 Unified Reality Kernel — comprehensive, single-file, no FFT/QFT")
    ap.add_argument("--mode", choices=[
        "analog","quantized","paradox","relativistic","neutrino",
        "intentionfermions","fluidtime","ultimate"
    ], required=True)
    ap.add_argument("--n", type=int, default=32)
    ap.add_argument("--L", type=float, default=1.0)
    ap.add_argument("--steps", type=int, default=120)
    ap.add_argument("--dt", type=float, default=1e-4)

    # Λ0 params (for relativistic/ultimate)
    ap.add_argument("--B", type=float, default=1e-9)          # Tesla
    ap.add_argument("--rho", type=float, default=1e-26)       # kg/m^3
    ap.add_argument("--Lc", type=float, default=3.086e22)     # m  (~1 kpc)

    # neutrino baseline increment per step (km)
    ap.add_argument("--dLkm", type=float, default=295/120)    # ~T2K-like over 120 steps

    # Anchors (JSON)
    ap.add_argument("--tesseract", type=str, default=None)
    ap.add_argument("--drift", type=str, default=None)
    ap.add_argument("--sigma", type=str, default=None)

    args = ap.parse_args()

    # Anchors
    anchors = Anchors()
    anchors.load_paths(args.tesseract, args.drift, args.sigma)

    # Engine
    rk = RealityKernelEngine(n=args.n, L=args.L, mode=args.mode, anchors=anchors)

    # Time stepping
    for _ in range(args.steps):
        if args.mode == "analog":
            rk.step_analog(args.dt)
        elif args.mode == "quantized":
            rk.step_quantized(args.dt)
        elif args.mode == "paradox":
            rk.step_paradox(args.dt)
        elif args.mode == "relativistic":
            rk.step_relativistic(args.dt, args.B, args.rho, args.Lc)
        elif args.mode == "neutrino":
            rk.step_neutrino(args.dt, args.dLkm)
        elif args.mode == "intentionfermions":
            rk.step_intentionfermions(args.dt)
        elif args.mode == "fluidtime":
            rk.step_fluidtime(args.dt)
        elif args.mode == "ultimate":
            rk.step_ultimate(args.dt, args.B, args.rho, args.Lc, args.dLkm)

    # Metrics
    vis = RealityVisualizer()
    vis.quick_summary(rk.metrics())

if __name__ == "__main__":
    main()