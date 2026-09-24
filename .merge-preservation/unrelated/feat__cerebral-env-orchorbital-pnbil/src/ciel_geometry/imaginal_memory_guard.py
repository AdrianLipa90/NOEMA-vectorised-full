"""Bounded persistent catalog for the NOEMA imaginal memory.

The imaginal surface is a generator, not a mirror of ``/dev/shm``.  Its
catalog lives on the canonical New Volume memory root and is deliberately
bounded before any mmap or phase-memory file is created.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path


_CONFIG_ROOT = Path(__file__).resolve().parents[2] / "config" / "noema_paths.json"
try:
    _CONFIG = json.loads(_CONFIG_ROOT.read_text(encoding="utf-8"))
    _IMAGINAL_ROOT_VALUE = _CONFIG.get("roots", {}).get(
        "imaginal_catalog", "/media/adrian/New Volume/CIEL_memories/imaginal"
    )
except (OSError, json.JSONDecodeError, AttributeError):
    _IMAGINAL_ROOT_VALUE = "/media/adrian/New Volume/CIEL_memories/imaginal"

IMAGINAL_CATALOG_ROOT = Path(_IMAGINAL_ROOT_VALUE)
IMAGINAL_CATALOG_SCHEMA = "noema/imaginal-memory-catalog/v1"
MAX_CATALOG_BYTES = int(
    os.environ.get("NOEMA_IMAGINAL_MAX_BYTES", str(512 * 1024 * 1024))
)
MIN_FREE_BYTES = int(
    os.environ.get("NOEMA_IMAGINAL_MIN_FREE_BYTES", str(2 * 1024 * 1024 * 1024))
)
MAX_SLOTS = int(os.environ.get("NOEMA_IMAGINAL_MAX_SLOTS", "4096"))
MAX_BITS = int(os.environ.get("NOEMA_IMAGINAL_MAX_BITS", "4096"))


class ImaginalMemoryGuardError(RuntimeError):
    """Raised before an imaginal write could exceed its safety contract."""


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def is_canonical_imaginal_path(path: Path) -> bool:
    """Return whether ``path`` belongs to the one persistent imaginal tree."""
    return _is_within(Path(path), IMAGINAL_CATALOG_ROOT)


def _tree_bytes(root: Path) -> int:
    total = 0
    if not root.exists():
        return 0
    for entry in root.rglob("*"):
        if entry.is_file() and not entry.is_symlink():
            try:
                total += entry.stat().st_size
            except OSError as exc:
                raise ImaginalMemoryGuardError(
                    f"cannot inspect imaginal catalog entry: {entry}"
                ) from exc
    return total


def ensure_imaginal_catalog(root: Path) -> Path:
    """Create/validate the single imaginal catalog, never a mirror."""
    root = Path(root)
    if not is_canonical_imaginal_path(root):
        raise ImaginalMemoryGuardError(
            f"imaginal path outside canonical catalog: {root}"
        )
    if root.exists() and root.is_symlink():
        raise ImaginalMemoryGuardError(
            f"imaginal catalog must not be a symlink: {root}"
        )
    IMAGINAL_CATALOG_ROOT.mkdir(parents=True, exist_ok=True)
    marker = IMAGINAL_CATALOG_ROOT / ".catalog-contract.json"
    if marker.exists():
        try:
            contract = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ImaginalMemoryGuardError(
                "imaginal catalog contract is unreadable"
            ) from exc
        if contract.get("schema") != IMAGINAL_CATALOG_SCHEMA:
            raise ImaginalMemoryGuardError(
                "imaginal catalog contract schema mismatch"
            )
    else:
        marker.write_text(
            json.dumps(
                {
                    "schema": IMAGINAL_CATALOG_SCHEMA,
                    "purpose": "imaginal-memory-only",
                    "root": str(IMAGINAL_CATALOG_ROOT),
                    "max_catalog_bytes": MAX_CATALOG_BYTES,
                    "min_free_bytes": MIN_FREE_BYTES,
                    "max_slots": MAX_SLOTS,
                    "max_bits": MAX_BITS,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        marker.chmod(0o600)
    root.mkdir(parents=True, exist_ok=True)
    return root


def guard_imaginal_write(
    root: Path,
    *,
    additional_bytes: int = 0,
    slots: int | None = None,
    bits: int | None = None,
) -> None:
    """Reject unsafe growth before creating or extending imaginal files."""
    root = ensure_imaginal_catalog(Path(root))
    if slots is not None and (slots < 1 or slots > MAX_SLOTS):
        raise ImaginalMemoryGuardError(
            f"imaginal slots {slots} outside [1,{MAX_SLOTS}]"
        )
    if bits is not None and (bits < 256 or bits > MAX_BITS or bits % 256):
        raise ImaginalMemoryGuardError(
            f"imaginal bits {bits} outside 256-byte-aligned [256,{MAX_BITS}]"
        )
    usage = shutil.disk_usage(IMAGINAL_CATALOG_ROOT)
    current = _tree_bytes(IMAGINAL_CATALOG_ROOT)
    projected = current + max(0, int(additional_bytes))
    if projected > MAX_CATALOG_BYTES:
        raise ImaginalMemoryGuardError(
            f"imaginal catalog quota exceeded: {projected} > {MAX_CATALOG_BYTES} bytes"
        )
    if usage.free < MIN_FREE_BYTES + max(0, int(additional_bytes)):
        raise ImaginalMemoryGuardError(
            f"insufficient free space for imaginal write: {usage.free} bytes"
        )


def phase_memory_bytes(*, slots: int, bits: int, n_flavors: int) -> int:
    """Calculate the bounded mmap footprint before allocation."""
    if slots < 1 or slots > MAX_SLOTS:
        raise ImaginalMemoryGuardError(f"imaginal slots {slots} outside quota")
    if bits < 256 or bits > MAX_BITS or bits % 256:
        raise ImaginalMemoryGuardError(f"imaginal bits {bits} outside quota")
    # vectors + occupied + phase + coherence + tick + flavor + event_hash + head
    return (
        slots * bits
        + slots
        + slots * 8 * 2
        + slots * 8
        + slots * n_flavors * 8
        + slots * 32
        + 8
    )


__all__ = [
    "IMAGINAL_CATALOG_ROOT",
    "IMAGINAL_CATALOG_SCHEMA",
    "MAX_CATALOG_BYTES",
    "MIN_FREE_BYTES",
    "MAX_SLOTS",
    "MAX_BITS",
    "ImaginalMemoryGuardError",
    "ensure_imaginal_catalog",
    "guard_imaginal_write",
    "is_canonical_imaginal_path",
    "phase_memory_bytes",
]
