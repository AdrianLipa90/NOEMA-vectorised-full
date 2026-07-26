from __future__ import annotations

import importlib.util
import warnings
from pathlib import Path


def test_inactive_binding_warning_names_loaded_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "cielingo_core"
        / "bridge"
        / "knowledge_bridge.py"
    )
    module_name = "knowledge_bridge_provenance_probe"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        spec.loader.exec_module(module)

    messages = [str(item.message) for item in captured]
    assert any(
        f"module {module_name} loaded with binding INACTIVE" in message
        for message in messages
    )
    assert all("{__name__}" not in message for message in messages)
