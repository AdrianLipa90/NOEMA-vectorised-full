from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PORTAL_PATH = PROJECT_ROOT / "scripts" / "noema_portal_daemon.py"
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def _load_portal_module():
    spec = importlib.util.spec_from_file_location("noema_portal_daemon", PORTAL_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["noema_portal_daemon"] = module
    spec.loader.exec_module(module)
    return module


portal = _load_portal_module()


def test_build_metrics_catalog_uses_live_state(monkeypatch) -> None:
    monkeypatch.setattr(portal, "start_time", time.time() - 42.0)
    monkeypatch.setattr(
        portal,
        "init_noema",
        lambda: {
            "tick": 9,
            "coherence": 0.81,
            "euler_residual": 0.12,
            "omega_mean": 1.3,
            "tau_mean": 0.4,
            "semantic_density": 0.6,
            "tau_dilation": 0.7,
            "mass_total": 2.1,
            "unruh_power": 3.5,
            "mood": 0.2,
            "ethical_score": 0.88,
            "soul_invariant": 0.91,
        },
    )
    monkeypatch.setattr(portal, "scan_registry", lambda: [{"alive": True}, {"alive": False}])

    catalog = portal.build_metrics_catalog()

    assert catalog["status"] == "ok"
    assert catalog["summary"]["active_daemons"] == 1
    assert any(item["key"] == "tick" for item in catalog["metrics"])
    assert "surface" in catalog["groups"]
    assert "portal" in catalog["groups"]


def test_build_portal_manifest_exposes_architecture_page() -> None:
    manifest = portal.build_portal_manifest()

    assert manifest["status"] == "ok"
    assert manifest["version"] == "portal-manifest/v1"
    assert manifest["layers"]
    assert manifest["endpoints"]
    pages = {page["route"]: page for page in manifest["pages"]}
    assert "architecture" in pages
    assert "/api/portal/manifest" in pages["architecture"]["sources"]
    assert "/api/phasenav/graphics" in pages["phasenav"]["sources"]
    assert any(pipe["to"] == "/api/cielingo/chat" for pipe in manifest["pipelines"])
