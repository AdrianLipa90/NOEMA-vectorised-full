from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from ciel_geometry.daemon_registry import REGISTRY_FILE, REGISTRY_PATH, Registry  # noqa: E402


def test_registry_uses_file_inside_directory() -> None:
    with Registry() as reg:
        assert isinstance(reg.scan(), list)
    assert REGISTRY_PATH.is_dir()
    assert REGISTRY_FILE.parent == REGISTRY_PATH
    assert REGISTRY_FILE.exists()
