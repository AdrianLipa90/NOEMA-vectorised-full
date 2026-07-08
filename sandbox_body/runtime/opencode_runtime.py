#!/usr/bin/env python3
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json, os, pathlib, subprocess, time, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body')
CONFIG_HOME = ROOT / 'xdg_config'
STATE_HOME = ROOT / 'xdg_state'
PROTO = ROOT / 'proto'
STATE = ROOT / 'state'
PROTO.mkdir(parents=True, exist_ok=True)
STATE.mkdir(parents=True, exist_ok=True)

HOST = '127.0.0.1'
PORT = 4098
BASE = f'http://{HOST}:{PORT}'
DIRECTORY = '/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA'
OPENCODE_BIN = '/home/adrian/.opencode/bin/opencode'

class SandboxServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.base = f'http://{host}:{port}'
        self.proc = None

    def start(self):
        env = os.environ.copy()
        env['XDG_CONFIG_HOME'] = str(CONFIG_HOME)
        env['XDG_STATE_HOME'] = str(STATE_HOME)
        self.proc = subprocess.Popen(
            [OPENCODE_BIN, 'serve', f'--hostname={self.host}', f'--port={self.port}', '--print-logs'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
        )
        buf = []
        start = time.time()
        while time.time() - start < 25:
            line = self.proc.stdout.readline()
            if line:
                buf.append(line)
                if 'opencode server listening' in line:
                    (STATE/'sandbox_serve.log').write_text(''.join(buf), encoding='utf-8')
                    return self
        raise RuntimeError('timeout waiting for sandbox server')

    def stop(self):
        if not self.proc:
            return
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/opencode_runtime.py:54 quiet except scope=SandboxServer.stop reason=Expr")
            self.proc.kill()

class BodyClient:
    def __init__(self, base_url: str, directory: str):
        self.base_url = base_url.rstrip('/')
        self.directory = directory

    def request(self, method: str, path: str, body=None):
        url = self.base_url + path
        sep = '&' if '?' in url else '?'
        url += sep + 'directory=' + urllib.parse.quote(self.directory)
        data = None if body is None else json.dumps(body).encode('utf-8')
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header('Content-Type', 'application/json')
        req.add_header('x-opencode-directory', self.directory)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = r.read().decode('utf-8')
                ctype = r.headers.get('Content-Type', '')
                debug = {'url': url, 'status': getattr(r, 'status', None), 'content_type': ctype, 'raw': raw[:4000]}
                (PROTO / 'last_http_debug.json').write_text(json.dumps(debug, indent=2, ensure_ascii=False), encoding='utf-8')
                if not raw:
                    return None
                try:
                    return json.loads(raw)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/opencode_runtime.py:80 quiet except scope=BodyClient.request reason=return {'_raw': raw, '_content_type': ctype}")
                    return {'_raw': raw, '_content_type': ctype}
        except urllib.error.HTTPError as e:
            raw = e.read().decode('utf-8', errors='replace') if hasattr(e, 'read') else ''
            debug = {'url': url, 'status': e.code, 'content_type': getattr(e, 'headers', {}).get('Content-Type', ''), 'raw': raw[:4000]}
            (PROTO / 'last_http_debug.json').write_text(json.dumps(debug, indent=2, ensure_ascii=False), encoding='utf-8')
            raise

    def create_session(self, title: str, parent_id: str | None = None):
        body = {'title': title}
        if parent_id:
            body['parentID'] = parent_id
        return self.request('POST', '/session', body)

    def get_session(self, session_id: str):
        return self.request('GET', f'/session/{session_id}')

    def prompt(self, session_id: str, text: str, agent='build'):
        return self.request('POST', f'/session/{session_id}/message', {
            'agent': agent,
            'tools': {},
            'parts': [{'type': 'text', 'text': text}],
        })

    def messages(self, session_id: str, limit=50):
        return self.request('GET', f'/session/{session_id}/message?limit={limit}')

    def status(self):
        return self.request('GET', '/session/status')

    def agents(self):
        return self.request('GET', '/app/agents')
