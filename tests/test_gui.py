"""Tests for the Flask-based CIEL Quiet Orbital Control GUI.

These tests use Flask's built-in test client and do not require a running
server. They verify route contracts, JSON schemas, rendering, and cache use.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

pytest.importorskip("flask")

from src.ciel_sot_agent.gui.app import create_app  # noqa: E402
import src.ciel_sot_agent.gui.routes as routes  # noqa: E402


@pytest.fixture()
def app():
    root = Path(__file__).resolve().parents[1]
    app = create_app(root=root, debug=False)
    app.config["TESTING"] = True
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


class TestIndexRoute:
    def test_index_returns_200(self, client):
        assert client.get("/").status_code == 200

    def test_index_returns_html(self, client):
        resp = client.get("/")
        assert b"text/html" in resp.content_type.encode() or b"html" in resp.data.lower()

    def test_index_contains_ciel_brand(self, client):
        assert b"CIEL" in client.get("/").data

    def test_index_contains_nav_sections(self, client):
        data = client.get("/").data
        assert b"Control" in data
        assert b"Settings" in data
        assert b"Support" in data

    def test_index_contains_quiet_orbital_identity(self, client):
        data = client.get("/").data
        assert b"Orbital" in data or b"orbital" in data


class TestApiStatus:
    def test_status_returns_200(self, client):
        assert client.get("/api/status").status_code == 200

    def test_status_returns_json(self, client):
        assert client.get("/api/status").is_json

    def test_status_schema(self, client):
        assert client.get("/api/status").get_json()["schema"] == "ciel-gui-status/v1"

    def test_status_has_required_fields(self, client):
        data = client.get("/api/status").get_json()
        required = {
            "system_mode",
            "writeback_gate",
            "backend_status",
            "manifest_version",
            "coherence_index",
            "system_health",
            "closure_penalty",
            "energy_budget",
        }
        for field in required:
            assert field in data, f"Missing field: {field}"

    def test_status_coherence_is_float(self, client):
        assert isinstance(client.get("/api/status").get_json()["coherence_index"], (int, float))

    def test_status_health_is_float(self, client):
        assert isinstance(client.get("/api/status").get_json()["system_health"], (int, float))


class TestApiPanel:
    def test_panel_returns_200(self, client):
        assert client.get("/api/panel").status_code == 200

    def test_panel_returns_json(self, client):
        assert client.get("/api/panel").is_json

    def test_panel_schema(self, client):
        assert client.get("/api/panel").get_json()["schema"] == "ciel-gui-panel/v1"

    def test_panel_has_control_section(self, client):
        data = client.get("/api/panel").get_json()
        assert "control" in data
        assert "coherence_index" in data["control"]
        assert "system_health" in data["control"]
        assert "mode" in data["control"]

    def test_panel_has_communication_section(self, client):
        assert "communication" in client.get("/api/panel").get_json()

    def test_panel_has_support_section(self, client):
        assert "support" in client.get("/api/panel").get_json()


class TestApiModels:
    def test_models_returns_200_or_500(self, client):
        assert client.get("/api/models").status_code in (200, 500)

    def test_models_returns_json(self, client):
        assert client.get("/api/models").is_json

    def test_models_has_schema_on_success(self, client):
        resp = client.get("/api/models")
        if resp.status_code == 200:
            data = resp.get_json()
            assert data["schema"] == "ciel-gui-models/v1"
            assert isinstance(data["models"], list)
            assert "default_installed" in data

    def test_models_ensure_post_method_required(self, client):
        assert client.get("/api/models/ensure").status_code == 405


class TestApiContracts:
    def test_intentions_returns_canonical_shape(self, client):
        resp = client.get("/api/intentions")
        assert resp.status_code == 200
        assert "intentions" in resp.get_json()

    def test_consolidator_results_returns_canonical_shape(self, client):
        resp = client.get("/api/consolidator/results")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "results" in data
        assert "status" in data

    def test_critical_routes_are_unique(self, app):
        critical = {
            "/api/intentions",
            "/api/intentions/add",
            "/api/intentions/done",
            "/api/projects/add",
            "/api/sub/recent",
            "/api/consolidator/results",
        }
        counts = {rule: 0 for rule in critical}
        for rule in app.url_map.iter_rules():
            if rule.rule in counts:
                counts[rule.rule] += 1
        for rule, count in counts.items():
            assert count == 1, f"duplicate route registered: {rule} ({count})"


class TestErrorHandlers:
    def test_404_returns_json(self, client):
        resp = client.get("/nonexistent-route-xyz")
        assert resp.status_code == 404
        assert resp.is_json
        assert "error" in resp.get_json()


class TestAppFactory:
    def test_create_app_with_explicit_root(self, tmp_path):
        app = create_app(root=tmp_path, debug=False)
        assert app is not None
        assert app.config["CIEL_ROOT"] == tmp_path

    def test_create_app_debug_mode(self, tmp_path):
        app = create_app(root=tmp_path, debug=True)
        assert app.config["DEBUG"] is True

    def test_create_app_registers_routes(self, tmp_path):
        app = create_app(root=tmp_path)
        rules = {rule.rule for rule in app.url_map.iter_rules()}
        assert "/" in rules
        assert "/api/status" in rules
        assert "/api/panel" in rules
        assert "/api/models" in rules
        assert "/api/models/ensure" in rules


class TestGuiCaching:
    def test_load_memory_stats_uses_short_ttl_cache(self, monkeypatch, tmp_path):
        app = create_app(root=tmp_path, debug=False)
        state_path = tmp_path / "memory" / "state" / "ciel_orch_state.pkl"
        state_path.parent.mkdir(parents=True)
        state_path.write_bytes(b"stub")
        monkeypatch.setattr(
            routes,
            "P",
            SimpleNamespace(STATE=SimpleNamespace(ORCH_STATE_PKL=str(state_path))),
        )

        calls: list[list[str]] = []

        class Result:
            returncode = 0
            stdout = '{"m2_count":1,"m3_count":2,"identity_phase":0.1,"cycle":3}'

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            return Result()

        monkeypatch.setattr(routes.subprocess, "run", fake_run)
        monkeypatch.setattr(routes, "_MEMORY_STATS_CACHE", {})
        monkeypatch.setattr(routes, "_MEMORY_STATS_CACHE_TS", 0.0)
        monkeypatch.setattr(routes, "_MEMORY_STATS_CACHE_TTL_S", 60.0)

        with app.app_context():
            first = routes._load_memory_stats()
            second = routes._load_memory_stats()

        assert first == second
        assert len(calls) == 1
