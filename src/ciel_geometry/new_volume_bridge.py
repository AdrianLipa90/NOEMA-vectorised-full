from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — hardcoded, immutable.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


import json
from pathlib import Path

NEW_VOLUME = Path("/media/adrian/New Volume")
NOEMA_LIBRARY = NEW_VOLUME / "NOEMA_LIBRARY"
NOEMA_PHASE_DATA = NEW_VOLUME / "NOEMA_PHASE_DATA"

TIER3_SOURCES = {
    "agent_db": NOEMA_LIBRARY / "agent_db",
    "pdf_archive": NOEMA_LIBRARY / "PDF",
    "library_index": NOEMA_PHASE_DATA / "PHASE_INDEX",
    "surface_history": NOEMA_PHASE_DATA / "SURFACE_HISTORY",
    "wave_archive": NOEMA_PHASE_DATA / "WAVE_ARCHIVE",
    "experiments": NOEMA_PHASE_DATA / "EXPERIMENTS",
    "training": NOEMA_PHASE_DATA / "TRAINING",
    "query_cache": NOEMA_PHASE_DATA / "QUERY_CACHE",
}


def available() -> bool:
    return NEW_VOLUME.exists()


def disk_gb() -> float:
    if not available():
        return 0.0
    s = NEW_VOLUME.stat()
    try:
        import os
        st = os.statvfs(str(NEW_VOLUME))
        return (st.f_bavail * st.f_frsize) / (1024 ** 3)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/new_volume_bridge.py:40 quiet except scope=disk_gb reason=return 0.0")
        return 0.0


def status() -> dict:
    if not available():
        return {"available": False, "path": str(NEW_VOLUME), "gb": 0.0, "sources": {}}
    sources = {}
    for name, p in TIER3_SOURCES.items():
        ok = p.exists()
        count = -1
        if ok:
            try:
                count = len(list(p.iterdir()))
            except PermissionError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/new_volume_bridge.py:54 quiet except scope=status reason=assign_fallback")
                count = -2
        sources[name] = {"exists": ok, "items": count}
    return {
        "available": True,
        "path": str(NEW_VOLUME),
        "gb": round(disk_gb(), 2),
        "sources": sources,
    }


def sync_library_index(target: Path | None = None) -> dict:
    """Copy library_index.npy from PHASE_INDEX to a local path if needed."""
    src = TIER3_SOURCES["library_index"] / "library_index.npy"
    if not src.exists():
        return {"ok": False, "reason": "source missing"}
    if target is None:
        target = Path("/dev/shm/ciel_noema/library_index.npy")
    import shutil
    try:
        shutil.copy2(str(src), str(target))
        return {"ok": True, "target": str(target), "size_kb": round(src.stat().st_size / 1024, 1)}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/new_volume_bridge.py:76 quiet except scope=sync_library_index reason=return {\"ok\": False, \"reason\": str(e)}")
        return {"ok": False, "reason": str(e)}
