#!/usr/bin/env python3
"""NOEMA HTTP Server — własny, zero-zależnościowy serwer HTTP na raw socket.

Architektura:
- Thread-per-connection (accept → spawn thread)
- SSE przez długie połączenia z okresowym heartbeat
- Routing: dekorator @server.route(method, path) lub dict
- Static file serving z katalogu

Usage:
    from ciel_geometry.noema_httpd import NOEMAServer

    server = NOEMAServer(host="0.0.0.0", port=18888, static_dir="/path/to/site")
    server.route("GET", "/api/status", handler_fn)
    server.start()
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import enum
import json
import mimetypes
import os
import socket
import struct
import sys
import threading
import time
import traceback
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from email.utils import formatdate
from pathlib import Path
from typing import Any, Callable, Optional
from urllib.parse import unquote, urlparse

__version__ = "0.1.0"

# ─── MIME types ─────────────────────────────────────────────────────────
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("application/wasm", ".wasm")


# ─── Request / Response ─────────────────────────────────────────────────

@dataclass
class Request:
    """Parsed HTTP request."""
    method: str = ""
    path: str = ""
    query: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    body: bytes = b""
    client_addr: tuple = ("0.0.0.0", 0)

    @property
    def path_clean(self) -> str:
        """Normalizowana ścieżka (bez query string, bez ../)."""
        p = unquote(self.path.split("?")[0])
        # Security: zapobiegaj path traversal
        parts = []
        for part in p.split("/"):
            if part in ("", ".", ".."):
                continue
            parts.append(part)
        return "/" + "/".join(parts)


@dataclass
class Response:
    """HTTP response builder."""
    status: int = 200
    headers: dict = field(default_factory=dict)
    body: bytes = b""
    _stream: Optional[Callable] = None  # SSE stream generator

    @staticmethod
    def json(data: Any, status: int = 200) -> "Response":
        body = json.dumps(data, default=str, separators=(",", ":")).encode("utf-8")
        return Response(
            status=status,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
            },
            body=body,
        )

    @staticmethod
    def html(body: str, status: int = 200) -> "Response":
        data = body.encode("utf-8")
        return Response(
            status=status,
            headers={
                "Content-Type": "text/html; charset=utf-8",
            },
            body=data,
        )

    @staticmethod
    def text(body: str, status: int = 200) -> "Response":
        data = body.encode("utf-8")
        return Response(
            status=status,
            headers={
                "Content-Type": "text/plain; charset=utf-8",
            },
            body=data,
        )

    @staticmethod
    def error(status: int, message: str = "") -> "Response":
        codes = {400: "Bad Request", 404: "Not Found", 405: "Method Not Allowed",
                 413: "Payload Too Large", 500: "Internal Server Error", 502: "Bad Gateway"}
        msg = message or codes.get(status, "Error")
        body = json.dumps({"error": msg}, separators=(",", ":")).encode("utf-8")
        return Response(
            status=status,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
            },
            body=body,
        )

    @staticmethod
    def sse(stream_gen: Callable) -> "Response":
        """SSE endpoint — stream_gen to generator (yield SSE-formatted str)."""
        return Response(
            status=200,
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "X-Accel-Buffering": "no",
            },
            _stream=stream_gen,
        )

    @staticmethod
    def redirect(location: str, status: int = 302) -> "Response":
        return Response(
            status=status,
            headers={"Location": location},
            body=b"",
        )


# ─── Route matching ─────────────────────────────────────────────────────

class Route:
    """Pojedyncza trasa: metoda + wzorzec ścieżki + handler."""

    def __init__(self, method: str, path_pattern: str, handler: Callable):
        self.method = method.upper()
        self.handler = handler
        # Proste dopasowanie: wspiera :param w ścieżce
        self._parts = []
        self._param_names = []
        for part in path_pattern.strip("/").split("/"):
            if part.startswith(":"):
                self._param_names.append(part[1:])
                self._parts.append(None)
            else:
                self._parts.append(part)

    def match(self, method: str, path_clean: str) -> Optional[dict]:
        """Sprawdza czy request pasuje do trasy. Zwraca dict z parametrami lub None."""
        if method != self.method:
            return None
        req_parts = path_clean.strip("/").split("/")
        if len(req_parts) != len(self._parts):
            return None
        params = {}
        pnames = list(self._param_names)  # copy — nie modyfikuj oryginału!
        for i, (req_part, pattern_part) in enumerate(zip(req_parts, self._parts)):
            if pattern_part is None:
                params[pnames.pop(0)] = req_part
            elif req_part != pattern_part:
                return None
        return params if params else {}


# ─── Server ─────────────────────────────────────────────────────────────

class NOEMAServer:
    """Własny serwer HTTP. Thread-per-connection, routing, SSE, static files."""

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 18888,
        static_dir: Optional[str | Path] = None,
        name: str = "noema-portal",
        request_max_size: int = 1024 * 1024,  # 1MB max body
    ):
        self.host = host
        self.port = port
        self.name = name
        self.static_dir = Path(static_dir).resolve() if static_dir else None
        self.request_max_size = request_max_size

        self._routes: list[Route] = []
        self._sse_clients: list[tuple[Callable, Callable]] = []  # (stream_gen, cancel_fn)
        self._running = False
        self._server_socket: Optional[socket.socket] = None
        self._threads: list[threading.Thread] = []

    # ── Routing ─────────────────────────────────────────────────────

    def route(self, method: str, path: str):
        """Dekorator rejestrujący handler dla metody i ścieżki.

        Użycie:
            @server.route("GET", "/api/status")
            def status_handler(req):
                return Response.json({"ok": True})
        """
        def decorator(handler):
            self._routes.append(Route(method, path, handler))
            return handler
        return decorator

    def _find_handler(self, method: str, path_clean: str) -> tuple[Optional[Callable], dict]:
        """Znajduje handler i parametry dla ścieżki."""
        for route in self._routes:
            params = route.match(method, path_clean)
            if params is not None:
                return route.handler, params
        return None, {}

    # ── HTTP Parsing ────────────────────────────────────────────────

    def _parse_request(self, client_socket: socket.socket, addr: tuple) -> Optional[Request]:
        """Parsuje surowe HTTP z socketa. Zwraca Request lub None (błąd/zamknięcie)."""
        try:
            client_socket.settimeout(10)

            # Read request line + headers
            data = b""
            while b"\r\n\r\n" not in data and b"\n\n" not in data:
                chunk = client_socket.recv(4096)
                if not chunk:
                    return None
                data += chunk
                if len(data) > 65536:  # header too large
                    return None

            # Split headers from body
            if b"\r\n\r\n" in data:
                header_part, rest = data.split(b"\r\n\r\n", 1)
            else:
                header_part, rest = data.split(b"\n\n", 1)

            header_text = header_part.decode("utf-8", errors="replace")

            # Parse request line
            lines = header_text.split("\r\n") if "\r\n" in header_text else header_text.split("\n")
            if not lines:
                return None

            request_line = lines[0].strip()
            parts = request_line.split(" ")
            if len(parts) < 2:
                return None

            method = parts[0].upper()
            raw_path = parts[1]

            # Parse path + query
            parsed = urlparse(raw_path)
            path = unquote(parsed.path)
            query = {}
            if parsed.query:
                for qp in parsed.query.split("&"):
                    if "=" in qp:
                        k, v = qp.split("=", 1)
                        query[unquote(k)] = unquote(v)
                    else:
                        query[unquote(qp)] = ""

            # Parse headers
            headers = {}
            for line in lines[1:]:
                line = line.strip()
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().lower()] = v.strip()

            # Read body
            body = rest
            content_length = int(headers.get("content-length", "0"))
            if content_length > self.request_max_size:
                return None  # too large
            while len(body) < content_length:
                chunk = client_socket.recv(min(65536, content_length - len(body)))
                if not chunk:
                    break
                body += chunk

            return Request(
                method=method,
                path=path,
                query=query,
                headers=headers,
                body=body,
                client_addr=addr,
            )

        except socket.timeout:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_httpd.py:314 quiet except scope=NOEMAServer._parse_request reason=return None")
            return None
        except Exception as e:
            traceback.print_exc()
            return None

    # ── Response writer ─────────────────────────────────────────────

    def _send_response(self, client_socket: socket.socket, req: Request, resp: Response):
        """Wysyła Response przez socket."""
        try:
            # SSE — strumieniowanie
            if resp._stream:
                self._handle_sse(client_socket, resp._stream)
                return

            # Normal response
            status_text = {200: "OK", 201: "Created", 204: "No Content",
                           301: "Moved", 302: "Found", 304: "Not Modified",
                           400: "Bad Request", 403: "Forbidden", 404: "Not Found",
                           405: "Method Not Allowed", 413: "Payload Too Large",
                           429: "Too Many Requests", 500: "Internal Server Error",
                           502: "Bad Gateway"}.get(resp.status, "Unknown")

            now = formatdate(timeval=time.time(), localtime=False, usegmt=True)
            status_line = f"HTTP/1.1 {resp.status} {status_text}"
            headers = OrderedDict()
            headers["Server"] = self.name
            headers["Date"] = now
            headers["Content-Length"] = str(len(resp.body))
            for k, v in resp.headers.items():
                headers[k] = v

            response_bytes = (
                status_line.encode("utf-8") + b"\r\n" +
                b"\r\n".join(f"{k}: {v}".encode("utf-8") for k, v in headers.items()) +
                b"\r\n\r\n" + resp.body
            )

            client_socket.sendall(response_bytes)

        except (ConnectionResetError, BrokenPipeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_httpd.py:355 quiet except scope=NOEMAServer._send_response reason=pass")
            pass
        except Exception as e:
            traceback.print_exc()
        finally:
            try:
                client_socket.close()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_httpd.py:362 quiet except scope=NOEMAServer._send_response reason=pass")
                pass

    # ── SSE ─────────────────────────────────────────────────────────

    def _handle_sse(self, client_socket: socket.socket, stream_gen: Callable):
        """Obsługa SSE — długie połączenie z okresowym wysyłaniem danych."""
        cancel_event = threading.Event()
        self._sse_clients.append((stream_gen, cancel_event))

        try:
            client_socket.settimeout(None)  # no timeout for SSE
            try:
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_httpd.py:376 quiet except scope=NOEMAServer._handle_sse reason=pass")
                pass

            # Send initial headers
            now = formatdate(timeval=time.time(), localtime=False, usegmt=True)
            header_lines = (
                "HTTP/1.1 200 OK",
                f"Server: {self.name}",
                f"Date: {now}",
                "Content-Type: text/event-stream",
                "Cache-Control: no-cache",
                "Connection: keep-alive",
                "Access-Control-Allow-Origin: *",
                "X-Accel-Buffering: no",
                "",
                "",
            )
            client_socket.sendall("\r\n".join(header_lines).encode("utf-8"))

            # Stream data — wywołaj funkcję, aby uzyskać generator
            try:
                gen = stream_gen()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_httpd.py:398 quiet except scope=NOEMAServer._handle_sse reason=return None")
                return
            for chunk in gen:
                if cancel_event.is_set():
                    break
                if isinstance(chunk, str):
                    chunk = chunk.encode("utf-8")
                try:
                    client_socket.sendall(chunk)
                except (ConnectionResetError, BrokenPipeError, OSError):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_httpd.py:407 quiet except scope=NOEMAServer._handle_sse reason=break")
                    break

        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_httpd.py:410 quiet except scope=NOEMAServer._handle_sse reason=pass")
            pass
        finally:
            cancel_event.set()
            try:
                client_socket.close()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_httpd.py:416 quiet except scope=NOEMAServer._handle_sse reason=pass")
                pass

    def stop_sse_clients(self):
        """Zatrzymuje wszystkie SSE strumienie."""
        for _, cancel in self._sse_clients:
            cancel.set()
        self._sse_clients.clear()

    # ── Static files ───────────────────────────────────────────────

    def _serve_static(self, path_clean: str) -> Optional[Response]:
        """Serwuje plik statyczny z katalogu static_dir."""
        if not self.static_dir:
            return None

        # Security: path_clean jest już znormalizowane (bez ..)
        file_path = self.static_dir / path_clean.lstrip("/")

        # Directory index
        if file_path.is_dir():
            file_path = file_path / "index.html"

        if not file_path.exists() or not file_path.is_file():
            return None

        try:
            body = file_path.read_bytes()
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type is None:
                mime_type = "application/octet-stream"

            return Response(
                status=200,
                headers={
                    "Content-Type": mime_type,
                    "Cache-Control": "public, max-age=3600",
                    "Access-Control-Allow-Origin": "*",
                },
                body=body,
            )
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_httpd.py:457 quiet except scope=NOEMAServer._serve_static reason=return None")
            return None

    # ── Connection handler ─────────────────────────────────────────

    def _handle_client(self, client_socket: socket.socket, addr: tuple):
        """Obsługuje pojedyncze połączenie."""
        try:
            req = self._parse_request(client_socket, addr)
            if req is None:
                return

            # CORS preflight
            if req.method == "OPTIONS":
                resp = Response(
                    status=204,
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Max-Age": "86400",
                    },
                )
                self._send_response(client_socket, req, resp)
                return

            path_clean = req.path_clean

            # Find handler
            handler, params = self._find_handler(req.method, path_clean)
            if handler:
                try:
                    resp = handler(req, **params)
                except Exception as e:
                    traceback.print_exc()
                    resp = Response.debug(500, str(e))
                self._send_response(client_socket, req, resp)
                return

            # Try static file
            if req.method == "GET":
                static_resp = self._serve_static(path_clean)
                if static_resp:
                    self._send_response(client_socket, req, static_resp)
                    return

            # 404
            self._send_response(client_socket, req, Response.error(404))

        except Exception as e:
            traceback.print_exc()
        finally:
            try:
                client_socket.close()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_httpd.py:511 quiet except scope=NOEMAServer._handle_client reason=pass")
                pass

    # ── Start / Stop ───────────────────────────────────────────────

    def start(self):
        """Uruchamia serwer (blokujący)."""
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except (AttributeError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_httpd.py:522 quiet except scope=NOEMAServer.start reason=pass")
            pass
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(128)
        self._server_socket.settimeout(1.0)  # 1s timeout for accept (allows checking _running)
        self._running = True

        print(f"[{self.name}] ✦ Serving on http://{self.host}:{self.port}")
        print(f"[{self.name}]   Static dir: {self.static_dir or '(none)'}")
        print(f"[{self.name}]   Routes: {len(self._routes)}")
        if self._routes:
            for r in self._routes:
                print(f"[{self.name}]     {r.method} {r._parts}")

        try:
            while self._running:
                try:
                    client_socket, addr = self._server_socket.accept()
                    t = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, addr),
                        daemon=True,
                    )
                    t.start()
                    self._threads.append(t)
                except socket.timeout:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_httpd.py:547 quiet except scope=NOEMAServer.start reason=continue")
                    continue
                except OSError:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_httpd.py:549 quiet except scope=NOEMAServer.start reason=break")
                    break
        except KeyboardInterrupt:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_httpd.py:551 quiet except scope=NOEMAServer.start reason=pass")
            pass
        finally:
            self.stop()

    def stop(self):
        """Zatrzymuje serwer."""
        print(f"\n[{self.name}] Shutting down...")
        self._running = False
        self.stop_sse_clients()
        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_httpd.py:564 quiet except scope=NOEMAServer.stop reason=pass")
                pass
        print(f"[{self.name}] Goodbye.")


# ─── Example SSE generator ──────────────────────────────────────────────

def example_sse_gen():
    """Przykładowy generator SSE — tick co 2 sekundy."""
    import math
    while True:
        t = time.time()
        data = json.dumps({
            "time": t,
            "random": math.sin(t),
        })
        yield f"data: {data}\n\n"
        time.sleep(2)


# ─── Main (standalone test) ─────────────────────────────────────────────

if __name__ == "__main__":
    server = NOEMAServer(host="0.0.0.0", port=18888, name="noema-httpd-test")

    @server.route("GET", "/api/hello")
    def hello(req, **params):
        return Response.json({"message": "Hello from NOEMA HTTPD!", "version": __version__})

    @server.route("GET", "/api/time")
    def get_time(req, **params):
        return Response.json({"time": time.time(), "iso": datetime.now().isoformat()})

    @server.route("GET", "/api/echo")
    def echo(req, **params):
        return Response.json({
            "method": req.method,
            "path": req.path,
            "query": req.query,
            "headers": dict(req.headers),
            "body": req.body.decode("utf-8", errors="replace")[:500],
        })

    @server.route("GET", "/api/stream")
    def stream(req, **params):
        return Response.sse(example_sse_gen)

    print("✦ NOEMA HTTPD v" + __version__)
    print("  Test endpoints:")
    print("    GET /api/hello")
    print("    GET /api/time")
    print("    GET /api/echo?foo=bar")
    print("    GET /api/stream (SSE)")
    print("    GET / (static file)")
    server.start()
