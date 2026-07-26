"""Local dependency bootstrap for NOEMA.

The module is intentionally top-level because installed console entrypoints and
``ciel_sot_agent`` import it before any optional package paths are activated.
It prepends the repository-local ``.python_packages`` directory only when the
code is running from a checkout that actually contains that directory.
"""

from __future__ import annotations

import sys
from pathlib import Path


def activate_local_packages() -> str | None:
    root = Path(__file__).resolve().parent
    local_packages = root / ".python_packages"
    if not local_packages.is_dir():
        return None
    path = str(local_packages)
    if path not in sys.path:
        sys.path.insert(0, path)
    return path


__all__ = ["activate_local_packages"]
