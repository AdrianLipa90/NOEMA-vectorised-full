from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import sys
from pathlib import Path

import pytest

from binding_state import ensure_active_binding

ensure_active_binding()

ROOT = Path(__file__).resolve().parent.parent
EXTRA_PATHS = (
    ROOT,
    ROOT / "src",
    ROOT / "src" / "ciel_rh_control_mini_repo",
    ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM",
)

for path in EXTRA_PATHS:
    text = str(path)
    if path.exists() and text not in sys.path:
        sys.path.insert(0, text)

try:
    import integration.Orbital.main.bootstrap  # noqa: F401
except Exception:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("tests/conftest.py:23 quiet except scope=<module> reason=pass")
    pass


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--skip-slow",
        action="store_true",
        default=False,
        help="Skip tests marked as @pytest.mark.slow (orbital bridge, full sapiens pipeline).",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "slow: test requires orbital bridge / full sapiens pipeline (several seconds).")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--skip-slow"):
        skip_slow = pytest.mark.skip(reason="skipped with --skip-slow flag")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


@pytest.fixture(scope="session", autouse=True)
def warm_ciel_pipeline() -> None:
    """Pre-warm the CIEL engine and lingo caches before any test runs.

    The first call to ``build_orbital_bridge`` / ``run_ciel_pipeline`` /
    ``build_lingo_frame`` is by far the most expensive (~7-8 s).  Running a
    minimal warm-up once at session start ensures that the heavy imports and
    engine initialisation happen before the first slow test, rather than
    inside it.
    """
    from src.ciel_sot_agent.ciel_pipeline import warm_ciel_pipeline

    warm_ciel_pipeline(ROOT)
