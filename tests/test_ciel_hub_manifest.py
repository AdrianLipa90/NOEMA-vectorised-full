from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
HUB_PATH = PROJECT_ROOT / "scripts" / "ciel_hub_daemon.py"
sys.path.insert(0, str(SRC_ROOT))


def _load_hub_module():
    spec = importlib.util.spec_from_file_location("ciel_hub_daemon", HUB_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["ciel_hub_daemon"] = module
    spec.loader.exec_module(module)
    return module


hub = _load_hub_module()


def test_portal_manifest_covers_full_architecture() -> None:
    manifest = hub.build_portal_manifest()

    assert manifest["status"] == "ok"
    assert manifest["version"] == "hub-manifest/v2"
    assert manifest["hub"]["port"] == 18888
    assert manifest["summary"]["page_count"] == 19
    assert any(layer["name"] == "PhaseNav / Geometry" for layer in manifest["layers"])
    assert any(ep["path"] == "/api/phasenav/graphics" for ep in manifest["endpoints"])
    assert any(ep["path"] == "/api/portal/manifest" for ep in manifest["endpoints"])
    assert any(ep["path"] == "/api/modules" for ep in manifest["endpoints"])
    assert any(page["route"] == "live" for page in manifest["pages"])
    assert any(page["route"] == "metrics" for page in manifest["pages"])
    assert any(page["route"] == "monograph" for page in manifest["pages"])
    assert any(page["route"] == "graph" for page in manifest["pages"])
    assert any(page["route"] == "science" for page in manifest["pages"])
    assert any(page["route"] == "engineering" for page in manifest["pages"])
    assert any(page["route"] == "simulations" for page in manifest["pages"])
    pages = {page["route"]: page for page in manifest["pages"]}
    assert "architecture" in pages
    assert "/api/hub/contracts" in pages["architecture"]["sources"]
    assert "/api/phasenav/graphics" in pages["phasenav"]["sources"]
    assert "/api/noema/surface" in pages["preferences"]["sources"]
    assert "/api/knowledge/stats" in pages["graph"]["sources"]
    assert "/api/skills/stats" in pages["engineering"]["sources"]
    assert "/api/phasenav/graphics" in pages["simulations"]["sources"]


def test_phasenav_graphics_route_uses_scene_query(monkeypatch) -> None:
    monkeypatch.setattr(
        hub,
        "_build_phasenav_graphics_bundle",
        lambda query, surface=None: {
            "query": query,
            "surface": {"tick": 1, "coherence": 0.5},
            "scene_counts": {"memory": {"nodes": 2, "edges": 1}},
            "scenes": {
                "surface": {"svg": "<svg/>", "summary": {"node_count": 1, "edge_count": 0}},
                "memory": {"svg": "<svg/>", "summary": {"node_count": 2, "edge_count": 1}},
            },
        },
    )
    monkeypatch.setattr(hub, "surface", {"phi": [], "omega": [], "g": []})

    result = hub.api_phasenav_graphics({"query": {"q": "arch", "scene": "memory"}})
    if isinstance(result, tuple):
        payload, status = result
    else:
        payload, status = result, 200

    assert status == 200
    assert payload["ok"] is True
    assert payload["data"]["scene_name"] == "memory"
    assert payload["data"]["scene_counts"]["memory"]["nodes"] == 2
    assert payload["data"]["scene"]["summary"]["node_count"] == 2


def test_metrics_route_exposes_metric_list_and_surface_state() -> None:
    result = hub.api_metrics({})
    if isinstance(result, tuple):
        payload, status = result
    else:
        payload, status = result, 200
    assert status == 200
    assert payload["ok"] is True
    data = payload["data"]
    assert isinstance(data["metrics"], list)
    live_result = hub.api_live({})
    live_payload = live_result[0] if isinstance(live_result, tuple) else live_result
    assert "surface_ready" in live_payload["data"]
