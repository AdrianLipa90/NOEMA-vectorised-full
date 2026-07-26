"""CIEL Server Hub response envelopes and endpoint registry."""

from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Any, Callable

_LOG = logging.getLogger(__name__)


def ok(data: Any, source: str = "ciel_hub", duration_ms: float = 0.0) -> dict[str, Any]:
    """Return the standard successful response envelope."""
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


def fail(
    errors: list[str] | str,
    status: int = 400,
    source: str = "ciel_hub",
) -> tuple[dict[str, Any], int]:
    """Return the standard failed response envelope and HTTP status."""
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


def error_reply(
    errors: list[str] | str,
    status: int = 500,
    source: str = "ciel_hub",
) -> tuple[dict[str, Any], int]:
    """Server-error alias for :func:`fail`."""
    return fail(errors, status, source)


Handler = Callable[..., tuple[dict[str, Any], int]]


def _normalise_handler(handler: Callable[..., Any]) -> Handler:
    """Adapt legacy envelope-only handlers to the canonical tuple ABI."""
    if getattr(handler, "_ciel_hub_normalised", False):
        return handler  # type: ignore[return-value]

    @wraps(handler)
    def normalised(*args: Any, **kwargs: Any) -> tuple[dict[str, Any], int]:
        result = handler(*args, **kwargs)
        if (
            isinstance(result, tuple)
            and len(result) == 2
            and isinstance(result[1], int)
        ):
            return result
        if not isinstance(result, dict):
            _LOG.warning("Hub handler %s returned a non-envelope value", handler)
            return error_reply("invalid hub handler response", 500)
        return result, 200

    setattr(normalised, "_ciel_hub_normalised", True)
    return normalised


class EndpointRegistry:
    """Map an HTTP method and path pattern to a canonical handler.

    Re-registering the same method/path replaces the previous handler. This lets
    safe read-only bootstrap routes exist before an optional full server module
    loads, while ensuring the full implementation takes precedence afterwards.
    """

    def __init__(self) -> None:
        self._routes: list[tuple[str, str, Handler, bool]] = []

    def register(self, method: str, path: str, handler: Callable[..., Any]) -> None:
        method = method.upper()
        has_params = "<" in path and ">" in path
        self._routes = [
            route
            for route in self._routes
            if not (route[0] == method and route[1] == path)
        ]
        self._routes.append((method, path, _normalise_handler(handler), has_params))

    def get(self, path: str, handler: Callable[..., Any]) -> None:
        self.register("GET", path, handler)

    def post(self, path: str, handler: Callable[..., Any]) -> None:
        self.register("POST", path, handler)

    def put(self, path: str, handler: Callable[..., Any]) -> None:
        self.register("PUT", path, handler)

    def delete(self, path: str, handler: Callable[..., Any]) -> None:
        self.register("DELETE", path, handler)

    def resolve(self, method: str, path: str) -> tuple[Handler | None, dict[str, Any]]:
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

    @staticmethod
    def _match_pattern(pattern: str, actual: str) -> dict[str, Any] | None:
        pattern_parts = pattern.strip("/").split("/")
        actual_parts = actual.strip("/").split("/")
        if len(pattern_parts) != len(actual_parts):
            return None

        params: dict[str, Any] = {}
        for expected, value in zip(pattern_parts, actual_parts):
            if expected.startswith("<") and expected.endswith(">"):
                raw = expected[1:-1]
                parameter_type, parameter_name = (
                    raw.split(":", 1) if ":" in raw else ("str", raw)
                )
                try:
                    if parameter_type == "int":
                        params[parameter_name] = int(value)
                    elif parameter_type == "float":
                        params[parameter_name] = float(value)
                    else:
                        params[parameter_name] = value
                except (ValueError, TypeError):
                    return None
            elif expected != value:
                return None
        return params

    def list_endpoints(self) -> list[dict[str, Any]]:
        return [
            {"method": method, "path": path, "has_params": has_params}
            for method, path, _, has_params in self._routes
        ]


registry = EndpointRegistry()


def register(method: str, path: str) -> Callable[[Callable[..., Any]], Handler]:
    """Decorator registering a handler in the global hub registry."""
    def decorator(function: Callable[..., Any]) -> Handler:
        registry.register(method, path, function)
        resolved, _ = registry.resolve(method, path)
        assert resolved is not None
        return resolved

    return decorator


def _search_fallback(context: dict[str, Any]) -> tuple[dict[str, Any], int]:
    query = str((context.get("query") or {}).get("q", ""))
    return ok({"query": query, "results": []}, source="ciel_hub/bootstrap"), 200


def _projects_fallback(_context: dict[str, Any]) -> tuple[dict[str, Any], int]:
    return ok({"projects": []}, source="ciel_hub/bootstrap"), 200


# These read-only bootstrap contracts close the frontend/backend surface even
# when the optional project index or search subsystem is not loaded. A later
# full registration replaces them by design.
registry.get("/api/search", _search_fallback)
registry.get("/api/projects", _projects_fallback)


def check_endpoint_coverage(registry_obj: EndpointRegistry | None = None) -> dict[str, Any]:
    target = registry_obj or registry
    return {
        "endpoints": target.list_endpoints(),
        "total": len(target._routes),
        "note": "Compare this registry with frontend fetch calls to locate gaps.",
    }


__all__ = [
    "EndpointRegistry",
    "Handler",
    "check_endpoint_coverage",
    "error_reply",
    "fail",
    "ok",
    "register",
    "registry",
]
