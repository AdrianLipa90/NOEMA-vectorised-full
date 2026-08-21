from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pytest

from ciel_geometry.critical_fail_loud import (
    CriticalQuietFallbackError,
    SurfaceStateIntegrityError,
)
from ciel_geometry.cielingo_phase_memory import (
    PhaseMemory,
    PhaseMemoryPersistenceError,
)
from ciel_geometry.noema_config import NoemaConfigError, load_config
from ciel_geometry import noema_surface_mmap as surface_mod


def test_corrupt_existing_config_fails_loud(tmp_path: Path) -> None:
    config_path = tmp_path / "noema_config.json"
    config_path.write_text("{broken", encoding="utf-8")
    with pytest.raises(NoemaConfigError):
        load_config(config_path)


def test_missing_config_is_legitimate_first_run(tmp_path: Path) -> None:
    cfg = load_config(tmp_path / "missing.json")
    assert cfg.kuramoto.dt > 0.0


def test_nested_v2_config_is_honoured(tmp_path: Path) -> None:
    config_path = tmp_path / "noema_config.json"
    config_path.write_text(
        '{"system":{"surface_root":"/tmp/noema-audit"},'
        '"daemons":{"kuramoto":{"dt":0.123}}}',
        encoding="utf-8",
    )
    cfg = load_config(config_path)
    assert cfg.surface_root == "/tmp/noema-audit"
    assert cfg.kuramoto.dt == pytest.approx(0.123)


def test_partial_phase_memory_pair_never_becomes_empty_memory(tmp_path: Path) -> None:
    base = tmp_path / "phase_memory"
    base.with_suffix(".json").write_text("{}", encoding="utf-8")
    with pytest.raises(PhaseMemoryPersistenceError):
        PhaseMemory.load_or_create(base)


def test_missing_phase_memory_pair_is_clean_first_run(tmp_path: Path) -> None:
    pm = PhaseMemory.load_or_create(tmp_path / "phase_memory")
    assert pm.size == 0


def test_surface_open_never_truncates_existing_wrong_size_state(tmp_path: Path) -> None:
    root = tmp_path / "surface"
    surface = surface_mod.ensure_surface(root)
    surface["phi"][...] = np.arange(surface_mod.N_OSCILLATORS, dtype=np.float64)
    surface_mod.flush_surface(surface)
    del surface

    phi_path = root / "phi"
    corrupt = phi_path.read_bytes()[:-8]
    phi_path.write_bytes(corrupt)
    before_open = phi_path.read_bytes()

    with pytest.raises(SurfaceStateIntegrityError):
        surface_mod.open_surface(root)

    assert phi_path.read_bytes() == before_open


def test_corrupt_existing_ciel_state_never_returns_empty_dict(tmp_path: Path) -> None:
    root = tmp_path / "surface"
    root.mkdir()
    (root / "ciel_state.json").write_text("{broken", encoding="utf-8")
    with pytest.raises(SurfaceStateIntegrityError):
        surface_mod.read_ciel_internal_state(root)


def test_existing_all_zero_omega_never_triggers_implicit_reset(tmp_path: Path) -> None:
    root = tmp_path / "surface"
    surface = surface_mod.ensure_surface(root)
    surface["omega"][...] = 0.0
    surface_mod.flush_surface(surface)
    del surface

    with pytest.raises(SurfaceStateIntegrityError, match="all-zero"):
        surface_mod.update_surface_from_ciel_state({}, root=root)


def test_critical_legacy_logger_fallback_is_interrupted_before_fallback() -> None:
    logger = logging.getLogger("ciel_geometry.noema_surface_mmap")
    try:
        raise ValueError("operator failure")
    except ValueError:
        with pytest.raises(CriticalQuietFallbackError):
            logger.exception(
                "src/ciel_geometry/noema_surface_mmap.py:1337 quiet except "
                "scope=sync_surface_holonomy reason=assign_fallback"
            )
