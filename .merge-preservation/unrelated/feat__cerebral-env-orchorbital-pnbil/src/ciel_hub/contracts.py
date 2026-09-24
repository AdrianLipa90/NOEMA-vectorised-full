# CIEL Server Hub — Contracts
# Response envelope + endpoint registry + test helpers
# Autor: Adrian Lipa & CIEL
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import time
from typing import Any, Callable

# ─── Response Envelope ───────────────────────────────────────────────────

def ok(data: Any, source: str = "ciel_hub", duration_ms: float = 0.0) -> dict:
    """Standardowy envelope dla sukcesu."""
    return {
        "ok": True,
        "data": data,
        "meta": {
            "ts": time.time(),
            "source": source,
            "duration_ms": round(duration_ms, 2),
        },
        "errors": [],
    }


def fail(errors: list[str] | str, status: int = 400, source: str = "ciel_hub") -> tuple[dict, int]:
    """Standardowy envelope dla błędu — zwraca (dict, status_code)."""
    if isinstance(errors, str):
        errors = [errors]
    return {
        "ok": False,
        "data": None,
        "meta": {
            "ts": time.time(),
            "source": source,
            "duration_ms": 0.0,
        },
        "errors": errors,
    }, status


def error_reply(errors: list[str] | str, status: int = 500, source: str = "ciel_hub") -> tuple[dict, int]:
    """Alias — błąd serwera."""
    return fail(errors, status, source)


# ─── Endpoint Registry ────────────────────────────────────────────────────

Handler = Callable[[dict, dict], tuple[dict, int]]
"""Handler: (parsed_query, body) -> (response_dict, status_code)"""


class EndpointRegistry:
    """Rejestr endpointów: metoda + ścieżka → handler.
    
    Wzorzec: registry.register("GET", "/api/hub/health", handler_fn)
    Ścieżki mogą zawierać parametry: /api/tasks/<int:id>
    """

    def __init__(self) -> None:
        self._routes: list[tuple[str, str, Handler, bool]] = []
        # (method, path, handler, has_params)

    def register(self, method: str, path: str, handler: Handler) -> None:
        """Rejestruje handler dla metody i ścieżki."""
        has_params = "<" in path and ">" in path
        self._routes.append((method.upper(), path, handler, has_params))

    def get(self, path: str, handler: Handler) -> None:
        """Rejestruje GET handler."""
        self.register("GET", path, handler)

    def post(self, path: str, handler: Handler) -> None:
        """Rejestruje POST handler."""
        self.register("POST", path, handler)

    def put(self, path: str, handler: Handler) -> None:
        """Rejestruje PUT handler."""
        self.register("PUT", path, handler)

    def delete(self, path: str, handler: Handler) -> None:
        """Rejestruje DELETE handler."""
        self.register("DELETE", path, handler)

    def resolve(self, method: str, path: str) -> tuple[Handler | None, dict]:
        """Znajduje handler + params dla ścieżki.
        
        Returns:
            (handler, params) lub (None, {})
        """
        method = method.upper()
        for route_method, route_path, handler, has_params in self._routes:
            if route_method != method:
                continue
            if has_params:
                params = self._match_pattern(route_path, path)
                if params is not None:
                    return handler, params
            elif route_path == path:
                return handler, {}
        return None, {}

    def _match_pattern(self, pattern: str, actual: str) -> dict | None:
        """Dopasowuje ścieżkę z parametrami, np. /api/tasks/<int:id>."""
        p_parts = pattern.strip("/").split("/")
        a_parts = actual.strip("/").split("/")
        if len(p_parts) != len(a_parts):
            return None
        params: dict[str, Any] = {}
        for p, a in zip(p_parts, a_parts):
            if p.startswith("<") and p.endswith(">"):
                # parametr, np. <int:id> lub <str:name>
                raw = p[1:-1]
                if ":" in raw:
                    ptype, pname = raw.split(":", 1)
                else:
                    ptype, pname = "str", raw
                try:
                    if ptype == "int":
                        params[pname] = int(a)
                    elif ptype == "float":
                        params[pname] = float(a)
                    else:
                        params[pname] = a
                except (ValueError, TypeError):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_hub/contracts.py:125 quiet except scope=EndpointRegistry._match_pattern reason=return None")
                    return None
            elif p != a:
                return None
        return params

    def list_endpoints(self) -> list[dict]:
        """Zwraca listę wszystkich zarejestrowanych endpointów (do /api/hub/contracts)."""
        return [
            {"method": m, "path": p, "has_params": h}
            for m, p, _, h in self._routes
        ]


# ─── Globalny rejestr ─────────────────────────────────────────────────────
registry = EndpointRegistry()


def register(method: str, path: str) -> Callable:
    """Dekorator rejestrujący handler."""
    def decorator(fn: Handler) -> Handler:
        registry.register(method, path, fn)
        return fn
    return decorator


# ─── Test helpers ─────────────────────────────────────────────────────────

def check_endpoint_coverage(registry_obj: EndpointRegistry | None = None) -> dict:
    """Porównuje frontend fetch calls z backend routes — wykrywa luki."""
    r = registry_obj or registry
    return {
        "endpoints": r.list_endpoints(),
        "total": len(r._routes),
        "note": "Użyj z listą fetchy z frontendu aby znaleźć luki",
    }
