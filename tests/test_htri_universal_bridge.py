from __future__ import annotations

import importlib.util
from pathlib import Path


BRIDGE_PATH = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/runtime/wrappers/vector_continuous_cqcl_lingophysics_htri/noema_vector_continuous_bridge.py")


def load_bridge_module():
    spec = importlib.util.spec_from_file_location("noema_htri_universal_bridge", BRIDGE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bridge_builds_report():
    mod = load_bridge_module()
    report = mod.build_bridge_report()

    assert report["schema"] == "noema/htri-universal-bridge/v1"
    assert "binding" in report
    assert "htri" in report
    assert "phasenav" in report
    assert "surface" in report


def test_bridge_write_roundtrip(tmp_path, monkeypatch):
    mod = load_bridge_module()
    out = tmp_path / "bridge.json"
    monkeypatch.setattr(mod, "BRIDGE_OUTPUT", out)

    report = mod.build_bridge_report()
    written = mod.write_bridge_report(report)

    assert written == out
    assert out.exists()
