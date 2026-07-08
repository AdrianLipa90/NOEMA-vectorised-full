"""N-body Newtonian gravitational engine for CIEL orbital dynamics.

Extends the single-body Kepler III (T² = a³/M_sem) with pairwise
gravitational forces F_ij = -G_sem · M_i · M_j / r²_ij.

Uses leapfrog Verlet integration for symplectic stability.

G_sem is the semantic gravitational constant (dimensionless analog),
distinct from the physical G = 6.67430e-11 in ciel0_framework.py.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable


G_SEM: float = 0.42
"""Semantic gravitational constant for CIEL N-body dynamics."""

SOFTENING: float = 1e-6
"""Softening parameter to prevent singularities at r → 0."""

DEFAULT_DT: float = 1e-3
"""Default integration time step."""


@dataclass
class Body:
    """A single massive body in the N-body system.

    Each Body corresponds to a CIEL semantic entity with M_sem mass,
    positioned on the Poincaré disk (x, y) with optional z for 3D.
    """
    label: str
    mass: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0

    ax: float = 0.0
    ay: float = 0.0
    az: float = 0.0

    @property
    def r(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    @property
    def v(self) -> float:
        return math.sqrt(self.vx**2 + self.vy**2 + self.vz**2)

    @property
    def ke(self) -> float:
        return 0.5 * self.mass * self.v**2


@dataclass
class NBodySystem:
    """N-body gravitational system with leapfrog integration."""

    bodies: list[Body] = field(default_factory=list)
    G: float = G_SEM
    softening: float = SOFTENING
    dt: float = DEFAULT_DT
    t: float = 0.0

    # Diagnostics
    E_kin_history: list[float] = field(default_factory=list)
    E_pot_history: list[float] = field(default_factory=list)

    def add_body(self, body: Body) -> None:
        self.bodies.append(body)

    def _compute_accelerations(self) -> None:
        """Compute pairwise gravitational accelerations for all bodies."""
        n = len(self.bodies)
        for i in range(n):
            ax_i = 0.0
            ay_i = 0.0
            az_i = 0.0
            bi = self.bodies[i]
            for j in range(n):
                if i == j:
                    continue
                bj = self.bodies[j]
                dx = bj.x - bi.x
                dy = bj.y - bi.y
                dz = bj.z - bi.z
                r2 = dx*dx + dy*dy + dz*dz + self.softening**2
                inv_r3 = 1.0 / (r2 * math.sqrt(r2))
                ax_i += self.G * bj.mass * dx * inv_r3
                ay_i += self.G * bj.mass * dy * inv_r3
                az_i += self.G * bj.mass * dz * inv_r3
            bi.ax, bi.ay, bi.az = ax_i, ay_i, az_i

    def _total_potential(self) -> float:
        """Compute total gravitational potential energy."""
        n = len(self.bodies)
        U = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                bi = self.bodies[i]
                bj = self.bodies[j]
                dx = bj.x - bi.x
                dy = bj.y - bi.y
                dz = bj.z - bi.z
                r = math.sqrt(dx*dx + dy*dy + dz*dz + self.softening**2)
                U -= self.G * bi.mass * bj.mass / r
        return U

    def _total_kinetic(self) -> float:
        return sum(b.ke for b in self.bodies)

    def step(self, dt: float | None = None) -> None:
        """Advance the system by one time step using leapfrog Verlet.

        Velocity-Verlet variant for symplectic integration:
          1. v(t + dt/2) = v(t) + a(t) · dt/2
          2. x(t + dt)   = x(t) + v(t + dt/2) · dt
          3. a(t + dt)   = computed from x(t + dt)
          4. v(t + dt)   = v(t + dt/2) + a(t + dt) · dt/2
        """
        if dt is None:
            dt = self.dt

        # 1. Half-step velocities
        for b in self.bodies:
            b.vx += 0.5 * b.ax * dt
            b.vy += 0.5 * b.ay * dt
            b.vz += 0.5 * b.az * dt

        # 2. Full-step positions
        for b in self.bodies:
            b.x += b.vx * dt
            b.y += b.vy * dt
            b.z += b.vz * dt

        # 3. Compute new accelerations
        self._compute_accelerations()

        # 4. Half-step velocities (completion)
        for b in self.bodies:
            b.vx += 0.5 * b.ax * dt
            b.vy += 0.5 * b.ay * dt
            b.vz += 0.5 * b.az * dt

        self.t += dt

    def evolve(self, steps: int, record_energy: bool = False) -> None:
        """Evolve the system for a given number of steps."""
        for _ in range(steps):
            self.step()
            if record_energy:
                self.E_kin_history.append(self._total_kinetic())
                self.E_pot_history.append(self._total_potential())

    def energy_error(self) -> float:
        """Fractional energy drift as a stability metric."""
        if not self.E_kin_history:
            return 0.0
        E_total = [k + p for k, p in
                   zip(self.E_kin_history, self.E_pot_history)]
        E0 = E_total[0] if E_total else 1.0
        return abs(max(E_total) - min(E_total)) / abs(E0) if E0 != 0 else 0.0

    def orbital_elements(self, label: str, central_label: str | None = None
                         ) -> dict[str, float]:
        """Compute Keplerian orbital elements for a body.

        If central_label is given, computes elements w.r.t. that body;
        otherwise w.r.t. the system barycenter.
        """
        body = next((b for b in self.bodies if b.label == label), None)
        if body is None:
            return {}

        if central_label:
            central = next((b for b in self.bodies
                            if b.label == central_label), None)
            if central is None:
                return {}
            dx = body.x - central.x
            dy = body.y - central.y
            dz = body.z - central.z
            dvx = body.vx - central.vx
            dvy = body.vy - central.vy
            dvz = body.vz - central.vz
            M = central.mass + body.mass
        else:
            M_total = sum(b.mass for b in self.bodies)
            cx = sum(b.x * b.mass for b in self.bodies) / M_total
            cy = sum(b.y * b.mass for b in self.bodies) / M_total
            cz = sum(b.z * b.mass for b in self.bodies) / M_total
            dx = body.x - cx
            dy = body.y - cy
            dz = body.z - cz
            dvx = body.vx
            dvy = body.vy
            dvz = body.vz
            M = M_total

        r = math.sqrt(dx*dx + dy*dy + dz*dz)
        v2 = dvx*dvx + dvy*dvy + dvz*dvz
        mu = self.G * M

        # Specific orbital energy
        epsilon = 0.5 * v2 - mu / max(r, self.softening)

        # Semi-major axis from vis-viva
        a = -mu / (2 * epsilon) if epsilon < 0 else float('inf')

        # Orbital period (Kepler III)
        T = 2 * math.pi * math.sqrt(a**3 / mu) if a != float('inf') else float('inf')

        return {
            "a": a,
            "T": T,
            "epsilon": epsilon,
            "r": r,
            "v": math.sqrt(v2),
            "mu": mu,
        }


def from_mass_table(
    mass_records: list,
    G: float = G_SEM,
    scale: float = 1.0,
) -> NBodySystem:
    """Build an NBodySystem from a SemanticMassRecord list.

    Each record's M_sem becomes the body mass. The orbit_radius from
    the Poincaré disk maps to the initial radial position.
    Angular velocity is set from the Kepler III period.
    """
    import random
    system = NBodySystem(G=G)
    for rec in mass_records:
        r = getattr(rec, 'orbit_radius', 1.0) * scale
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)

        # Keplerian circular velocity at this radius
        M_central = max(getattr(rec, 'M_sem', 1.0), 1e-9)
        v_circ = math.sqrt(G * M_central / max(r, 1e-6))

        body = Body(
            label=getattr(rec, 'label', str(rec)),
            mass=float(getattr(rec, 'M_sem', 1.0)),
            x=r * math.sin(phi) * math.cos(theta),
            y=r * math.sin(phi) * math.sin(theta),
            z=r * math.cos(phi),
            vy=v_circ,
        )
        system.add_body(body)
    return system
