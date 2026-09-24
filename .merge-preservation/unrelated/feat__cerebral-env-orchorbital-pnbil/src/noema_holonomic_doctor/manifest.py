"""Deterministic local manifest builder for NOEMA Holonomic Doctor."""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

_DEFAULT_EXCLUDES = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "node_modules", ".venv", "venv", "dist", "build",
}


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    size: int
    sha256: str
    suffix: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# Files larger than this get a lightweight metadata digest (path+size+mtime)
# instead of a full-content SHA256. Reading and hashing every one of
# ~23000 files' full bytes on every doctor cycle — including large PDFs,
# .npz weight files, HDF5 archives — was the actual cause of the tool
# hanging >500s in D-state (uninterruptible disk I/O wait) on this external
# volume (confirmed 2026-07-08). 1MB keeps genuine source/config files
# fully content-hashed (real change detection) while treating large binary
# assets the way they're actually used here: as opaque blobs whose
# identity for doctor purposes is "did size or mtime change", not their
# exact bytes.
_LARGE_FILE_THRESHOLD = 1_000_000


def _lightweight_digest(path: Path, size: int, mtime_ns: int) -> str:
    payload = f"{path.as_posix()}:{size}:{mtime_ns}".encode("utf-8")
    return "meta:" + hashlib.sha256(payload).hexdigest()


def _should_skip(path: Path, root: Path, excludes: set[str]) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/manifest.py:31 quiet except scope=_should_skip reason=assign_fallback")
        parts = path.parts
    return any(part in excludes for part in parts)


def _cache_path(root_path: Path, report_dir: str = "doctor_reports") -> Path:
    return root_path / report_dir / ".manifest_cache.json"


def _load_cache(cache_file: Path) -> dict[str, dict]:
    if not cache_file.exists():
        return {}
    try:
        return json.loads(cache_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/manifest.py:cache quiet except scope=_load_cache reason=return {}")
        return {}


def _save_cache(cache_file: Path, cache: dict[str, dict]) -> None:
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache, separators=(",", ":")), encoding="utf-8")
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/manifest.py:cache quiet except scope=_save_cache reason=pass")


def noema_ls(
    root: str | Path,
    *,
    excludes: Iterable[str] | None = None,
    use_cache: bool = True,
    report_dir: str = "doctor_reports",
) -> list[ManifestEntry]:
    """Build a deterministic local file manifest without shell ls/grep.

    Reading and full-content-hashing every one of ~23000 files on every
    cycle (this repo, 2026-07-08) was the actual cause of the doctor
    hanging >500s in D-state (uninterruptible disk I/O wait) on this
    external volume — most files are individually small, but per-file
    open/read syscall overhead on this disk adds up across that many
    files, every single run. Fixed with two changes: (1) files above
    _LARGE_FILE_THRESHOLD get a metadata-only digest instead of a full
    read; (2) an mtime/size-keyed cache (doctor_reports/.manifest_cache.json)
    lets unchanged files reuse their previous digest instead of being
    re-read every cycle — this is the one that actually matters for a
    tool meant to run every 30 minutes on a mostly-unchanging tree.
    """
    root_path = Path(root).resolve()
    skip = set(_DEFAULT_EXCLUDES)
    if excludes:
        skip.update(excludes)

    cache_file = _cache_path(root_path, report_dir)
    cache = _load_cache(cache_file) if use_cache else {}
    new_cache: dict[str, dict] = {}

    entries: list[ManifestEntry] = []
    for path in sorted(root_path.rglob("*")):
        if not path.is_file() or _should_skip(path, root_path, skip):
            continue
        rel_path = path.relative_to(root_path)
        rel_str = rel_path.as_posix()
        try:
            stat = path.stat()
        except OSError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/manifest.py:48 quiet except scope=noema_ls reason=continue")
            continue

        cached = cache.get(rel_str)
        if cached and cached.get("size") == stat.st_size and cached.get("mtime_ns") == stat.st_mtime_ns:
            digest = cached["sha256"]
            new_cache[rel_str] = cached
            entries.append(ManifestEntry(path=rel_str, size=stat.st_size, sha256=digest, suffix=path.suffix))
            continue

        if stat.st_size > _LARGE_FILE_THRESHOLD:
            digest = _lightweight_digest(rel_path, stat.st_size, stat.st_mtime_ns)
        else:
            try:
                digest = sha256_bytes(path.read_bytes())
            except OSError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/manifest.py:48 quiet except scope=noema_ls reason=continue")
                continue

        new_cache[rel_str] = {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "sha256": digest}
        entries.append(ManifestEntry(path=rel_str, size=stat.st_size, sha256=digest, suffix=path.suffix))

    if use_cache:
        _save_cache(cache_file, new_cache)

    return entries


def manifest_digest(manifest: Iterable[ManifestEntry]) -> str:
    rows = [asdict(entry) for entry in manifest]
    data = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(data)


__all__ = ["ManifestEntry", "manifest_digest", "noema_ls", "sha256_bytes"]
