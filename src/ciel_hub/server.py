# CIEL Server Hub — ThreadingHTTPServer + Router
# Autor: Adrian Lipa & CIEL
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import signal
import sys
import time
from http.server import HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn
from typing import Any

from .contracts import EndpointRegistry, ok, fail, error_reply
from .snapshot import cache as snapshot_cache

# ─── Threading HTTP Server ────────────────────────────────────────────────

MIME_TYPES: dict[str, str] = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".txt": "text/plain; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".yaml": "text/yaml; charset=utf-8",
    ".yml": "text/yaml; charset=utf-8",
    ".pdf": "application/pdf",
}


class ThreadingHubServer(ThreadingMixIn, HTTPServer):
    """Threading HTTP server dla CIEL Hub — każdy request w osobnym wątku.
    
    Wiele requestów może być obsługiwanych jednocześnie.
    """
    allow_reuse_address = True
    daemon_threads = True


class HubHandler:
    """Handler routingowy — deleguje do routera, serwuje statyczne pliki.
    
    Nie dziedziczy po BaseHTTPRequestHandler — jest czystym routingiem
    używanym przez HubServer.
    """

    def __init__(self, registry: EndpointRegistry, static_root: Path, 
                 registry_obj: Any = None, token: Any = None) -> None:
        self.registry = registry
        self.static_root = static_root.resolve()
        self.registry_obj = registry_obj
        self.token = token
        self.start_time = time.time()

    def handle(self, method: str, path: str, headers: dict, 
               body: bytes, query: dict) -> tuple[dict, int, str]:
        """Główny dispatch — zwraca (response_dict, status_code, content_type)."""
        clean_path = path.split("?")[0].rstrip("/")
        
        # Routing przez registry
        handler, params = self.registry.resolve(method, clean_path)
        if handler is not None:
            try:
                result = handler({
                    "method": method,
                    "path": clean_path,
                    "query": query,
                    "params": params,
                    "headers": headers,
                    "body": body,
                    "server_start": self.start_time,
                    "registry": self.registry_obj,
                    "token": self.token,
                })
                # Handler może zwrócić (dict, int) lub sam dict (wtedy status=200)
                if isinstance(result, tuple):
                    resp, status = result
                else:
                    resp, status = result, 200
                return resp, status, "application/json"
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_hub/server.py:92 quiet except scope=HubHandler.handle reason=no_log_no_raise")
                resp_d, status_d = error_reply(f"handler error: {e}", 500)
                return resp_d, status_d, "application/json"

        # Fallback: pliki statyczne
        if clean_path == "" or clean_path == "/":
            clean_path = "/index.html"
        filepath = (self.static_root / clean_path.lstrip("/")).resolve()
        try:
            if not str(filepath).startswith(str(self.static_root)):
                resp_d, status_d = fail("forbidden", 403)
                return resp_d, status_d, "application/json"
        except (ValueError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_hub/server.py:104 quiet except scope=HubHandler.handle reason=no_log_no_raise")
            resp_d, status_d = fail("forbidden", 403)
            return resp_d, status_d, "application/json"

        if filepath.is_file():
            ext = filepath.suffix.lower()
            ctype = MIME_TYPES.get(ext, "application/octet-stream")
            try:
                data = filepath.read_bytes()
                # Zwracamy surowe dane — caller zapisuje do wfile
                return {
                    "_raw": True,
                    "data": data,
                    "ctype": ctype,
                }, 200, ctype
            except OSError as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_hub/server.py:119 quiet except scope=HubHandler.handle reason=no_log_no_raise")
                resp_d, status_d = fail(f"read error: {e}", 500)
                return resp_d, status_d, "application/json"
        
        resp_d, status_d = fail(f"not found: {path}", 404)
        return resp_d, status_d, "application/json"


def run_server(registry: EndpointRegistry, static_root: str | Path,
               host: str = "0.0.0.0", port: int = 18888,
               registry_obj: Any = None, token: Any = None) -> None:
    """Uruchamia ThreadingHubServer z danym registry.
    
    Używa HubHandler do routingu. Nie modyfikuje starego portala —
    zastępuje go całkowicie.
    """
    static_root = Path(static_root).resolve()
    handler = HubHandler(registry, static_root, registry_obj, token)

    class _RequestHandler:
        """Adapter: BaseHTTPRequestHandler → HubHandler."""

        def __init__(self, request, client_address, server):
            self._handler = handler
            # BaseHTTPRequestHandler init
            super().__init__(request, client_address, server)

        def do_GET(self):
            self._handle_request("GET")

        def do_POST(self):
            self._handle_request("POST")

        def do_PUT(self):
            self._handle_request("PUT")

        def do_DELETE(self):
            self._handle_request("DELETE")

        def _handle_request(self, method: str):
            import urllib.parse
            parsed = urllib.parse.urlparse(self.path)
            query = dict(urllib.parse.parse_qsl(parsed.query))
            
            # Przeczytaj body
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b""

            t0 = time.time()
            resp, status, ctype = self._handler.handle(
                method, self.path, dict(self.headers), body, query
            )
            duration = (time.time() - t0) * 1000

            # Jeśli _raw — zwróć surowe dane
            if isinstance(resp, dict) and resp.get("_raw"):
                self.send_response(200)
                self.send_header("Content-Type", resp["ctype"])
                self.send_header("Content-Length", str(len(resp["data"])))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(resp["data"])
                return

            # JSON response z envelope
            # Dodaj duration do meta jeśli to nasz envelope
            if "meta" in resp and isinstance(resp["meta"], dict):
                resp["meta"]["duration_ms"] = round(duration, 2)

            resp_body = json.dumps(resp, ensure_ascii=False, default=str).encode()
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(resp_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(resp_body)

        def log_message(self, fmt: str, *args):
            t = time.strftime("%H:%M:%S")
            safe = " ".join(str(a) for a in args) if args else fmt
            sys.stderr.write(f"[hub] {t} {safe}\n")

    # Zbuduj klasę handlera z mixin
    import http.server
    HandlerClass = type(
        "HubHTTPHandler",
        (http.server.BaseHTTPRequestHandler,),
        {
            "do_GET": _RequestHandler.do_GET,
            "do_POST": _RequestHandler.do_POST,
            "do_PUT": _RequestHandler.do_PUT,
            "do_DELETE": _RequestHandler.do_DELETE,
            "_handle_request": _RequestHandler._handle_request,
            "log_message": _RequestHandler.log_message,
            "_handler": handler,
        },
    )

    server = ThreadingHubServer((host, port), HandlerClass)
    server.server_name = "ciel_hub"
    server.server_port = port

    print(f"[hub] ThreadingHubServer listening on {host}:{port}", file=sys.stderr)
    print(f"[hub] serving static from {static_root}", file=sys.stderr)
    print(f"[hub] {len(registry._routes)} registered endpoints", file=sys.stderr)

    running = True

    def _stop(signum, frame):
        nonlocal running
        print(f"[hub] stopping (signal {signum})", file=sys.stderr)
        running = False

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    server.timeout = 0.5
    try:
        while running:
            server.handle_request()
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_hub/server.py:241 quiet except scope=run_server reason=assign_fallback")
        running = False
    except Exception as e:
        print(f"[hub] error in loop: {e}", file=sys.stderr)
    finally:
        server.server_close()
        print(f"[hub] stopped", file=sys.stderr)
