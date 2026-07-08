#!/usr/bin/env python3
"""Testy kontraktu CIEL Server Hub — Phase 1.

Sprawdza:
1. Response envelope (ok/data/meta/errors)
2. Endpoint registry (rejestracja, resolve, params)
3. Snapshot cache (register, get, refresh)
4. Endpoint coverage — frontend vs backend
"""
from __future__ import annotations

import json
import os
import sys
import time
import unittest
from pathlib import Path

NOEMA_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(NOEMA_ROOT / "src"))

from ciel_hub.contracts import (
    ok, fail, error_reply,
    EndpointRegistry,
    registry as global_registry,
    check_endpoint_coverage,
)
from ciel_hub.snapshot import SnapshotCache


class TestResponseEnvelope(unittest.TestCase):
    """Test 1: Response envelope ma poprawny format."""

    def test_ok_has_all_fields(self):
        r = ok({"foo": "bar"}, source="test", duration_ms=1.5)
        self.assertTrue(r["ok"])
        self.assertEqual(r["data"], {"foo": "bar"})
        self.assertIn("ts", r["meta"])
        self.assertEqual(r["meta"]["source"], "test")
        self.assertEqual(r["meta"]["duration_ms"], 1.5)
        self.assertEqual(r["errors"], [])

    def test_fail_has_all_fields(self):
        r, status = fail("something went wrong", 400)
        self.assertFalse(r["ok"])
        self.assertIsNone(r["data"])
        self.assertEqual(r["errors"], ["something went wrong"])
        self.assertEqual(status, 400)

    def test_fail_multiple_errors(self):
        r, status = fail(["err1", "err2"], 500)
        self.assertEqual(r["errors"], ["err1", "err2"])
        self.assertEqual(status, 500)

    def test_error_reply(self):
        r, status = error_reply("internal error", 500)
        self.assertFalse(r["ok"])
        self.assertEqual(status, 500)

    def test_ok_default_source(self):
        r = ok(42)
        self.assertEqual(r["meta"]["source"], "ciel_hub")
        self.assertEqual(r["data"], 42)


class TestEndpointRegistry(unittest.TestCase):
    """Test 2: Endpoint registry rejestruje i rozwiązuje ścieżki."""

    def setUp(self):
        self.reg = EndpointRegistry()

    def test_register_and_resolve(self):
        handler = lambda ctx: (ok("hello"), 200)
        self.reg.register("GET", "/api/hello", handler)
        
        fn, params = self.reg.resolve("GET", "/api/hello")
        self.assertIsNotNone(fn)
        self.assertEqual(params, {})

    def test_resolve_wrong_method(self):
        handler = lambda ctx: (ok("hello"), 200)
        self.reg.register("GET", "/api/hello", handler)
        
        fn, params = self.reg.resolve("POST", "/api/hello")
        self.assertIsNone(fn)

    def test_resolve_not_found(self):
        fn, params = self.reg.resolve("GET", "/api/nonexistent")
        self.assertIsNone(fn)

    def test_register_convenience_methods(self):
        self.reg.get("/api/test", lambda ctx: (ok("g"), 200))
        self.reg.post("/api/test", lambda ctx: (ok("p"), 201))
        self.reg.put("/api/test", lambda ctx: (ok("u"), 200))
        self.reg.delete("/api/test", lambda ctx: (ok("d"), 200))
        
        self.assertIsNotNone(self.reg.resolve("GET", "/api/test")[0])
        self.assertIsNotNone(self.reg.resolve("POST", "/api/test")[0])
        self.assertIsNotNone(self.reg.resolve("PUT", "/api/test")[0])
        self.assertIsNotNone(self.reg.resolve("DELETE", "/api/test")[0])

    def test_list_endpoints(self):
        self.reg.get("/api/a", lambda ctx: (ok("a"), 200))
        self.reg.post("/api/b", lambda ctx: (ok("b"), 200))
        eps = self.reg.list_endpoints()
        self.assertEqual(len(eps), 2)
        methods = {e["method"] for e in eps}
        self.assertIn("GET", methods)
        self.assertIn("POST", methods)

    def test_health_endpoint(self):
        # Symulacja endpointu zdrowia
        def health(ctx):
            return ok({
                "status": "ok",
                "pid": os.getpid(),
                "uptime_s": 42.0,
            })
        self.reg.register("GET", "/api/hub/health", health)
        fn, _ = self.reg.resolve("GET", "/api/hub/health")
        self.assertIsNotNone(fn)
        
        ctx = {"method": "GET", "path": "/api/hub/health", "server_start": 0}
        resp, status = fn(ctx)
        self.assertEqual(status, 200)
        self.assertTrue(resp["ok"])
        self.assertEqual(resp["data"]["uptime_s"], 42.0)


class TestEndpointParams(unittest.TestCase):
    """Test 3: Pattern matching z parametrami."""

    def setUp(self):
        self.reg = EndpointRegistry()

    def test_int_param(self):
        self.reg.get("/api/tasks/<int:id>", lambda ctx: (ok(ctx["params"]["id"]), 200))
        
        fn, params = self.reg.resolve("GET", "/api/tasks/42")
        self.assertIsNotNone(fn)
        self.assertEqual(params, {"id": 42})

    def test_str_param(self):
        self.reg.get("/api/modules/<str:name>/<str:action>", 
                     lambda ctx: (ok({"name": ctx["params"]["name"], "action": ctx["params"]["action"]}), 200))
        
        fn, params = self.reg.resolve("GET", "/api/modules/portal/restart")
        self.assertIsNotNone(fn)
        self.assertEqual(params, {"name": "portal", "action": "restart"})

    def test_no_match_wrong_type(self):
        self.reg.get("/api/tasks/<int:id>", lambda ctx: (ok("ok"), 200))
        
        fn, params = self.reg.resolve("GET", "/api/tasks/abc")
        self.assertIsNone(fn)

    def test_short_path(self):
        self.reg.get("/api/tasks/<int:id>", lambda ctx: (ok("ok"), 200))
        
        fn, params = self.reg.resolve("GET", "/api/tasks")
        self.assertIsNone(fn)

    def test_long_path(self):
        self.reg.get("/api/tasks/<int:id>", lambda ctx: (ok("ok"), 200))
        
        fn, params = self.reg.resolve("GET", "/api/tasks/1/extra")
        self.assertIsNone(fn)


class TestSnapshotCache(unittest.TestCase):
    """Test 4: Snapshot cache działa poprawnie."""

    def setUp(self):
        self.cache = SnapshotCache()

    def test_register_and_get(self):
        self.cache.register("test", fetcher=lambda: 42, interval=60.0)
        self.cache._refresh_all()  # force refresh
        val = self.cache.get("test")
        self.assertEqual(val, 42)

    def test_get_unregistered(self):
        val = self.cache.get("nonexistent", default="x")
        self.assertEqual(val, "x")

    def test_get_all(self):
        self.cache.register("a", fetcher=lambda: 1, interval=60.0)
        self.cache.register("b", fetcher=lambda: 2, interval=60.0)
        self.cache._refresh_all()
        all_data = self.cache.get_all()
        self.assertIn("a", all_data)
        self.assertIn("b", all_data)
        self.assertEqual(all_data["a"], 1)
        self.assertEqual(all_data["b"], 2)

    def test_refresh_on_interval(self):
        calls = []
        def fetcher():
            calls.append(1)
            return len(calls)
        
        self.cache.register("counter", fetcher=fetcher, interval=0.1)
        self.cache._refresh_all()
        v1 = self.cache.get("counter")
        
        # Force second refresh by changing last_fetch
        import time
        self.cache._snapshots["counter"].last_fetch = 0
        self.cache._refresh_all()
        v2 = self.cache.get("counter")
        
        self.assertEqual(v1, 1)
        self.assertEqual(v2, 2)

    def test_error_handling(self):
        def broken():
            raise ValueError("test error")
        
        self.cache.register("broken", fetcher=broken, interval=60.0)
        self.cache._refresh_all()
        
        val = self.cache.get("broken", default="fallback")
        self.assertEqual(val, "fallback")
        
        all_data = self.cache.get_all()
        self.assertIn("broken", all_data)
        self.assertIn("error", all_data["broken"])

    def test_status(self):
        self.cache.register("a", fetcher=lambda: None, interval=10.0)
        status = self.cache.status()
        self.assertIn("snapshots", status)
        self.assertIn("keys", status)
        self.assertIn("a", status["keys"])

    def test_start_stop(self):
        self.cache.register("x", fetcher=lambda: 1, interval=1.0)
        self.cache.start()
        self.assertTrue(self.cache._running)
        self.cache.stop()
        self.assertFalse(self.cache._running)

    def test_unregister(self):
        self.cache.register("tmp", fetcher=lambda: 1, interval=1.0)
        self.cache.unregister("tmp")
        self.assertNotIn("tmp", self.cache._snapshots)


class TestHubContractCoverage(unittest.TestCase):
    """Test 5: Sprawdza czy endpointy z frontendu mają pokrycie w backendzie.
    
    To jest TEST STRUKTURALNY — nie uruchamia serwera, tylko porównuje rejestry.
    """

    def setUp(self):
        # Lista fetchy z frontendu (z audytu site/js/)
        self.frontend_fetches = {
            "/api/live",
            "/api/bloch",
            "/api/cards",
            "/api/modules",
            "/api/metrics",
            "/api/knowledge/stats",
            "/api/search",
            "/api/ciel/state",
            "/api/settings",
            "/api/decisions",
            "/api/cielingo/thread",
            "/api/tasks",
            "/api/projects",
            "/api/cielingo/writings",
            "/api/status",
            "/api/status/summary",
            "/api/skills",
            "/api/skills/stats",
            "/api/lessons",
            "/api/plans",
            "/api/hub/health",
            "/api/hub/contracts",
            "/api/hub/snapshot",
            "/api/ciel/identity",
            "/api/ciel/mode",
            "/api/noema/surface",
            "/api/noema/phase",
            "/api/noema/gravity",
            "/api/noema/daemons",
            "/api/noema/modules",
            "/api/memory/stats",
            "/api/phasenav/state",
            "/api/analog",
            "/api/orbital",
            "/api/agent/hint",
            "/api/linux/load",
            "/api/surface/phi",
            "/api/surface/omega",
            "/api/surface/g",
            "/api/tasks/queue",
            "/api/decisions/tree",
        }

        self.backend_routes = set()
        for ep in global_registry.list_endpoints():
            path = ep["path"]
            # Zamień parametry na przykładowe wartości dla porównania
            simple_path = path
            if "<int:" in path:
                simple_path = path.split("<")[0] + "1"  # np. /api/tasks/1
            elif "<str:" in path:
                simple_path = path.split("<")[0] + "test"
            self.backend_routes.add(simple_path)

    def test_all_frontend_endpoints_have_backend(self):
        """Każdy frontend fetch ma odpowiednik w backendzie."""
        missing = []
        for fe in sorted(self.frontend_fetches):
            found = False
            for be in self.backend_routes:
                if fe == be or fe.startswith(be) or be.startswith(fe):
                    found = True
                    break
            if not found:
                missing.append(fe)
        
        if missing:
            self.fail(f"Frontend fetches without backend: {missing}")

    def test_health_endpoint_returns_ok(self):
        """Test logiczny: endpoint health zwraca ok envelope."""
        from ciel_hub.contracts import registry as r
        fn, _ = r.resolve("GET", "/api/hub/health")
        self.assertIsNotNone(fn, "Health endpoint not registered")
        
        ctx = {
            "method": "GET",
            "path": "/api/hub/health",
            "query": {},
            "params": {},
            "server_start": time.time(),
        }
        resp, status = fn(ctx)
        self.assertEqual(status, 200)
        self.assertTrue(resp["ok"])
        self.assertIn("pid", resp["data"])

    def test_snapshot_cache_injected(self):
        """Snapshot cache jest globalny i ma snapshoty po setup."""
        from ciel_hub.snapshot import cache
        status = cache.status()
        self.assertIsInstance(status, dict)
        # Nie wymagamy konkretnych snapshotów — to zależy od setupu


class TestStaticFileServing(unittest.TestCase):
    """Test 6: Serwer potrafi serwować pliki statyczne."""

    def test_site_index_exists(self):
        """Plik index.html istnieje w site/."""
        path = NOEMA_ROOT / "site" / "index.html"
        self.assertTrue(path.exists(), "site/index.html not found")

    def test_site_js_exists(self):
        """Katalog js istnieje."""
        path = NOEMA_ROOT / "site" / "js"
        self.assertTrue(path.is_dir(), "site/js/ not found")


if __name__ == "__main__":
    unittest.main()
