"""Local dependency bootstrap for NOEMA.

This module prepends the repository-local ``.python_packages`` directory to
``sys.path`` so entrypoints imported from ``src/`` can see user-space
dependencies installed inside the repository.
"""

from __future__ import annotations

import sys
from pathlib import Path


def activate_local_packages() -> str | None:
    root = Path(__file__).resolve().parent.parent
    local_packages = root / ".python_packages"
    if not local_packages.is_dir():
        return None
    path = str(local_packages)
    if path not in sys.path:
        sys.path.insert(0, path)
    return path


__all__ = ["activate_local_packages"]
