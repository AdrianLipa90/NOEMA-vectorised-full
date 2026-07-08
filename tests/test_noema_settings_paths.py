from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
SETTINGS_PATH = SRC_ROOT / "ciel_geometry" / "noema_settings.py"
sys.path.insert(0, str(SRC_ROOT))


def _load_settings_module():
    spec = importlib.util.spec_from_file_location("ciel_geometry.noema_settings", SETTINGS_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["ciel_geometry.noema_settings"] = module
    spec.loader.exec_module(module)
    return module


def test_noema_settings_imports_with_library_defaults() -> None:
    mod = _load_settings_module()

    assert mod.NOEMA_DEFAULTS.system.agent_db.endswith("agent_db")
    assert mod.NOEMA_DEFAULTS.system.db_root.endswith("DB")
    assert mod.NOEMA_DEFAULTS.system.state_root.endswith("STATE")
    assert mod.NOEMA_DEFAULTS.system.logs_root.endswith("LOGS")
    assert mod.NOEMA_DEFAULTS.system.cards_root.endswith("CARDS")
    assert mod.NOEMA_DEFAULTS.system.memories_root.endswith("MEMORIES")

    settings = mod.load()
    assert settings.system.agent_db.endswith("agent_db")
    assert settings.system.noema_library
