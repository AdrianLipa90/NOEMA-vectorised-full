#!/usr/bin/env python3
"""Probe local opencode server and dump minimal API state into proto/."""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json, os, pathlib, subprocess, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body')
PROTO = ROOT / 'proto'
STATE = ROOT / 'state'
PROTO.mkdir(parents=True, exist_ok=True)
STATE.mkdir(parents=True, exist_ok=True)

HOST = '127.0.0.1'
PORT = 4097
BASE = f'http://{HOST}:{PORT}'
PROJECT_DIR = '/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA'


def http_json(path: str):
    req = urllib.request.Request(BASE + path)
    req.add_header('x-opencode-directory', PROJECT_DIR)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode('utf-8'))


def launch_server():
    env = os.environ.copy()
    proc = subprocess.Popen(
        ['opencode', 'serve', f'--hostname={HOST}', f'--port={PORT}', '--print-logs'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )
    output = []
    start = time.time()
    while time.time() - start < 20:
        line = proc.stdout.readline()
        if line:
            output.append(line)
            if 'opencode server listening' in line:
                return proc, output
    raise RuntimeError('timeout waiting for opencode serve')


def main():
    proc, logs = launch_server()
    (STATE / 'serve_boot.log').write_text(''.join(logs), encoding='utf-8')
    dump = {'base': BASE, 'directory': PROJECT_DIR, 'captured_at': time.time()}
    try:
        for path, key in [
            ('/config', 'config'),
            ('/project', 'project'),
            ('/path', 'path'),
            ('/provider', 'providers'),
            ('/app/agents', 'agents'),
            ('/session', 'sessions'),
            ('/command', 'commands'),
        ]:
            try:
                dump[key] = http_json(path)
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/opencode_runtime_probe.py:61 quiet except scope=main reason=assign_fallback")
                dump[key] = {'error': str(e), 'path': path}
        (PROTO / 'runtime_probe.json').write_text(json.dumps(dump, indent=2, ensure_ascii=False), encoding='utf-8')
        print(json.dumps({'ok': True, 'proto': str(PROTO / 'runtime_probe.json')}, ensure_ascii=False))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/opencode_runtime_probe.py:69 quiet except scope=main reason=Expr")
            proc.kill()


if __name__ == '__main__':
    main()
