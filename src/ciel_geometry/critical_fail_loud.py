"""Fail-loud continuity guard for critical NOEMA/CIEL state paths.

This module is deliberately small and auditable.  It does two things:

1. turns selected legacy ``logger.exception(...); fallback/pass`` handlers into
   hard failures before the fallback statement can execute;
2. replaces destructive surface open/ensure behaviour with non-mutating strict
   wrappers so existing mmap bytes are never truncated as error recovery.

The guard is an enforcement layer while legacy call sites are migrated to
explicit exceptions.  It does not make optional/telemetry failures fatal.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Mapping

import numpy as np


class CriticalQuietFallbackError(RuntimeError):
    """A legacy quiet fallback was reached on a continuity-critical path."""


class SurfaceStateIntegrityError(RuntimeError):
    """Existing surface state cannot be restored without mutation or guessing."""


# Only continuity-critical legacy handlers are blocked.  This is intentionally
# not a blanket ban on exception handling.
_CRITICAL_MARKERS = (
    "noema_surface_mmap.py:43 quiet except scope=<module> reason=assign_fallback",
    "noema_surface_mmap.py:1091 quiet except scope=evolve_surface reason=assign_fallback",
    "noema_surface_mmap.py:1209 quiet except scope=read_ciel_internal_state reason=return {}",
    "noema_surface_mmap.py:1229 quiet except scope=ensure_surface",
    "noema_surface_mmap.py:1251 quiet except scope=open_surface",
    "noema_surface_mmap.py:1337 quiet except scope=sync_surface_holonomy reason=assign_fallback",
    "noema_surface_mmap.py:1606 quiet except scope=update_surface_from_ciel_state reason=pass",
    "memory_palace.py:121 quiet except scope=MentalistMemoryPalace.__init__ reason=pass",
    "nonlocal_channel.py:93 quiet except scope=NonlocalChannel.__init__ reason=assign_fallback",
    "nonlocal_channel.py:438 quiet except scope=NonlocalChannel._load_rag_cache reason=pass",
    "nonlocal_channel.py:448 quiet except scope=NonlocalChannel._save_rag_cache reason=pass",
    "phasenav_unified.py:143 quiet except scope=PhaseNavUnified._load_knowledge_db",
    "phasenav_unified.py:165 quiet except scope=PhaseNavUnified._load_knowledge_db",
    "phasenav_unified.py:180 quiet except scope=PhaseNavUnified._load_knowledge_db",
    "phasenav_unified.py:214 quiet except scope=PhaseNavUnified._load_palace_rooms",
    "phasenav_unified.py:302 quiet except scope=PhaseNavUnified._load_taskplan_db",
    "phasenav_unified.py:318 quiet except scope=PhaseNavUnified._load_taskplan_db",
    "phasenav_unified.py:337 quiet except scope=PhaseNavUnified._load_taskplan_db",
    "phasenav_unified.py:353 quiet except scope=PhaseNavUnified._load_taskplan_db",
    "phasenav_unified.py:371 quiet except scope=PhaseNavUnified._load_taskplan_db",
    "phasenav_unified.py:399 quiet except scope=PhaseNavUnified._load_task_queue",
    "phasenav_unified.py:424 quiet except scope=PhaseNavUnified._load_system_map",
)


class _CriticalQuietHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        message = record.getMessage()
        if not any(marker in message for marker in _CRITICAL_MARKERS):
            return
        cause = record.exc_info[1] if record.exc_info else None
        error = CriticalQuietFallbackError(
            f"blocked continuity-critical quiet fallback: {message}"
        )
        if cause is not None:
            raise error from cause
        raise error


_HANDLER = _CriticalQuietHandler(level=logging.ERROR)
_HANDLER._noema_critical_fail_loud = True  # type: ignore[attr-defined]
_INSTALLED = False


def _install_log_guard() -> None:
    logger = logging.getLogger("ciel_geometry")
    if any(getattr(h, "_noema_critical_fail_loud", False) for h in logger.handlers):
        return
    logger.addHandler(_HANDLER)


def _strict_surface_functions(module: Any) -> None:
    specs_fn = module.surface_specs
    surface_path_fn = module._surface_path

    def strict_ensure_surface(
        root: Path = module.DEFAULT_SURFACE_ROOT,
        *,
        zero_fill: bool = False,
    ) -> dict[str, np.memmap]:
        root = Path(root)
        root.mkdir(parents=True, exist_ok=True)
        surface: dict[str, np.memmap] = {}
        for spec in specs_fn():
            path = surface_path_fn(root, spec)
            if not path.exists():
                with path.open("xb") as handle:
                    handle.truncate(spec.nbytes)
            else:
                actual = path.stat().st_size
                if actual != spec.nbytes:
                    raise SurfaceStateIntegrityError(
                        f"surface field size mismatch for {path}: "
                        f"{actual} != {spec.nbytes}; refusing truncate"
                    )
            try:
                mem = np.memmap(path, dtype=spec.dtype, mode="r+", shape=spec.shape)
            except (ValueError, OSError) as exc:
                raise SurfaceStateIntegrityError(
                    f"cannot mmap existing surface field without mutation: {path}"
                ) from exc
            if zero_fill:
                mem[...] = 0
                mem.flush()
            surface[spec.name] = mem
        return surface

    def strict_open_surface(
        root: Path = module.DEFAULT_SURFACE_ROOT,
        mode: str = "r+",
    ) -> dict[str, np.memmap]:
        root = Path(root)
        surface: dict[str, np.memmap] = {}
        for spec in specs_fn():
            path = surface_path_fn(root, spec)
            if not path.exists():
                raise FileNotFoundError(path)
            actual = path.stat().st_size
            if actual != spec.nbytes:
                raise SurfaceStateIntegrityError(
                    f"surface field size mismatch for {path}: "
                    f"{actual} != {spec.nbytes}; refusing truncate"
                )
            try:
                surface[spec.name] = np.memmap(
                    path, dtype=spec.dtype, mode=mode, shape=spec.shape
                )
            except (ValueError, OSError) as exc:
                raise SurfaceStateIntegrityError(
                    f"cannot mmap existing surface field without mutation: {path}"
                ) from exc
        return surface

    def strict_read_ciel_internal_state(
        root: Path = module.DEFAULT_SURFACE_ROOT,
    ) -> dict[str, float]:
        root = Path(root)
        path = root / "ciel_state.json"
        if not path.exists():
            return {}
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SurfaceStateIntegrityError(
                f"existing CIEL state cannot be restored: {path}"
            ) from exc
        if not isinstance(raw, dict):
            raise SurfaceStateIntegrityError(
                f"CIEL state root must be an object: {path}"
            )
        return dict(raw)

    original_update = module.update_surface_from_ciel_state

    def strict_update_surface_from_ciel_state(
        state: Mapping[str, object],
        root: Path = module.DEFAULT_SURFACE_ROOT,
        *,
        initialize_if_missing: bool = True,
        dt: float = module.DEFAULT_DT,
    ) -> dict[str, np.memmap]:
        root = Path(root)
        # Validate persistent JSON before legacy code sees it.  Missing is a
        # first-run condition; existing malformed state is not.
        cache_path = root / "ciel_state.json"
        cache: dict[str, Any] = {}
        if cache_path.exists():
            cache = strict_read_ciel_internal_state(root)

        any_surface_file = any(
            surface_path_fn(root, spec).exists() for spec in specs_fn()
        )
        all_surface_files = all(
            surface_path_fn(root, spec).exists() for spec in specs_fn()
        )
        if any_surface_file and not all_surface_files:
            raise SurfaceStateIntegrityError(
                f"partial existing surface at {root}; refusing implicit reconstruction"
            )

        if all_surface_files:
            current = strict_open_surface(root)
            omega = np.asarray(current["omega"], dtype=np.float64)
            if not np.all(np.isfinite(omega)):
                raise SurfaceStateIntegrityError("existing omega contains non-finite values")
            if np.all(omega == 0.0):
                raise SurfaceStateIntegrityError(
                    "existing omega is all-zero; refusing implicit initialize_surface reset"
                )
            flavor = np.asarray(current["flavor"], dtype=np.float64)
            if flavor.shape != (module.N_FLAVORS,) or not np.all(np.isfinite(flavor)):
                raise SurfaceStateIntegrityError("existing flavor state is invalid")
            # If the cache does not carry closure state, validate the live read
            # before legacy code reaches its broad try/except-pass fallback.
            if cache.get("closure_penalty_raw") is None:
                module.read_surface_state(current)

        return original_update(
            state,
            root=root,
            initialize_if_missing=initialize_if_missing,
            dt=dt,
        )

    module.SurfaceStateIntegrityError = SurfaceStateIntegrityError
    module.ensure_surface = strict_ensure_surface
    module.open_surface = strict_open_surface
    module.read_ciel_internal_state = strict_read_ciel_internal_state
    module.update_surface_from_ciel_state = strict_update_surface_from_ciel_state


def install() -> None:
    """Install the critical guard once for the current interpreter."""
    global _INSTALLED
    if _INSTALLED:
        return
    # The parent logger must be armed before importing legacy submodules so
    # import-time quiet fallbacks cannot run.
    _install_log_guard()
    from . import noema_surface_mmap

    _strict_surface_functions(noema_surface_mmap)
    _INSTALLED = True


__all__ = [
    "CriticalQuietFallbackError",
    "SurfaceStateIntegrityError",
    "install",
]
