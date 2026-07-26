from __future__ import annotations

import sys
from pathlib import Path

import pytest

from binding_state import ensure_active_binding


ROOT = Path(__file__).resolve().parent.parent
EXTRA_PATHS = (
    ROOT,
    ROOT / "src",
    ROOT / "scripts",
    ROOT / "src" / "ciel_rh_control_mini_repo",
    ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM",
)

for path in EXTRA_PATHS:
    text = str(path)
    if path.exists() and text not in sys.path:
        sys.path.insert(0, text)

# Tests use the local emulator binding contract.  This creates only the explicit
# status file; it does not boot the Orbital runtime, warm caches, modify module
# identities, or claim access to an external NOEMA Source of Truth.
ensure_active_binding()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--skip-slow",
        action="store_true",
        default=False,
        help="Skip tests marked as @pytest.mark.slow (orbital bridge, full sapiens pipeline).",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "slow: test requires orbital bridge / full sapiens pipeline (several seconds).",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if not config.getoption("--skip-slow"):
        return
    skip_slow = pytest.mark.skip(reason="skipped with --skip-slow flag")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
