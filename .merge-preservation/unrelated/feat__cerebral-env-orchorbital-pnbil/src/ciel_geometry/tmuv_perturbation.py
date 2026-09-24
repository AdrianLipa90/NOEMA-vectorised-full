"""T_μν stress-energy perturbation bridge for CIEL orbital dynamics.

Connects the stress-energy tensor from ciel0_framework.py to the N-body
orbital engine (nbody_gravity.py) via an effective mass perturbation.

The T_μν tensor (matter + intention) from the unified CIEL/0 field theory
modifies each orbital body's effective gravitational mass:

    M_eff = M_sem + α · ΔM_Tμν

where ΔM_Tμν is the integrated energy density from T_μν projected onto
each orbital body's phase-space neighborhood.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import math
from typing import Any

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/tmuv_perturbation.py:23 quiet except scope=<module> reason=assign_fallback")
    HAS_NUMPY = False


# Coupling strength: how much T_μν energy density affects M_eff
ALPHA_TMUV: float = 0.1

# Number of T_μν components (4×4 symmetric tensor)
T_COMPONENTS: int = 10


def tmuv_total_energy_density(
    T_matter: np.ndarray,
    T_intention: np.ndarray | None = None,
) -> np.ndarray:
    """Extract the T^00 (energy density) component from the stress-energy tensor.

    Args:
        T_matter: Matter stress-energy tensor [grid_x, grid_y, 4, 4] or [4, 4]
        T_intention: Optional intention stress-energy tensor [same shape]

    Returns:
        Total energy density scalar field [grid_x, grid_y] or scalar.
    """
    if not HAS_NUMPY:
        return np.array(0.0)

    T_total = T_matter.copy()
    if T_intention is not None:
        T_total = T_total + T_intention

    if T_total.ndim >= 3:
        return T_total[..., 0, 0]
    else:
        return T_total[0, 0]


def mass_perturbation_from_tmuv(
    energy_density: np.ndarray,
    body_x: float,
    body_y: float,
    body_z: float = 0.0,
    grid_extent: tuple[float, float, float, float] = (-1.0, 1.0, -1.0, 1.0),
    kernel_width: float = 0.1,
) -> float:
    """Compute ΔM_Tμν by integrating energy density around a body's position.

    Uses a Gaussian kernel to weight the T_μν energy density contribution
    based on proximity to the body's position in configuration space.

    Args:
        energy_density: 2D array of energy density on the CIEL grid.
        body_x, body_y, body_z: Body position (Poincaré disk coords).
        grid_extent: (xmin, xmax, ymin, ymax) of the T_μν grid.
        kernel_width: Width of the Gaussian sampling kernel.

    Returns:
        Scalar mass perturbation ΔM_Tμν.
    """
    if not HAS_NUMPY or energy_density.ndim < 2:
        return 0.0

    ny, nx = energy_density.shape
    xmin, xmax, ymin, ymax = grid_extent

    # Map body position to grid indices
    ix = (body_x - xmin) / (xmax - xmin) * (nx - 1)
    iy = (body_y - ymin) / (ymax - ymin) * (ny - 1)
    ix = int(round(max(0, min(nx - 1, ix))))
    iy = int(round(max(0, min(ny - 1, iy))))

    # Kernel half-width in grid units
    kw = max(1, int(round(kernel_width / ((xmax - xmin) / nx))))

    # Extract neighborhood
    i0, i1 = max(0, ix - kw), min(nx, ix + kw + 1)
    j0, j1 = max(0, iy - kw), min(ny, iy + kw + 1)
    patch = energy_density[j0:j1, i0:i1]

    # Simple integrated energy density
    dA = ((xmax - xmin) / nx) * ((ymax - ymin) / ny)
    delta_m = float(np.sum(patch)) * dA

    return delta_m


def compute_effective_masses(
    bodies: list[Any],
    T_matter: np.ndarray,
    T_intention: np.ndarray | None = None,
    alpha: float = ALPHA_TMUV,
    grid_extent: tuple[float, float, float, float] = (-1.0, 1.0, -1.0, 1.0),
) -> dict[str, float]:
    """Compute M_eff = M_sem + α · ΔM_Tμν for each body.

    Args:
        bodies: List of objects with .label, .x, .y, .mass attributes.
        T_matter: Matter T_μν grid from the CIEL/0 framework.
        T_intention: Optional intention T_μν grid.
        alpha: Coupling strength (default ALPHA_TMUV).
        grid_extent: Physical extent of the T_μν grid.

    Returns:
        Dict mapping body label → M_eff.
    """
    rho = tmuv_total_energy_density(T_matter, T_intention)

    effective = {}
    for b in bodies:
        delta = mass_perturbation_from_tmuv(
            rho, b.x, b.y, getattr(b, 'z', 0.0), grid_extent,
        )
        M_eff = b.mass + alpha * delta
        effective[b.label] = max(M_eff, 1e-9)

    return effective


def total_stress_energy_scalar(T_matter: np.ndarray,
                                T_intention: np.ndarray | None = None) -> float:
    """Total integrated stress-energy scalar (diagnostic).

    Returns the sum of all T_μν components as a single diagnostic value.
    """
    if not HAS_NUMPY:
        return 0.0
    T = T_matter.copy()
    if T_intention is not None:
        T += T_intention
    return float(np.sum(np.abs(T)))
