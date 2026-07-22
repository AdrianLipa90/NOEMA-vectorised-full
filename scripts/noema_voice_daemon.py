#!/usr/bin/env python3

"""
noema_voice_daemon.py  —  HTTP daemon na porcie 18521

Serwuje odpowiedzi generowane lokalnie przez Voice (ciel_geometry.voice),
bez LLM, bez internetu. Endpoint /v1/chat/completions (zgodny z OpenAI).

Endpointy:
  GET  /health          → {"service": "noema_voice", "status": "running", "mode": "..."}
  POST /v1/chat/completions  → odpowiedź Voice jako OpenAI-compatible response

Usage:
  .venv/bin/python3 scripts/noema_voice_daemon.py [--port 18521]
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import json
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ciel_geometry.voice import Voice, DEFAULT_OPERATOR_VECTOR
from ciel_geometry.noema_registry import registry as nreg

# TTS engine
_TTS_ENGINE = None

def _mic_mute(mute: bool):
    """Mute/unmute capture device to avoid echo loop."""
    import subprocess
    state = "nocap" if mute else "cap"
    subprocess.run(
        ["amixer", "-q", "sset", "Capture", state],
        stderr=subprocess.DEVNULL)

def _say(text: str, lang: str = "pl"):
    global _TTS_ENGINE
    _mic_mute(True)  # mute mic before speaking
    try:
        if _TTS_ENGINE is None:
            import pyttsx3
            _TTS_ENGINE = pyttsx3.init()
            for v in _TTS_ENGINE.getProperty("voices"):
                if "pl" in str(v.languages) or "Polish" in v.name:
                    _TTS_ENGINE.setProperty("voice", v.id)
                    break
            _TTS_ENGINE.setProperty("rate", 170)
        _TTS_ENGINE.say(text)
        _TTS_ENGINE.runAndWait()
    finally:
        _mic_mute(False)  # unmute after speaking

PORT = int(os.environ.get("NOEMA_VOICE_PORT", "18521"))
VOICE = Voice()

class VoiceHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _respond_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._respond_json({
                "service": "noema_voice",
                "status": "running",
                "mode": VOICE.mode,
                "tick": VOICE.surface.get("tick", 0),
                "coh": round(VOICE.surface.get("coh", 0.0), 4),
            })
        else:
            self._respond_json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/say":
            self._handle_say()
        elif self.path == "/v1/chat/completions":
            self._handle_chat()
        else:
            self._respond_json({"error": "not found"}, 404)

    def _read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            return json.loads(raw) if raw else {}
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_voice_daemon.py:108 quiet except scope=VoiceHandler._read_json_body reason=return None")
            raise
            return None

    def _handle_say(self):
        req = self._read_json_body()
        if not req or "text" not in req:
            self._respond_json({"error": "text field required"}, 400)
            return
        text = req["text"][:500]
        lang = req.get("lang", "pl")
        try:
            _say(text, lang)
            self._respond_json({"spoken": text, "lang": lang})
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_voice_daemon.py:121 quiet except scope=VoiceHandler._handle_say reason=Expr")
            raise
            self._respond_json({"error": str(e)}, 500)

    def _handle_chat(self):
        req = self._read_json_body()
        if req is None:
            self._respond_json({"error": "bad request"}, 400)
            return

        messages = req.get("messages", [])
        query = messages[-1]["content"] if messages else ""

        style = "PLAIN"
        if req.get("style"):
            style = req["style"].upper()
        if style not in ("PLAIN", "FORMAL", "RELATIONAL_FORMAL", "POETIC_BOUNDED"):
            style = "PLAIN"

        try:
            resp = VOICE.respond(query_text=query, style=style)
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_voice_daemon.py:141 quiet except scope=VoiceHandler._handle_chat reason=no_log_no_raise")
            raise
            self._respond_json({
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"Błąd syntezy: {e}"
                    }
                }],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            })
            return

        voice_text = resp["text"]
        vm = resp["context"]
        vm["mode"] = resp["mode"]

        self._respond_json({
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": voice_text,
                }
            }],
            "usage": {
                "prompt_tokens": len(query),
                "completion_tokens": len(voice_text),
                "total_tokens": len(query) + len(voice_text),
            },
            "voice_meta": vm,
        })

def _voice_hb_loop(reg_token: Any) -> None:
    """Background heartbeat."""
    while True:
        time.sleep(15)
        try:
            nreg.heartbeat(reg_token)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_voice_daemon.py:180 quiet except scope=_voice_hb_loop reason=pass")
            raise
            pass

def main():
    port = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--port" else PORT
    server = HTTPServer(("0.0.0.0", port), VoiceHandler)
    reg_token = None
    try:
        reg_token = nreg.register("voice")
        print(f"[voice] registered in noema registry", flush=True)
        t = threading.Thread(target=_voice_hb_loop, args=(reg_token,), daemon=True)
        t.start()
    except Exception as e:
        print(f"[voice] registry registration failed: {e}", flush=True)
    print(f"noema_voice on :{port}  mode={VOICE.mode} tick={VOICE.surface.get('tick',0)}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_voice_daemon.py:197 quiet except scope=main reason=Expr")
        raise
        server.shutdown()
    finally:
        if reg_token is not None:
            try:
                nreg.unregister("voice")
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_voice_daemon.py:203 quiet except scope=main reason=pass")
                raise
                pass

if __name__ == "__main__":
    main()
