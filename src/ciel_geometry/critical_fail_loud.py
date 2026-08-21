"""Fail-loud continuity guard for critical NOEMA/CIEL state paths.

The guard blocks continuity-critical legacy ``logger.exception(...); fallback``
handlers before the fallback can execute, and post-processes the NOEMA surface
module at import time so existing mmap state is never truncated as recovery.

It deliberately preserves the package's lazy-import contract.
"""
from __future__ import annotations

import importlib.abc
import importlib.machinery
import json
import logging
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Mapping

import numpy as np


class CriticalQuietFallbackError(RuntimeError):
    """A legacy quiet fallback was reached on a continuity-critical path."""


class SurfaceStateIntegrityError(RuntimeError):
    """Existing surface state cannot be restored without mutation or guessing."""


_CRITICAL_MARKERS = (
    "scope=<module> reason=assign_fallback",
    "scope=evolve_surface reason=assign_fallback",
    "scope=read_ciel_internal_state reason=return {}",
    "scope=ensure_surface",
    "scope=open_surface",
    "scope=sync_surface_holonomy reason=assign_fallback",
    "scope=update_surface_from_ciel_state reason=pass",
    "scope=MentalistMemoryPalace.__init__ reason=pass",
    "scope=NonlocalChannel.__init__ reason=assign_fallback",
    "scope=NonlocalChannel._load_rag_cache reason=pass",
    "scope=NonlocalChannel._save_rag_cache reason=pass",
    "scope=UnifiedPhaseNavIndex._load_knowledge_db",
    "scope=UnifiedPhaseNavIndex._load_palace_rooms",
    "scope=UnifiedPhaseNavIndex._load_taskplan_db",
    "scope=UnifiedPhaseNavIndex._load_task_queue",
    "scope=UnifiedPhaseNavIndex._load_system_map",
    "scope=UnifiedPhaseNavIndex._load_cielingo_source",
)

_CRITICAL_LOGGERS = (
    "ciel_geometry.noema_surface_mmap",
    "ciel_geometry.memory_palace",
    "ciel_geometry.nonlocal_channel",
    "ciel_geometry.phasenav_unified",
)
_SURFACE_MODULE = "ciel_geometry.noema_surface_mmap"
_INSTALLED = False


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


def _install_log_guard() -> None:
    for logger_name in _CRITICAL_LOGGERS:
        logger = logging.getLogger(logger_name)
        if any(getattr(h, "_noema_critical_fail_loud", False) for h in logger.handlers):
            continue
        handler = _CriticalQuietHandler(level=logging.ERROR)
        handler._noema_critical_fail_loud = True  # type: ignore[attr-defined]
        logger.addHandler(handler)


def _strict_surface_functions(module: Any) -> None:
    if getattr(module, "__noema_fail_loud_patched__", False):
        return
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
    module.__noema_fail_loud_patched__ = True


class _SurfacePostLoader(importlib.abc.Loader):
    def __init__(self, wrapped: importlib.abc.Loader):
        self._wrapped = wrapped

    def create_module(self, spec):  # type: ignore[no-untyped-def]
        create = getattr(self._wrapped, "create_module", None)
        return create(spec) if create is not None else None

    def exec_module(self, module: ModuleType) -> None:
        execute = getattr(self._wrapped, "exec_module", None)
        if execute is None:
            raise ImportError(f"loader for {_SURFACE_MODULE} has no exec_module")
        execute(module)
        _strict_surface_functions(module)


class _SurfacePostFinder(importlib.abc.MetaPathFinder):
    _noema_fail_loud_finder = True

    def find_spec(self, fullname, path, target=None):  # type: ignore[no-untyped-def]
        if fullname != _SURFACE_MODULE:
            return None
        spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
        if spec is None or spec.loader is None:
            return spec
        if isinstance(spec.loader, _SurfacePostLoader):
            return spec
        spec.loader = _SurfacePostLoader(spec.loader)
        return spec


def _install_surface_hook() -> None:
    existing = sys.modules.get(_SURFACE_MODULE)
    if existing is not None:
        _strict_surface_functions(existing)
        return
    if any(getattr(finder, "_noema_fail_loud_finder", False) for finder in sys.meta_path):
        return
    sys.meta_path.insert(0, _SurfacePostFinder())


def install() -> None:
    """Install the critical guard once for the current interpreter."""
    global _INSTALLED
    if _INSTALLED:
        return
    _install_log_guard()
    _install_surface_hook()
    _INSTALLED = True


__all__ = [
    "CriticalQuietFallbackError",
    "SurfaceStateIntegrityError",
    "install",
]
