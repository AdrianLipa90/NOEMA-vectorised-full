"""Project root path resolution for the CIEL-SOT-Agent package.

Provides ``resolve_project_root(anchor)`` which locates the repository root
by checking the ``CIEL_SOT_ROOT`` environment variable first, then walking
parent directories until one containing an ``integration/`` subdirectory is
found.

Also provides ``resolve_existing_path`` which returns the first candidate
relative path (under a given root) that already exists on disk.
"""
from __future__ import annotations

import os
from pathlib import Path


def resolve_project_root(anchor: str | Path) -> Path:
    env_root = os.getenv("CIEL_SOT_ROOT")
    if env_root:
        candidate = Path(env_root).resolve()
        if (candidate / "integration").exists():
            return candidate

    anchor_path = Path(anchor).resolve()
    for parent in [anchor_path.parent, *anchor_path.parents]:
        if (parent / "integration").exists():
            return parent

    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "integration").exists():
            return parent

    return anchor_path.parents[2]


def resolve_existing_path(root: str | Path, *candidates: str) -> Path:
    """Return the first candidate path under *root* that exists on disk.

    Falls back to ``root / candidates[0]`` when none of the candidates exist,
    so callers can safely use the result without an existence check.
    """
    root = Path(root)
    for candidate in candidates:
        candidate_path = root / candidate
        if candidate_path.exists():
            return candidate_path
    return root / candidates[0]


def ciel_memories_root() -> Path:
    """Canonical CIEL_memories location — never Pulpit (Desktop).

    Delegates to ``ciel_geometry.paths.P.MEMORY``, the single existing
    config-driven source of truth (already correctly resolving to New
    Volume1 via ~/.config/noema/paths.json). Do not hardcode
    ``Path.home() / "Pulpit" / "CIEL_memories"`` anywhere — call this
    function instead. (2026-07-08: consolidated after 39 files were found
    hardcoding the Pulpit path directly, bypassing this config system
    entirely, which kept recreating a CIEL_memories folder on the Desktop
    despite it being repeatedly moved to New Volume1.)
    """
    try:
        from ciel_geometry.paths import P
        return Path(P.MEMORY)
    except Exception:
        env_root = os.getenv("CIEL_MEMORIES_ROOT")
        if env_root:
            return Path(env_root)
        return Path("/media/adrian/New Volume/CIEL_memories")
