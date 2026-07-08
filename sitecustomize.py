"""NOEMA local dependency bootstrap.

Python imports this module automatically on startup when the repository root is
on ``sys.path``. It prepends the local ``.python_packages`` directory so NOEMA
can use repo-local dependencies without system-wide installation.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOCAL_PACKAGES = ROOT / ".python_packages"

if LOCAL_PACKAGES.is_dir():
    local_path = str(LOCAL_PACKAGES)
    if local_path not in sys.path:
        sys.path.insert(0, local_path)
