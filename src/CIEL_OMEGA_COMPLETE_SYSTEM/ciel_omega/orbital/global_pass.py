"""Global orbital coherence pass used by the CIEL/Ω runtime loop.

The pass may run as a durable report writer or as a side-effect-bounded runtime
probe. Both modes return the same result schema, including sector diagnostics.
"""

from __future__ import annotations

import json
import logging
import math
import sys
from pathlib import Path
from typing import Any

from .dynamics import step
from .extract_geometry import build, repo_root_from_here
from .metrics import (
    chord_tension,
    closure_penalty,
    effective_phase_zeta,
    effective_tau_zeta,
    global_chirality,
    global_coherence,
    radial_spread,
    spectral_observables,
    total_relational_potential,
    zeta_coupling_norm,
    zeta_coupling_norm_raw,
    zeta_tetra_defect,
)
from .registry import load_system

_LOG = logging.getLogger(__name__)


def _param(system: Any, key: str, default: float) -> float:
    return float(system.params.get(key, default))


DEFAULT_PARAMS = {
    "dt": 0.0205,
    "tau_eta": 0.0085,
    "tau_reg": 0.0024,
    "sigma": 0.20992708860770198,
    "beta": 0.8858849039288708,
    "gamma": 0.3383621712598693,
    "I0": 0.008114359738066937,
    "mesh_boost": 0.9902072303068182,
    "tension_weight": 0.24841695319131418,
    "closure_weight": 0.08945494489662148,
    "use_zeta_pole": True,
    "zeta_coupling_scale": 0.35,
    "zeta_tetra_weight": 0.50,
    "zeta_amplitude": 0.35,
    "zeta_relax": 0.08,
    "zeta_global_rotation": 0.0,
    "zeta_heisenberg_alpha": 8.0,
    "zeta_i0_scale": 1.0,
    "use_relational_lagrangian": True,
    "kappa_H": 1.0,
    "lambda_tension": 0.15,
    "lambda_distortion": 1.0,
    "lambda_zeta_tetra": 1.0,
    "alpha_spin": 4.0,
    "mu_phi": 0.18,
    "mu_rho": 0.14,
    "epsilon_hom": 0.22,
    "spin_vorticity_gain": 0.20,
    "relax_amp": 0.28,
    "grad_eps": 1e-3,
    "use_euler_leak_rotation": True,
    "D_f": 2.57,
    "euler_angular_gain": 1.0,
    "zeta_phase0": 0.0,
}


def snapshot(system: Any) -> dict[str, Any]:
    spec = spectral_observables(system)
    snap: dict[str, Any] = {
        "R_H": global_coherence(system),
        "T_glob": chord_tension(system),
        "Lambda_glob": global_chirality(system),
        "closure_penalty": closure_penalty(system),
        "V_rel_total": total_relational_potential(system),
        "radial_spread": radial_spread(system),
        "mean_spin": sum(s.spin for s in system.sectors.values()) / max(1, len(system.sectors)),
        "spectral_radius_A": spec["spectral_radius_A"],
        "spectral_gap_A": spec["spectral_gap_A"],
        "fiedler_L": spec["fiedler_L"],
        "zeta_enabled": bool(system.zeta_pole is not None),
    }
    if system.zeta_pole is not None:
        snap.update(
            {
                "zeta_tetra_defect": zeta_tetra_defect(system),
                "zeta_effective_tau": effective_tau_zeta(system),
                "zeta_effective_phase": effective_phase_zeta(system),
                "zeta_coupling_norm": zeta_coupling_norm(system),
                "zeta_coupling_norm_raw": zeta_coupling_norm_raw(system),
                "zeta_spin": system.zeta_pole.spin,
                "zeta_rho": system.zeta_pole.rho,
                "D_f": _param(system, "D_f", 2.57),
                "euler_leak_angle": 0.5 * math.pi * (_param(system, "D_f", 2.57) - 2.0),
            }
        )
    return snap


def _sector_diagnostics(system: Any) -> dict[str, Any]:
    """Return finite, comparable per-sector closure and vorticity diagnostics."""
    closure_residuals: dict[str, float] = {}
    vorticity: dict[str, float] = {}
    for sector_id, sector in system.sectors.items():
        phi = float(getattr(sector, "phi", 0.0))
        tau = float(getattr(sector, "tau", 0.0))
        berry = float(getattr(sector, "berry_phase", 0.0))
        rho = abs(float(getattr(sector, "rho", 0.0)))
        spin = abs(float(getattr(sector, "spin", 0.0)))
        wrapped = math.atan2(math.sin(phi + berry - tau), math.cos(phi + berry - tau))
        closure_residuals[str(sector_id)] = abs(wrapped) / math.pi
        vorticity[str(sector_id)] = rho * spin

    if not closure_residuals:
        closure_residuals = {"none": 0.0}
    if not vorticity:
        vorticity = {"none": 0.0}

    return {
        "closure_residuals": closure_residuals,
        "dominant_residual_sector": max(closure_residuals, key=closure_residuals.get),
        "sector_vorticity": vorticity,
        "dominant_vorticity_sector": max(vorticity, key=vorticity.get),
    }


def run_global_pass(
    steps: int = 20,
    params: dict[str, Any] | None = None,
    *,
    write_reports: bool = True,
    pass_label: str = "runtime",
) -> dict[str, Any]:
    repo_root = repo_root_from_here()
    payload = build(repo_root)
    out_dir = repo_root / "reports" / "global_orbital_coherence_pass"
    if write_reports:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "real_geometry.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    config_dir = repo_root / "manifests" / "orbital"
    config_dir.mkdir(parents=True, exist_ok=True)
    sectors_path = config_dir / "sectors_global.json"
    couplings_path = config_dir / "couplings_global.json"

    fresh_sectors = payload["sectors"]
    if sectors_path.exists():
        try:
            prev = json.loads(sectors_path.read_text(encoding="utf-8"))
            prev_inner = prev.get("sectors", prev) if isinstance(prev, dict) else {}
            target = fresh_sectors.get("sectors", fresh_sectors)
            for sector_id, previous in prev_inner.items():
                if sector_id in target and isinstance(previous, dict) and "berry_phase" in previous:
                    target[sector_id]["berry_phase"] = previous["berry_phase"]
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            _LOG.warning("Ignoring unreadable persisted orbital sector state: %s", exc)

    try:
        source_root = Path(__file__).resolve().parents[4] / "src"
        if str(source_root) not in sys.path:
            sys.path.insert(0, str(source_root))
        from ciel_sot_agent.orch_orbital import build_entity_injection

        fresh_sectors, fresh_couplings = build_entity_injection(
            fresh_sectors.get("sectors", fresh_sectors),
            payload["couplings"].get("couplings", payload["couplings"]),
        )
        fresh_sectors = {"sectors": fresh_sectors}
        fresh_couplings = {"couplings": fresh_couplings}
    except (ImportError, AttributeError, TypeError, ValueError) as exc:
        _LOG.warning("Entity orbital injection unavailable: %s", exc)
        fresh_couplings = payload["couplings"]

    sectors_path.write_text(json.dumps(fresh_sectors, indent=2), encoding="utf-8")
    couplings_path.write_text(json.dumps(fresh_couplings, indent=2), encoding="utf-8")

    effective_params = dict(DEFAULT_PARAMS)
    if params:
        effective_params.update(params)
    system = load_system(sectors_path, couplings_path, params=effective_params)
    initial = snapshot(system)
    history = [initial]
    for _ in range(steps):
        system = step(
            system,
            dt=effective_params["dt"],
            tau_eta=effective_params["tau_eta"],
            tau_reg=effective_params["tau_reg"],
        )
        history.append(snapshot(system))

    final = history[-1]
    diagnostics = _sector_diagnostics(system)
    result = {
        "engine": "global_orbital_coherence_pass_v63_euler_df257",
        "pass_label": pass_label,
        "steps": steps,
        "params": effective_params,
        "initial": initial,
        "final": final,
        "history": history,
        "diagnostics": diagnostics,
    }

    if write_reports:
        (out_dir / "summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        _writeback_sectors(system, sectors_path)
        markdown = [
            "# Global Orbital Coherence Pass",
            "",
            f"- pass_label: {pass_label}",
            "- Geometry derived from repository manifests and imports.",
            "",
            "## Initial",
        ]
        for key, value in initial.items():
            markdown.append(f"- {key}: {value}" if isinstance(value, bool) else f"- {key}: {value:.6f}")
        markdown += ["", "## Final"]
        for key, value in final.items():
            markdown.append(f"- {key}: {value}" if isinstance(value, bool) else f"- {key}: {value:.6f}")
        (out_dir / "summary.md").write_text("\n".join(markdown), encoding="utf-8")

    return result


def _writeback_sectors(system: Any, path: Path) -> None:
    """Persist accumulated Berry phase for durable orbital continuity."""
    try:
        document = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"sectors": {}}
        sectors = document.get("sectors", {})
        for sector_id, sector in system.sectors.items():
            entry = sectors.get(sector_id, {})
            entry["berry_phase"] = getattr(sector, "berry_phase", 0.0)
            sectors[sector_id] = entry
        document["sectors"] = sectors
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2), encoding="utf-8")
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        _LOG.warning("Could not persist orbital Berry phase: %s", exc)


if __name__ == "__main__":
    print(json.dumps(run_global_pass(), indent=2))
