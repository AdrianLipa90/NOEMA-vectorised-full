"""Orbital bridge — runs the global orbital coherence pass and writes
bridge state, health, and control-recommendation manifests.

Connects the CIEL integration kernel to the Orbital diagnostic subsystem
living under ``integration/Orbital/``, ensuring phase-coherence and
resource health are reported at each synchronisation cycle.

After the orbital physics pass the bridge routes the resulting state through
the CIEL/Ω consciousness pipeline (``ciel_pipeline.run_ciel_pipeline``) so
that emotional, ethical, and soul-invariant metrics are embedded in every
report alongside the raw geometry.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — hardcoded, immutable.
import os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


import json
import logging
import time
import argparse
import math
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .paths import resolve_project_root
from .rh_jfunctional import rh_defect_score

_LOG = logging.getLogger(__name__)

_integration_loaded = False
_ensure_orbital_manifests = None
_ensure_orbital_report_dirs = None
_run_global_pass = None
_build_health_manifest = None
_build_state_manifest = None
_recommend_control = None


def _load_integration():
    global _integration_loaded
    global _ensure_orbital_manifests, _ensure_orbital_report_dirs
    global _run_global_pass
    global _build_health_manifest, _build_state_manifest, _recommend_control
    if _integration_loaded:
        return
    from integration.Orbital.main.bootstrap import ensure_orbital_manifests, ensure_orbital_report_dirs
    from integration.Orbital.main.global_pass import run_global_pass
    from integration.Orbital.main.phase_control import build_health_manifest, build_state_manifest, recommend_control
    _ensure_orbital_manifests = ensure_orbital_manifests
    _ensure_orbital_report_dirs = ensure_orbital_report_dirs
    _run_global_pass = run_global_pass
    _build_health_manifest = build_health_manifest
    _build_state_manifest = build_state_manifest
    _recommend_control = recommend_control
    _integration_loaded = True

BRIDGE_DIR = Path('integration') / 'reports' / 'orbital_bridge'
DEFINITIONS_DIR = Path('integration') / 'registries' / 'definitions'


def _load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        _LOG.debug("Could not load %s: %s", path, exc)
        return None


def _build_sync_manifest(root: Path) -> dict[str, Any]:
    defs_root = root / DEFINITIONS_DIR
    sync_registry = _load_json_if_exists(defs_root / 'subsystem_sync_registry.json') or {}
    sync_report = _load_json_if_exists(defs_root / 'subsystem_sync_report.json') or {}
    orbital_report = _load_json_if_exists(defs_root / 'orbital_assignment_report.json') or {}
    horizon_policy = _load_json_if_exists(defs_root / 'horizon_policy_matrix.json') or {}
    nonlocal_cards = _load_json_if_exists(defs_root / 'nonlocal_cards_registry.json') or {}

    boards = sync_registry.get('records', [])
    board_preview = [
        {
            'board_card_id': board.get('board_card_id'),
            'tau_orbit': board.get('tau_orbit'),
            'tau_system': board.get('tau_system'),
            'member_count': board.get('member_count'),
            'board_export_result': board.get('board_export_result'),
            'aggregation_model': board.get('aggregation_model'),
        }
        for board in boards[:5]
    ]
    classes = (horizon_policy.get('classes') or {})
    export_boundary_policy = {
        horizon_class: {
            'privacy_constraint': payload.get('privacy_constraint'),
            'leak_channel_mode': payload.get('leak_channel_mode'),
            'leak_budget_class': payload.get('leak_budget_class'),
            'exportable_fields': payload.get('exportable_fields', []),
        }
        for horizon_class, payload in classes.items()
    }
    nonlocal_records = nonlocal_cards.get('records', [])
    nonlocal_card_manifest = {
        'registry_present': bool(nonlocal_cards),
        'card_count': len(nonlocal_records),
        'active_statuses': sorted({rec.get('active_status') for rec in nonlocal_records if rec.get('active_status')}),
        'classes': sorted({rec.get('class') for rec in nonlocal_records if rec.get('class')}),
        'card_ids': [rec.get('card_id') for rec in nonlocal_records],
    }

    return {
        'schema': 'ciel-sot-agent/subsystem-sync-manifest/v0.1',
        'sync_registry_present': bool(sync_registry),
        'sync_report_present': bool(sync_report),
        'board_count': sync_report.get('board_count', len(boards)),
        'avg_members_per_board': sync_report.get('avg_members_per_board', 0.0),
        'tau_orbit_count': sync_report.get('tau_orbit_count', 0),
        'tau_system_count': sync_report.get('tau_system_count', 0),
        'sync_law_counts': sync_report.get('sync_law_counts', {}),
        'condensation_operator_counts': sync_report.get('condensation_operator_counts', {}),
        'sync_scope_counts': sync_report.get('sync_scope_counts', {}),
        'privacy_constraint_counts': orbital_report.get('privacy_constraint_counts', {}),
        'horizon_class_counts': orbital_report.get('horizon_class_counts', {}),
        'export_boundary_policy': export_boundary_policy,
        'nonlocal_card_manifest': nonlocal_card_manifest,
        'board_preview': board_preview,
    }


def _build_runtime_gating(sync_manifest: dict[str, Any]) -> dict[str, Any]:
    privacy_counts = sync_manifest.get('privacy_constraint_counts', {}) or {}
    horizon_counts = sync_manifest.get('horizon_class_counts', {}) or {}
    board_count = int(sync_manifest.get('board_count', 0) or 0)
    tau_system_count = int(sync_manifest.get('tau_system_count', 0) or 0)
    dominant_privacy = max(privacy_counts.items(), key=lambda kv: kv[1])[0] if privacy_counts else 'UNKNOWN'
    dominant_horizon = max(horizon_counts.items(), key=lambda kv: kv[1])[0] if horizon_counts else 'UNKNOWN'
    return {
        'schema': 'ciel-sot-agent/runtime-gating/v0.1',
        'dominant_privacy_constraint': dominant_privacy,
        'dominant_horizon_class': dominant_horizon,
        'export_boundary_mode': 'PROJECTED_ONLY',
        'private_state_export_allowed': False,
        'board_sync_ready': board_count > 0,
        'system_tau_coherent': tau_system_count <= 1,
        'requires_projection_operator': True,
    }


def _bridge_markdown(summary: dict[str, Any]) -> str:
    lines = [
        '# Orbital Bridge Report', '', '## Source',
        f"- source_report: {summary['source_report']}",
        f"- engine: {summary['orbital_run'].get('engine', 'unknown')}",
        f"- steps: {summary['orbital_run'].get('steps', 0)}", '', '## State Manifest',
    ]
    for key, value in summary['state_manifest'].items():
        lines.append(f'- {key}: {value}')
    lines += ['', '## Health Manifest']
    for key, value in summary['health_manifest'].items():
        lines.append(f'- {key}: {value}')
    lines += ['', '## Recommended Control']
    for key, value in summary['recommended_control'].items():
        lines.append(f'- {key}: {value}')
    lines += ['', '## Bridge Metrics']
    for key, value in summary['bridge_metrics'].items():
        lines.append(f'- {key}: {value}')
    sync_manifest = summary.get('subsystem_sync_manifest', {})
    if sync_manifest:
        lines += ['', '## Subsystem Sync Manifest']
        for key in ['board_count', 'avg_members_per_board', 'tau_orbit_count', 'tau_system_count']:
            lines.append(f'- {key}: {sync_manifest.get(key)}')
        nonlocal_cards = sync_manifest.get('nonlocal_card_manifest', {})
        if nonlocal_cards:
            lines.append(f"- nonlocal_card_count: {nonlocal_cards.get('card_count')}")
            lines.append(f"- nonlocal_card_classes: {', '.join(nonlocal_cards.get('classes', []))}")
    runtime_gating = summary.get('runtime_gating', {})
    if runtime_gating:
        lines += ['', '## Runtime Gating']
        for key, value in runtime_gating.items():
            if key != 'schema':
                lines.append(f'- {key}: {value}')
    ciel = summary.get('ciel_pipeline', {})
    if ciel:
        lines += ['', '## CIEL Pipeline']
        for key, value in ciel.items():
            lines.append(f'- {key}: {value}')
    return '\n'.join(lines)


_BRIDGE_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}
_BRIDGE_CACHE_TTL = 600  # 10 minutes


def _build_phase_eba_observables(root: Path) -> dict[str, Any]:
    """Evaluate canonical EBA loops against the live PhaseNav surface.

    This is deliberately a read-only observation path.  It does not create or
    repair the mmap and it does not call the semantic CIEL pipeline.  The EBA
    values come from ``HolonomicMemoryOrchestrator`` and are published only
    after a successful read of the live phase vector.
    """
    import numpy as np

    from ciel_geometry.noema_surface_mmap import open_surface

    surface_root = Path("/dev/shm/ciel_noema")
    surface = open_surface(surface_root, mode="r")
    tick_values = np.asarray(surface["tick"], dtype=np.uint64).reshape(-1)
    if tick_values.size != 1:
        raise RuntimeError(f"canonical tick is not scalar: shape={tick_values.shape}")
    tick = int(tick_values[0])
    phases = np.asarray(surface["phi"], dtype=np.float64).reshape(-1).copy()
    if phases.size == 0 or not np.isfinite(phases).all():
        raise RuntimeError("canonical PhaseNav surface has no finite phase vector")

    mean_cos = float(np.cos(phases).mean())
    mean_sin = float(np.sin(phases).mean())
    phase = float(math.atan2(mean_sin, mean_cos))
    coherence = float(math.hypot(mean_cos, mean_sin))
    novelty = float(max(0.0, min(1.0, 1.0 - coherence)))

    omega_root = root / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
    if not (omega_root / "ciel_omega").is_dir():
        raise RuntimeError(f"canonical CIEL/Ω package missing: {omega_root}")
    omega_path = str(omega_root)
    if omega_path not in sys.path:
        sys.path.insert(0, omega_path)
    from ciel_omega.memory.orchestrator import HolonomicMemoryOrchestrator

    orchestrator = HolonomicMemoryOrchestrator(identity_phase=phase)
    cycle = orchestrator.process_input(
        {"content": f"PhaseNav surface tick={tick}", "source": str(surface_root)},
        metadata={
            "phase": phase,
            "target_phase": phase,
            "salience": coherence,
            "confidence": coherence,
            "novelty": novelty,
            "modality": "phase_surface",
            "source": str(surface_root),
            "tick": tick,
        },
    )
    eba_results = getattr(cycle, "eba_results", None)
    if not isinstance(eba_results, dict) or not eba_results:
        raise RuntimeError("canonical EBA producer returned no loop results")

    loops: dict[str, dict[str, Any]] = {}
    for name, evaluation in eba_results.items():
        payload = asdict(evaluation) if hasattr(evaluation, "__dataclass_fields__") else dict(evaluation)
        required = ("defect_magnitude", "epsilon_eba", "phi_berry", "phi_ab", "nu_e", "is_coherent")
        if any(key not in payload for key in required):
            raise RuntimeError(f"EBA loop {name!r} is missing canonical fields")
        loops[str(name)] = {
            "loop_type": str(payload["loop_type"]),
            "epsilon_eba": float(payload["epsilon_eba"]),
            "defect_magnitude": float(payload["defect_magnitude"]),
            "is_coherent": bool(payload["is_coherent"]),
            "phi_dyn": float(payload["phi_dyn"]),
            "phi_berry": float(payload["phi_berry"]),
            "phi_ab": float(payload["phi_ab"]),
            "nu_e": int(payload["nu_e"]),
        }

    values = list(loops.values())
    return {
        "schema": "ciel-sot-agent/phase-eba-observables/v0.1",
        "producer": "ciel_omega.memory.orchestrator.HolonomicMemoryOrchestrator",
        "imports": [
            "ciel_omega.memory.orchestrator.HolonomicMemoryOrchestrator",
            "ciel_omega.memory.holonomy.HolonomyCalculator",
            "ciel_geometry.noema_surface_mmap.open_surface",
        ],
        "source": str(surface_root),
        "source_mode": "read-only",
        "tick": tick,
        "phase": phase,
        "surface_coherence": coherence,
        "loop_count": len(values),
        "eba_defect_mean": float(np.mean([item["defect_magnitude"] for item in values])),
        "epsilon_eba_mean": float(np.mean([item["epsilon_eba"] for item in values])),
        "phi_berry_mean": float(np.mean([item["phi_berry"] for item in values])),
        "phi_ab_mean": float(np.mean([item["phi_ab"] for item in values])),
        "nonlocal_coherent_fraction": float(np.mean([item["is_coherent"] for item in values])),
        "nu_e_total": int(sum(item["nu_e"] for item in values)),
        "loops": loops,
        "observed_at": time.time(),
    }


def _persist_phase_orbital_result(root: Path, summary: dict[str, Any]) -> None:
    """Persist the refreshed report and its manifests on the canonical volume."""
    bridge_dir = root / BRIDGE_DIR
    bridge_dir.mkdir(parents=True, exist_ok=True)
    (bridge_dir / "orbital_bridge_report.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (bridge_dir / "orbital_bridge_report.md").write_text(_bridge_markdown(summary), encoding="utf-8")
    (bridge_dir / "orbital_state_manifest.json").write_text(
        json.dumps(summary["state_manifest"], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (bridge_dir / "orbital_health_manifest.json").write_text(
        json.dumps(summary["health_manifest"], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (bridge_dir / "subsystem_sync_manifest.json").write_text(
        json.dumps(summary["subsystem_sync_manifest"], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (bridge_dir / "runtime_gating.json").write_text(
        json.dumps(summary["runtime_gating"], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    try:
        from .state_db import save_bridge_snapshot

        save_bridge_snapshot(
            summary,
            summary["runtime_gating"],
            summary["health_manifest"],
            summary["state_manifest"],
            summary.get("ciel_pipeline", {}),
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug(
            "src/ciel_sot_agent/orbital_bridge.py:phase persist state_db write failed"
        )


def build_orbital_bridge(
    root: str | Path,
    encoder_phase: float | None = None,
    cqcl_ref: dict | None = None,
    phase_orbital_only: bool = False,
) -> dict[str, Any]:
    root = Path(root).resolve()
    cache_key = f"{root}|phase_orbital_only={phase_orbital_only}"
    now = time.monotonic()
    cached = _BRIDGE_CACHE.get(cache_key)
    if cached is not None and (now - cached[0]) < _BRIDGE_CACHE_TTL:
        return cached[1]

    _load_integration()
    orbital_root = root / 'integration' / 'Orbital' / 'main'
    _ensure_orbital_manifests(orbital_root)
    orbital_paths = _ensure_orbital_report_dirs(orbital_root)

    params = {}
    if encoder_phase is not None:
        params['encoder_phase'] = encoder_phase
    orbital_run = _run_global_pass(repo_root=orbital_root, steps=20, params=params)
    final = dict(orbital_run.get('final', {}))
    entity_orbital = orbital_run.get('entity_orbital', {})
    sync_manifest = _build_sync_manifest(root)
    runtime_gating = _build_runtime_gating(sync_manifest)

    bridge_dir = root / BRIDGE_DIR
    bridge_dir.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        'schema': 'ciel-sot-agent/orbital-bridge-report/v0.2',
        'source_report': str(Path('integration/Orbital/main/reports/global_orbital_coherence_pass/summary.json')),
        'source_paths': orbital_paths,
        'orbital_run': {
            'engine': orbital_run.get('engine'),
            'steps': orbital_run.get('steps'),
            'params': orbital_run.get('params', {}),
            'n_sectors': int(final.get('n_sectors', 0) or 0),
        },
        'state_manifest': {},
        'health_manifest': {},
        'recommended_control': {},
        'subsystem_sync_manifest': sync_manifest,
        'runtime_gating': runtime_gating,
        'bridge_metrics': {
            'orbital_R_H': float(final.get('R_H', 0.0)),
            'orbital_n_sectors': int(final.get('n_sectors', 0) or 0),
            'orbital_closure_penalty': float(final.get('closure_penalty', 0.0)),
            'integration_closure_defect_proxy': rh_defect_score(final),
            'topological_charge_global': float(final.get('Lambda_glob', 0.0)),
            'subsystem_board_count': int(sync_manifest.get('board_count', 0) or 0),
            'tau_system_count': int(sync_manifest.get('tau_system_count', 0) or 0),
            'nonlocal_card_count': int((sync_manifest.get('nonlocal_card_manifest') or {}).get('card_count', 0) or 0),
        },
        'entity_orbital': entity_orbital,
    }

    control_view = dict(final)

    # CQCL fast path — when a PhaseNav surface snapshot is provided as cqcl_ref,
    # populate ciel_pipeline from it directly, bypassing engine.step() (>45s).
    # Connector values: IDENTITY, AFFECT, CONSENT, RISK, phi[] from surface state.
    if phase_orbital_only:
        summary['ciel_pipeline'] = {
            'status': 'phase_orbital_only',
            'source': 'PhaseNav → integration.Orbital.main.global_pass',
            'enrichment': 'not_run',
            'eba_defect_mean': None,
        }
    elif cqcl_ref:
        _phi = cqcl_ref.get("phi", 0.0)
        _flavor = cqcl_ref.get("flavor", [0.5, 0.5, 0.5, 0.5])
        _affect = float(_flavor[3]) if len(_flavor) > 3 else 0.5
        _coherence = float(cqcl_ref.get("coherence", 0.5))
        _identity = float(cqcl_ref.get("identity_phase", 0.0))
        _risk = float(cqcl_ref.get("risk", 0.0))
        _ethical = max(0.0, 1.0 - abs(_risk))
        summary["ciel_pipeline"] = {
            "status": "cqcl_ref",
            "dominant_emotion": cqcl_ref.get("dominant_emotion", "curiosity"),
            "mood": _affect,
            "soul_invariant": _coherence,
            "ethical_score": _ethical,
            "orbital_context": f"cqcl_ref|phi={_phi:.4f}|coherence={_coherence:.4f}",
            "identity_phase": _identity,
            "cycle_index": int(cqcl_ref.get("tick", 0)),
            "phi_ab_mean": float(_phi),
            "phi_berry_mean": float(cqcl_ref.get("phi", 0.0)),
            "eba_defect_mean": 0.0,
            "nonlocal_coherent_fraction": _coherence,
            "bridge_closure_score": _coherence,
            "bridge_target_phase": float(_phi),
            "nonlocal_card_count": 0,
            "nonlocal_card_ids": [],
            "phase_R_H": float(summary["bridge_metrics"].get("orbital_R_H", 0.0)),
            "collatz_seed": int(cqcl_ref.get("tick", 0)) % 1000 or 1,
            "lie4_trace": float(cqcl_ref.get("coherence", 0.5)),
        }
        control_view.update({
            "nonlocal_phi_ab_mean": float(_phi),
            "nonlocal_phi_berry_mean": float(_phi),
            "nonlocal_eba_defect_mean": 0.0,
            "nonlocal_coherent_fraction": _coherence,
        })
    if not cqcl_ref and not phase_orbital_only:
        try:
            from .ciel_pipeline import run_ciel_pipeline
            ciel_result = run_ciel_pipeline(summary, context='orbital_bridge', root=root)
            summary['ciel_pipeline'] = {
                'status': ciel_result['ciel_status'],
                'dominant_emotion': ciel_result['dominant_emotion'],
                'mood': ciel_result['mood'],
                'soul_invariant': ciel_result['soul_invariant'],
                'ethical_score': ciel_result['ethical_score'],
                'orbital_context': ciel_result['orbital_context'],
                'identity_phase': ciel_result.get('identity_phase', 0.0),
                'cycle_index': ciel_result.get('cycle_index', 0),
                'phi_ab_mean': ciel_result.get('phi_ab_mean', 0.0),
                'phi_berry_mean': ciel_result.get('phi_berry_mean', 0.0),
                'eba_defect_mean': ciel_result.get('eba_defect_mean', 0.0),
                'nonlocal_coherent_fraction': ciel_result.get('nonlocal_coherent_fraction', 0.0),
                'bridge_closure_score': ciel_result.get('bridge_closure_score', 0.0),
                'bridge_target_phase': ciel_result.get('bridge_target_phase', 0.0),
                'nonlocal_card_count': ciel_result.get('nonlocal_card_count', 0),
                'nonlocal_card_ids': ciel_result.get('nonlocal_card_ids', []),
                'phase_R_H': ciel_result.get('phase_R_H', 0.0),
                'collatz_seed': ciel_result.get('collatz_seed', 0),
                'lie4_trace': ciel_result.get('lie4_trace', 0.0),
            }
            lingo_frame = ciel_result.get('lingo_frame', {}) if isinstance(ciel_result, dict) else {}
            lingo_phase_projection = lingo_frame.get('phase_projection', {}) if isinstance(lingo_frame, dict) else {}
            if isinstance(lingo_phase_projection, dict) and lingo_phase_projection:
                summary['ciel_pipeline']['lingo_phase_target'] = float(lingo_phase_projection.get('target_phase', 0.0))
                summary['ciel_pipeline']['lingo_phase_shift'] = float(lingo_phase_projection.get('target_phase_shift', 0.0))
                summary['ciel_pipeline']['lingo_phase_confidence'] = float(lingo_phase_projection.get('phase_confidence', 0.0))
                summary['ciel_pipeline']['lingo_phase_projection'] = lingo_phase_projection
            lingo_tau_bridge = lingo_frame.get('tau_bridge', {}) if isinstance(lingo_frame, dict) else {}
            if isinstance(lingo_tau_bridge, dict) and lingo_tau_bridge:
                summary['ciel_pipeline']['lingo_tau_bridge'] = lingo_tau_bridge
                summary['ciel_pipeline']['lingo_tau_gradient_mean'] = float(lingo_tau_bridge.get('tau_gradient_mean', 0.0))
                summary['ciel_pipeline']['lingo_imaginal_drive'] = float(lingo_tau_bridge.get('imaginal_drive', 0.0))
                summary['ciel_pipeline']['lingo_tau_curvature_rms'] = float(lingo_tau_bridge.get('tau_curvature_rms', 0.0))
            control_view.update({
                'nonlocal_phi_ab_mean': ciel_result.get('phi_ab_mean', 0.0),
                'nonlocal_phi_berry_mean': ciel_result.get('phi_berry_mean', 0.0),
                'nonlocal_eba_defect_mean': ciel_result.get('eba_defect_mean', 0.0),
                'nonlocal_coherent_fraction': ciel_result.get('nonlocal_coherent_fraction', 0.0),
                'euler_bridge_closure_score': ciel_result.get('bridge_closure_score', 0.0),
                'euler_bridge_target_phase': ciel_result.get('bridge_target_phase', 0.0),
            })
            if isinstance(lingo_phase_projection, dict) and lingo_phase_projection:
                control_view.update({
                    'lingo_phase_target': float(lingo_phase_projection.get('target_phase', 0.0)),
                    'lingo_phase_shift': float(lingo_phase_projection.get('target_phase_shift', 0.0)),
                    'lingo_phase_confidence': float(lingo_phase_projection.get('phase_confidence', 0.0)),
                })
            if isinstance(lingo_tau_bridge, dict) and lingo_tau_bridge:
                control_view.update({
                    'lingo_tau_gradient_mean': float(lingo_tau_bridge.get('tau_gradient_mean', 0.0)),
                    'lingo_imaginal_drive': float(lingo_tau_bridge.get('imaginal_drive', 0.0)),
                    'lingo_tau_curvature_rms': float(lingo_tau_bridge.get('tau_curvature_rms', 0.0)),
                })

            # --- Local Nonlocality Fallback ---
            canonical_cf = ciel_result.get('nonlocal_coherent_fraction', 0.0)
            try:
                from .local_nonlocality_fallback import (
                    run_local_nonlocality_fallback,
                    merge_with_canonical,
                    save_report,
                )
                fallback_result = run_local_nonlocality_fallback(
                    canonical_coherent_fraction=canonical_cf,
                    root=root,
                )
                save_report(fallback_result, root=root)
                fallback_obs = fallback_result['observables']
                canonical_obs = {
                    'nonlocal_coherent_fraction': canonical_cf,
                    'eba_defect_mean': ciel_result.get('eba_defect_mean', 1.0),
                    'phi_ab_mean': ciel_result.get('phi_ab_mean', 0.0),
                    'phi_berry_mean': ciel_result.get('phi_berry_mean', 0.0),
                }
                merged = merge_with_canonical(canonical_obs, fallback_obs)
                summary['ciel_pipeline'].update({
                    'nonlocal_coherent_fraction': merged['nonlocal_coherent_fraction'],
                    'eba_defect_mean': merged['eba_defect_mean'],
                    'phi_ab_mean': merged['phi_ab_mean'],
                    'phi_berry_mean': merged['phi_berry_mean'],
                    'local_nonlocality_fallback': {
                        'active': fallback_result.get('fallback_active', False),
                        'fallback_coherent_fraction': fallback_obs.get('nonlocal_coherent_fraction', 0.0),
                        'merged_coherent_fraction': merged['nonlocal_coherent_fraction'],
                    },
                })
                control_view.update({
                    'nonlocal_coherent_fraction': merged['nonlocal_coherent_fraction'],
                    'nonlocal_eba_defect_mean': merged['eba_defect_mean'],
                    'nonlocal_phi_ab_mean': merged['phi_ab_mean'],
                    'nonlocal_phi_berry_mean': merged['phi_berry_mean'],
                })
            except Exception as fb_exc:
                _LOG.debug("Local nonlocality fallback unavailable: %s", fb_exc)

        except Exception as exc:
            _LOG.debug("CIEL/Ω pipeline unavailable: %s", exc)
            summary['ciel_pipeline'] = {'status': 'unavailable'}

    # Optional semantic/memory enrichment never blocks the phase-orbital path.
    if not phase_orbital_only:
        try:
            from .noema_sot import run as run_noema_sot
            noema_report = run_noema_sot()
            summary['noema_sot'] = {
                'global_coherence': noema_report.get('global_coherence', 0.0),
                'global_health': noema_report.get('global_health', 0.0),
                'operating_mode': noema_report.get('operating_mode', 'standard'),
                'memory_projection': noema_report.get('memory_projection', {}),
                'priority_order': noema_report.get('priority_order', []),
            }
            memory_projection = noema_report.get('memory_projection', {}) or {}
            summary['memory_projection'] = memory_projection
            control_view.update({
                'memory_projection_confidence': float(memory_projection.get('projection_confidence', 0.0)),
                'memory_projection_residual': float(memory_projection.get('projection_residual', 1.0)),
                'memory_projection_error': float(memory_projection.get('projection_error', 1.0)),
                'j_noema': float(memory_projection.get('j_noema', 1.0)),
            })
        except Exception as noema_exc:
            _LOG.debug("NOEMA memory projection unavailable: %s", noema_exc)

    try:
        from ciel_geometry.resonance_bridge import DEFAULT_IMAGINAL_SURFACE_ROOT, resonance_snapshot

        if DEFAULT_IMAGINAL_SURFACE_ROOT.exists():
            dual = resonance_snapshot()
            summary['dual_surface'] = dual
            summary.setdefault('ciel_pipeline', {}).update({
                'imaginal_drive': float(dual.get('imaginal_drive', 0.0)),
                'resonance_score': float(dual.get('resonance_score', 0.0)),
                'phase_lock': float(dual.get('phase_lock', 0.0)),
                'flavor_lock': float(dual.get('flavor_lock', 0.0)),
            })
            control_view.update({
                'imaginal_drive': float(dual.get('imaginal_drive', 0.0)),
                'resonance_score': float(dual.get('resonance_score', 0.0)),
                'phase_lock': float(dual.get('phase_lock', 0.0)),
                'flavor_lock': float(dual.get('flavor_lock', 0.0)),
            })
    except Exception as dual_exc:
        _LOG.debug("Dual-surface resonance unavailable: %s", dual_exc)

    # ── Kuramoto R → orbital bridge: coherence DERIVES from synchronization ──
    # The NOEMA surface oscillators define spacetime. Orbital dynamics
    # (Kepler/Newton) happen ON that spacetime. Coherence is a property
    # of Kuramoto synchronization — bridge reads it, doesn't compute own.
    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface
        _surf = ensure_surface(zero_fill=False)
        if _surf is not None:
            import math as _math
            _phi_raw = _surf["phi"]
            _n = len(_phi_raw)
            if _n > 0:
                _sum_re = sum(_math.cos(float(v)) for v in _phi_raw)
                _sum_im = sum(_math.sin(float(v)) for v in _phi_raw)
                _kuramoto_R = _math.sqrt((_sum_re / _n)**2 + (_sum_im / _n)**2)
            else:
                _kuramoto_R = 0.0
            control_view["kuramoto_R"] = _kuramoto_R
            control_view["nonlocal_coherent_fraction"] = max(
                float(control_view.get("nonlocal_coherent_fraction", 0.0)),
                _kuramoto_R,
            )
    except Exception:
        _LOG.debug("Kuramoto R injection into orbital bridge skipped")

    _load_integration()
    state_manifest = _build_state_manifest(control_view)
    health_manifest = _build_health_manifest(control_view)
    recommended_control = _recommend_control(control_view)
    if phase_orbital_only:
        # These observables require a real memory-loop/EBA publication.  The
        # orbital-only gate must not inherit stale values from the previous
        # bridge report or expose the phase-control helper's numeric defaults.
        for payload in (state_manifest,):
            for key in (
                'nonlocal_phi_ab_mean', 'nonlocal_phi_berry_mean',
                'nonlocal_eba_defect_mean', 'nonlocal_coherent_fraction',
                'euler_bridge_closure_score', 'euler_bridge_target_phase',
            ):
                payload[key] = None
        for payload in (health_manifest, recommended_control):
            drivers = payload.get('rh_drivers')
            if isinstance(drivers, dict):
                for key in ('eba_defect', 'coherent_fraction', 'closure_score', 'phase_gap'):
                    drivers[key] = None
        recommended_control['nonlocal_gate'] = None
        recommended_control['euler_memory_lock'] = None
        recommended_control['writeback_gate'] = False
    summary['state_manifest'] = state_manifest
    summary['health_manifest'] = health_manifest
    summary['recommended_control'] = recommended_control

    (bridge_dir / 'orbital_bridge_report.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    (bridge_dir / 'orbital_bridge_report.md').write_text(_bridge_markdown(summary), encoding='utf-8')
    (bridge_dir / 'orbital_state_manifest.json').write_text(json.dumps(state_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (bridge_dir / 'orbital_health_manifest.json').write_text(json.dumps(health_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (bridge_dir / 'subsystem_sync_manifest.json').write_text(json.dumps(sync_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (bridge_dir / 'runtime_gating.json').write_text(json.dumps(runtime_gating, ensure_ascii=False, indent=2), encoding='utf-8')

    # Mirror key reports to unified SQLite state store — single transaction
    try:
        from .state_db import save_bridge_snapshot
        ciel_pipe = summary.get('ciel_pipeline', {})
        save_bridge_snapshot(summary, runtime_gating, health_manifest, state_manifest, ciel_pipe)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/orbital_bridge.py:387 quiet except scope=build_orbital_bridge reason=pass")
        pass  # SQLite write never blocks pipeline

    _BRIDGE_CACHE[cache_key] = (time.monotonic(), summary)
    return summary


def build_phase_orbital_bridge(root: str | Path) -> dict[str, Any]:
    """Run the canonical orbital generator through an explicit PhaseNav gate."""
    from ciel_geometry.phasenav_bypass_language import BypassRuntime, Φ

    chain = Φ.COMPOSITION(
        Φ.SOURCE("phase_orbital_refresh"),
        Φ.MODAL_NECESSITY(
            lambda _ctx: build_orbital_bridge(root, phase_orbital_only=True)
        ),
    )
    result = BypassRuntime(_LOG).execute(chain, {"phase": "orbital", "enrichment": "separate"})
    if not isinstance(result, dict) or result.get("bridge_metrics", {}).get("orbital_R_H") is None:
        raise RuntimeError("PhaseNav orbital gate did not produce a validated bridge report")
    root = Path(root).resolve()
    eba = _build_phase_eba_observables(root)
    ciel_pipeline = result.setdefault("ciel_pipeline", {})
    ciel_pipeline.update({
        "status": "phase_orbital_eba",
        "source": "PhaseNav → NoemaSurface → CIEL/Ω HolonomicMemoryOrchestrator",
        "enrichment": "canonical_eba_only",
        "eba_defect_mean": eba["eba_defect_mean"],
        "epsilon_eba_mean": eba["epsilon_eba_mean"],
        "phi_ab_mean": eba["phi_ab_mean"],
        "phi_berry_mean": eba["phi_berry_mean"],
        "nonlocal_coherent_fraction": eba["nonlocal_coherent_fraction"],
        "phase_surface_coherence": eba["surface_coherence"],
        "phase_surface_tick": eba["tick"],
        "eba": eba,
    })
    bridge_metrics = result["bridge_metrics"]
    bridge_metrics.update({
        "nonlocal_eba_defect_mean": eba["eba_defect_mean"],
        "nonlocal_phi_ab_mean": eba["phi_ab_mean"],
        "nonlocal_phi_berry_mean": eba["phi_berry_mean"],
        "nonlocal_coherent_fraction": eba["nonlocal_coherent_fraction"],
        "phase_surface_coherence": eba["surface_coherence"],
        "phase_surface_tick": eba["tick"],
    })
    control_view = {
        "R_H": bridge_metrics.get("orbital_R_H"),
        "n_sectors": bridge_metrics.get("orbital_n_sectors"),
        "closure_penalty": bridge_metrics.get("orbital_closure_penalty"),
        "Lambda_glob": bridge_metrics.get("topological_charge_global"),
        "nonlocal_eba_defect_mean": eba["eba_defect_mean"],
        "nonlocal_phi_ab_mean": eba["phi_ab_mean"],
        "nonlocal_phi_berry_mean": eba["phi_berry_mean"],
        "nonlocal_coherent_fraction": eba["nonlocal_coherent_fraction"],
        "euler_bridge_closure_score": eba["surface_coherence"],
        "euler_bridge_target_phase": eba["phase"],
    }
    _load_integration()
    result["state_manifest"] = _build_state_manifest(control_view)
    result["health_manifest"] = _build_health_manifest(control_view)
    result["recommended_control"] = _recommend_control(control_view)
    result["recommended_control"]["writeback_gate"] = False
    result["recommended_control"]["phase_orbital_read_only"] = True
    _persist_phase_orbital_result(root, result)
    _BRIDGE_CACHE[f"{root}|phase_orbital_only=True"] = (time.monotonic(), result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the canonical NOEMA orbital bridge report")
    parser.add_argument(
        "--phase-orbital-only",
        action="store_true",
        help="run global orbital mathematics through the PhaseNav gate without semantic enrichment",
    )
    args = parser.parse_args(argv)
    root = resolve_project_root(Path(__file__))
    summary = build_phase_orbital_bridge(root) if args.phase_orbital_only else build_orbital_bridge(root)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
